const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");

const source = fs.readFileSync(path.join(__dirname, "../script.js"), "utf8");

function runPromotion({ seen = false, blocked = false, landing = false, otherDialog = false, analytics = true, acknowledge = false, productId = "cx-na-operacao", productTitle = "CX na Operação" } = {}) {
  class Element {
    constructor(dataset = {}) { this.dataset = dataset; this.events = {}; }
    addEventListener(name, fn) { this.events[name] = fn; }
    closest(selector) { return selector === "[data-ebook-id]" && this.dataset.ebookId ? this : null; }
  }
  const closeButton = new Element({ ebookClose: "close_icon" });
  const continueButton = new Element({ ebookClose: "continue_button" });
  class Dialog extends Element {
    open = false;
    showModal() { this.open = true; }
    close() { this.open = false; this.events.close?.(); }
    querySelectorAll() { return [closeButton, continueButton]; }
    getBoundingClientRect() { return { left: 100, top: 100, right: 500, bottom: 500 }; }
  }
  const identity = { ebookId: productId, ebookTitle: productTitle };
  const dialog = new Dialog({ ...identity, ebookAdId: "cx_na_operacao_launch_v1" });
  const landingBody = new Element(identity);
  const checkout = new Element({ ...identity, ebookCheckout: "hero" });
  const announcement = new Element({ ...identity, ebookPlacement: "announcement" });
  const introduction = new Element({ ...identity, ebookPlacement: "introduction" });
  introduction.href = "https://www.luizterra.com.br/pt/ebooks/cx-na-operacao/";
  introduction.target = "";
  const storage = new Map(seen ? [["luiz-terra-ebook-cx-v1-introduced", "1"]] : []);
  const timers = [];
  const events = [];
  const navigations = [];
  const flushTimers = () => { while (timers.length) timers.shift()(); };
  const document = {
    activeElement: new Element(), visibilityState: "visible",
    body: { classList: { contains: () => false } },
    querySelector(selector) {
      if (selector === "#ebook-introduction") return landing ? null : dialog;
      if (selector === "body.ebook-landing[data-ebook-id]") return landing ? landingBody : null;
      if (selector === "dialog[open]") return otherDialog ? {} : null;
      return null;
    },
    querySelectorAll(selector) {
      if (selector === "[data-ebook-checkout]") return [checkout];
      if (selector === "[data-ebook-placement]") return [announcement, introduction];
      return [];
    },
    addEventListener() {},
  };
  const context = {
    document, HTMLElement: Element, HTMLDialogElement: Dialog,
    window: {
      setTimeout: (fn) => timers.push(fn),
      location: { assign: (url) => navigations.push(url) },
      ...(analytics ? { gtag: (...args) => {
        events.push(args);
        if (acknowledge) args[2]?.event_callback?.();
      } } : {}),
    },
    sessionStorage: {
      getItem(key) { if (blocked) throw new Error("Storage blocked"); return storage.get(key); },
      setItem(key, value) { if (blocked) throw new Error("Storage blocked"); storage.set(key, value); },
    },
  };
  vm.runInNewContext(source, context);
  flushTimers();
  return { dialog, closeButton, continueButton, checkout, announcement, introduction, storage, events, navigations, flushTimers };
}

const choices = (state) => state.events.filter((event) => ["ebook_offer_continue", "ebook_site_continue"].includes(event[1]));
const click = (extra = {}) => ({ button: 0, preventDefault() { this.defaultPrevented = true; }, ...extra });

test("first visit opens a dismissible dialog and remembers the session", () => {
  const state = runPromotion();
  assert.equal(state.dialog.open, true);
  assert.equal(state.storage.get("luiz-terra-ebook-cx-v1-introduced"), "1");
  assert.equal(state.events.filter((event) => event[1] === "ebook_introduction_view").length, 1);
  state.closeButton.events.click();
  assert.equal(state.dialog.open, false);
});

test("returning visits, blocked storage and another dialog do not reopen it", () => {
  for (const options of [{ seen: true }, { blocked: true }, { otherDialog: true }, { landing: true }]) {
    assert.equal(runPromotion(options).dialog.open, false);
  }
});

test("checkout clicks are intent events, never purchases or revenue", () => {
  const state = runPromotion({ landing: true });
  state.checkout.events.click();
  state.announcement.events.click();
  assert.deepEqual(state.events.map((event) => event[1]), ["ebook_landing_view", "ebook_checkout_click", "ebook_landing_click"]);
  assert.equal(state.events.some((event) => event[1] === "purchase" || "value" in event[2]), false);
  assert.equal(state.events.every((event) => event[2].send_to === "G-68E95X4DZT"), true);
});

test("offer choice is captured once and is not also a site continuation", () => {
  const state = runPromotion();
  const event = click();
  state.introduction.events.click(event);
  assert.equal(event.defaultPrevented, true);
  assert.equal(state.dialog.open, false);
  assert.equal(choices(state).length, 1);
  assert.equal(choices(state)[0][1], "ebook_offer_continue");
  assert.equal(choices(state)[0][2].ebook_ad_id, "cx_na_operacao_launch_v1");
  assert.equal(choices(state)[0][2].interaction_method, "offer_button");
  assert.equal(state.navigations.length, 0);
  state.flushTimers();
  assert.deepEqual(state.navigations, [state.introduction.href]);
});

test("Analytics acknowledgement and fallback never navigate twice", () => {
  const state = runPromotion({ acknowledge: true });
  state.introduction.events.click(click());
  state.flushTimers();
  assert.equal(state.navigations.length, 1);
});

test("continue button and close icon have distinct methods, one decision each", () => {
  for (const [button, method] of [["continueButton", "continue_button"], ["closeButton", "close_icon"]]) {
    const state = runPromotion();
    state[button].events.click();
    state.dialog.close();
    assert.equal(choices(state).length, 1);
    assert.equal(choices(state)[0][1], "ebook_site_continue");
    assert.equal(choices(state)[0][2].interaction_method, method);
  }
});

test("Escape and backdrop are site choices, clicks inside are not", () => {
  const escape = runPromotion();
  escape.dialog.events.cancel();
  escape.dialog.close();
  assert.equal(choices(escape).length, 1);
  assert.equal(choices(escape)[0][2].interaction_method, "escape");
  const backdrop = runPromotion();
  backdrop.dialog.events.click({ target: backdrop.dialog, clientX: 200, clientY: 200 });
  assert.equal(choices(backdrop).length, 0);
  backdrop.dialog.events.click({ target: backdrop.dialog, clientX: 0, clientY: 0 });
  assert.equal(choices(backdrop).length, 1);
  assert.equal(choices(backdrop)[0][2].interaction_method, "backdrop");
});

test("no exposure means no choice, and banner clicks are not modal choices", () => {
  const state = runPromotion({ seen: true });
  state.announcement.events.click(click());
  state.continueButton.events.click();
  assert.equal(choices(state).length, 0);
});

test("modified clicks and missing Analytics preserve normal navigation", () => {
  for (const [options, extra] of [[{}, { ctrlKey: true }], [{ analytics: false }, {}]]) {
    const state = runPromotion(options);
    const event = click(extra);
    state.introduction.events.click(event);
    state.flushTimers();
    assert.notEqual(event.defaultPrevented, true);
    assert.equal(state.navigations.length, 0);
  }
});

test("product identity is supplied by the page and supports future ebooks", () => {
  const current = runPromotion({ landing: true });
  current.checkout.events.click();
  for (const event of current.events) {
    assert.equal(event[2].ebook_id, "cx-na-operacao");
    assert.equal(event[2].ebook_title, "CX na Operação");
  }
  const future = runPromotion({ landing: true, productId: "qa-future-book", productTitle: "QA future book" });
  future.checkout.events.click();
  assert.equal(future.events.length, 2);
  assert.equal(future.events.every(event => event[2].ebook_id === "qa-future-book" && event[2].item_id === "qa-future-book"), true);
  assert.equal(future.events.every(event => event[2].ebook_title === "QA future book"), true);
});
