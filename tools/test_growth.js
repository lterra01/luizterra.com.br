const assert = require("node:assert/strict");
const { test } = require("node:test");
const { selectActions } = require("../growth.js");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const checks = Array.from({ length: 5 }, (_, index) => [`check ${index}`, `action ${index}`, `evidence ${index}`]);

test("the first three unchecked points determine the plan without a hidden score", () => {
  const plan = selectActions(checks, [0, 2]);
  assert.deepEqual(plan.actions, [checks[1], checks[3], checks[4]]);
  assert.equal(plan.maintenance, false);
  assert.equal("score" in plan, false);
});

test("zero, one and five pending checks remain bounded and ordered", () => {
  assert.deepEqual(selectActions(checks, []).actions, checks.slice(0, 3));
  assert.deepEqual(selectActions(checks, [0, 1, 2, 3]).actions, [checks[4]]);
  assert.deepEqual(selectActions(checks, [0, 1, 2, 3, 4]), { maintenance: true, actions: checks.slice(0, 3) });
});

function runResource({ hostname = "www.luizterra.com.br", analytics = true, search = "", ready = [] } = {}) {
  class Element {
    constructor() { this.events = {}; this.hidden = false; this.disabled = false; this.children = []; this.dataset = {}; }
    addEventListener(name, callback) { this.events[name] = callback; }
    append(...children) { this.children.push(...children); }
    replaceChildren(...children) { this.children = children; }
    focus() { this.focused = true; }
    click() { this.clicked = true; }
    remove() { this.removed = true; }
    setAttribute(name, value) { this[name] = value; }
  }
  const form = new Element();
  const submit = new Element();
  const result = new Element();
  const list = new Element();
  const maintenance = new Element();
  const download = new Element();
  const status = new Element();
  form.querySelector = () => submit;
  form.querySelectorAll = () => ready.map((value) => ({ value }));
  const track = new Element();
  track.dataset.cxTrack = "operations";
  const nodes = { form, "[data-cx-result]": result, "[data-cx-actions]": list, "[data-cx-maintenance]": maintenance, "[data-cx-download]": download, "[data-cx-status]": status };
  track.querySelector = (selector) => nodes[selector];
  const resource = new Element();
  resource.querySelectorAll = () => [track];
  const select = new Element();
  select.value = "operations";
  const link = new Element();
  link.dataset.cxResourceLink = "home";
  const events = [];
  const data = { lang: "pt", tracks: { operations: checks }, evidence: "Evidence", cadence: "Next week", downloaded: "Prepared", download_error: "Unavailable", download_loading: "Preparing", pdf_copy: {}, pdf_topics: { operations: { label: "Operations", relatedTitle: "CX", relatedUrl: "https://www.luizterra.com.br/ebooks/" } } };
  const createdLinks = [];
  const blobs = [];
  const pdf = { create: async () => ({ bytes: new Uint8Array([37, 80, 68, 70, 45]) }) };
  const document = {
    body: new Element(),
    documentElement: { lang: "pt-BR" },
    querySelector(selector) {
      return { "[data-cx-resource]": resource, "#cx-plan-data": { textContent: JSON.stringify(data) }, "#cx-priority": select }[selector];
    },
    querySelectorAll: () => [link],
    createElement: (name) => { const element = new Element(); if (name === "a") createdLinks.push(element); return element; },
  };
  class FakeUrl extends URL {
    static createObjectURL(blob) { blobs.push(blob); return "blob:local-plan"; }
    static revokeObjectURL() {}
  }
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, "../growth.js"), "utf8"), {
    document, URL: FakeUrl, URLSearchParams, Blob,
    window: { location: { hostname, search }, PDFLib: {}, CxPlanPdf: pdf, setTimeout() {}, ...(analytics ? { gtag: (...event) => events.push(event) } : {}) },
  });
  return { form, result, list, download, status, select, track, events, link, submit, pdf, createdLinks, blobs };
}

test("generation and PDF download are counted at most once per page, without checklist contents", async () => {
  const state = runResource({ ready: [0, 2] });
  state.form.events.submit({ preventDefault() {} });
  state.form.events.submit({ preventDefault() {} });
  await state.download.events.click();
  await state.download.events.click();
  assert.deepEqual(state.events.map((event) => event[1]), ["cx_resource_view", "cx_plan_generate", "cx_plan_download"]);
  assert.equal(state.list.children.length, 3);
  assert.equal(state.result.focused, true);
  assert.ok(state.events.every((event) => Object.keys(event[2]).every((key) => ["send_to", "placement", "file_format"].includes(key))));
  assert.equal(state.events[2][2].file_format, "pdf");
  assert.ok(state.createdLinks.every((link) => link.download.endsWith(".pdf")));
  assert.ok(state.blobs.every((blob) => blob.type === "application/pdf"));
  assert.ok(state.events.every((event) => event[2].send_to === "G-68E95X4DZT"));
  state.form.events.change();
  assert.equal(state.result.hidden, true);
  assert.equal(state.download.disabled, true);
});

test("local previews and missing Analytics do not collect events or break the PDF", async () => {
  for (const options of [{ hostname: "127.0.0.1" }, { analytics: false }]) {
    const state = runResource(options);
    state.form.events.submit({ preventDefault() {} });
    await state.download.events.click();
    assert.equal(state.result.hidden, false);
    assert.equal(state.status.textContent, "Prepared");
    assert.equal(state.events.length, 0);
  }
});

test("double clicks share one PDF operation and a changed plan cannot download stale actions", async () => {
  const state = runResource();
  state.form.events.submit({ preventDefault() {} });
  let finish;
  let calls = 0;
  state.pdf.create = () => { calls += 1; return new Promise((resolve) => { finish = resolve; }); };
  const first = state.download.events.click();
  await Promise.resolve();
  await state.download.events.click();
  assert.equal(calls, 1);
  assert.equal(state.download.disabled, true);
  state.form.events.change();
  finish({ bytes: new Uint8Array([37, 80, 68, 70]) });
  await first;
  assert.equal(state.createdLinks.length, 0);
  assert.equal(state.events.some((event) => event[1] === "cx_plan_download"), false);
  assert.equal(state.download.disabled, true);
});

test("a failed PDF can be retried without losing actions or emitting a download event", async () => {
  const state = runResource();
  state.form.events.submit({ preventDefault() {} });
  state.pdf.create = async () => { throw new Error("Unavailable"); };
  await state.download.events.click();
  assert.equal(state.status.textContent, "Unavailable");
  assert.equal(state.list.children.length, 3);
  assert.equal(state.download.disabled, false);
  assert.equal(state.events.some((event) => event[1] === "cx_plan_download"), false);
  state.pdf.create = async () => ({ bytes: new Uint8Array([37, 80, 68, 70]) });
  await state.download.events.click();
  assert.equal(state.status.textContent, "Prepared");
});

test("unknown and prototype-like topic parameters preserve a usable default", () => {
  for (const search of ["?topic=unknown", "?topic=__proto__", "?topic=constructor", "?topic=operations"]) {
    const state = runResource({ search });
    assert.equal(state.select.value, "operations");
    assert.equal(state.track.hidden, false);
  }
});

test("resource referral clicks use their placement and never financial events", () => {
  const state = runResource();
  state.link.events.click();
  assert.deepEqual(state.events.map((event) => event[1]), ["cx_resource_view", "cx_resource_click"]);
  assert.equal(state.events[1][2].placement, "home");
});
