"""Validate the independently sold AI subscription after rebuilding the site."""

import json
import unittest
from xml.etree import ElementTree as ET

from mini_expert_content import MINI_EXPERT, MINI_EXPERT_COPY
from test_ebook import BASE, ROOT, Page


class MiniExpertTests(unittest.TestCase):
    def test_localized_pages_and_subscription_terms(self):
        for lang, prefix in (("en", ""), ("pt", "pt/"), ("es", "es/")):
            with self.subTest(lang=lang):
                route = prefix + MINI_EXPERT["path"]
                text = (ROOT / route / "index.html").read_text(encoding="utf-8")
                page = Page(text)
                self.assertIn(("link", {"rel": "canonical", "href": BASE + "/" + route}), page.tags)
                self.assertEqual(sum(t == "h1" for t, _ in page.tags), 1)
                self.assertNotIn("noindex", text)
                self.assertNotIn('id="ebook-introduction"', text)
                self.assertIn(MINI_EXPERT_COPY[lang]["terms"], text)
                self.assertIn(MINI_EXPERT_COPY[lang]["privacy"], text)
                self.assertIn(MINI_EXPERT_COPY[lang]["limits"], text)
                self.assertIn(MINI_EXPERT_COPY[lang]["language"], text)
                links = [a for t, a in page.tags if "data-mini-expert-checkout" in a]
                self.assertEqual(len(links), 1)
                self.assertTrue(links[0]["href"].startswith(MINI_EXPERT["checkout"] + "?sck="))
                self.assertEqual(links[0]["target"], "_blank")
                self.assertFalse(any("data-ebook-checkout" in a for _, a in page.tags))
                service = next(x for schema in page.schemas for x in schema["@graph"] if x.get("@type") == "Service")
                self.assertEqual(service["availableLanguage"], "pt-BR")
                offer = service["offers"]
                self.assertEqual(offer["price"], "199.90")
                self.assertEqual(offer["priceCurrency"], "BRL")
                self.assertEqual(offer["priceSpecification"]["billingDuration"], "P1M")
                self.assertEqual(offer["url"], MINI_EXPERT["checkout"])
                alternates = [a for t, a in page.tags if t == "link" and a.get("hreflang")]
                self.assertEqual({a["hreflang"] for a in alternates}, {"en", "pt-BR", "es", "x-default"})

    def test_discovery_and_independent_identity(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [e.text for e in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)]
        for prefix in ("", "pt/", "es/"):
            self.assertIn(BASE + "/" + prefix + MINI_EXPERT["path"], urls)
            for route in (prefix, prefix + "ebooks/"):
                text = (ROOT / route / "index.html").read_text(encoding="utf-8")
                page = Page(text)
                feature = [a for _, a in page.tags if "data-mini-expert-product" in a]
                self.assertEqual(len(feature), 1)
                self.assertEqual(feature[0]["data-hotmart-product-id"], "8822826")
                self.assertNotIn("data-ebook-id", feature[0])
                self.assertIn('href="/' + prefix + MINI_EXPERT["path"] + '"', text)
        self.assertTrue((ROOT / MINI_EXPERT["cover"].lstrip("/")).exists())
        receiver = json.loads((ROOT / "integrations/hotmart-ga4/products.json").read_text(encoding="utf-8"))
        self.assertEqual({x["hotmart_id"] for x in receiver}, {"8811187", "8811999", "8812046"})


if __name__ == "__main__":
    unittest.main()
