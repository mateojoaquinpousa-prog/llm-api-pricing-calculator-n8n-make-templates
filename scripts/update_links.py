#!/usr/bin/env python3
"""
1-Command Link & Monetization Updater (`scripts/update_links.py`).
Updates config.json and automatically rebuilds all 78+ SEO pages and the Gumroad bundle.

Usage Examples:
  python scripts/update_links.py --gumroad "https://tuusuario.gumroad.com/l/ai-automation-vault"
  python scripts/update_links.py --make "https://www.make.com/en/register?pc=TU_CODIGO" --n8n "https://n8n.io/?ref=TU_CODIGO"
  python scripts/update_links.py --domain "https://tu-dominio.pages.dev"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"


def main():
    parser = argparse.ArgumentParser(description="Update monetization URLs and rebuild the entire platform.")
    parser.add_argument("--domain", help="Your live Cloudflare Pages / Vercel domain URL")
    parser.add_argument("--gumroad", help="Your Gumroad or Lemon Squeezy checkout URL")
    parser.add_argument("--price", type=int, help="Product price in USD (e.g., 29)")
    parser.add_argument("--make", help="Your Make.com affiliate link")
    parser.add_argument("--n8n", help="Your n8n affiliate link")
    parser.add_argument("--customgpt", help="Your CustomGPT.ai affiliate link")
    parser.add_argument("--elevenlabs", help="Your ElevenLabs affiliate link")
    parser.add_argument("--synthflow", help="Your Synthflow AI affiliate link")

    args = parser.parse_args()
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))

    if args.domain:
        config["brand"]["domain"] = args.domain.rstrip("/")
    if args.gumroad:
        config["gumroad"]["product_url"] = args.gumroad
    if args.price:
        config["gumroad"]["price_standard"] = args.price
    if args.make:
        config["affiliates"]["make"]["url"] = args.make
    if args.n8n:
        config["affiliates"]["n8n"]["url"] = args.n8n
    if args.customgpt:
        config["affiliates"]["customgpt"]["url"] = args.customgpt
    if args.elevenlabs:
        config["affiliates"]["elevenlabs"]["url"] = args.elevenlabs
    if args.synthflow:
        config["affiliates"]["synthflow"]["url"] = args.synthflow

    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print("[1/3] Updated config.json successfully.")

    subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "build_digital_product.py")], check=True)
    print("[2/3] Rebuilt digital product bundle and ZIP.")

    subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "build_site.py")], check=True)
    print("[3/3] Rebuilt all 78+ SEO pages with your updated links!")


if __name__ == "__main__":
    main()
