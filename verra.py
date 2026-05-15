from __future__ import annotations

import html
from urllib.parse import urljoin

import requests

CONSUMER_URL = "https://www.verra.nl/nl/realtime-listings/consumer"
BASE_URL = "https://www.verra.nl"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.verra.nl/nl/woningaanbod",
    "Accept": "application/json",
}


def fetch_listings(
    *,
    only_available: bool = True,
) -> list[dict]:
    response = requests.get(CONSUMER_URL, headers=HEADERS, timeout=60)
    response.raise_for_status()
    items = []
    for obj in response.json():
        if only_available and obj.get("statusOrig") != "available":
            continue

        listing_id = f"verra:{obj['_id']}"
        if obj.get("isRentals"):
            kind = "Huur"
        elif obj.get("isSales"):
            kind = "Koop"
        else:
            kind = "Aanbod"

        address = obj.get("address") or obj.get("title") or "Woning"
        city = obj.get("city") or ""
        title = f"[{kind}] {address}"
        price = html.unescape(obj.get("price") or "")

        items.append(
            {
                "id": listing_id,
                "title": title,
                "url": urljoin(BASE_URL, obj.get("url", "")),
                "price": price,
                "city": city,
                "surface": str(obj.get("livingSurface") or ""),
                "bedrooms": str(obj.get("bedrooms") or ""),
                "source": "Verra",
            }
        )
    return items
