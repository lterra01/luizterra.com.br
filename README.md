# Luiz Terra Executive Website

Static executive website for Luiz Terra, published with GitHub Pages.

## Current Positioning

International Sales Executive in Telecom, CX, BPO and AI, focused on strategic partnerships, market-entry conversations, speaking opportunities and executive networking across LATAM, North America, Europe and Africa.

## Routes

- `/` - English home and x-default
- `/en/` - English version
- `/pt/` - Portuguese version
- `/es/` - Spanish version
- `/insights/`, `/pt/insights/`, `/es/insights/`
- Localized article pages under each insights route
- `/executive-bio/`, `/pt/executive-bio/`, `/es/executive-bio/`
- Six localized topic clusters under `/topics/`, `/pt/topics/` and `/es/topics/`

## Assets

- `public/luiz-terra-executive-bio.pdf`
- `public/og-image.png`
- Article-specific social images under `public/og/`
- `public/favicon.svg`

## Search Discovery

- Canonical and hreflang metadata for English, Brazilian Portuguese and Spanish
- ProfilePage, Person, BlogPosting, BreadcrumbList and FAQPage structured data
- `sitemap.xml` with canonical localized URLs and image discovery
- `feed.xml` for article discovery
- `llms.txt` for AI search and answer-engine context
- IndexNow key file for search-engine notifications

## Editorial Note

The initial authority collection was developed editorially for the requested search topics. New newsletter editions are synchronized only after public publication is confirmed on LinkedIn, with a visible original-edition link and editorial versions in English, Portuguese and Spanish. Confirmed editions incorporated through this flow: The New CX Stack (16 October 2026) and Voice AI Needs Telecom Discipline (23 October 2026). Earlier LinkedIn post texts are not assumed to be newsletter editions.

## eBook Storefront

- Collection: `/ebooks/`, `/pt/ebooks/`, `/es/ebooks/`, with 6 independently sold titles from `tools/ebook_catalog.py`.
- Additional titles and release receipts: `tools/ebook_launches.py`. Drafts are excluded from sale links, bonus choices and the financial allowlist until author release approval, Hotmart terms, delivery, active sales and checkout are verified.
- Sales pages: `/ebooks/cx-na-operacao/`, `/pt/ebooks/cx-na-operacao/`, `/es/ebooks/cx-na-operacao/`.
- Every existing product includes Portuguese, English and Spanish PDFs at the unchanged R$ 9.99 price. The original Portuguese files were preserved; the six translated files were added and read back from Hotmart on 29 October 2026.
- First-book detailed copy: `tools/ebook_content.py`; catalog facts, copy and Hotmart IDs: `tools/ebook_catalog.py`. Rebuild with `tools/build_static_site.py`.
- The public site contains promotional images only. Do not add the paid PDF or editable manuscript to this repository.
- Existing pages include a persistent announcement and a dismissible native dialog shown once per browser session. Blocked session storage disables the dialog, not the announcement.
- GA4 `G-68E95X4DZT` receives `ebook_introduction_view`, `ebook_offer_continue`, `ebook_site_continue`, `ebook_landing_view`, `ebook_catalog_view`, `ebook_product_view`, `ebook_landing_click` and `ebook_checkout_click`. Product interactions supply their own ID and title; collection exposure supplies only the collection ID. These are not paid purchases. Localhost does not send Analytics events.
- Authenticated server-side purchase/refund receiver: `integrations/hotmart-ga4/`. Deployment, secrets, validation and financial limitations are documented there; code availability alone does not mean it is activated. See `docs/EBOOK_ANALYTICS.md` and `docs/GA4_REPORTS.md` for reporting definitions.
- Verified checkout links and promotional covers are in the catalog. Recheck Hotmart before changing price, refund period or delivery claims. Paid files must remain outside this public repository.

## Mini Expert

- Independent AI assistant subscription: `/mini-expert/indicadores-de-atendimento/`, `/pt/mini-expert/indicadores-de-atendimento/`, `/es/mini-expert/indicadores-de-atendimento/`.
- Canonical offer and localized copy: `tools/mini_expert_content.py`. Verified on 27 October 2026: Hotmart product `8822826`, active sales, individual monthly plan at R$ 199.90 until cancelled, 7-day refund period.
- The service is in Portuguese, accessed through Hotmart. It is not an eBook, is not included with an eBook purchase and does not include human consulting or automatic integrations. AI responses require verification; submit only authorised aggregated or anonymised data.
- Featured on the home pages and eBook collection; linked from every footer. Public promotional cover only; no private agent instructions or knowledge files are published.
- GA4 intent events use `mini_expert_landing_view`, `mini_expert_product_view`, `mini_expert_landing_click` and `mini_expert_checkout_click`, separate from `ebook_*`. No purchase is emitted by the website. The financial allowlist follows released eBooks only; subscription purchases and renewals are not yet connected to GA4.
- Rebuild with `tools/build_static_site.py`. Rollback this addition through a dedicated Git revert and republish GitHub Pages; do not delete financial events or change the existing receiver.

## Consulting and Manual Bonuses

- Localized Fiverr landing pages use `/consultoria/indicadores-de-atendimento/` with `/pt/` and `/es/` variants. Public offer and scope are in `tools/commerce_content.py`.
- The service uses one aggregated file, one operation/channel, two comparable periods, up to ten KPIs, a Portuguese PDF, five-day delivery and one in-scope revision. Ordering, payment and delivery stay on Fiverr.
- `/bonus/`, `/pt/bonus/` and `/es/bonus/` prepare a choice of exactly two titles. A prepared message is neither sent nor approved. No paid file is exposed by the website.
- First approved AI Agent or Fiverr consulting purchase: two chosen titles once per customer across services, not per renewal. Each title includes three language PDFs. Fiverr redemption remains in the paid order's messages.
- `tools/voucher_registry.py` manages private 30-day, single-use manual grants outside Git. It does not verify payments, automatically deliver files or emit purchase events. See `docs/BONUS_OPERATIONS.md` for the operator workflow.
- `fiverr_*` and `bonus_*` events measure intent only, without voucher codes, buyer details, order IDs, purchase or revenue. The financial receiver's eBook allowlist follows only released catalogue IDs; service purchases remain separate.

## Manual Checks

- Validate social preview with LinkedIn Post Inspector and WhatsApp after cache propagation.
- Validate structured data after deployment with Google Rich Results Test.
