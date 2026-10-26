import assert from "node:assert/strict";
import products from "./products.json" with { type: "json" };

const base = new URL(process.env.WORKER_URL);
assert.equal(base.protocol, "https:");
assert.equal(base.hostname, "luizterra-hotmart-ga4.luizterra-hotmart-ga4.workers.dev", "Unapproved credential destination");
assert.ok(process.env.HOTMART_HOTTOK, "Missing private Hottok environment variable");
const health = await fetch(new URL("/health", base));
assert.equal(health.status, 200);
assert.equal((await health.json()).code, "ready_validate", "Refusing synthetic events outside validation mode");
const endpoint = new URL("/hotmart", base);
const denied = await fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
assert.equal(denied.status, 401);
const receipts = [];
for (const book of products) {
  const at = Date.now();
  const notification = {
    version: "2.0.0", event: "PURCHASE_APPROVED", creation_date: at,
    data: { product: { id: Number(book.hotmart_id) }, purchase: {
      status: "APPROVED", transaction: `HPQA-${at}-${book.hotmart_id}`, approved_date: at,
      price: { value: 9.99, currency_value: "BRL" },
    } },
  };
  const post = () => fetch(endpoint, { method: "POST", headers: {
    "Content-Type": "application/json", "X-HOTMART-HOTTOK": process.env.HOTMART_HOTTOK,
  }, body: JSON.stringify(notification) });
  const response = await post();
  const receipt = await response.json();
  assert.equal(response.status, 200, `${book.id}: ${receipt.code}`);
  assert.equal(receipt.code, "validated_not_collected");
  const duplicate = await post();
  assert.equal(duplicate.status, 200);
  assert.equal((await duplicate.json()).code, "duplicate_ignored");
  receipts.push({ product: book.id, receipt: receipt.code, duplicate: "ignored" });
}
console.log(JSON.stringify({ mode: "validate", productionPurchasesSent: 0, receipts }, null, 2));
