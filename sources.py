from og_additional_agencies import fetch_listings as fetch_og_extra
from rentvalley import fetch_listings as fetch_rentvalley
from thehague_realty import fetch_listings as fetch_thehague
from verra import fetch_listings as fetch_verra


def fetch_all_listings() -> list[dict]:
    items: list[dict] = []
    items.extend(fetch_rentvalley())
    items.extend(fetch_verra())
    items.extend(fetch_og_extra())
    items.extend(fetch_thehague())
    return items
