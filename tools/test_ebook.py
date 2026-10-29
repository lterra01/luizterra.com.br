"""Run after building: python -B -m unittest discover -s tools -p test_ebook.py."""

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from ebook_content import EBOOK, EBOOK_COPY
from ebook_catalog import EBOOKS, COLLECTION_PATH, COLLECTION_ID

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.luizterra.com.br"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.schemas = []
        self.buffer = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.buffer = ""

    def handle_data(self, data):
        if self.buffer is not None:
            self.buffer += data

    def handle_endtag(self, tag):
        if tag == "script" and self.buffer is not None:
            self.schemas.append(json.loads(self.buffer))
            self.buffer = None


class EbookTests(unittest.TestCase):
    def test_localized_sales_pages(self):
        for lang, prefix in (("en", ""), ("pt", "pt/"), ("es", "es/")):
            with self.subTest(lang=lang):
                route = prefix + EBOOK["path"]
                text = (ROOT / route / "index.html").read_text(encoding="utf-8")
                page = Page(text)
                self.assertIn(("link", {"rel": "canonical", "href": BASE + "/" + route}), page.tags)
                self.assertEqual(sum(tag == "h1" for tag, _ in page.tags), 1)
                body = next(attrs for tag, attrs in page.tags if tag == "body")
                self.assertEqual(body.get("data-ebook-id"), EBOOK["id"])
                self.assertEqual(body.get("data-ebook-title"), EBOOK["name"])
                self.assertNotIn('id="ebook-introduction"', text)
                self.assertNotIn("noindex", text)
                self.assertIn(EBOOK_COPY[lang]["buy"], text)
                checkout_links = [a for t, a in page.tags if t == "a" and "data-ebook-checkout" in a]
                self.assertEqual(len(checkout_links), 4)
                self.assertEqual(sum(a["href"] == EBOOK["checkout"] for a in checkout_links), 2)
                book = next(item for schema in page.schemas for item in schema["@graph"] if item.get("@type") == ["Book", "Product"])
                self.assertEqual(book["offers"]["price"], "9.99")
                self.assertEqual(book["offers"]["priceCurrency"], "BRL")
                self.assertEqual(book["offers"]["url"], EBOOK["checkout"])
                self.assertEqual(book["inLanguage"], ["pt-BR", "en", "es"])
                self.assertEqual(book["numberOfPages"], 27)
                self.assertEqual(len(EBOOK_COPY[lang]["routines"]), 7)
                self.assertEqual(len(EBOOK_COPY[lang]["materials"]), 4)

    def test_sitewide_promotion_and_links(self):
        for path in ROOT.rglob("*.html"):
            if "node_modules" in path.parts or ".wrangler" in path.parts:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                page = Page(text)
                is_sales_page = any(tag == "body" and any(name in attrs.get("class", "").split() for name in ("ebook-landing", "ebook-catalog", "mini-expert-landing")) for tag, attrs in page.tags)
                if not is_sales_page:
                    self.assertEqual(text.count('id="ebook-introduction"'), 1)
                    self.assertIn('class="ebook-announcement"', text)
                    modal = next(attrs for tag, attrs in page.tags if attrs.get("id") == "ebook-introduction")
                    self.assertEqual(modal.get("data-ebook-collection-id"), COLLECTION_ID)
                    self.assertEqual(modal.get("data-ebook-ad-id"), "cx_na_pratica_collection_v1")
                for tag, attrs in page.tags:
                    if tag not in ("a", "img", "script", "link"):
                        continue
                    value = attrs.get("href") or attrs.get("src") or ""
                    parsed = urlsplit(value)
                    if parsed.scheme and parsed.scheme not in ("http", "https"):
                        continue
                    if parsed.netloc and parsed.netloc != "www.luizterra.com.br":
                        continue
                    if not parsed.path:
                        continue
                    target = ROOT / unquote(parsed.path.lstrip("/")) if parsed.path.startswith("/") else path.parent / unquote(parsed.path)
                    self.assertTrue(target.exists() or (target / "index.html").exists(), value)
                self.assertNotIn("CX_na_Operacao_Luiz_Terra_v1.0.pdf", text)
                for tag, attrs in page.tags:
                    if tag == "meta" and attrs.get("name") == "author":
                        self.assertEqual(attrs.get("content"), "Luiz Terra")

    def test_sitemap_and_public_assets(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [e.text for e in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)]
        self.assertEqual(len(urls), len(set(urls)))
        for prefix in ("", "pt/", "es/"):
            self.assertIn(BASE + "/" + prefix + EBOOK["path"], urls)
            self.assertIn(BASE + "/" + prefix + COLLECTION_PATH, urls)
        self.assertTrue((ROOT / EBOOK["cover"].lstrip("/")).exists())
        self.assertFalse(any((ROOT / "public").rglob("CX_na_Operacao*.pdf")))

    def test_collection_products_and_tracking(self):
        self.assertEqual(len({book["id"] for book in EBOOKS}), 3)
        for prefix in ("", "pt/", "es/"):
            route = prefix + COLLECTION_PATH
            page = Page((ROOT / route / "index.html").read_text(encoding="utf-8"))
            self.assertIn(("link", {"rel": "canonical", "href": BASE + "/" + route}), page.tags)
            products = [attrs for tag, attrs in page.tags if tag == "article" and "data-ebook-product" in attrs]
            self.assertEqual({attrs["data-ebook-id"] for attrs in products}, {book["id"] for book in EBOOKS})
            offers = [attrs["href"] for tag, attrs in page.tags if "data-ebook-checkout" in attrs]
            self.assertEqual({urlsplit(url)._replace(query="").geturl() for url in offers}, {book["checkout"] for book in EBOOKS})
            listing = next(item for schema in page.schemas for item in schema["@graph"] if item.get("@type") == "ItemList")
            self.assertEqual(listing["numberOfItems"], 3)
            self.assertEqual({item["item"]["numberOfPages"] for item in listing["itemListElement"]}, {25, 27})
        for book in EBOOKS:
            self.assertTrue((ROOT / book["cover"].lstrip("/")).exists())
        self.assertFalse(any((ROOT / "public" / "ebooks").glob("*.pdf")))


if __name__ == "__main__":
    unittest.main()
