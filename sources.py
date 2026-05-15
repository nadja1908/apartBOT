from __future__ import annotations

from collections.abc import Callable

from requests import RequestException

from og_additional_agencies import fetch_listings as fetch_og_extra
from rentvalley import fetch_listings as fetch_rentvalley
from thehague_realty import fetch_listings as fetch_thehague
from verra import fetch_listings as fetch_verra


def _safe_extend(items: list, fetch_fn: Callable[[], list], name: str) -> None:
    try:
        batch = fetch_fn()
        items.extend(batch)
        print(f"  {name}: {len(batch)} oglasa", flush=True)
    except RequestException as exc:
        print(
            f"  {name}: preskočeno — mreža/DNS ({exc.__class__.__name__})",
            flush=True,
        )
    except Exception as exc:
        print(
            f"  {name}: preskočeno — {exc.__class__.__name__}: {exc}",
            flush=True,
        )


def fetch_all_listings() -> list[dict]:
    print("Skidanje izvora (1–3 min je normalno)...", flush=True)
    items: list[dict] = []
    _safe_extend(items, fetch_rentvalley, "Rent Valley")
    _safe_extend(items, fetch_verra, "Verra")
    _safe_extend(items, fetch_og_extra, "OG makelari")
    _safe_extend(items, fetch_thehague, "The Hague RE")
    return items
