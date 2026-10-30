#!/usr/bin/env python3
"""
8-Hour / Daily Telemetry & Sales Dashboard (`scripts/check_metrics.py`).
Queries Gumroad API, GitHub Traffic API, Dev.to API, and Cloudflare/GitHub Pages health
to give a 10-second executive summary of traffic, stars, and USD revenue.
"""

import json
import os
import urllib.request
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env.json"
ENV_DATA = json.loads(ENV_PATH.read_text(encoding="utf-8")) if ENV_PATH.exists() else {}

GUMROAD_TOKEN = os.environ.get("GUMROAD_TOKEN", ENV_DATA.get("gumroad_token", ""))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", ENV_DATA.get("github_token", ""))
REPO = "mateojoaquinpousa-prog/llm-api-pricing-calculator-n8n-make-templates"
DEVTO_USER = "mateojoaquinpousaprog"


def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    print("=" * 68)
    print("  AI ROI & AUTOMATION HUB — LIVE TELEMETRY & REVENUE DASHBOARD")
    print("=" * 68)

    # 1. Gumroad Sales
    g_data = fetch_json(f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}")
    for p in g_data.get("products", []):
        sales = p.get("sales_count", 0)
        rev_usd = p.get("sales_usd_cents", 0) / 100.0
        status = "LIVE & PUBLISHED" if p.get("published") else "DRAFT"
        print(f"[GUMROAD] Product: {p['name'][:48]}...")
        print(f"          Status : {status} | Price: {p['formatted_price']}")
        print(f"          Sales  : {sales} units | Total Revenue: ${rev_usd:.2f} USD")
        print(f"          URL    : {p['short_url']}")

    print("-" * 68)

    # 2. GitHub Repo & Traffic
    gh_headers = {"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Mozilla/5.0"}
    repo_info = fetch_json(f"https://api.github.com/repos/{REPO}", gh_headers)
    views_info = fetch_json(f"https://api.github.com/repos/{REPO}/traffic/views", gh_headers)
    clones_info = fetch_json(f"https://api.github.com/repos/{REPO}/traffic/clones", gh_headers)
    print(f"[GITHUB]  Repo   : https://github.com/{REPO}")
    print(f"          Stars  : {repo_info.get('stargazers_count', 0)} | Forks: {repo_info.get('forks_count', 0)}")
    print(f"          Views  : {views_info.get('count', 0)} total ({views_info.get('uniques', 0)} unique visitors)")
    print(f"          Clones : {clones_info.get('count', 0)} total ({clones_info.get('uniques', 0)} unique cloners)")

    print("-" * 68)

    # 3. Dev.to Articles
    arts = fetch_json(f"https://dev.to/api/articles?username={DEVTO_USER}")
    total_reactions = sum(a.get("public_reactions_count", 0) for a in arts)
    total_comments = sum(a.get("comments_count", 0) for a in arts)
    print(f"[DEV.TO]  Published Articles: {len(arts)} | Reactions: {total_reactions} | Comments: {total_comments}")
    for a in arts:
        print(f"          - {a['title'][:55]}... (Reactions: {a['public_reactions_count']})")

    print("=" * 68)


if __name__ == "__main__":
    main()
