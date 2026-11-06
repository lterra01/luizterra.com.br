"""Publication-gated newsletter updates must preserve canonical page identity."""

import unittest
import xml.etree.ElementTree as ET

import build_static_site as site
from test_ebook import Page


SLUG = "global-cx-local-operating-intelligence"
SOURCE = "https://www.linkedin.com/pulse/global-cx-must-locally-intelligent-luiz-terra-npkye/"


class NewsletterSyncTests(unittest.TestCase):
    def setUp(self):
        self.article = next(item for item in site.ARTICLES if item["slug"] == SLUG)

    def test_existing_canonical_article_is_expanded_not_duplicated_or_redated(self):
        self.assertEqual(sum(item["slug"] == SLUG for item in site.ARTICLES), 1)
        self.assertEqual(sum(item.get("source_url") == SOURCE for item in site.ARTICLES), 1)
        self.assertEqual(self.article["published"], "2026-08-19")
        self.assertEqual(self.article["modified"], "2026-11-02")
        self.assertFalse(any(item["slug"] == "global-cx-must-be-locally-intelligent" for item in site.ARTICLES))

    def test_full_editorial_versions_and_source_are_available_in_each_language(self):
        for lang in ("en", "pt", "es"):
            with self.subTest(language=lang):
                sections = self.article["sections"][lang]
                self.assertEqual(len(sections), 5)
                self.assertGreaterEqual(sum(len(paragraphs) for _, paragraphs in sections), 12)
                self.assertGreater(len(" ".join(text for _, paragraphs in sections for text in paragraphs).split()), 400)
                markup = site.render_article(lang, self.article)
                self.assertIn(SOURCE, markup)
                self.assertIn("30", self.article["lead"][lang])
                self.assertIn("2026", self.article["lead"][lang])

    def test_schema_canonical_and_dates_match_the_stable_article(self):
        for lang in ("en", "pt", "es"):
            with self.subTest(language=lang):
                page = Page(site.render_article(lang, self.article))
                canonical = next(attrs["href"] for tag, attrs in page.tags if tag == "link" and attrs.get("rel") == "canonical")
                self.assertEqual(canonical, site.BASE_URL + site.lang_url(lang, f"insights/{SLUG}/"))
                post = next(node for node in page.schemas[0]["@graph"] if node.get("@type") == "BlogPosting")
                self.assertEqual(post["isBasedOn"], SOURCE)
                self.assertEqual(post["datePublished"], "2026-08-19")
                self.assertEqual(post["dateModified"], "2026-11-02")
                self.assertFalse(any(tag == "meta" and attrs.get("name") == "robots" and "noindex" in attrs.get("content", "") for tag, attrs in page.tags))


class ContextNewsletterSyncTests(unittest.TestCase):
    slug = "context-contact-center-infrastructure"
    source = "https://www.linkedin.com/pulse/context-new-contact-center-infrastructure-luiz-terra-kbbze/"

    def setUp(self):
        self.article = next(item for item in site.ARTICLES if item["slug"] == self.slug)

    def test_confirmed_edition_is_unique_and_correctly_dated(self):
        self.assertEqual(sum(item["slug"] == self.slug for item in site.ARTICLES), 1)
        self.assertEqual(sum(item.get("source_url") == self.source for item in site.ARTICLES), 1)
        self.assertEqual(self.article["published"], "2026-11-06")
        self.assertEqual(self.article["modified"], "2026-11-06")

    def test_complete_editorial_versions_preserve_continuity_and_governance(self):
        for lang in ("en", "pt", "es"):
            with self.subTest(language=lang):
                sections = self.article["sections"][lang]
                self.assertEqual(len(sections), 5)
                self.assertGreaterEqual(sum(len(paragraphs) for _, paragraphs in sections), 18)
                self.assertGreater(len(" ".join(text for _, paragraphs in sections for text in paragraphs).split()), 500)
                self.assertEqual(len(sections[1][1]), 6)
                self.assertEqual(len(sections[3][1]), 5)
                self.assertIn("2026", self.article["lead"][lang])
                self.assertIn(self.source, site.render_article(lang, self.article))

    def test_canonical_schema_languages_and_robots_agree(self):
        for lang in ("en", "pt", "es"):
            with self.subTest(language=lang):
                page = Page(site.render_article(lang, self.article))
                links = [attrs for tag, attrs in page.tags if tag == "link"]
                canonical = next(attrs["href"] for attrs in links if attrs.get("rel") == "canonical")
                self.assertEqual(canonical, site.BASE_URL + site.lang_url(lang, f"insights/{self.slug}/"))
                alternates = {attrs["hreflang"]: attrs["href"] for attrs in links if attrs.get("rel") == "alternate" and "hreflang" in attrs}
                self.assertEqual(set(alternates), {"en", "pt-BR", "es", "x-default"})
                post = next(node for node in page.schemas[0]["@graph"] if node.get("@type") == "BlogPosting")
                self.assertEqual(post["isBasedOn"], self.source)
                self.assertEqual(post["datePublished"], "2026-11-06")
                self.assertEqual(post["dateModified"], "2026-11-06")
                self.assertEqual(post["headline"], self.article["title"][lang])
                self.assertFalse(any(tag == "meta" and attrs.get("name") == "robots" and "noindex" in attrs.get("content", "") for tag, attrs in page.tags))

    def test_edition_is_linked_from_its_localized_topic_and_hub(self):
        topic = site.TOPIC_BY_SLUG["ai-contact-centers"]
        self.assertEqual(topic["articles"].count(self.slug), 1)
        for lang in ("en", "pt", "es"):
            self.assertIn(site.article_path(lang, self.article), site.render_insights_index(lang))
            self.assertIn(site.article_path(lang, self.article), site.render_topic(lang, topic))

    def test_generated_sitemap_contains_each_localized_canonical_once(self):
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        root = ET.parse(site.ROOT / "sitemap.xml").getroot()
        for lang in ("en", "pt", "es"):
            url = site.BASE_URL + site.lang_url(lang, f"insights/{self.slug}/")
            matches = [entry for entry in root.findall("sm:url", ns) if entry.findtext("sm:loc", namespaces=ns) == url]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0].findtext("sm:lastmod", namespaces=ns), "2026-11-06")


if __name__ == "__main__":
    unittest.main()
