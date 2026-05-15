"""24/7 petlja za VPS / Docker."""

import os
import time

from monitor import load_env, run_once

INTERVAL_SEC = int(os.environ.get("CHECK_INTERVAL_SEC", "600"))


def main() -> None:
    load_env()
    print(f"Cloud monitor start — provera svakih {INTERVAL_SEC}s")
    while True:
        try:
            count = run_once()
            print(f"Provera zavrsena. Novih: {count}")
        except Exception as exc:
            print(f"Greska: {exc}")
        time.sleep(INTERVAL_SEC)


if __name__ == "__main__":
    main()
