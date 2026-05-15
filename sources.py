from rentvalley import fetch_listings as fetch_rentvalley
from verra import fetch_listings as fetch_verra


def fetch_all_listings() -> list[dict]:
    items: list[dict] = []
    items.extend(fetch_rentvalley())
    items.extend(fetch_verra())
    return items
