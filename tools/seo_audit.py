"""Audit canonical HTML and public HTTP responses without executing Analytics."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.luizterra.com.br"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class Document(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.schemas = []
        self.json_errors = []
        self.title = ""
        self._title = False
        self._schema = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "title":
            self._title = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._schema = ""

    def handle_data(self, value):
        if self._title:
            self.title += value
        if self._schema is not None:
            self._schema += value

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False
        if tag == "script" and self._schema is not None:
            try:
                self.schemas.append(json.loads(self._schema))
            except ValueError as error:
                self.json_errors.append(str(error))
            self._schema = None

    def meta(self, key):
        return [a.get("content", "") for t, a in self.tags if t == "meta" and (a.get("name") == key or a.get("property") == key)]

    def links(self, rel):
        return [a for t, a in self.tags if t == "link" and a.get("rel") == rel]

    def asset_urls(self, url):
        assets = set()
        for tag, attrs in self.tags:
            values = []
            if tag in ("img", "script"):
                values.append(attrs.get("src", ""))
            if tag == "link" and attrs.get("rel") in ("stylesheet", "icon", "preload"):
                values.append(attrs.get("href", ""))
            if tag == "img":
                values.extend(item.strip().split()[0] for item in attrs.get("srcset", "").split(",") if item.strip())
            if tag == "meta" and attrs.get("property") == "og:image":
                values.append(attrs.get("content", ""))
            for value in values:
                target = urljoin(url, value)
                if value and urlsplit(target).netloc == urlsplit(BASE).netloc:
                    assets.add(target)
        return assets


def schema_nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from schema_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from schema_nodes(child)


def types(node):
    value = node.get("@type", [])
    return value if isinstance(value, list) else [value]


def local_path(url):
    route = unquote(urlsplit(url).path).lstrip("/")
    path = ROOT / route
    return path / "index.html" if path.is_dir() or not Path(route).suffix else path


def audit_document(url, text):
    page = Document(text)
    errors, warnings = [], []
    if not page.title.strip():
        errors.append("missing_title")
    if sum(t == "h1" for t, _ in page.tags) != 1:
        errors.append("h1_count")
    if not any(t == "html" and a.get("lang") for t, a in page.tags):
        errors.append("missing_language")
    for key in ("description", "og:title", "og:description", "og:url", "og:image", "twitter:card", "viewport"):
        if len(page.meta(key)) != 1 or not page.meta(key)[0].strip():
            errors.append("missing_or_duplicate_meta:" + key)
    if any("noindex" in value.lower() for value in page.meta("robots")):
        errors.append("noindex_in_sitemap")
    if page.links("canonical") != [{"rel": "canonical", "href": url}]:
        errors.append("canonical_mismatch")
    if page.meta("og:url") != [url]:
        errors.append("og_url_mismatch")
    alternates = {a.get("hreflang"): a.get("href") for a in page.links("alternate") if a.get("hreflang")}
    if set(alternates) != {"en", "pt-BR", "es", "x-default"}:
        errors.append("hreflang_set")
    for target in alternates.values():
        if not local_path(target).exists():
            errors.append("hreflang_missing_target:" + target)
    if not page.schemas or page.json_errors:
        errors.append("invalid_json_ld")
    missing = []
    for tag, attrs in page.tags:
        if tag == "img" and "alt" not in attrs:
            errors.append("image_missing_alt")
        if tag == "img" and not all(attrs.get(key) for key in ("width", "height")):
            warnings.append("image_missing_dimensions:" + attrs.get("src", ""))
        reference = attrs.get("src") if tag in ("img", "script") else attrs.get("href") if tag in ("a", "link") else None
        if not reference or reference.startswith(("mailto:", "tel:", "data:", "#")):
            continue
        target = urljoin(url, reference)
        if urlsplit(target).netloc == urlsplit(BASE).netloc and not local_path(target).exists():
            missing.append(target)
    errors.extend("missing_internal_target:" + target for target in sorted(set(missing)))
    for target in page.asset_urls(url):
        if not local_path(target).is_file():
            errors.append("missing_asset:" + target)
    nodes = [node for schema in page.schemas for node in schema_nodes(schema)]
    products = [node for node in nodes if "Product" in types(node)]
    is_collection = any("CollectionPage" in types(node) for node in nodes)
    if is_collection and products:
        warnings.append("product_rich_markup_on_category_page")
    for node in products:
        for key in ("name", "description", "image", "offers"):
            if not node.get(key):
                warnings.append("product_missing_" + key + ":" + node.get("name", ""))
        if not node.get("brand"):
            warnings.append("product_missing_brand:" + node.get("name", ""))
    if len(page.title) > 75:
        warnings.append("long_title:" + str(len(page.title)))
    if page.meta("description") and len(page.meta("description")[0]) > 175:
        warnings.append("long_description:" + str(len(page.meta("description")[0])))
    return {"url": url, "title": page.title, "errors": sorted(set(errors)), "warnings": sorted(set(warnings)), "alternates": alternates, "products": len(products)}, page


def fetch(url):
    try:
        request = Request(url, headers={"User-Agent": "LuizTerra-SEO-Audit/1.0", "Accept": "text/html,application/xml,text/plain,*/*"})
        with urlopen(request, timeout=30) as response:
            return {"url": url, "status": response.status, "final_url": response.url, "content_type": response.headers.get("Content-Type", ""), "x_robots_tag": response.headers.get("X-Robots-Tag", ""), "body": response.read()}
    except (HTTPError, URLError, TimeoutError) as error:
        return {"url": url, "status": getattr(error, "code", None), "error": str(error)}


def audit(live=False):
    sitemap_bytes = (ROOT / "sitemap.xml").read_bytes()
    sitemap = ET.fromstring(sitemap_bytes)
    urls = [node.text for node in sitemap.findall("s:url/s:loc", NS)]
    results, pages = [], {}
    global_errors = []
    if len(urls) != len(set(urls)):
        global_errors.append("duplicate_sitemap_url")
    responses = {}
    if live:
        with ThreadPoolExecutor(max_workers=4) as executor:
            responses = {item["url"]: item for item in executor.map(fetch, urls + [BASE + "/robots.txt", BASE + "/sitemap.xml"])}
        remote_sitemap = responses[BASE + "/sitemap.xml"]
        if remote_sitemap.get("body") != sitemap_bytes:
            global_errors.append("public_sitemap_differs_from_local")
    for url in urls:
        source = responses.get(url) if live else None
        if live and (source.get("status") != 200 or "body" not in source):
            results.append({"url": url, "errors": ["http_failure"], "warnings": [], "http": source})
            continue
        text = source["body"].decode("utf-8") if live else local_path(url).read_text(encoding="utf-8")
        result, page = audit_document(url, text)
        if live:
            result["http"] = {key: value for key, value in source.items() if key != "body"}
            if source["final_url"] != url:
                result["errors"].append("canonical_redirects")
            if "noindex" in source["x_robots_tag"].lower():
                result["errors"].append("x_robots_noindex")
        results.append(result)
        pages[url] = page
    for result in results:
        for language, target in result.get("alternates", {}).items():
            if target not in pages:
                result["errors"].append("alternate_not_in_sitemap:" + language)
            elif result["url"] not in {link.get("href") for link in pages[target].links("alternate")}:
                result["errors"].append("nonreciprocal_hreflang:" + language)
    title_counts = Counter(result.get("title") for result in results)
    description_counts = Counter(page.meta("description")[0] for page in pages.values() if page.meta("description"))
    duplicate_titles = {key: count for key, count in title_counts.items() if key and count > 1}
    duplicate_descriptions = {key: count for key, count in description_counts.items() if count > 1}
    if duplicate_titles:
        global_errors.append("duplicate_titles")
    if duplicate_descriptions:
        global_errors.append("duplicate_descriptions")
    assets = []
    if live:
        asset_urls = sorted({target for url, page in pages.items() for target in page.asset_urls(url)})
        with ThreadPoolExecutor(max_workers=4) as executor:
            for response in executor.map(fetch, asset_urls):
                target = local_path(response["url"])
                matched = target.is_file() and response.get("body") == target.read_bytes()
                assets.append({key: value for key, value in response.items() if key != "body"} | {"matches_local": matched})
                if response.get("status") != 200 or not matched:
                    global_errors.append("public_asset_missing_or_changed:" + response["url"])
    robots_text = responses.get(BASE + "/robots.txt", {}).get("body", b"").decode("utf-8") if live else (ROOT / "robots.txt").read_text(encoding="utf-8")
    robots = RobotFileParser()
    robots.parse(robots_text.splitlines())
    for url in urls:
        if not robots.can_fetch("Googlebot", url):
            global_errors.append("googlebot_disallowed:" + url)
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(), "mode": "public_http" if live else "local_generated_html",
        "summary": {"canonical_urls": len(urls), "pages_with_errors": sum(bool(row["errors"]) for row in results),
                    "pages_with_warnings": sum(bool(row["warnings"]) for row in results), "global_errors": global_errors,
                    "duplicate_titles": duplicate_titles, "duplicate_descriptions": duplicate_descriptions,
                    "public_assets_checked": len(assets),
                    "googlebot_allowed": not any(error.startswith("googlebot_disallowed:") for error in global_errors)},
        "pages": results, "assets": assets,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.live)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    raise SystemExit(bool(result["summary"]["pages_with_errors"] or result["summary"]["global_errors"]))


if __name__ == "__main__":
    main()
