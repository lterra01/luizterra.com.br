const ACCEPTED = new Map([
  ["PURCHASE_APPROVED", ["purchase", "APPROVED"]],
  ["PURCHASE_REFUNDED", ["refund", "REFUNDED"]],
  ["PURCHASE_CHARGEBACK", ["refund", "CHARGEBACK"]],
]);

export function normalizeNotification(payload, products) {
  if (payload?.version !== "2.0.0") throw new Error("UNSUPPORTED_VERSION");
  const expected = ACCEPTED.get(payload.event);
  if (!expected) return null;
  const data = payload.data;
  const product = products.find(book => book.hotmart_id === String(data?.product?.id));
  if (!product) throw new Error("UNKNOWN_PRODUCT");
  const purchase = data?.purchase;
  if (purchase?.status !== expected[1]) throw new Error("STATUS_REQUIRES_REVIEW");
  if (typeof purchase.transaction !== "string" || !/^HP[A-Za-z0-9_-]{5,78}$/.test(purchase.transaction)) throw new Error("INVALID_TRANSACTION");
  const price = purchase.price;
  if (typeof price?.value !== "number" || !Number.isFinite(price.value) || price.value < 0 || price.value > 100000 || !/^[A-Z]{3}$/.test(price.currency_value)) throw new Error("INVALID_PRICE");
  const at = expected[0] === "purchase" ? purchase.approved_date : payload.creation_date;
  if (!Number.isSafeInteger(at) || at <= 0) throw new Error("INVALID_DATE");
  // Allowlist only financial fields. Buyer, address and payment details stop here.
  return {
    kind: expected[0], transaction: purchase.transaction, at,
    value: price.value, currency: price.currency_value,
    ebook_id: product.id, ebook_title: product.name, hotmart_product_id: product.hotmart_id,
  };
}

export async function authenticated(provided, expected) {
  if (!provided || !expected || provided.length > 1024) return false;
  const encoder = new TextEncoder();
  const actualHash = new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(provided)));
  const expectedHash = new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(expected)));
  let difference = 0;
  for (let i = 0; i < expectedHash.length; i++) difference |= actualHash[i] ^ expectedHash[i];
  return difference === 0;
}

export async function transactionIdentity(transaction, secret) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", encoder.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const bytes = new Uint8Array(await crypto.subtle.sign("HMAC", key, encoder.encode(transaction)));
  const hex = Array.from(bytes, byte => byte.toString(16).padStart(2, "0")).join("");
  // Transaction-scoped identity, not a person or an attributed website session.
  return { key: hex, clientId: `${BigInt(`0x${hex.slice(0, 16)}`)}.${BigInt(`0x${hex.slice(16, 32)}`)}` };
}

export function measurement(record, clientId) {
  return {
    client_id: clientId,
    timestamp_micros: record.at * 1000,
    consent: { ad_user_data: "DENIED", ad_personalization: "DENIED" },
    validation_behavior: "ENFORCE_RECOMMENDATIONS",
    events: [{ name: record.kind, params: {
      transaction_id: `hotmart:${record.transaction}`, value: record.value, currency: record.currency,
      ebook_id: record.ebook_id, ebook_title: record.ebook_title, hotmart_product_id: record.hotmart_product_id,
      measurement_origin: "hotmart_webhook", attribution_scope: "transaction_only",
      items: [{ item_id: record.ebook_id, item_name: record.ebook_title, item_brand: "Luiz Terra",
        item_category: "eBook", affiliation: "Hotmart", price: record.value, quantity: 1 }],
    } }],
  };
}
