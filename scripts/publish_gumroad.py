#!/usr/bin/env python3
"""
Automated Publisher for Gumroad API & Link Rebuilder (`scripts/publish_gumroad.py`).
Creates or updates the digital product on Gumroad via official REST API,
retrieves the live short_url, injects it into config.json, and rebuilds all 78 SEO pages.
"""

import argparse
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"


def create_gumroad_product(access_token: str):
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    description = """Stop Building AI Automations from Scratch. Deploy Proven B2B Workflows in 15 Minutes.

What You Get Inside (Instant ZIP Download):
1. 10 Ready-to-Import JSON Automation Blueprints (5 for n8n + 5 for Make.com)
2. The 50 Enterprise B2B Prompt Systems Vault (.md + Notion/Excel .csv)
3. AI Agency ROI & Token Margin Calculator (.csv with pre-built formulas)
4. High-Ticket Client Proposal & 14-Day Sprint Template

Built for AI Automation Agencies (AAA), Freelancers, Founders, and RevOps teams scaling with OpenAI, Claude 3.5, and Google Gemini."""

    payload = urllib.parse.urlencode({
        "access_token": access_token,
        "name": config["gumroad"]["product_name"],
        "price": int(config["gumroad"]["price_standard"]) * 100,  # in cents ($29.00 = 2900)
        "description": description,
        "url": "ai-automation-vault"
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.gumroad.com/v2/products",
        data=payload,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                short_url = data["product"].get("short_url")
                print(f"[SUCCESS] Created Gumroad Product: {short_url}")
                return short_url
            else:
                print("[ERROR] Gumroad API response:", data)
    except Exception as e:
        print("[ERROR] Could not create Gumroad product via API:", e)
    return None


def main():
    parser = argparse.ArgumentParser(description="Create product on Gumroad via API and update all site links.")
    parser.add_argument("--token", required=True, help="Gumroad API Access Token")
    args = parser.parse_args()

    short_url = create_gumroad_product(args.token)
    if short_url:
        subprocess.run(
            [sys.executable, str(BASE_DIR / "scripts" / "update_links.py"), "--gumroad", short_url],
            check=True
        )


if __name__ == "__main__":
    main()
