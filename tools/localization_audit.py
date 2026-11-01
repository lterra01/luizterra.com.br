"""Audit reader-facing text without treating URLs or technical IDs as prose."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {"en": "en", "pt-BR": "pt", "es": "es"}
MISSING_ACCENTS = {
    "pt": {
        "nao", "voce", "voces", "sao", "alem", "ate", "ja", "tambem",
        "experiencia", "experiencias", "estrategica", "estrategicas",
        "estrategico", "estrategicos", "estrategia", "estrategias",
        "operacao", "operacoes", "comunicacao", "comunicacoes",
        "avaliacao", "avaliacoes", "integracao", "integracoes",
        "expansao", "relacao", "relacoes", "solucao", "solucoes",
        "presenca", "industria", "reunioes", "negocio", "negocios",
        "referencias", "exposicao", "tecnologicas", "tecnologicos",
        "decisoes", "tecnico", "tecnica", "tecnicos", "tecnicas",
        "acuracia", "resiliencia", "disponivel", "disponiveis",
        "conteudo", "conteudos", "numero", "numeros", "publico",
        "publicos", "pagina", "paginas", "proximo", "proximos",
        "basico", "basicos", "pratico", "praticos", "capacitacao",
        "informacao", "informacoes", "responsavel", "responsaveis",
        "metrica", "metricas", "seguranca", "comecar", "validacao",
        "gestao", "regioes", "lideranca", "latinoamerica",
    },
    "es": {
        "anos", "tecnologia", "tecnologias", "estrategica", "estrategicas",
        "estrategico", "estrategicos", "ejecucion", "conversacion",
        "construyo", "funcion", "tecnologicos",
        "tecnologicas", "comunicacion", "brasilena", "brasileno",
        "interseccion", "expansion", "linea", "articulo", "articulos",
        "exposicion", "interes", "evaluacion", "precision",
        "integracion", "optimizacion", "tecnico", "tecnica", "tecnicos",
        "tecnicas", "operacion", "gestion", "numero", "numeros",
        "pagina", "paginas", "proximo", "proximos", "decision",
        "informacion", "atencion", "automatizacion", "senalizacion",
        "conexion", "conexiones", "calculo", "diagnostico",
        "suscripcion", "renovacion", "aprobacion", "revision",
        "Africa", "Norteamerica", "Bogota", "Mexico", "publicacion", "codec", "codecs",
    },
}
UNTRANSLATED = {
    "pt": {
        "Current Role", "Current role", "Main navigation", "Language versions",
        "Footer links", "All rights reserved.", "Career", "Schedule",
        "Primary actions", "Key sectors and markets", "Career statistics",
        "Skills and expertise", "Insight categories", "Breadcrumb",
        "International partner meetings", "Building trust with operators",
        "Contact center and telecom events", "Market selection",
        "Voice quality", "Carrier diversity", "Quality and governance",
    },
    "es": {
        "Current Role", "Current role", "Main navigation", "Language versions",
        "Footer links", "All rights reserved.", "Career", "Schedule",
        "Primary actions", "Key sectors and markets", "Career statistics",
        "Skills and expertise", "Insight categories", "Breadcrumb",
        "International partner meetings", "Building trust with operators",
        "Contact center and telecom events", "Market selection",
        "Voice quality", "Carrier diversity", "Quality and governance",
    },
}
MOJIBAKE = ("\ufffd", "Ã§", "Ã£", "Ã¡", "Ã©", "Ã³", "Ã±", "Â ", "â€")
TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
URL = re.compile(r"(?:https?://|mailto:|/)[^\s<>]+")
JSON_TEXT_KEYS = {
    "name", "headline", "description", "articleBody", "text", "jobTitle",
    "label", "heading", "intro", "generate", "download", "reset", "error",
    "evidence", "cadence", "maintenance", "selection", "result", "pending",
    "footer", "review", "owner", "deadline", "status", "notes", "title",
}


class PageText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.texts: list[str] = []
        self.script_type = ""
        self.script_parts: list[str] = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "style":
            self.in_style = True
        if tag == "script":
            self.script_type = a.get("type", "text/javascript")
            self.script_parts = []
        if tag == "meta" and (a.get("name") == "description" or a.get("property", "").startswith("og:") or a.get("name", "").startswith("twitter:")):
            self.texts.append(a.get("content", ""))
        for key in ("alt", "aria-label", "title", "placeholder", "data-copy-label"):
            if a.get(key):
                self.texts.append(a[key])

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        if tag == "script":
            if self.script_type in {"application/json", "application/ld+json"}:
                try:
                    self.collect_json(json.loads("".join(self.script_parts)))
                except json.JSONDecodeError:
                    pass
            self.script_type = ""
            self.script_parts = []

    def handle_data(self, data):
        if self.script_type:
            self.script_parts.append(data)
        elif not self.in_style and data.strip():
            self.texts.append(data.strip())

    def collect_json(self, value, key="", in_copy=False):
        in_copy = in_copy or key in {"tracks", "pdf_copy", "pdf_topics"}
        if isinstance(value, dict):
            for name, item in value.items():
                self.collect_json(item, name, in_copy)
        elif isinstance(value, list):
            for item in value:
                self.collect_json(item, key, in_copy)
        elif isinstance(value, str) and (in_copy or key in JSON_TEXT_KEYS):
            self.texts.append(value)


def text_findings(text: str, lang: str):
    prose = URL.sub("", text)
    for marker in MOJIBAKE:
        if marker in prose:
            yield "encoding", marker
    if unicodedata.normalize("NFC", prose) != prose:
        yield "unicode_normalization", "NFC"
    bad = {word.casefold() for word in MISSING_ACCENTS.get(lang, set())}
    for word in sorted(set(TOKEN.findall(prose))):
        if word.casefold() in bad:
            yield "missing_accent", word
    for phrase in sorted(UNTRANSLATED.get(lang, set())):
        if re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", prose):
            yield "untranslated", phrase


def audit(root: Path = ROOT):
    findings = []
    pages = Counter()
    unique = {lang: set() for lang in LANGUAGES.values()}
    for path in sorted(root.rglob("*.html")):
        relative = path.relative_to(root)
        if any(part in {"node_modules", ".git", "public", "output"} for part in relative.parts):
            continue
        page = PageText()
        page.feed(path.read_text(encoding="utf-8", errors="strict"))
        lang = LANGUAGES.get(page.lang)
        if not lang:
            findings.append({"path": relative.as_posix(), "kind": "html_language", "term": page.lang})
            continue
        pages[lang] += 1
        for text in dict.fromkeys(page.texts):
            unique[lang].add(text)
            for kind, term in text_findings(text, lang):
                findings.append({"path": relative.as_posix(), "language": lang, "kind": kind, "term": term, "text": text})
    return {"pages": dict(pages), "unique_texts": {lang: len(texts) for lang, texts in unique.items()}, "findings": findings}, unique


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--export-text", type=Path)
    args = parser.parse_args()
    report, unique = audit(args.root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.export_text:
        args.export_text.mkdir(parents=True, exist_ok=True)
        for lang, texts in unique.items():
            (args.export_text / f"{lang}.txt").write_text("\n\n".join(sorted(texts)) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "findings"} | {"findings": len(report["findings"])}, ensure_ascii=False))
    return bool(report["findings"])


if __name__ == "__main__":
    raise SystemExit(main())
