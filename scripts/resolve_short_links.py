"""Resolve surl.li image links in the source dataset to the image URLs they point to.

surl.li answers with an HTML interstitial page instead of a redirect, so browsers cannot load these
links as images. The result is saved to data/short_links.csv and used by build_dataset.py.
"""

import csv
import re
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "short_links.csv"
SHORT_LINK = re.compile(r"^https?://surl\.li/\w+$")
IMAGE_URL = re.compile(r"https?://[^\"'<>\s]+?\.(?:jpe?g|png|webp|gif)(?:\?[^\"'<>\s]*)?", re.IGNORECASE)


def resolve(session, url):
    html = session.get(url, timeout=20).text
    for candidate in IMAGE_URL.findall(html):
        # The interstitial also embeds its own screenshot of the target page.
        if "surl.li" not in candidate and "web-screen.com" not in candidate:
            return candidate
    return ""


def main():
    raw = pd.read_excel(ROOT / "data" / "DataSet.xlsx")
    links = sorted({u.strip() for u in raw["Ảnh"].dropna() if SHORT_LINK.match(u.strip())})

    session = requests.Session()
    session.headers["User-Agent"] = "VietNam-Travel-Recommendation-System dataset builder"
    rows = []
    for url in links:
        rows.append({"short_url": url, "image_url": resolve(session, url)})
        time.sleep(1)

    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["short_url", "image_url"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{sum(bool(r['image_url']) for r in rows)}/{len(rows)} short links resolved -> {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
