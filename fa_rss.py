#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from curl_cffi import requests as crequests


SOURCES = {
    "movistar": {
        "title": "Estrenos Movistar Plus+ - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/cat_new_movistar_f.html",
    },
    "filmin": {
        "title": "Estrenos Filmin - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/cat_new_filmin.html",
    },
    "prime-video": {
        "title": "Estrenos Prime Video España - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/rdcat.php?id=new_amazon_es",
    },
    "cartelera": {
        "title": "Estrenos en cartelera - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/rdcat.php?id=new_th_es",
    },
    "hbo-max": {
        "title": "Estrenos HBO Max / Max España - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/rdcat.php?id=new_hbo_es",
    },
    "netflix": {
        "title": "Estrenos Netflix España - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/rdcat.php?id=new_netflix",
    },
    "apple-tv-plus": {
        "title": "Estrenos Apple TV+ - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/rdcat.php?id=apple_tv_plus",
    },
    "skyshowtime": {
        "title": "Estrenos SkyShowtime - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/rdcat.php?id=skyshowtime",
    },
    "disney-plus": {
        "title": "Estrenos Disney+ España - FilmAffinity",
        "url": "https://www.filmaffinity.com/es/rdcat.php?id=disneyplus",
    },
}

HEADERS = {
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.7",
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def fetch(url: str) -> BeautifulSoup:
    response = crequests.get(url, headers=HEADERS, impersonate="chrome124", timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


_DATE_WORDS = {
    # months (full + common abbreviations)
    "ene", "enero", "feb", "febrero", "mar", "marzo", "abr", "abril",
    "may", "mayo", "jun", "junio", "jul", "julio", "ago", "agosto",
    "sep", "sept", "septiembre", "oct", "octubre", "nov", "noviembre",
    "dic", "diciembre",
    # weekdays (full + common abbreviations)
    "lun", "lunes", "mar", "martes", "mie", "mié", "miércoles",
    "jue", "jueves", "vie", "viernes", "sab", "sáb", "sábado",
    "dom", "domingo",
}


def is_date(text: str) -> bool:
    text = clean(text).lower()
    if not text:
        return False
    if text == "hoy":
        return True
    patterns = [
        r"^\d{1,2}\s+[a-záéíóúñ]{3,}\.?$",
        r"^\d{1,2}\s+de\s+[a-záéíóúñ]+\s+de\s+\d{4}$",
        r"^\d{1,2}\s+de\s+[a-záéíóúñ]+$",
        r"^[a-záéíóúñ]+,\s*\d{1,2}\s+de\s+[a-záéíóúñ]+$",
        r"^[a-záéíóúñ]+,\s*\d{1,2}\s+de\s+[a-záéíóúñ]+\s+de\s+\d{4}$",
    ]
    if not any(re.match(p, text) for p in patterns):
        return False
    words = re.findall(r"[a-záéíóúñ]+", text)
    if not words:
        return False
    # Every alphabetic token must be either "de" or a known date word.
    return all(w in _DATE_WORDS or w.rstrip(".") in _DATE_WORDS or w == "de" for w in words) and any(
        w in _DATE_WORDS or w.rstrip(".") in _DATE_WORDS for w in words
    )


def is_real_film_link(href: str | None) -> bool:
    return bool(href and re.search(r"/film\d+", href))


def extract_items(soup: BeautifulSoup, page_url: str, max_items: int = 80) -> list[dict]:
    items = []
    seen = set()
    current_date = ""

    def relevant(tag) -> bool:
        if not getattr(tag, "name", None):
            return False
        text = clean(tag.get_text(" "))
        # Date containers (non-anchor elements whose whole text is a date).
        if tag.name != "a" and is_date(text) and len(text) < 80:
            return True
        # Film links.
        if tag.name == "a" and is_real_film_link(tag.get("href")):
            if not text:
                return False
            if is_date(text):
                return True
            # Skip icons, pure ratings like "5,4" and "[+]" read-more links.
            if not re.search(r"[a-záéíóúñ0-9]", text.lower()):
                return False
            if re.fullmatch(r"[\d,\.\s]+", text):
                return False
            if re.fullmatch(r"\[\+\]", text):
                return False
            # Skip blurred-out titles used as spoiler/unreleased placeholders.
            if re.fullmatch(r"[\.\u2022\s]+", text):
                return False
            return True
        return False

    for tag in soup.find_all(relevant):
        if tag.name == "a":
            text = clean(tag.get_text(" "))
            href = tag.get("href")
            link = urljoin(page_url, href)

            if is_date(text):
                current_date = text
                continue

            if link in seen:
                continue
            seen.add(link)

            title = f"{text} — {current_date}" if current_date else text
            items.append({
                "title": title,
                "link": link,
                "description": f"Estreno/incorporación según FilmAffinity{(' — ' + current_date) if current_date else ''}",
            })

            if len(items) >= max_items:
                break
        else:
            text = clean(tag.get_text(" "))
            if is_date(text):
                current_date = text

    return items


def rss_xml(channel_title: str, channel_link: str, items: list[dict]) -> str:
    now = format_datetime(datetime.now(timezone.utc))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '<channel>',
        f'<title>{html.escape(channel_title)}</title>',
        f'<link>{html.escape(channel_link)}</link>',
        f'<description>{html.escape(channel_title)}</description>',
        f'<lastBuildDate>{now}</lastBuildDate>',
    ]

    for item in items:
        lines.extend([
            '<item>',
            f'<title>{html.escape(item["title"])}</title>',
            f'<link>{html.escape(item["link"])}</link>',
            f'<guid isPermaLink="true">{html.escape(item["link"])}</guid>',
            f'<description>{html.escape(item["description"])}</description>',
            f'<pubDate>{now}</pubDate>',
            '</item>',
        ])

    lines.extend(['</channel>', '</rss>'])
    return "\n".join(lines)


def main() -> None:
    out_dir = Path("feeds")
    out_dir.mkdir(exist_ok=True)

    for slug, cfg in SOURCES.items():
        print(f"Generando {slug}...")
        soup = fetch(cfg["url"])
        items = extract_items(soup, cfg["url"])

        if not items:
            raise RuntimeError(f"No se encontraron títulos para {slug}")

        out_file = out_dir / f"{slug}.xml"
        out_file.write_text(
            rss_xml(cfg["title"], cfg["url"], items),
            encoding="utf-8",
        )

        print(f"OK: {out_file} ({len(items)} items)")


if __name__ == "__main__":
    main()
