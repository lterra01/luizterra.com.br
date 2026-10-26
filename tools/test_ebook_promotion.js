const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");

const source = fs.readFileSync(path.join(__dirname, "../script.js"), "utf8");

function runPromotion({ seen = false, blocked = false, landing = false, otherDialog = false } = {}) {
  class Element {
    constructor(dataset = {}) { this.dataset = dataset; this.events = {}; }
    addEventListener(name, fn) { this.events[name] = fn; }
    closest() { return null; }
  }
  const closeButton = new Element();
  class Dialog extends Element {
    open = false;
    showModal() { this.open = true; }
    close() { this.open = false; this.events.close?.(); }
    querySelectorAll() { return [closeButton]; }
  }
  const dialog = new Dialog();
  const checkout = new Element({ ebookCheckout: "hero" });
  const announcement = new Element({ ebookPlacement: "announcement" });
  const storage = new Map(seen ? [["luiz-terra-ebook-cx-v1-introduced", "1"]] : []);
  const timers = [];
  const events = [];
  const document = {
    activeElement: new Element(), visibilityState: "visible",
    body: { classList: { contains: () => false } },
    querySelector(selector) {
      if (selector === "#ebook-introduction") return landing ? null : dialog;
      if (selector === "dialog[open]") return otherDialog ? {} : null;
      return null;
    },
    querySelectorAll(selector) {
      if (selector === "[data-ebook-checkout]") return [checkout];
      if (selector === "[data-ebook-placement]") return [announcement];
      return [];
    },
    addEventListener() {},
  };
  const context = {
    document, HTMLElement: Element, HTMLDialogElement: Dialog,
    window: { setTimeout: (fn) => timers.push(fn), gtag: (...args) => events.push(args) },
    sessionStorage: {
      getItem(key) { if (blocked) throw new Error("Storage blocked"); return storage.get(key); },
      setItem(key, value) { if (blocked) throw new Error("Storage blocked"); storage.set(key, value); },
    },
  };
  vm.runInNewContext(source, context);
  timers.forEach((fn) => fn());
  return { dialog, closeButton, checkout, announcement, storage, events };
}

test("first visit opens a dismissible dialog and remembers the session", () => {
  const state = runPromotion();
  assert.equal(state.dialog.open, true);
  assert.equal(state.storage.get("luiz-terra-ebook-cx-v1-introduced"), "1");
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
  assert.deepEqual(state.events.map((event) => event[1]), ["ebook_checkout_click", "ebook_landing_click"]);
  assert.equal(state.events.some((event) => event[1] === "purchase" || "value" in event[2]), false);
});
