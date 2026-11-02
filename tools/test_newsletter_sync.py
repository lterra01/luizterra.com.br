"""Publication-gated newsletter updates must preserve canonical page identity."""

import unittest

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


if __name__ == "__main__":
    unittest.main()
