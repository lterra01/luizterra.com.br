"""Validate multilingual delivery claims, manual bonuses and private grants."""

import json
import re
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from commerce_content import BONUS_COPY, BONUS_PATH, FIVERR, FIVERR_COPY
from ebook_catalog import BOOK_TITLES, DELIVERY_LANGUAGES, EBOOKS
from test_ebook import BASE, ROOT, Page
from voucher_registry import confirm_delivery, connect, issue, private_root, redeem


class CommercePagesTests(unittest.TestCase):
    def test_localized_routes_and_schema(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = {el.text for el in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)}
        for lang, prefix in (("en", ""), ("pt", "pt/"), ("es", "es/")):
            for path in (FIVERR["path"], BONUS_PATH):
                text = (ROOT / prefix / path / "index.html").read_text(encoding="utf-8")
                page = Page(text)
                self.assertEqual(sum(tag == "h1" for tag, _ in page.tags), 1)
                self.assertIn(("link", {"rel": "canonical", "href": BASE + "/" + prefix + path}), page.tags)
                self.assertNotIn("noindex", text)
                self.assertNotIn('id="ebook-introduction"', text)
                self.assertIn(BASE + "/" + prefix + path, urls)
                self.assertEqual(len([a for t, a in page.tags if t == "link" and a.get("hreflang")]), 4)
            service_page = Page((ROOT / prefix / FIVERR["path"] / "index.html").read_text(encoding="utf-8"))
            service = next(x for schema in service_page.schemas for x in schema["@graph"] if x.get("@type") == "Service")
            self.assertEqual(service["availableLanguage"], "pt-BR")
            self.assertEqual(service["offers"]["price"], "50.00")
            self.assertEqual(service["offers"]["url"], FIVERR["url"])
            self.assertEqual(service["offers"]["priceCurrency"], "USD")
            bonus = (ROOT / prefix / BONUS_PATH / "index.html").read_text(encoding="utf-8")
            for key in ("terms", "privacy", "voucher_terms", "fiverr_note"):
                self.assertIn(BONUS_COPY[lang][key], bonus)
            choices = [a for t, a in Page(bonus).tags if t == "input"]
            self.assertEqual({a["value"] for a in choices}, {book["id"] for book in EBOOKS})
            self.assertTrue(all(a.get("type") == "checkbox" for a in choices))
            self.assertNotRegex(bonus, r"LTCX-[A-F0-9]{24}")

    def test_delivery_languages_and_skus_unchanged(self):
        self.assertEqual({book["hotmart_id"] for book in EBOOKS}, {"8811187", "8811999", "8812046"})
        for prefix in ("", "pt/", "es/"):
            page = Page((ROOT / prefix / "ebooks/index.html").read_text(encoding="utf-8"))
            books = next(x for schema in page.schemas for x in schema["@graph"] if x.get("@type") == "ItemList")
            for item in books["itemListElement"]:
                self.assertEqual(item["item"]["inLanguage"], DELIVERY_LANGUAGES)
                self.assertEqual(item["item"]["offers"]["price"], "9.99")
            text = (ROOT / prefix / "ebooks/index.html").read_text(encoding="utf-8")
            self.assertIn(FIVERR_COPY["pt" if prefix == "pt/" else "es" if prefix == "es/" else "en"]["heading"], text)
        public_pdfs = {p.name for p in (ROOT / "public").rglob("*.pdf")}
        self.assertFalse(any("v1.0" in name or "EN_" in name or "ES_" in name for name in public_pdfs))
        self.assertEqual(set(BOOK_TITLES), {book["id"] for book in EBOOKS})


class VoucherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.now = datetime(2026, 10, 29, 15, tzinfo=timezone.utc)
        self.titles = sorted(BOOK_TITLES)[:2]

    def tearDown(self):
        self.temp.cleanup()

    def create(self, source="courtesy", **kwargs):
        result = issue(self.root, "customer-001", source=source, now=self.now, **kwargs)
        invitation = Path(result["invitation"]).read_text(encoding="utf-8")
        code = re.search(r"LTCX-[A-F0-9]{24}", invitation).group()
        return result, code

    def test_individual_expiry_and_single_use(self):
        result, code = self.create()
        self.assertEqual(datetime.fromisoformat(result["expires_at"]), self.now + timedelta(days=30))
        redeemed = redeem(self.root, code, self.titles, "customer-001", now=self.now)
        self.assertEqual(redeemed["status"], "reserved_pending_manual_delivery")
        with self.assertRaises(ValueError):
            redeem(self.root, code, self.titles, "customer-001", now=self.now)
        delivered = confirm_delivery(self.root, result["grant_id"], "private-email", now=self.now)
        self.assertEqual(delivered["status"], "delivery_manually_confirmed")
        with self.assertRaises(ValueError):
            confirm_delivery(self.root, result["grant_id"], "private-email", now=self.now)

    def test_expired_and_wrong_recipient_rejected(self):
        _, code = self.create()
        with self.assertRaises(ValueError):
            redeem(self.root, code, self.titles, "customer-002", now=self.now)
        with self.assertRaises(ValueError):
            redeem(self.root, code, self.titles, "customer-001", now=self.now + timedelta(days=30))
        redeem(self.root, code, self.titles, "customer-001", now=self.now + timedelta(days=29))

    def test_exactly_two_catalogue_titles(self):
        _, code = self.create()
        for titles in ([], self.titles[:1], self.titles + ["unlisted"], [self.titles[0]] * 2, ["unlisted", self.titles[0]]):
            with self.assertRaises(ValueError):
                redeem(self.root, code, titles, "customer-001", now=self.now)

    def test_payment_check_and_no_repeat_bonus(self):
        with self.assertRaises(ValueError):
            self.create("mini-expert", order_ref="hotmart-001")
        self.create("mini-expert", order_ref="hotmart-001", approved=True)
        with self.assertRaises(ValueError):
            issue(self.root, "customer-001", source="fiverr", order_ref="fiverr-002", approved=True, now=self.now)
        with self.assertRaises(ValueError):
            issue(self.root, "customer-002", source="mini-expert", order_ref="hotmart-001", approved=True, now=self.now)

    def test_fiverr_delivery_stays_on_platform(self):
        result, code = self.create("fiverr", order_ref="fiverr-001", approved=True)
        redeem(self.root, code, self.titles, "customer-001", now=self.now)
        with self.assertRaises(ValueError):
            confirm_delivery(self.root, result["grant_id"], "private-email", now=self.now)
        confirm_delivery(self.root, result["grant_id"], "fiverr-order", now=self.now)

    def test_concurrent_redemption_reserves_only_once(self):
        _, code = self.create()

        def attempt(_):
            try:
                redeem(self.root, code, self.titles, "customer-001", now=self.now)
                return "reserved"
            except ValueError:
                return "rejected"

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(attempt, range(2)))
        self.assertCountEqual(outcomes, ["reserved", "rejected"])

    def test_private_storage_and_hashed_code(self):
        _, code = self.create()
        with connect(self.root) as db:
            row = dict(db.execute("SELECT * FROM grants").fetchone())
        self.assertNotIn(code, json.dumps(row))
        self.assertNotIn("customer-001", json.dumps(row))
        with self.assertRaises(ValueError):
            private_root(ROOT / "private")
        with self.assertRaises(ValueError):
            issue(self.root, "person@example.com", now=self.now)


if __name__ == "__main__":
    unittest.main()
