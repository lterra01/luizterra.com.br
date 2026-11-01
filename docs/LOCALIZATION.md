# Language Review And Regression Checks

## Canonical Sources

Edit the source modules in `tools/`, not the generated HTML:

- `build_static_site.py`: homepage, career, shared layout and metadata.
- `content_hub.py`: biography, topic hubs, article tags and shared UI labels.
- `article_library.py`: the 18 articles and their complete EN/PT/ES editions.
- `ebook_content.py` and `ebook_catalog.py`: eBook offers and collection copy.
- `mini_expert_content.py` and `commerce_content.py`: service and bonus copy.
- `growth_content.py`: the free checklist, actions and generated PDF text.

Use UTF-8 and preserve Portuguese and Spanish accents, including capital letters.
Do not apply accent removal to prose. URLs, slugs, analytics IDs and product IDs
are stable technical identifiers and must not be translated.

## Editorial Rules

- Preserve the short public name Luiz Terra, 28+ years of experience, existing
  career facts, prices, payment terms, refund language and delivery scope.
- Translate navigation, accessibility labels, metadata, topic themes, article
  tags and dynamic PDF text as well as visible paragraphs.
- Keep formal company names and necessary industry acronyms. Explain unfamiliar
  concepts in the page language instead of copying English paragraphs.
- Do not confuse an operating model with a computer operating system, a metric's
  calculation method with a comparison baseline, or service outcomes with ROI.
- The Mini Expert and Fiverr report remain Portuguese-language services. The
  executive biography download is an English PDF and its labels state this on
  Portuguese and Spanish pages. Website translation does not expand the offer.
- Automated findings require editorial judgment. A valid verb can resemble an
  unaccented noun; do not perform automatic dictionary-wide replacements.

## Repeatable Checks

```powershell
python -X utf8 -B tools/build_static_site.py
python -X utf8 -B tools/localization_audit.py --report <private-output>/languages.json
python -X utf8 -B -m unittest discover -s tools -p 'test_*.py'
node --test tools/test_ebook_promotion.js tools/test_mini_expert.js tools/test_commerce.js tools/test_growth.js
python -X utf8 -B tools/seo_audit.py --output <private-output>/seo-local.json
python -X utf8 -B tools/seo_audit.py --live --output <private-output>/seo-live.json
```

The build and PDF tests require the existing Pillow/ReportLab dependencies and
Node.js. The language auditor itself uses only the Python standard library.
Use `--export-text <private-output>/texts` to collect unique prose for review.

The auditor reads generated HTML, metadata, accessibility attributes, JSON-LD
and embedded checklist/PDF copy. It detects known missing accents, untranslated
shared phrases, encoding damage and non-NFC text. It is a regression guard, not
a complete grammar checker or a substitute for reviewing meaning in context.

## Review On 2026-11-01

- Reviewed all 100 generated HTML files, representing 99 canonical URLs plus the
  English `/en/` alias. The alias continues to canonicalize to `/`.
- Corrected accents, agreement, unnatural translations, untranslated shared
  blocks, technical terminology and mismatched descriptions across EN/PT/ES.
- Reviewed the 18 articles in all three languages, plus commercial, biography,
  topic, navigation, accessibility and free-resource text.
- Python: 50 passing tests, including 108 generated-PDF scenarios.
- JavaScript: 31 passing tests. No financial events were sent by these tests.
- Local SEO audit: 99 canonical URLs, no errors or warnings.
- Browser QA: 11 templates, three languages and widths of 375, 768 and 1280 px;
  all 99 checks passed without horizontal overflow or clipped text.
- Visually inspected the updated public biography and the three-page action
  plan in each language. Accents rendered correctly and fields stayed in bounds.

Private evidence, screenshots and detailed audit output stay outside this public
repository. A successful build or local review is not proof of live deployment;
verify GitHub Pages and public responses separately after pushing.
