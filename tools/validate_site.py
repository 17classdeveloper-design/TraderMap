#!/usr/bin/env python3
"""Validate TraderMap's static localized pages before deployment."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASE = "/TraderMap"
SITE = "https://17classdeveloper-design.github.io/TraderMap"
LANGUAGES = {
    "en": "en",
    "ja": "ja",
    "ko": "ko",
    "zh-hans": "zh-Hans",
    "zh-hant": "zh-Hant",
    "de": "de",
    "fr": "fr",
    "ro": "ro",
    "uk": "uk",
    "ru": "ru",
    "id": "id",
    "tr": "tr",
    "pt": "pt",
    "es": "es",
    "ar": "ar",
}
PAGES = ("home", "privacy", "support", "terms", "operator")
EXPECTED_SECTIONS = {
    "home": 0,
    "privacy": 8,
    "support": 3,
    "terms": 7,
    "operator": 4,
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_attrs = {}
        self.ids = []
        self.hrefs = []
        self.canonicals = []
        self.alternates = []
        self.language_menu_depth = 0
        self.language_links = []

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = dict(attrs_list)
        if tag == "html":
            self.html_attrs = attrs
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "details" and "language" in attrs.get("class", "").split():
            self.language_menu_depth += 1
        if tag == "a" and "href" in attrs:
            self.hrefs.append(attrs["href"])
            if self.language_menu_depth:
                self.language_links.append(attrs)
        if tag == "link":
            rel = attrs.get("rel", "").split()
            if "canonical" in rel:
                self.canonicals.append(attrs.get("href", ""))
            if "alternate" in rel:
                self.alternates.append(attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "details" and self.language_menu_depth:
            self.language_menu_depth -= 1


def suffix(page: str) -> str:
    return "" if page == "home" else f"{page}/"


def local_target(href: str) -> Path | None:
    path = urlsplit(href).path
    if not path.startswith(f"{BASE}/"):
        return None
    relative = path[len(BASE) + 1 :]
    target = ROOT / relative
    return target / "index.html" if path.endswith("/") else target


def parse(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> None:
    errors = []
    localized_files = []

    for slug, html_lang in LANGUAGES.items():
        for page in PAGES:
            page_suffix = suffix(page)
            path = ROOT / slug / page_suffix / "index.html"
            localized_files.append(path)
            if not path.exists():
                errors.append(f"Missing page: {path.relative_to(ROOT)}")
                continue

            parsed = parse(path)
            expected_url = f"{SITE}/{slug}/{page_suffix}"
            if parsed.html_attrs.get("lang") != html_lang:
                errors.append(f"{path}: invalid html lang")
            if (parsed.html_attrs.get("dir") == "rtl") != (slug == "ar"):
                errors.append(f"{path}: invalid RTL direction")
            if parsed.canonicals != [expected_url]:
                errors.append(f"{path}: invalid canonical")
            if len(parsed.alternates) != len(LANGUAGES) + 1:
                errors.append(f"{path}: expected 16 alternate links")
            actual_hreflangs = {item.get("hreflang") for item in parsed.alternates}
            if actual_hreflangs != set(LANGUAGES.values()) | {"x-default"}:
                errors.append(f"{path}: incomplete hreflang set")
            expected_alternates = {
                html_code: f"{SITE}/{language_slug}/{page_suffix}"
                for language_slug, html_code in LANGUAGES.items()
            }
            expected_alternates["x-default"] = f"{SITE}/en/{page_suffix}"
            actual_alternates = {
                item.get("hreflang"): item.get("href")
                for item in parsed.alternates
            }
            if actual_alternates != expected_alternates:
                errors.append(f"{path}: incorrect alternate URL mapping")
            if len(parsed.language_links) != len(LANGUAGES):
                errors.append(f"{path}: expected 15 language menu links")
            expected_menu_hrefs = {
                f"{BASE}/{language_slug}/{page_suffix}"
                for language_slug in LANGUAGES
            }
            actual_menu_hrefs = {
                item.get("href") for item in parsed.language_links
            }
            if actual_menu_hrefs != expected_menu_hrefs:
                errors.append(f"{path}: incorrect language menu mapping")
            current_items = [
                item for item in parsed.language_links
                if item.get("aria-current") == "true"
            ]
            if len(current_items) != 1 or current_items[0].get("href") != (
                f"{BASE}/{slug}/{page_suffix}"
            ):
                errors.append(f"{path}: incorrect current language marker")
            if len(parsed.ids) != len(set(parsed.ids)):
                errors.append(f"{path}: duplicate IDs")

            source = path.read_text(encoding="utf-8")
            section_count = source.count('class="policy-section"')
            if section_count != EXPECTED_SECTIONS[page]:
                errors.append(
                    f"{path}: expected {EXPECTED_SECTIONS[page]} policy sections"
                )
            if page == "home" and source.count('class="link-card"') != 4:
                errors.append(f"{path}: home page must contain four document cards")

            for href in parsed.hrefs:
                target = local_target(href)
                if target is not None and not target.exists():
                    errors.append(f"{path}: broken link {href}")

    root_page = parse(ROOT / "index.html")
    root_language_links = [
        attrs for attrs in root_page.language_links
    ]
    if root_language_links:
        errors.append("Root selector unexpectedly uses a details menu")
    root_localized_links = [
        href for href in root_page.hrefs if href.startswith(f"{BASE}/")
    ]
    expected_root_links = {f"{BASE}/{slug}/" for slug in LANGUAGES}
    if (
        len(root_localized_links) != len(LANGUAGES)
        or set(root_localized_links) != expected_root_links
    ):
        errors.append("Root selector must contain 15 language links")

    all_html = list(ROOT.rglob("*.html"))
    if len(localized_files) != 75 or len(all_html) != 77:
        errors.append(
            f"Expected 75 localized and 77 total HTML files; found "
            f"{len(localized_files)} and {len(all_html)}"
        )

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [node.text for node in sitemap.findall("s:url/s:loc", namespace)]
    if len(locations) != 75 or len(locations) != len(set(locations)):
        errors.append("Sitemap must contain 75 unique localized URLs")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        raise SystemExit(1)

    print(
        "Validation passed: 15 languages, 75 localized pages, "
        "77 HTML files, complete links, hreflang metadata and RTL markers."
    )


if __name__ == "__main__":
    main()
