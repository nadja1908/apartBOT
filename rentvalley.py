from __future__ import annotations

import re
from html import unescape
from urllib.parse import urljoin

import requests

RENTVALLEY_URL = "https://rentvalley.nl/nl/te-huur/"
BASE_URL = "https://rentvalley.nl/nl/te-huur/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}

ITEM_RE = re.compile(
    r'<motion\.div[^>]*class="[^"]*objectItem[^"]*"[^>]*'
    r'data-city="([^"]*)"[^>]*'
    r'data-price="([^"]*)"[^>]*'
    r'data-surface="([^"]*)"[^>]*'
    r'data-bedrooms="([^"]*)"[^>]*'
    r'data-rooms="([^"]*)"[^>]*>.*?'
    r'href="([^"]+\.html)"[^>]*title="([^"]*)"',
    re.DOTALL | re.IGNORECASE,
)

# Fallback ako sajt ne koristi motion.div
ITEM_RE_FALLBACK = re.compile(
    r'class="[^"]*objectItem[^"]*"[^>]*'
    r'data-city="([^"]*)"[^>]*'
    r'data-price="([^"]*)"[^>]*'
    r'data-surface="([^"]*)"[^>]*'
    r'data-bedrooms="([^"]*)"[^>]*'
    r'data-rooms="([^"]*)"[^>]*>.*?'
    r'href="([^"]+\.html)"[^>]*title="([^"]*)"',
    re.DOTALL | re.IGNORECASE,
)


def _parse_items(html: str) -> list[dict]:
    matches = ITEM_RE.findall(html)
    if not matches:
        matches = ITEM_RE_FALLBACK.findall(html)
    items = []
    for city, price, surface, bedrooms, rooms, href, title in matches:
        slug = href.removesuffix(".html")
        items.append(
            {
                "id": slug,
                "title": unescape(title.strip()),
                "url": urljoin(BASE_URL, href),
                "price": f"\u20ac {price},-",
                "city": unescape(city.strip()),
                "surface": surface,
                "bedrooms": bedrooms,
                "rooms": rooms,
            }
        )
    return items


def fetch_listings() -> list[dict]:
    response = requests.get(RENTVALLEY_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or "utf-8"
    return _parse_items(response.text)
