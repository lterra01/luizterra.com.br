const assert = require("node:assert/strict");
const { test } = require("node:test");
const { selectActions, planCsv, csvCell } = require("../growth.js");
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

test("the CSV is UTF-8 compatible, quoted and contains actions rather than user answers", () => {
  const csv = planCsv(["Prioridade", "Ação", "Evidência", "Revisão"], [["private answer", 'Conferir "volume"; canal', "Período completo"]], "Próxima semana");
  assert.ok(csv.startsWith("\uFEFF"));
  assert.ok(csv.includes('"Conferir ""volume""; canal"'));
  assert.ok(csv.includes("Próxima semana"));
  assert.ok(!csv.includes("private answer"));
});

test("spreadsheet formula prefixes are escaped", () => {
  for (const value of ["=SUM(A1:A3)", "+1", "-1", "@formula", "\tvalue", "\rvalue"]) {
    assert.ok(csvCell(value).startsWith('"\''));
  }
  assert.equal(csvCell("Ação"), '"Ação"');
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
  const data = { lang: "pt", tracks: { operations: checks }, evidence: "Evidence", headers: ["#", "Action", "Evidence", "Review"], cadence: "Next week", downloaded: "Prepared", download_error: "Unavailable" };
  const document = {
    body: new Element(),
    querySelector(selector) {
      return { "[data-cx-resource]": resource, "#cx-plan-data": { textContent: JSON.stringify(data) }, "#cx-priority": select }[selector];
    },
    querySelectorAll: () => [link],
    createElement: () => new Element(),
  };
  class FakeUrl extends URL {
    static createObjectURL() { return "blob:local-plan"; }
    static revokeObjectURL() {}
  }
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, "../growth.js"), "utf8"), {
    document, URL: FakeUrl, URLSearchParams, Blob,
    window: { location: { hostname, search }, setTimeout() {}, ...(analytics ? { gtag: (...event) => events.push(event) } : {}) },
  });
  return { form, result, list, download, status, select, track, events, link, submit };
}

test("generation and download are counted at most once per page, without checklist contents", () => {
  const state = runResource({ ready: [0, 2] });
  state.form.events.submit({ preventDefault() {} });
  state.form.events.submit({ preventDefault() {} });
  state.download.events.click();
  state.download.events.click();
  assert.deepEqual(state.events.map((event) => event[1]), ["cx_resource_view", "cx_plan_generate", "cx_plan_download"]);
  assert.equal(state.list.children.length, 3);
  assert.equal(state.result.focused, true);
  assert.ok(state.events.every((event) => Object.keys(event[2]).sort().join() === "placement,send_to"));
  assert.ok(state.events.every((event) => event[2].send_to === "G-68E95X4DZT"));
  state.form.events.change();
  assert.equal(state.result.hidden, true);
  assert.equal(state.download.disabled, true);
});

test("local previews and missing Analytics do not collect events or break the plan", () => {
  for (const options of [{ hostname: "127.0.0.1" }, { analytics: false }]) {
    const state = runResource(options);
    state.form.events.submit({ preventDefault() {} });
    state.download.events.click();
    assert.equal(state.result.hidden, false);
    assert.equal(state.status.textContent, "Prepared");
    assert.equal(state.events.length, 0);
  }
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
