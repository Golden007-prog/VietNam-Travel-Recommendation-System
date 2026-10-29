"""Count image URLs in data/processed/places.csv that still return an image (used for DATASET.md)."""

import time
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent


def is_image(session, url):
    try:
        with session.get(url, timeout=15, stream=True) as response:
            return response.status_code == 200 and response.headers.get("content-type", "").startswith("image/")
    except requests.RequestException:
        return False


def main():
    places = pd.read_csv(ROOT / "data" / "processed" / "places.csv", keep_default_na=False)
    session = requests.Session()
    session.headers["User-Agent"] = "VietNam-Travel-Recommendation-System link check"

    broken = Counter()
    for url in places["image_url"]:
        if not url:
            broken["(missing)"] += 1
        elif not is_image(session, url):
            broken[urlparse(url).netloc] += 1
        time.sleep(0.2)

    working = len(places) - sum(broken.values())
    print(f"{working}/{len(places)} image links work; broken by host: {dict(broken.most_common(8))}")


if __name__ == "__main__":
    main()
