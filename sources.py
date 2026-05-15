from __future__ import annotations

import sys
from collections.abc import Callable

from requests import RequestException

from og_additional_agencies import fetch_listings as fetch_og_extra
from rentvalley import fetch_listings as fetch_rentvalley
from thehague_realty import fetch_listings as fetch_thehague
from verra import fetch_listings as fetch_verra


def _safe_extend(items: list, fetch_fn: Callable[[], list], name: str) -> None:
    try:
        items.extend(fetch_fn())
    except RequestException as exc:
        print(
            f"[upozorenje] {name}: nema internet/DNS blokira ({exc.__class__.__name__})",
            file=sys.stderr,
        )
    except Exception as exc:
        print(
            f"[upozorenje] {name}: {exc.__class__.__name__}: {exc}",
            file=sys.stderr,
        )


def fetch_all_listings() -> list[dict]:
    items: list[dict] = []
    _safe_extend(items, fetch_rentvalley, "Rent Valley")
    _safe_extend(items, fetch_verra, "Verra")
    _safe_extend(items, fetch_og_extra, "OG makelari")
    _safe_extend(items, fetch_thehague, "The Hague RE")
    return items
