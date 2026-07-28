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

## Assets

- `public/luiz-terra-executive-bio.pdf`
- `public/og-image.png`
- `public/favicon.svg`

## Search Discovery

- Canonical and hreflang metadata for English, Brazilian Portuguese and Spanish
- ProfilePage, Person, BlogPosting, BreadcrumbList and FAQPage structured data
- `sitemap.xml` with canonical localized URLs and image discovery
- `feed.xml` for article discovery
- `llms.txt` for AI search and answer-engine context
- IndexNow key file for search-engine notifications

## Editorial Note

The repository does not currently include the 12 previously prepared LinkedIn posts. The site uses the six approved insight topics already present in the website content and provides localized article routes for them. When the 12 posts are available, add them to the article data in `tools/build_static_site.py` and regenerate the static pages.

## Manual Checks

- Validate social preview with LinkedIn Post Inspector and WhatsApp after cache propagation.
- Add an executive photo at `public/images/luiz-terra-executive.jpg` if a final approved headshot is provided.
