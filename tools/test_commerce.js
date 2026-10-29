const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");

const source = fs.readFileSync(path.join(__dirname, "../script.js"), "utf8");

function run({ hostname = "www.luizterra.com.br", analytics = true } = {}) {
  class Element {
    constructor(dataset = {}) { this.dataset = dataset; this.events = {}; this.hidden = true; this.value = ""; this.textContent = ""; }
    addEventListener(name, callback) { this.events[name] = callback; }
    focus() { this.focused = true; }
    select() { this.selected = true; }
    closest() { return null; }
  }
  const choices = ["cx-na-operacao", "indicadores-de-atendimento-na-pratica", "qualidade-e-feedback-no-atendimento"].map((value) => {
    const choice = new Element({ titleName: value });
    Object.assign(choice, { value, checked: false, disabled: false });
    return choice;
  });
  const ids = Object.fromEntries(["bonus-request", "bonus-origin", "bonus-result", "bonus-message", "bonus-email", "bonus-status", "bonus-error", "bonus-count", "bonus-fiverr-note", "bonus-email-note", "bonus-copy", "bonus-copy-data"].map(id => ["#" + id, new Element()]));
  ids["#bonus-request"].querySelectorAll = () => choices;
  ids["#bonus-origin"].value = "mini-expert";
  ids["#bonus-copy-data"].textContent = JSON.stringify({ error: "Choose two", message: "Selection", subject: "Bonus", copied: "Copied", copy_error: "Copy below", pending: "Not yet sent or approved" });
  const offer = new Element({ fiverrCheckout: "offer" });
  const link = new Element({ fiverrLink: "catalog" });
  const feature = new Element({ productPlacement: "home" });
  const events = [], observers = [], clipboard = [];
  class Observer {
    constructor(callback) { this.callback = callback; this.targets = []; observers.push(this); }
    observe(target) { this.targets.push(target); }
    unobserve() {}
  }
  const document = {
    querySelector: (selector) => ids[selector] || (selector === "body.consulting-landing" ? new Element() : null),
    querySelectorAll: (selector) => ({ "[data-fiverr-link]": [link], "[data-fiverr-checkout]": [offer], "[data-fiverr-product]": [feature] }[selector] || []),
    addEventListener() {},
  };
  vm.runInNewContext(source, { document, HTMLElement: Element, IntersectionObserver: Observer,
    navigator: { clipboard: { writeText: async (value) => clipboard.push(value) } },
    window: { IntersectionObserver: Observer, location: { hostname }, ...(analytics ? { gtag: (...args) => events.push(args) } : {}) },
  });
  return { ids, choices, events, offer, link, feature, clipboard,
    submit: () => ids["#bonus-request"].events.submit({ preventDefault() {} }),
    change: () => ids["#bonus-request"].events.change(),
    observer: observers.find(o => o.targets.includes(feature)),
  };
}

test("Fiverr actions are intent, with no financial or buyer fields", () => {
  const state = run();
  state.offer.events.click(); state.link.events.click();
  for (const [, name, data] of state.events) {
    assert.notEqual(name, "purchase");
    assert.equal(data.send_to, "G-68E95X4DZT");
    for (const forbidden of ["value", "revenue", "transaction_id", "voucher", "email", "customer_ref", "message"]) assert.equal(forbidden in data, false);
  }
  assert.equal(state.events.filter(e => e[1] === "fiverr_offer_click").length, 1);
  state.observer.callback([{ target: state.feature, isIntersecting: true, intersectionRatio: 0.6 }]);
  state.observer.callback([{ target: state.feature, isIntersecting: true, intersectionRatio: 1 }]);
  assert.equal(state.events.filter(e => e[1] === "fiverr_product_view").length, 1);
});

test("A bonus needs exactly two titles and disables only the third", () => {
  const state = run();
  state.submit();
  assert.equal(state.ids["#bonus-error"].hidden, false);
  assert.equal(state.events.filter(e => e[1] === "bonus_request_prepare").length, 0);
  state.choices[0].checked = true; state.change(); state.submit();
  assert.equal(state.ids["#bonus-result"].hidden, true);
  state.choices[1].checked = true; state.change();
  assert.equal(state.choices[2].disabled, true);
  assert.equal(state.choices[0].disabled, false);
  state.submit(); state.submit();
  assert.equal(state.events.filter(e => e[1] === "bonus_request_prepare").length, 1);
  assert.equal(state.ids["#bonus-result"].hidden, false);
  assert.match(state.ids["#bonus-status"].textContent, /Not yet sent or approved/);
  state.choices[0].checked = false; state.change();
  assert.equal(state.choices[2].disabled, false);
  assert.equal(state.ids["#bonus-result"].hidden, true);
});

test("Fiverr redemption never opens email and selection can be copied", async () => {
  const state = run();
  state.ids["#bonus-origin"].value = "fiverr";
  state.choices[0].checked = state.choices[2].checked = true;
  state.change(); state.submit();
  assert.equal(state.ids["#bonus-email"].hidden, true);
  assert.equal(state.ids["#bonus-email"].href, "");
  assert.equal(state.ids["#bonus-fiverr-note"].hidden, false);
  assert.equal(state.ids["#bonus-email-note"].hidden, true);
  await state.ids["#bonus-copy"].events.click();
  assert.match(state.clipboard[0], /cx-na-operacao/);
  assert.match(state.clipboard[0], /qualidade-e-feedback-no-atendimento/);
  assert.equal(state.events.some(e => e[1] === "purchase" || /redeemed|approved|delivered/.test(e[1])), false);
});

test("Hotmart and courtesy prepare an unsent private email, never a checkout coupon", () => {
  for (const origin of ["mini-expert", "courtesy"]) {
    const state = run();
    state.ids["#bonus-origin"].value = origin;
    state.choices[0].checked = state.choices[1].checked = true;
    state.change(); state.submit();
    assert.equal(state.ids["#bonus-email"].hidden, false);
    assert.match(state.ids["#bonus-email"].href, /^mailto:contact@luizterra.com.br\?/);
    assert.equal(state.events.filter(e => e[1] === "bonus_contact_click").length, 0);
    state.ids["#bonus-email"].events.click();
    assert.equal(state.events.filter(e => e[1] === "bonus_contact_click").length, 1);
  }
});

test("Local previews and absent Analytics preserve forms without telemetry", () => {
  for (const options of [{ hostname: "127.0.0.1" }, { hostname: "localhost" }, { analytics: false }]) {
    const state = run(options);
    state.choices[0].checked = state.choices[1].checked = true;
    state.change(); state.submit(); state.offer.events.click();
    assert.equal(state.ids["#bonus-result"].hidden, false);
    assert.equal(state.events.length, 0);
  }
});
