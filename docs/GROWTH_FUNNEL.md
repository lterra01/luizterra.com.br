# CX Resource And Commercial Journey

Release date: 2026-11-01. The marketing plan, private account observations and social drafts remain outside this public repository.

## Journey

An external educational post or a search article can lead to the free CX action plan. The visitor chooses one of six topics, marks points already defined and generates up to three next actions. The visitor downloads a branded, three-page A4 PDF with priorities, execution fields and a follow-up worksheet. A matching released eBook is recommended. Only the metrics track presents the separate Portuguese-language AI subscription and Fiverr KPI analysis.

- Localised resource: `/resources/cx-action-plan/`, `/pt/resources/cx-action-plan/`, `/es/resources/cx-action-plan/`.
- Canonical copy and explicit recommendation rules: `tools/growth_content.py`.
- Rendering and related-article mapping: `tools/build_static_site.py`.
- Behaviour: `growth.js`; styling: `growth.css`. Both use versioned URLs.
- Browser PDF layout: `growth-pdf.js`, loaded on resource pages only. The local MIT-licensed `pdf-lib` 1.17.1 distribution is loaded on first export, not on ordinary site visits. No CDN, remote conversion service, API or framework is used for PDF generation.
- The six checklists contain original free educational material, not extracts of paid manuscripts.
- Existing prices, subscription terms, delivered languages and manual two-book bonus rules remain unchanged.
- The focused resource does not open the promotional dialog. Existing home/article introductions are preserved. Without JavaScript all six checklists and purchase links remain readable; generation buttons stay disabled rather than submitting answers in a URL.

## Measurement

| Event | Definition | Counting rule |
|---|---|---|
| `cx_resource_click` | Click on an internal resource CTA. | Per click; controlled `placement` only. |
| `cx_resource_view` | Resource initialised with working JavaScript. | Once per page load. Not a person, read or lead. |
| `cx_plan_generate` | Visitor generated a plan. | At most once per page load, across all topics and regenerations. |
| `cx_plan_download` | PDF prepared and a browser download triggered. | At most once per page load, with `file_format=pdf`. Not proof the file was saved or read. |
| `ebook_product_view` | A book recommendation is at least half visible. | Existing once-per-element observer; placement distinguishes `article` and `resource`. |
| `ebook_checkout_click` | Click to the matching real Hotmart checkout. | Intent only; product identity and placement are retained. |
| `mini_expert_landing_click` | Click to the AI service detail page. | Existing non-financial event. |
| `fiverr_landing_click` | Click to the consulting detail page. | Existing non-financial event. |

All new events explicitly target GA4 `G-68E95X4DZT`, only on the two own-domain hostnames. They do not emit `purchase`, `refund`, revenue or Google Ads conversion events. Local previews do not collect production events. Paid transaction processing and the financial allowlist were not changed.

Checklist choices, text, files, contact details and calculated action lists are not sent as event parameters or stored in browser storage. A public `topic` URL parameter can choose a track but does not contain checklist answers. The PDF is generated locally. Its initially empty owner, deadline, progress and review fields can be completed later in a PDF reader; they have no submission action and are never uploaded to the site. Ordinary page-location collection still follows the site's existing Google tag configuration; do not put personal information in campaign URLs.

The PDF replaces the original CSV export. Historical `cx_plan_download` events without `file_format` must not be relabelled as PDF downloads. The new parameter is not a new paid conversion, native GA4 report or registered custom dimension. A loading state prevents simultaneous exports; errors allow retry without losing the on-screen plan. Editing the checklist during generation cancels stale output.

### Reading The Funnel

Use the same complete dates, hostname and campaign cohort for visit metrics. Compare resource views and generation events as page-load actions, not unique-person conversion. Reloading can create another view and generation; browsers, consent, blockers and processing can limit observation. Do not sum overlapping users or divide cross-product events by unrelated exposures.

The existing eBook report filters `ebook_`; it does not include `cx_*`. Resource events can be read in GA4's standard Events report. To break them down by placement, use the existing event-scoped `placement` custom definition. This release does not create another native report, key event, collecting filter or paid campaign. Allow processing before interpreting missing rows.

Use external UTMs only on distribution links, for example `utm_source=linkedin&utm_medium=social&utm_campaign=cx-plan-nov26&utm_content=wk1-plan-pt`. Internal links do not reset campaign attribution with new UTMs. Do not copy incoming arbitrary query strings into external checkout links.

## Hotmart Origin

`hotmart_checkout()` preserves the product, existing checkout parameters and price configuration, and adds one controlled SCK placement code: `luizterra-site-catalog`, `luizterra-site-related`, `luizterra-site-article`, `luizterra-site-resource`, `luizterra-site-hero`, `luizterra-site-final` or `luizterra-site-mini-expert`.

The previous underscore codes were replaced because Hotmart reserves underscores and documents a 30-character limit. This is a compatibility correction, not proof that historical sales were lost. The new SCK identifies the site's checkout placement, not the original channel or person. It does not link the server-side GA4 purchase to a browser session, establish ROAS, or prove a paid purchase. Confirm payment and actual price in Hotmart, then reconcile the exact transaction in processed GA4 without a hostname filter on financial events.

Reference: [Hotmart sales-origin documentation](https://suportehotmart.zendesk.com/hc/pt-br/articles/216441797-Como-identificar-a-origem-das-minhas-vendas-na-Hotmart).

## Verification And Reversal

Run Python unit discovery, the existing commerce/financial JavaScript tests and `tools/test_growth.js`. The PDF regression test invokes the actual browser renderer for 108 combinations, reopens each PDF and checks text, accents, A4 pages, field names, canonical form values and widget appearances. A representative exported PDF must also be rendered and visually inspected. Run `tools/seo_audit.py` locally and after deployment. Check all three languages at 375, 768 and 1280 pixels, the six topic choices, partial/all/no selections, download output, no-JavaScript fallback and reduced motion. Browser QA must not send synthetic financial events.

Rebuild from canonical source; do not manually edit generated HTML. Verify GitHub Pages success separately from public HTTP 200, matching assets, sitemap discovery, indexing, visits and sales. None of those later outcomes is proved by a commit or an IndexNow receipt.

Rollback with a dedicated `git revert` of the growth release and another verified Pages build. Do not delete Analytics history, paid delivery files, buyer records, credentials or financial ledger entries.
