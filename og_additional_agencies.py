"""Dodatni OGonline makelari (isti engine kao Verra)."""

from __future__ import annotations

from urllib.parse import urlparse

import requests

from og_consumer import (
    discover_consumer_from_listings_page,
    fetch_consumer_json,
    og_object_to_row,
    optional_max_monthly_rent_eur,
)

ADDITIONAL_OG_SITES: list[tuple[str, str, str]] = [
    ("vesting", "Vesting Vastgoed", "https://www.vestingvastgoed.nl/en/listings?salesRentals=rentals"),
    ("bwhousing", "BW Housing", "https://www.bwhousing.nl/en/rental-listings"),
    ("belvedere", "Belvedère", "https://www.belvederemakelaars.nl/en/listings"),
    ("epm", "Expat & PM", "https://www.expatpropertymanagement.nl/en/listings"),
    ("lutz", "Lutz Real Estate", "https://www.lutzrealestate.nl/en/listings-rentals"),
]


def fetch_listings() -> list[dict]:
    cap = optional_max_monthly_rent_eur()
    session = requests.Session()
    out: list[dict] = []

    for prefix, label, page in ADDITIONAL_OG_SITES:
        try:
            consumer = discover_consumer_from_listings_page(session, page)
            raw = fetch_consumer_json(session, consumer, referer=page)
        except Exception:
            continue
        parsed = urlparse(page)
        base = f"{parsed.scheme}://{parsed.netloc}"
        for obj in raw:
            if not isinstance(obj, dict) or "_id" not in obj:
                continue
            row = og_object_to_row(
                obj,
                id_prefix=prefix,
                source_label=label,
                base_url=base,
                rentals_only=True,
                only_available=True,
                max_monthly_rent=cap,
            )
            if row:
                out.append(row)
    return out
