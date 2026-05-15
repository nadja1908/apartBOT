from __future__ import annotations

import requests

from og_consumer import (
    fetch_consumer_json,
    og_object_to_row,
    optional_max_monthly_rent_eur,
)

LISTINGS_PAGE = "https://www.verra.nl/nl/woningaanbod"
CONSUMER_URL = "https://www.verra.nl/nl/realtime-listings/consumer"
BASE_URL = "https://www.verra.nl"


def fetch_listings(
    *,
    only_available: bool = True,
    rentals_only: bool = False,
) -> list[dict]:
    cap = optional_max_monthly_rent_eur()
    session = requests.Session()
    raw_list = fetch_consumer_json(
        session,
        CONSUMER_URL,
        referer=LISTINGS_PAGE,
    )
    out: list[dict] = []
    for obj in raw_list:
        if not isinstance(obj, dict) or "_id" not in obj:
            continue
        row = og_object_to_row(
            obj,
            id_prefix="verra",
            source_label="Verra",
            base_url=BASE_URL,
            rentals_only=rentals_only,
            only_available=only_available,
            max_monthly_rent=cap,
        )
        if row:
            out.append(row)
    return out
