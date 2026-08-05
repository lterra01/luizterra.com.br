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

The repository still does not include the source text for the 12 previously prepared LinkedIn posts. The six existing Insights were preserved and expanded in place, and seven new long-form articles were added for the requested search topics without creating near-duplicate pages. If the original LinkedIn source becomes available, it should be reviewed editorially before import.

## Manual Checks

- Validate social preview with LinkedIn Post Inspector and WhatsApp after cache propagation.
- Validate structured data after deployment with Google Rich Results Test.
