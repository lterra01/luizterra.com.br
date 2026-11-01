"""Exercise the same PDF renderer used by visitors, without external requests."""

import base64
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

from pypdf import PdfReader

from ebook_catalog import BOOK_TITLES
from growth_content import GROWTH_COPY, PDF_COPY, TRACKS

ROOT = Path(__file__).resolve().parents[1]


def pdf_case(lang="pt", track=None, ready=0, identifier=None):
    track = track or TRACKS[1]
    copy = {**GROWTH_COPY[lang], **PDF_COPY[lang]}
    checks = track["checks"][lang]
    pending = checks[ready:]
    return {
        "id": identifier or f"{lang}-{track['id']}-{ready}",
        "data": {
            "language": {"pt": "pt-BR", "en": "en", "es": "es"}[lang],
            "topic": track["label"][lang], "copy": copy,
            "plan": {"maintenance": not pending, "actions": (pending or checks)[:3]},
            "dateLabel": {"pt": "01 de novembro de 2026", "en": "November 01, 2026", "es": "01 de noviembre de 2026"}[lang],
            "relatedTitle": BOOK_TITLES[track["book"]][lang],
            "relatedUrl": "https://www.luizterra.com.br/" + {"pt": "pt/", "en": "", "es": "es/"}[lang] + "ebooks/#" + track["book"],
        },
    }


class GrowthPdfTests(unittest.TestCase):
    def test_all_languages_topics_and_selection_counts(self):
        node = os.environ.get("NODE_BINARY") or shutil.which("node")
        if not node:
            self.skipTest("Node.js is required to verify the browser PDF renderer")
        cases = [pdf_case(lang, track, ready) for lang in ("pt", "en", "es") for track in TRACKS for ready in range(6)]
        process = subprocess.run([node, str(ROOT / "tools" / "render_growth_pdf.js")],
                                 input=json.dumps({"cases": cases, "includeBytes": True}),
                                 text=True, encoding="utf-8", capture_output=True, timeout=100)
        self.assertEqual(process.returncode, 0, process.stderr)
        results = json.loads(process.stdout)
        self.assertEqual(len(results), 108)
        for case, result in zip(cases, results):
            with self.subTest(case=case["id"]):
                reader = PdfReader(io.BytesIO(base64.b64decode(result["pdf"])))
                self.assertEqual(len(reader.pages), 3)
                self.assertEqual(reader.metadata.author, "Luiz Terra")
                self.assertEqual(reader.trailer["/Root"]["/Lang"], case["data"]["language"])
                text = "\n".join(page.extract_text() for page in reader.pages)
                self.assertIn(case["data"]["topic"], text)
                self.assertIn(case["data"]["relatedTitle"], text)
                for action in case["data"]["plan"]["actions"]:
                    self.assertIn(action[1], " ".join(text.split()))
                    self.assertIn(action[2], " ".join(text.split()))
                self.assertNotIn("\ufffd", text)
                fields = reader.get_fields()
                count = len(case["data"]["plan"]["actions"])
                expected = {f"{name}_{index}" for name in ("owner", "due", "progress") for index in range(1, count + 1)} | {"review_notes", "review_date"}
                if count < 3:
                    expected.add("execution_notes")
                self.assertEqual(set(fields), expected)
                widgets = []
                for page in reader.pages:
                    self.assertAlmostEqual(float(page.mediabox.width), 595.28, places=1)
                    self.assertAlmostEqual(float(page.mediabox.height), 841.89, places=1)
                    for reference in page.get("/Annots", []):
                        widget = reference.get_object()
                        if widget.get("/Subtype") != "/Widget":
                            continue
                        parent = widget.get("/Parent")
                        owner = parent.get_object() if parent else widget
                        self.assertEqual(str(owner.get("/V", "")), "")
                        self.assertTrue(widget.get("/AP", {}).get("/N"))
                        widgets.append(owner.get("/T"))
                self.assertEqual(set(widgets), expected)
                self.assertTrue(all(item["top"] >= 0 and item["bottom"] < 818 for item in result["layout"]))


if __name__ == "__main__":
    unittest.main()
