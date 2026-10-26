"""Run after building: python -B -m unittest discover -s tools -p test_ebook.py."""

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from ebook_content import EBOOK, EBOOK_COPY

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
                self.assertNotIn('id="ebook-introduction"', text)
                self.assertNotIn("noindex", text)
                self.assertIn(EBOOK_COPY[lang]["buy"], text)
                self.assertEqual(len([a for t, a in page.tags if t == "a" and "data-ebook-checkout" in a]), 2)
                book = next(item for schema in page.schemas for item in schema["@graph"] if item.get("@type") == ["Book", "Product"])
                self.assertEqual(book["offers"]["price"], "9.99")
                self.assertEqual(book["offers"]["priceCurrency"], "BRL")
                self.assertEqual(book["offers"]["url"], EBOOK["checkout"])
                self.assertEqual(book["inLanguage"], "pt-BR")
                self.assertEqual(book["numberOfPages"], 27)
                self.assertEqual(len(EBOOK_COPY[lang]["routines"]), 7)
                self.assertEqual(len(EBOOK_COPY[lang]["materials"]), 4)

    def test_sitewide_promotion_and_links(self):
        for path in ROOT.rglob("*.html"):
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                page = Page(text)
                if EBOOK["path"] not in path.as_posix():
                    self.assertEqual(text.count('id="ebook-introduction"'), 1)
                    self.assertIn('class="ebook-announcement"', text)
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
                self.assertNotIn("LUIZ FERNANDO COELHO TERRA", text)

    def test_sitemap_and_public_assets(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [e.text for e in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)]
        self.assertEqual(len(urls), len(set(urls)))
        for prefix in ("", "pt/", "es/"):
            self.assertIn(BASE + "/" + prefix + EBOOK["path"], urls)
        self.assertTrue((ROOT / EBOOK["cover"].lstrip("/")).exists())
        self.assertFalse(any((ROOT / "public").rglob("CX_na_Operacao*.pdf")))


if __name__ == "__main__":
    unittest.main()
