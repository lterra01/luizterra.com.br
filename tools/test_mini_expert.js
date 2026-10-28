const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");

const source = fs.readFileSync(path.join(__dirname, "../script.js"), "utf8");

function run({ hostname = "www.luizterra.com.br", analytics = true, landing = true, observe = true } = {}) {
  class Element {
    constructor(dataset = {}) { this.dataset = dataset; this.events = {}; }
    addEventListener(name, fn) { this.events[name] = fn; }
    closest(selector) { return selector === "[data-mini-expert-id]" ? identity : null; }
  }
  const identity = new Element({ miniExpertId: "mini-expert-indicadores-de-atendimento", miniExpertTitle: "Mini Expert de Indicadores de Atendimento", hotmartProductId: "8822826" });
  const checkout = new Element({ miniExpertCheckout: "offer" });
  const link = new Element({ miniExpertLink: "catalog" });
  const feature = new Element({ productPlacement: "catalog" });
  const observers = [];
  class Observer {
    constructor(callback) { this.callback = callback; this.targets = []; observers.push(this); }
    observe(target) { this.targets.push(target); }
    unobserve() {}
  }
  const events = [];
  const document = {
    querySelector: (s) => s === "body.mini-expert-landing" && landing ? identity : null,
    querySelectorAll(s) {
      if (s === "[data-mini-expert-link]") return [link];
      if (s === "[data-mini-expert-checkout]") return [checkout];
      if (s === "[data-mini-expert-product]") return [feature];
      return [];
    },
    addEventListener() {},
  };
  vm.runInNewContext(source, {
    document, HTMLElement: Element,
    ...(observe ? { IntersectionObserver: Observer } : {}),
    window: { location: { hostname }, ...(observe ? { IntersectionObserver: Observer } : {}),
      ...(analytics ? { gtag: (...args) => events.push(args) } : {}) },
  });
  return { events, checkout, link, feature, observer: observers.find(o => o.targets.includes(feature)) };
}

test("Mini Expert intent is separate from ebooks, revenue and purchase events", () => {
  const state = run();
  state.checkout.events.click();
  state.link.events.click();
  assert.deepEqual(state.events.map(e => e[1]), ["mini_expert_landing_view", "mini_expert_checkout_click", "mini_expert_landing_click"]);
  for (const [, , data] of state.events) {
    assert.equal(data.item_id, "mini-expert-indicadores-de-atendimento");
    assert.equal(data.hotmart_product_id, "8822826");
    assert.equal(data.billing_period, "monthly");
    assert.equal(data.send_to, "G-68E95X4DZT");
    assert.equal("ebook_id" in data || "value" in data || "transaction_id" in data, false);
  }
});

test("Preview and absent Analytics do not send events or block links", () => {
  for (const options of [{ hostname: "127.0.0.1" }, { hostname: "localhost" }, { analytics: false }]) {
    const state = run(options);
    state.checkout.events.click();
    state.link.events.click();
    assert.equal(state.events.length, 0);
  }
});

test("Product exposure is recorded only once after half visibility", () => {
  const state = run({ landing: false });
  const entry = { target: state.feature, isIntersecting: true, intersectionRatio: 0.4 };
  state.observer.callback([entry]);
  assert.equal(state.events.length, 0);
  state.observer.callback([{ ...entry, intersectionRatio: 0.7 }]);
  state.observer.callback([{ ...entry, intersectionRatio: 1 }]);
  assert.deepEqual(state.events.map(e => e[1]), ["mini_expert_product_view"]);
  assert.equal(state.events[0][2].placement, "catalog");
});

test("Older browsers preserve links without exposure observer", () => {
  const state = run({ observe: false });
  state.checkout.events.click();
  assert.equal(state.events.length, 2);
});
