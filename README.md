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

- Sales pages: `/ebooks/cx-na-operacao/`, `/pt/ebooks/cx-na-operacao/`, `/es/ebooks/cx-na-operacao/`.
- The product is a Portuguese PDF. English and Spanish pages describe the same Portuguese edition.
- Product facts and copy: `tools/ebook_content.py`; rebuild with `tools/build_static_site.py`.
- The public site contains promotional images only. Do not add the paid PDF or editable manuscript to this repository.
- Existing pages include a persistent announcement and a dismissible native dialog shown once per browser session. Blocked session storage disables the dialog, not the announcement.
- GA4 `G-68E95X4DZT` receives `ebook_introduction_view` (exposure), `ebook_offer_continue` (offer choice), `ebook_site_continue` (continue browsing), `ebook_landing_click` and `ebook_checkout_click` (separate intent events). They are not purchase or revenue confirmations. See `docs/EBOOK_ANALYTICS.md` for definitions and validation limits.
- The verified checkout is https://pay.hotmart.com/Q108197102H. Recheck Hotmart before changing price, refund period or delivery claims.

## Manual Checks

- Validate social preview with LinkedIn Post Inspector and WhatsApp after cache propagation.
- Validate structured data after deployment with Google Rich Results Test.
