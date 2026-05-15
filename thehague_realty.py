"""
The Hague Real Estate — https://www.thehaguerealestate.nl/huur

Povlači JSON preko /aanbod/get (isti API kao sajt). Filtar: samo izdavanje,
status BESCHIKBAAR, maks. mesečna kirija (THRE_MAX_HIRE_EUR, default 1500).
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

import requests

HUUR_PAGE = "https://www.thehaguerealestate.nl/huur"
LIST_URL = "https://www.thehaguerealestate.nl/aanbod/get"

HEADERS_BASE = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": HUUR_PAGE,
}

PAGE_SIZE = 150
MAX_PAGES = 30

RENT_TYPES = frozenset({"IS_FOR_RENT", "IS_FOR_SALE_AND_RENT"})


def _inertia_version(session: requests.Session) -> str:
    html = session.get(HUUR_PAGE, timeout=60).text
    m = re.search(r'<div id="app"[^>]*data-page="([^"]+)"', html)
    if not m:
        raise RuntimeError("The Hague Real Estate: nema data-page (sajt se promenio)")
    raw = m.group(1).replace("&quot;", '"').replace("&amp;", "&")
    ver = json.loads(raw).get("version")
    if not ver:
        raise RuntimeError("The Hague Real Estate: nema Inertia verzije")
    return str(ver)


def _fetch_raw_listings(session: requests.Session, version: str) -> list[dict[str, Any]]:
    headers = {**HEADERS_BASE, "X-Inertia-Version": version}
    out: list[dict[str, Any]] = []
    seen: set[Any] = set()

    for page in range(1, MAX_PAGES + 1):
        r = session.get(
            LIST_URL,
            params={"limit": PAGE_SIZE, "page": page},
            headers=headers,
            timeout=120,
        )
        r.raise_for_status()
        batch = r.json()
        if not isinstance(batch, list) or not batch:
            break
        new_rows = 0
        for obj in batch:
            oid = obj.get("id")
            if oid is None or oid in seen:
                continue
            seen.add(oid)
            out.append(obj)
            new_rows += 1
        # Ako stranica ne donosi nove ID-jeve, API verovatno ignorise page
        if new_rows == 0:
            break
        if len(batch) < PAGE_SIZE:
            break

    return out


def _hire_eur_max() -> float:
    raw = os.environ.get("THRE_MAX_HIRE_EUR", "1500").strip()
    if not raw:
        raw = "1500"
    return float(raw.replace(",", "."))


def _monthly_price_eur(obj: dict[str, Any]) -> float | None:
    hp = obj.get("hire_price")
    if hp is None:
        return None
    try:
        return float(hp)
    except (TypeError, ValueError):
        return None


def fetch_listings() -> list[dict]:
    """Samo dostupni najam, maks THRE_MAX_HIRE_EUR (default 1500)."""
    max_eur = _hire_eur_max()
    session = requests.Session()
    session.headers.update({"User-Agent": HEADERS_BASE["User-Agent"]})
    version = _inertia_version(session)
    raw_list = _fetch_raw_listings(session, version)

    items: list[dict] = []
    for obj in raw_list:
        if obj.get("object_status") != "BESCHIKBAAR":
            continue
        if obj.get("transfer_type") not in RENT_TYPES:
            continue
        hire = _monthly_price_eur(obj)
        if hire is None or hire <= 0 or hire > max_eur:
            continue

        obj_id = obj.get("id")
        link = obj.get("link") or ""
        addr = obj.get("address") or {}
        city = ""
        if isinstance(addr, dict):
            city = (addr.get("plaats") or "").strip()

        title_addr = obj.get("formatted_address") or f"Object {obj_id}"
        hpt = obj.get("hire_price_type") or ""
        if hpt == "PER_MAAND":
            price_str = f"€ {int(hire)} /mnd"
        elif hpt:
            price_str = f"€ {int(hire)} ({hpt})"
        else:
            price_str = f"€ {int(hire)}"

        items.append(
            {
                "id": f"thre:{obj_id}",
                "title": title_addr.strip(),
                "url": link if link.startswith("http") else "",
                "price": price_str,
                "city": city,
                "surface": str(obj.get("area") or ""),
                "bedrooms": str(obj.get("number_of_bedrooms") or ""),
                "source": "THRE",
            }
        )

    return items
