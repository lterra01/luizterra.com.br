import products from "./products.json" with { type: "json" };
import { authenticated, normalizeNotification, transactionIdentity, measurement } from "./core.mjs";

const reply = (status, code) => Response.json({ code }, { status, headers: { "Cache-Control": "no-store" } });
const MAX_BODY = 128 * 1024;

async function boundedJson(request) {
  if (!request.headers.get("content-type")?.startsWith("application/json")) throw new Error("CONTENT_TYPE");
  const reader = request.body?.getReader();
  if (!reader) throw new Error("EMPTY_BODY");
  const chunks = [];
  let size = 0;
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > MAX_BODY) { await reader.cancel(); throw new Error("BODY_TOO_LARGE"); }
    chunks.push(value);
  }
  const body = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) { body.set(chunk, offset); offset += chunk.length; }
  return JSON.parse(new TextDecoder().decode(body));
}

export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    const ready = Boolean(env.HOTMART_HOTTOK && env.GA4_API_SECRET && env.IDENTITY_SECRET && env.TRANSACTIONS);
    if (request.method === "GET" && path === "/health") return reply(ready ? 200 : 503, ready ? `ready_${env.DELIVERY_MODE}` : "not_configured");
    if (path !== "/hotmart" || request.method !== "POST") return reply(404, "not_found");
    if (!ready || !["validate", "live"].includes(env.DELIVERY_MODE)) return reply(503, "not_configured");
    if (!await authenticated(request.headers.get("X-HOTMART-HOTTOK"), env.HOTMART_HOTTOK)) return reply(401, "unauthorized");
    let record;
    try { record = normalizeNotification(await boundedJson(request), products); }
    catch (error) {
      // Hotmart's configuration test uses a fictitious, unregistered product.
      if (error.message === "UNKNOWN_PRODUCT") return reply(200, "ignored_unregistered_product");
      return reply(error.message === "BODY_TOO_LARGE" ? 413 : 422, "requires_review");
    }
    if (!record) return reply(200, "ignored_non_financial_event");
    const identity = await transactionIdentity(record.transaction, env.IDENTITY_SECRET);
    const ledger = env.TRANSACTIONS.get(env.TRANSACTIONS.idFromName(identity.key));
    return ledger.fetch(new Request("https://internal/notification", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ record, clientId: identity.clientId }),
    }));
  },
};

export class TransactionLedger {
  constructor(state, env) { this.state = state; this.env = env; }

  async fetch(request) {
    // Serialize a transaction, including simultaneous approved/refund deliveries.
    return this.state.blockConcurrencyWhile(async () => {
      const { record, clientId } = await request.json();
      const key = `${this.env.DELIVERY_MODE}:${record.kind}`;
      const previous = await this.state.storage.get(key);
      if (["submitted", "validated"].includes(previous?.status)) return reply(200, "duplicate_ignored");
      if (["sending", "uncertain"].includes(previous?.status)) return reply(202, "delivery_requires_review");
      if (record.at > Date.now() + 300000 || record.at < Date.now() - 72 * 3600000) {
        await this.state.storage.put(key, { status: "review", reason: "timestamp_outside_ga4_window", record });
        return reply(202, "timestamp_requires_review");
      }
      if (record.kind === "refund") {
        const purchase = await this.state.storage.get(`${this.env.DELIVERY_MODE}:purchase`);
        if (!purchase || !["submitted", "validated"].includes(purchase.status)) {
          await this.state.storage.put(key, { status: "review", reason: "purchase_not_submitted", record });
          return reply(503, "refund_waiting_for_purchase");
        }
        record.value = purchase.record.value;
        record.currency = purchase.record.currency;
      }
      const validate = this.env.DELIVERY_MODE === "validate";
      const target = new URL(`https://www.google-analytics.com/${validate ? "debug/" : ""}mp/collect`);
      target.searchParams.set("measurement_id", this.env.GA4_MEASUREMENT_ID);
      target.searchParams.set("api_secret", this.env.GA4_API_SECRET);
      await this.state.storage.put(key, { status: "sending", record });
      try {
        const result = await fetch(target, { method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify(measurement(record, clientId)), signal: AbortSignal.timeout(15000) });
        if (!result.ok) {
          await this.state.storage.put(key, { status: "review", reason: "ga4_http_error", record });
          return reply(502, "delivery_failed");
        }
        if (validate && (await result.json()).validationMessages?.length) {
          await this.state.storage.put(key, { status: "review", reason: "ga4_validation_error", record });
          return reply(422, "validation_failed");
        }
        await this.state.storage.put(key, { status: validate ? "validated" : "submitted", record });
        return reply(200, validate ? "validated_not_collected" : "submitted_not_report_verified");
      } catch {
        // A timeout can follow acceptance. Do not blindly resend financial events.
        await this.state.storage.put(key, { status: "uncertain", record });
        return reply(202, "delivery_requires_review");
      }
    });
  }
}
