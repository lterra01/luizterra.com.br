# eBook Launch - 29 October 2026

Status: the author confirmed product finalisation and terms acceptance and explicitly requested website publication. All three additional products show active sales and their public checkouts were verified. Website deployment is in progress.

| Volume | Title | Hotmart ID | Price setting | Files |
| --- | --- | --- | --- | --- |
| 4 | IA no Atendimento: do Piloto a Operacao | 8836219 | BRL 9.99, one-time | PT, EN, ES |
| 5 | Voz e Telecom para CX | 8836306 | BRL 9.99, one-time | PT, EN, ES |
| 6 | Vendas Consultivas em Telecom e CX | 8836331 | BRL 9.99, one-time | PT, EN, ES |

Each edition has 25 pages, a simulated worked case and four worksheets. Paid files, editable manuscripts, ZIPs and platform screenshots remain outside this public repository. Each new product has its own cover and explicit AI-assistance disclosure. No real customer examples or performance claims were added.

The saved base refund setting is 7 days. Hotmart also displays regional conditions; the checkout remains authoritative for the buyer's applicable conditions. Donations are inactive and automatic international currency conversion is active. No subscription or price change to an existing offer is part of this addition.

## Release Control

`tools/ebook_launches.py` holds prepared catalogue metadata and the observed Hotmart links. A generated link does not prove that a checkout is available for sale. Keep `checkout_verified` false until the destination itself is checked.

`released_additions()` excludes draft/prepared records. A release requires all of:

1. Luiz Terra's approval to release the current version after the requested corrections.
2. The author's confirmation that he completed Hotmart finalisation and accepted its terms.
3. Read-back of all three saved files in the product.
4. An observed active-sales state.
5. A verified public checkout with correct title, price and refund terms.

Changing a flag is not a substitute for the corresponding evidence. An explicit platform eligibility question must be answered truthfully; the materials were prepared with AI assistance. Do not assert otherwise.

The `author_release_approved` receipt records the explicit request to publish after
the cover-only correction. It does not assert that the agent witnessed a particular
manuscript-reading process. Terms were accepted by Luiz, not by the agent.

Public checkouts verified without entering buyer data or submitting payment:

- IA: `https://pay.hotmart.com/P108249096W`, author Luiz Terra, total BRL 9.99.
- Voice: `https://pay.hotmart.com/A108249258G`, author Luiz Terra, total BRL 9.99.
- Sales: `https://pay.hotmart.com/F108249305B`, author Luiz Terra, total BRL 9.99.

## Website and Analytics

- The storefront, localized titles, bonus selectors and private voucher title list follow only `EBOOKS`, the released catalogue.
- The financial `products.json` is generated from that same catalogue. Prepared drafts must not be collected as approved sales.
- The original three products, their IDs, checkouts and prices remain unchanged.
- Announcements, service FAQs and bonus copy use the actual released count. The benefit stays at two distinct titles, once per customer, not per renewal or order.
- When additions are released, the presentation receives a catalogue-specific campaign ID and session key. Existing historical campaign data is preserved; the unchanged three-title catalogue keeps its original ID and session key.
- Browser events remain intent only. Do not emit `purchase`, invent revenue or send live financial tests.
- Report 01 uses `ebook_*` events, and report 04 uses the `eBook` item category according to the existing configuration record. Their generic definitions do not require a separate report for every title. Recheck the authenticated report before claiming a live configuration change.

## Activation Sequence

1. Completed by Luiz: finalise the three Hotmart submissions and accept the terms; release explicitly requested.
2. Verified: active sales and each actual checkout, without submitting buyer or payment data.
3. Completed locally: update the release evidence/flags and copy only promotional WebP covers into `public/ebooks/`.
4. Completed locally: rebuild pages, discovery files and README. The 22 Python and 34 Node tests passed; the Worker bundle passed its official dry-run.
5. Completed: the six-product allowlist was deployed with official Wrangler, preserving secrets, Durable Objects and the financial ledger. The existing Hotmart GA4 webhook was saved and reopened with these same six eBooks and only the original three financial events. The Mini Expert and the other webhook were not added or modified.
6. Update the Mini Expert's bonus description and the existing Fiverr FAQ to two of six. Do not change service prices, scope, renewal terms or Fiverr delivery channels. Do not add an eleventh FAQ.
7. Publish the website; read back the real six-title catalogue, bonus choices, schema, campaign ID, sitemap and asset versions.
8. If the genuine-sale automation is still active and its purpose remains valid, update its product scope without creating a duplicate or replaying events. No sale is inferred from this launch.

Local private layout preview: all six titles, with draft checkout controls disabled. The preview is `noindex,nofollow`, has no Google collection scripts and contains no paid files. It does not constitute deployment, a public offer, a Google indexing request or a purchase receipt.

## Checks Performed

- PDF rendering: 225 pages across nine editions, plus focused table/worksheet inspection. No text bounds failures; example arithmetic independently checked.
- Responsive catalogue preview: PT/EN/ES at 375, 768 and 1280 pixels, no horizontal overflow, visible cover files loaded, reduced-motion scrolling respected.
- Six-title bonus preview: exactly two selected titles, other four disabled; Fiverr origin hides email and prepares an unsent request. No message or voucher was sent.
- Current release tests: Python 22, Node site 23, receiver 11. All passed locally.
- The six-product Worker allowlist was published in the existing live Worker. HTTPS `/health` returned 200 `ready_live`. The Hotmart webhook product selection was saved and reopened with six eBooks and three financial events. Public site deployment is recorded separately; none of these receipts proves an approved sale or processed GA4 revenue.
- No purchase, payment submission, live financial test, replay or credentials change was performed.

## Rollback

For preparatory code, use a dedicated Git revert if needed. Do not reset unrelated work, delete Analytics history, rotate credentials or clear the financial ledger. If a later live launch is reverted, reconcile website, webhook selection and Worker allowlist together rather than leaving mismatched product scopes.

## Cover Revision

The user limited the requested corrections to the three covers. Matching
illustrated artwork was prepared from the existing collection's visual direction,
including localized first pages for all nine PDF editions. Every manuscript and
all 216 internal PDF pages were preserved without reflow or text edits.

The three draft product images were saved and checked after reloading. With the
user's specific authorization, the nine old draft PDFs were removed and their
cover-only replacements uploaded. All three saved lists were reopened with
exactly one PT, one EN and one ES file. The AI/PT remote cover was also sampled
through the platform's PDF viewer; no remote binary equivalence claim is made.

The private layout preview and delivery ZIPs use the revised artwork. No paid
files or private evidence were added to this repository. Only the promotional
WebP covers were copied for the authorised launch. The prior cover-only operation
did not finalise products or accept terms; Luiz performed those actions afterwards.
