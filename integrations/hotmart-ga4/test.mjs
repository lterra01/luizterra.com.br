import assert from "node:assert/strict";
import { test } from "node:test";
import products from "./products.json" with { type: "json" };
import worker, { TransactionLedger } from "./worker.mjs";
import { normalizeNotification, measurement, authenticated, transactionIdentity } from "./core.mjs";

const fixture = (event = "PURCHASE_APPROVED", status = "APPROVED") => ({
  id: "unit-test-event", version: "2.0.0", event, creation_date: Date.now(),
  data: { product: { id: 8811999 }, purchase: { status, transaction: "HPUNITTEST12345", approved_date: Date.now(),
    price: { value: 9.99, currency_value: "BRL" }, full_price: { value: 10.49, currency_value: "BRL" },
    payment: { card: "PRIVATE_TEST_CARD" } }, buyer: { name: "PRIVATE_TEST_BUYER", email: "private@example.invalid" },
    commissions: [{ value: 7.11 }] },
});

function harness(mode = "validate", fetcher = async () => Response.json({ validationMessages: [] })) {
  const values = new Map();
  let serial = Promise.resolve();
  const state = {
    storage: { async get(key) { return values.get(key); }, async put(key, value) { values.set(key, structuredClone(value)); } },
    blockConcurrencyWhile(callback) { const result = serial.then(callback); serial = result.catch(() => {}); return result; },
  };
  const env = { HOTMART_HOTTOK: "TEST_ONLY_HOTTOK", GA4_API_SECRET: "TEST_ONLY_API_SECRET", IDENTITY_SECRET: "TEST_ONLY_IDENTITY_KEY",
    GA4_MEASUREMENT_ID: "G-68E95X4DZT", DELIVERY_MODE: mode };
  const ledger = new TransactionLedger(state, env);
  env.TRANSACTIONS = { idFromName: value => value, get: () => ({ fetch: req => ledger.fetch(req) }) };
  const calls = [];
  const original = globalThis.fetch;
  globalThis.fetch = async (url, options) => { calls.push({ url: String(url), body: JSON.parse(options.body) }); return fetcher(url, options); };
  return { env, values, calls, restore() { globalThis.fetch = original; },
    post(payload, token = env.HOTMART_HOTTOK) { return worker.fetch(new Request("https://unit.test/hotmart", {
      method: "POST", headers: { "Content-Type": "application/json", "X-HOTMART-HOTTOK": token }, body: JSON.stringify(payload),
    }), env); },
  };
}

test("only approved payments become purchases, never pending boleto or Pix", () => {
  for (const status of ["WAITING_PAYMENT", "PRINTED_BILLET", "STARTED", "PROCESSING_TRANSACTION"]) {
    assert.throws(() => normalizeNotification(fixture("PURCHASE_APPROVED", status), products), /STATUS/);
  }
  for (const event of ["PURCHASE_BILLET_PRINTED", "PURCHASE_COMPLETE", "PURCHASE_CANCELED"]) {
    assert.equal(normalizeNotification(fixture(event), products), null);
  }
});

test("actual offer amount is used, not commission, fixed list price, tax or interest", () => {
  const payload = fixture(); payload.data.purchase.price.value = 7.99;
  const normalized = normalizeNotification(payload, products);
  assert.equal(normalized.value, 7.99);
  assert.equal(normalized.ebook_id, "indicadores-de-atendimento-na-pratica");
  const json = JSON.stringify(measurement(normalized, "123.456"));
  assert.equal(/PRIVATE_TEST|private@|buyer|commissions|payment/.test(json), false);
});

test("every released eBook retains its own identity in a purchase item", () => {
  assert.equal(new Set(products.map(product => product.id)).size, products.length);
  assert.equal(new Set(products.map(product => product.hotmart_id)).size, products.length);
  for (const product of products) {
    const payload = fixture();
    payload.data.product.id = Number(product.hotmart_id);
    const normalised = normalizeNotification(payload, products);
    assert.equal(normalised.ebook_id, product.id);
    const event = measurement(normalised, "123.456").events[0];
    assert.equal(event.name, "purchase");
    assert.equal(event.params.items.length, 1);
    assert.equal(event.params.items[0].item_id, product.id);
    assert.equal(event.params.items[0].item_name, product.name);
    assert.equal(event.params.items[0].quantity, 1);
    assert.equal(event.params.value, 9.99);
    assert.equal(event.params.currency, "BRL");
  }
});

test("unregistered products cannot normalize; malformed amounts and partial refunds require review", () => {
  const unknown = fixture(); unknown.data.product.id = 999;
  assert.throws(() => normalizeNotification(unknown, products), /UNKNOWN_PRODUCT/);
  for (const value of [-1, Infinity, NaN, "9.99", null]) {
    const payload = fixture(); payload.data.purchase.price.value = value;
    assert.throws(() => normalizeNotification(payload, products), /INVALID_PRICE/);
  }
  assert.throws(() => normalizeNotification(fixture("PURCHASE_REFUNDED", "PARTIALLY_REFUNDED"), products), /STATUS/);
});

test("Hottok validation is mandatory and transaction identities are stable and opaque", async () => {
  assert.equal(await authenticated("wrong", "TEST_ONLY_SECRET"), false);
  assert.equal(await authenticated("TEST_ONLY_SECRET", "TEST_ONLY_SECRET"), true);
  const a = await transactionIdentity("HPUNITTEST12345", "TEST_ONLY_SECRET");
  assert.deepEqual(a, await transactionIdentity("HPUNITTEST12345", "TEST_ONLY_SECRET"));
  assert.notEqual(a.key, (await transactionIdentity("HPUNITTEST67890", "TEST_ONLY_SECRET")).key);
  assert.equal(a.key.includes("HPUNITTEST"), false);
});

test("authenticated fictitious or unregistered products are acknowledged but never collected", async () => {
  const h = harness("live");
  try {
    const payload = fixture(); payload.data.product.id = 999;
    assert.equal((await h.post(payload, "wrong")).status, 401);
    const response = await h.post(payload);
    assert.equal(response.status, 200);
    assert.equal((await response.json()).code, "ignored_unregistered_product");
    assert.equal(h.calls.length, 0);
    assert.equal(h.values.size, 0);
  } finally { h.restore(); }
});

test("validation mode never posts to the collection endpoint and stores no buyer data", async () => {
  const h = harness();
  try {
    assert.equal((await h.post(fixture(), "wrong")).status, 401);
    assert.equal(h.calls.length, 0);
    assert.equal((await h.post(fixture())).status, 200);
    assert.equal(new URL(h.calls[0].url).pathname, "/debug/mp/collect");
    assert.equal(h.values.get("validate:purchase").status, "validated");
    assert.equal(JSON.stringify([...h.values.values()]).includes("PRIVATE_TEST"), false);
  } finally { h.restore(); }
});

test("simultaneous retries and different approval notifications count only once", async () => {
  const h = harness("live", async () => new Response(null, { status: 204 }));
  try {
    const responses = await Promise.all([h.post(fixture()), h.post(fixture())]);
    assert.equal(responses.every(response => response.status === 200), true);
    assert.equal(h.calls.length, 1);
    assert.equal(h.calls[0].body.events[0].name, "purchase");
    assert.equal(h.values.get("live:purchase").status, "submitted");
  } finally { h.restore(); }
});

test("uncertain network acceptance never blindly resends a financial event", async () => {
  const h = harness("live", async () => { throw new Error("test timeout"); });
  try {
    assert.equal((await h.post(fixture())).status, 202);
    assert.equal((await h.post(fixture())).status, 202);
    assert.equal(h.calls.length, 1);
    assert.equal(h.values.get("live:purchase").status, "uncertain");
  } finally { h.restore(); }
});

test("refunds need a recorded approval and cannot be counted twice as refund and chargeback", async () => {
  const h = harness("live", async () => new Response(null, { status: 204 }));
  try {
    assert.equal((await h.post(fixture("PURCHASE_REFUNDED", "REFUNDED"))).status, 503);
    assert.equal(h.calls.length, 0);
    await h.post(fixture());
    await h.post(fixture("PURCHASE_REFUNDED", "REFUNDED"));
    await h.post(fixture("PURCHASE_CHARGEBACK", "CHARGEBACK"));
    assert.deepEqual(h.calls.map(call => call.body.events[0].name), ["purchase", "refund"]);
  } finally { h.restore(); }
});

test("old financial notifications are preserved for review, not backdated incorrectly", async () => {
  const h = harness();
  try {
    const payload = fixture(); payload.data.purchase.approved_date = Date.now() - 73 * 3600000;
    assert.equal((await h.post(payload)).status, 202);
    assert.equal(h.calls.length, 0);
  } finally { h.restore(); }
});
