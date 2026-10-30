#!/usr/bin/env python3
"""
IndexNow Instant Search Engine Submitter (`scripts/ping_indexnow.py`).
Generates the IndexNow verification key file inside `site/`, deploys it,
and submits all 95 URLs to IndexNow (Bing, Yandex, DuckDuckGo, ChatGPT Search) in one batch.
"""

import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = BASE_DIR / "site"
KEY = "6366f110b9814f46e534d399a5b4fc88"
HOST = "ai-roi-hub.pages.dev"


def write_key_file():
    key_path = SITE_DIR / f"{KEY}.txt"
    key_path.write_text(KEY, encoding="utf-8")
    print(f"[1/2] Created IndexNow verification file: {key_path.name}")


def submit_all_urls():
    all_htmls = [
        f"https://{HOST}/" + str(p.relative_to(SITE_DIR)).replace("\\", "/")
        for p in SITE_DIR.rglob("*.html")
    ]
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": all_htmls
    }
    req = urllib.request.Request(
        "https://api.indexnow.org/IndexNow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(f"[2/2] Submitted {len(all_htmls)} URLs to IndexNow (Status HTTP {resp.status})!")


if __name__ == "__main__":
    write_key_file()
