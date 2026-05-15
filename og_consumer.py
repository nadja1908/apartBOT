"""Deljena OGonline ('realtime-listings/consumer') logika kao kod Veree."""

from __future__ import annotations

import html
import os
import re
from typing import Any
from urllib.parse import urljoin

import requests

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_consumer_json(
    session: requests.Session, consumer_url: str, *, referer: str
) -> list[dict]:
    heads = {
        "User-Agent": USER_AGENT,
        "Referer": referer,
        "Accept": "application/json",
    }
    resp = session.get(consumer_url, headers=heads, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return data if isinstance(data, list) else []


def discover_consumer_from_listings_page(
    session: requests.Session, listings_page_url: str
) -> str:
    resp = session.get(
        listings_page_url,
        headers={"User-Agent": USER_AGENT},
        timeout=60,
    )
    resp.raise_for_status()
    block = re.search(
        r'class="[^"]*realtime-listings[^"]*"[^>]*data-url="([^"]+)"',
        resp.text,
    )
    if not block:
        raise RuntimeError(f"Nema realtime-listings na: {listings_page_url}")
    return urljoin(listings_page_url, block.group(1))


def optional_max_monthly_rent_eur() -> float | None:
    raw = os.environ.get("GLOBAL_MAX_MONTHLY_RENT_EUR", "").strip()
    if not raw:
        return None
    return float(raw.replace(",", "."))


def og_object_to_row(
    obj: dict[str, Any],
    *,
    id_prefix: str,
    source_label: str,
    base_url: str,
    rentals_only: bool,
    only_available: bool,
    max_monthly_rent: float | None,
) -> dict | None:
    if only_available and obj.get("statusOrig") != "available":
        return None
    if rentals_only and not obj.get("isRentals"):
        return None
    if max_monthly_rent is not None and obj.get("isRentals"):
        rp = obj.get("rentalsPrice")
        try:
            if rp is None or float(rp) <= 0 or float(rp) > max_monthly_rent:
                return None
        except (TypeError, ValueError):
            return None

    listing_id = f"{id_prefix}:{obj['_id']}"
    if obj.get("isRentals"):
        kind = "Huur"
    elif obj.get("isSales"):
        kind = "Koop"
    else:
        kind = "Aanbod"
    addr = obj.get("address") or obj.get("title") or "Woning"
    city = obj.get("city") or ""
    title = f"[{kind}] {addr}"
    price = html.unescape(obj.get("price") or "")

    raw_url = obj.get("url") or ""
    url = raw_url if raw_url.startswith("http") else urljoin(base_url, raw_url)

    return {
        "id": listing_id,
        "title": title,
        "url": url,
        "price": price,
        "city": city,
        "surface": str(obj.get("livingSurface") or ""),
        "bedrooms": str(obj.get("bedrooms") or ""),
        "source": source_label,
    }
