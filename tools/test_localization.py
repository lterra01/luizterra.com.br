"""Regression checks for reviewed multilingual copy and generated pages."""

import unittest
from urllib.parse import parse_qs, urlsplit

import build_static_site as site
from localization_audit import PageText, audit, text_findings
from test_ebook import Page


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from strings(item)


class LocalizationTests(unittest.TestCase):
    def test_all_generated_pages(self):
        report, _ = audit()
        expected = len(site.ARTICLES) + len(site.TOPICS) + 9
        self.assertEqual(report["pages"], {"en": expected + 1, "pt": expected, "es": expected})
        self.assertEqual(report["findings"], [], report["findings"][:12])

    def test_localized_source_copy_including_dynamic_pdf_text(self):
        for lang in ("en", "pt", "es"):
            payloads = [source[lang] for source in (
                site.META, site.COPY, site.IMPACTS, site.UI, site.CAREER,
                site.EBOOK_COPY, site.COLLECTION_COPY, site.MINI_EXPERT_COPY,
                site.FIVERR_COPY, site.BONUS_COPY, site.GROWTH_COPY, site.PDF_COPY,
            )]
            for article in site.ARTICLES:
                payloads.extend(article[key][lang] for key in ("title", "summary", "body", "sections", "seo_title", "lead") if isinstance(article.get(key), dict) and lang in article[key])
                payloads.append(site.ARTICLE_ENHANCEMENTS[article["slug"]][lang])
            for track in site.TRACKS:
                payloads.extend((track["label"][lang], track["checks"][lang]))
            for payload in payloads:
                for text in strings(payload):
                    with self.subTest(lang=lang, text=text[:90]):
                        self.assertEqual(list(text_findings(text, lang)), [])

    def test_language_keys_and_professional_facts_preserved(self):
        self.assertEqual(set(site.COPY["en"]), set(site.COPY["pt"]))
        self.assertEqual(set(site.COPY["en"]), set(site.COPY["es"]))
        self.assertEqual(set(site.UI["en"]), set(site.UI["pt"]))
        self.assertEqual(set(site.UI["en"]), set(site.UI["es"]))
        for lang in ("en", "pt", "es"):
            self.assertEqual([row[1] for row in site.CAREER[lang]], [row[1] for row in site.CAREER["en"]])
            self.assertEqual(len(site.COPY[lang]["focus"]), 3)
            self.assertEqual(len(site.COPY[lang]["presence"]), 4)
            self.assertIn("28", site.COPY[lang]["support"])
            self.assertEqual(len(site.COPY[lang]["ticker"]), 12)

    def test_topic_themes_and_questions_use_the_page_language(self):
        for topic in site.TOPICS:
            self.assertEqual(set(topic["themes"]), {"en", "pt", "es"})
            for lang in ("en", "pt", "es"):
                self.assertEqual(len(topic["themes"][lang]), 6)
                page = site.render_topic(lang, topic)
                for theme in topic["themes"][lang]:
                    self.assertIn(site.esc(site.UI[lang]["question_template"].format(theme=theme)), page)

    def test_article_tags_are_localized_in_markup_and_schema(self):
        for article in site.ARTICLES:
            for tag in article["tags"]:
                self.assertIn(tag.casefold(), site.ARTICLE_TAG_LABELS)
            for lang in ("pt", "es"):
                tags = site.article_tags(lang, article)
                markup = site.render_article(lang, article)
                schema = Page(markup).schemas[0]
                post = next(node for node in schema["@graph"] if node.get("@type") == "BlogPosting")
                self.assertEqual(post["keywords"], tags)
                for tag in tags:
                    self.assertIn(f"<span>{site.esc(tag)}</span>", markup)

    def test_localized_accessibility_navigation_and_contact_subjects(self):
        for lang in ("en", "pt", "es"):
            markup = site.render_home(lang)
            page = Page(markup)
            nav = next(attrs for tag, attrs in page.tags if tag == "nav" and attrs.get("class") == "site-nav")
            self.assertEqual(nav["aria-label"], site.UI[lang]["nav_label"])
            self.assertIn(site.UI[lang]["rights"], markup)
            self.assertIn(site.UI[lang]["schedule"], markup)
            subjects = [parse_qs(urlsplit(a["href"]).query)["subject"][0] for tag, a in page.tags if tag == "a" and a.get("href", "").startswith("mailto:") and "subject=" in a["href"]]
            self.assertTrue(subjects)
            self.assertEqual(set(subjects), {site.UI[lang]["contact_subject"]})

    def test_offer_languages_are_not_changed_by_translation(self):
        for lang in ("en", "pt", "es"):
            page = site.render_mini_expert(lang)
            self.assertIn(site.MINI_EXPERT_COPY[lang]["language"], page)
            self.assertIn(site.esc(site.MINI_EXPERT_COPY[lang]["heading"]), page)
            self.assertEqual(site.EBOOK_COPY[lang]["modal_title"], site.BOOK_TITLES[site.EBOOK["id"]][lang])
        self.assertNotIn("PORTUGUESE EBOOK", site.EBOOK_COPY["en"]["bar_label"])
        self.assertIn("inglês", site.UI["pt"]["download_bio"])
        self.assertIn("inglés", site.UI["es"]["download_bio"])

    def test_contextual_terms_do_not_confuse_operations_with_an_os(self):
        for lang in ("en", "pt", "es"):
            for article in site.ARTICLES:
                rendered = site.render_article(lang, article)
                for phrase in ("as one operating system", "único sistema operacional", "único sistema operativo", "sistema operacional de telecomunicações", "sistema operativo de telecomunicaciones"):
                    self.assertNotIn(phrase, rendered)

    def test_spanish_customer_journey_agreement(self):
        for article in site.ARTICLES:
            rendered = site.render_article("es", article)
            for phrase in ("las recorridos", "a el recorrido", "recorrido completo más sencilla"):
                self.assertNotRegex(rendered, r"\b" + phrase + r"\b")

    def test_audit_covers_metadata_accessibility_dynamic_actions_and_pdf(self):
        page = PageText()
        page.feed('<html lang="es"><head><meta name="description" content="tecnologia" /></head><body><img alt="anos" /><script type="application/json">{"tracks":{"voice":[["Atención","revision","Acción"]]},"pdf_copy":{"pdf_notes":"proximo"}}</script></body></html>')
        findings = [finding for text in page.texts for finding in text_findings(text, "es")]
        self.assertEqual({term for kind, term in findings if kind == "missing_accent"}, {"tecnologia", "anos", "revision", "proximo"})
        self.assertEqual(list(text_findings("https://example.com/operacao/", "pt")), [])

    def test_valid_accents_and_contextual_verbs_are_not_rewritten(self):
        self.assertEqual(list(text_findings("Não há dúvida: a experiência apoia decisões e ações práticas.", "pt")), [])
        self.assertEqual(list(text_findings("La propuesta explicita las funciones y los límites para los próximos años.", "es")), [])
        self.assertEqual(list(text_findings("São Paulo and Bogotá: international customer service.", "en")), [])
        self.assertIn(("encoding", "Ã§"), list(text_findings("AÃ§Ã£o", "pt")))


if __name__ == "__main__":
    unittest.main()
