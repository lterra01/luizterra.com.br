"""Public growth funnel gates; no customer data or remote financial events."""

import json
import unittest
from urllib.parse import parse_qs, urlsplit

import build_static_site as build
from ebook_catalog import EBOOKS
from growth_content import GROWTH_COPY, GROWTH_PATH, TRACKS, article_track
from seo_audit import Document, schema_nodes, types


class GrowthTests(unittest.TestCase):
    def test_six_original_checklists_and_real_released_products(self):
        self.assertEqual(len(TRACKS), 6)
        self.assertEqual({track["book"] for track in TRACKS}, {book["id"] for book in EBOOKS})
        slugs = {article["slug"] for article in build.ARTICLES}
        for track in TRACKS:
            self.assertEqual(len(track["articles"]), 2)
            self.assertTrue(set(track["articles"]).issubset(slugs))
            for lang in ("en", "pt", "es"):
                self.assertEqual(len(track["checks"][lang]), 5)
                self.assertTrue(all(len(check) == 3 and all(check) for check in track["checks"][lang]))

    def test_resource_metadata_and_schema(self):
        for lang in ("en", "pt", "es"):
            text = build.render_resource(lang)
            doc = Document(text)
            self.assertEqual(text.count("<h1>"), 1)
            self.assertNotIn("ebook-introduction", text)
            self.assertNotIn('type="email"', text)
            self.assertNotIn('type="file"', text)
            self.assertEqual(text.count('data-cx-track="'), 6)
            self.assertEqual(text.count('name="ready"'), 30)
            canonical = next(attrs["href"] for tag, attrs in doc.tags if tag == "link" and attrs.get("rel") == "canonical")
            self.assertEqual(canonical, build.canonical(lang, GROWTH_PATH))
            nodes = list(schema_nodes(json.loads(build.schema_json(lang, GROWTH_PATH, "cx_resource", None))))
            page = next(node for node in nodes if "WebPage" in types(node))
            self.assertTrue(page["isAccessibleForFree"])
            self.assertFalse(any("Product" in types(node) for node in nodes))
            self.assertTrue(any("BreadcrumbList" in types(node) for node in nodes))
            self.assertIn(GROWTH_COPY[lang]["privacy"], text)
            self.assertIn(GROWTH_COPY[lang]["download"], text)
            self.assertNotIn("CSV", text)
            self.assertIn(build.GROWTH_PDF_URL, text)
            self.assertTrue((build.ROOT / "public/vendor/pdf-lib-1.17.1/pdf-lib.min.js").exists())
            self.assertTrue((build.ROOT / "public/vendor/pdf-lib-1.17.1/LICENSE.md").exists())

    def test_article_recommendations_match_the_subject_and_product_identity(self):
        for article in build.ARTICLES:
            track = article_track(article)
            book = next(book for book in EBOOKS if book["id"] == track["book"])
            for lang in ("en", "pt", "es"):
                offer = build.contextual_offer(lang, article)
                self.assertIn(f'?topic={track["id"]}', offer)
                self.assertIn(f'data-ebook-id="{book["id"]}"', offer)
                self.assertIn(f'data-hotmart-product-id="{book["hotmart_id"]}"', offer)
                self.assertIn('data-ebook-checkout="article"', offer)
                self.assertIn('data-product-placement="article"', offer)

    def test_hotmart_campaign_codes_are_valid_and_do_not_change_checkout_identity(self):
        for placement in ("catalog", "related", "article", "resource", "hero", "final", "mini-expert"):
            for book in EBOOKS:
                original = urlsplit(book["checkout"])
                tagged = urlsplit(build.hotmart_checkout(book["checkout"], placement))
                self.assertEqual((tagged.scheme, tagged.netloc, tagged.path), (original.scheme, original.netloc, original.path))
                code = parse_qs(tagged.query)["sck"][0]
                self.assertLessEqual(len(code), 30)
                self.assertNotIn("_", code)
                self.assertRegex(code, r"^[a-z0-9-]+$")
        tagged = build.hotmart_checkout("https://pay.hotmart.com/example?checkoutMode=10&sck=old", "hero")
        self.assertEqual(parse_qs(urlsplit(tagged).query), {"checkoutMode": ["10"], "sck": ["luizterra-site-hero"]})
        with self.assertRaises(ValueError):
            build.hotmart_checkout(EBOOKS[0]["checkout"], "bad&code")

    def test_every_public_checkout_uses_a_supported_origin_code(self):
        for lang in ("en", "pt", "es"):
            for text in (build.render_ebook_catalog(lang), build.render_ebook(lang), build.render_mini_expert(lang), build.render_resource(lang)):
                for tag, attrs in Document(text).tags:
                    href = attrs.get("href", "")
                    if tag == "a" and href.startswith("https://pay.hotmart.com/"):
                        code = parse_qs(urlsplit(href).query)["sck"][0]
                        self.assertRegex(code, r"^[a-z0-9-]{1,30}$")

    def test_prices_bonus_and_service_language_remain_explicit(self):
        for lang in ("en", "pt", "es"):
            text = build.render_resource(lang)
            self.assertEqual(text.count('data-ebook-checkout="resource"'), 6)
            self.assertIn("R$ 199,90", text)
            self.assertIn("US$ 50", text)
            self.assertIn(GROWTH_COPY[lang]["service_note"], text)
            self.assertIn(GROWTH_COPY[lang]["bonus"], text)
        self.assertTrue(all(book["price"] == "9.99" for book in EBOOKS))


if __name__ == "__main__":
    unittest.main()
