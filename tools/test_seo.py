"""Regression gates for the multilingual SEO and promotional image release."""

import json
import unittest

from PIL import Image

import build_static_site as build
from ebook_catalog import BOOK_TITLES, EBOOKS
from seo_audit import BASE, ROOT, Document, audit, audit_document, schema_nodes, types


class SeoTests(unittest.TestCase):
    def test_canonical_inventory(self):
        result = audit()
        self.assertEqual(result["summary"]["global_errors"], [])
        self.assertEqual(result["summary"]["pages_with_errors"], 0)
        self.assertTrue(result["summary"]["googlebot_allowed"])
        self.assertGreaterEqual(result["summary"]["canonical_urls"], 96)

    def test_collection_describes_books_not_a_single_product(self):
        for lang in ("en", "pt", "es"):
            nodes = list(schema_nodes(json.loads(build.schema_json(lang, "ebooks/", "ebook_catalog", None))))
            self.assertFalse(any("Product" in types(node) for node in nodes))
            books = [node for node in nodes if "Book" in types(node)]
            self.assertEqual(len(books), len(EBOOKS))
            for book, node in zip(EBOOKS, books):
                self.assertEqual(node["description"], book["summary"][lang])
                self.assertEqual(node["name"], BOOK_TITLES[book["id"]][lang])
                self.assertEqual(node["identifier"]["value"], book["hotmart_id"])
                self.assertEqual(node["offers"]["priceCurrency"], "BRL")
                self.assertEqual(node["offers"]["price"], book["price"])

    def test_single_product_has_real_identity_without_fabricated_reviews(self):
        for lang in ("en", "pt", "es"):
            nodes = list(schema_nodes(json.loads(build.schema_json(lang, EBOOKS[0]["path"], "ebook", None))))
            products = [node for node in nodes if "Product" in types(node)]
            self.assertEqual(len(products), 1)
            product = products[0]
            self.assertEqual(product["brand"]["name"], "Luiz Terra")
            self.assertEqual(product["sku"], "8811187")
            self.assertTrue(product["description"])
            self.assertNotIn("aggregateRating", product)
            self.assertNotIn("review", product)
            self.assertNotIn("gtin", product)
            self.assertNotIn("isbn", product)

    def test_commerce_breadcrumbs(self):
        for kind, path in (("ebook_catalog", "ebooks/"), ("ebook", EBOOKS[0]["path"]), ("mini_expert", build.MINI_EXPERT["path"]), ("consulting", build.FIVERR["path"]), ("bonus", build.BONUS_PATH)):
            for lang in ("en", "pt", "es"):
                nodes = list(schema_nodes(json.loads(build.schema_json(lang, path, kind, None))))
                trail = next(node for node in nodes if "BreadcrumbList" in types(node))
                self.assertEqual(trail["itemListElement"][-1]["item"], build.canonical(lang, path))

    def test_responsive_covers_preserve_originals_and_reduce_transfer(self):
        for book in EBOOKS:
            source = ROOT / book["cover"].lstrip("/")
            with Image.open(source) as image:
                self.assertEqual(image.size, (1254, 1254))
            for width in (320, 640, 960):
                variant = source.with_name(f"{source.stem}-{width}.webp")
                with Image.open(variant) as image:
                    self.assertEqual(image.size, (width, width))
                self.assertLess(variant.stat().st_size, source.stat().st_size)
            self.assertLess(source.with_name(f"{source.stem}-320.webp").stat().st_size, source.stat().st_size / 3)

    def test_all_promotional_covers_have_responsive_candidates(self):
        for route in ("pt/", "pt/ebooks/", "pt/bonus/", "pt/" + EBOOKS[0]["path"]):
            page = Document((ROOT / route / "index.html").read_text(encoding="utf-8"))
            covers = [attrs for tag, attrs in page.tags if tag == "img" and attrs.get("src", "").startswith("/public/ebooks/")]
            self.assertTrue(covers)
            for cover in covers:
                self.assertIn("320w", cover["srcset"])
                self.assertIn("1254w", cover["srcset"])
                self.assertTrue(cover["sizes"])

    def test_auditor_rejects_noindex_and_bad_canonical(self):
        text = build.render_ebook_catalog("pt").replace('content="index,follow,', 'content="noindex,follow,')
        result, _ = audit_document(BASE + "/wrong/", text)
        self.assertIn("noindex_in_sitemap", result["errors"])
        self.assertIn("canonical_mismatch", result["errors"])

    def test_auditor_rejects_broken_json_ld(self):
        text = build.render_ebook_catalog("pt").replace('"@context": "https://schema.org"', '"@context": invalid-json', 1)
        result, _ = audit_document(BASE + "/pt/ebooks/", text)
        self.assertIn("invalid_json_ld", result["errors"])


if __name__ == "__main__":
    unittest.main()
