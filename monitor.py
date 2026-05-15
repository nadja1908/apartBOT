"""
Listing monitor — Rent Valley + Telegram.

Pokreni SETUP.bat (prvi put), zatim run.bat ili monitor.py.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from sources import fetch_all_listings
from telegram_notify import send_message, send_test

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", SCRIPT_DIR))
ENV_FILE = SCRIPT_DIR / ".env"
STATE_FILE = DATA_DIR / "seen_ids.json"


def load_env() -> None:
    load_dotenv(ENV_FILE, encoding="utf-8-sig")
    os.chdir(SCRIPT_DIR)


def has_telegram_env() -> bool:
    return bool(
        os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID")
    )


def require_env() -> None:
    load_env()
    if has_telegram_env():
        return
    print()
    print("Nema Telegram podesavanja.")
    print(f"Folder: {SCRIPT_DIR}")
    print("Postavi TELEGRAM_BOT_TOKEN i TELEGRAM_CHAT_ID u .env ili env varijable.")
    print()
    sys.exit(1)


def load_seen() -> set[str]:
    if not STATE_FILE.exists():
        return set()
    return set(json.loads(STATE_FILE.read_text(encoding="utf-8")))


def save_seen(seen: set[str]) -> None:
    STATE_FILE.write_text(
        json.dumps(sorted(seen), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def format_listing(item: dict) -> str:
    lines = []
    if item.get("source"):
        lines.append(f"[{item['source']}]")
    lines.append(item["title"])
    if item.get("city"):
        lines.append(item["city"])
    details = []
    if item.get("price"):
        details.append(item["price"])
    if item.get("surface"):
        details.append(f"{item['surface']} m²")
    if item.get("bedrooms"):
        details.append(f"{item['bedrooms']} slaapk.")
    if details:
        lines.append(" · ".join(details))
    lines.append(item["url"])
    return "\n".join(lines)


def run_once(*, notify: bool = True) -> int:
    seen = load_seen()
    new_count = 0

    for item in fetch_all_listings():
        listing_id = str(item["id"])
        if listing_id in seen:
            continue
        seen.add(listing_id)
        if notify:
            send_message(format_listing(item))
        new_count += 1

    save_seen(seen)
    return new_count


def seed_seen() -> int:
    seen = load_seen()
    for item in fetch_all_listings():
        seen.add(str(item["id"]))
    save_seen(seen)
    return len(seen)


def main() -> None:
    load_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Test Telegram poruke")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Sacuvaj postojece oglase bez slanja",
    )
    args = parser.parse_args()

    if args.seed:
        total = seed_seen()
        print(f"Seed gotov. Sacuvano {total} oglasa (bez obavestenja).")
        print(f"Fajl: {STATE_FILE}")
        return

    require_env()

    if args.test:
        send_test()
        print("Test poruka poslata na Telegram.")
        return

    count = run_once()
    print(f"Gotovo. Novih listinga: {count}", flush=True)


if __name__ == "__main__":
    main()
