#!/usr/bin/env python3
"""
One-Click Deployment Script for Cloudflare Pages & Gumroad (`scripts/deploy_all.py`).
Supports two modes:
1. Interactive OAuth login (`npx.cmd wrangler login`) + `wrangler pages deploy site`
2. Token-based non-interactive deploy via CLOUDFLARE_API_TOKEN & CLOUDFLARE_ACCOUNT_ID
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = BASE_DIR / "site"


def deploy_cloudflare(project_name: str, api_token: str = None, account_id: str = None):
    env = os.environ.copy()
    if api_token:
        env["CLOUDFLARE_API_TOKEN"] = api_token
    if account_id:
        env["CLOUDFLARE_ACCOUNT_ID"] = account_id

    if not api_token:
        print("[1/3] Starting Cloudflare interactive login in your browser...")
        subprocess.run(["npx.cmd", "wrangler", "login"], cwd=str(BASE_DIR), env=env, check=True)

    print(f"[2/3] Ensuring Cloudflare Pages project '{project_name}' exists...")
    subprocess.run(
        ["npx.cmd", "wrangler", "pages", "project", "create", project_name, "--production-branch", "main"],
        cwd=str(BASE_DIR),
        env=env,
        check=False  # May already exist
    )

    print(f"[3/3] Deploying all 78 SEO pages from {SITE_DIR} to Cloudflare Pages...")
    subprocess.run(
        ["npx.cmd", "wrangler", "pages", "deploy", str(SITE_DIR), "--project-name", project_name, "--branch", "main"],
        cwd=str(BASE_DIR),
        env=env,
        check=True
    )
    print(f"\n[LIVE] Your platform is now live at: https://{project_name}.pages.dev")


def main():
    parser = argparse.ArgumentParser(description="Deploy AI ROI & Automation Hub to Cloudflare Pages.")
    parser.add_argument("--project", default="ai-roi-hub", help="Cloudflare Pages project name")
    parser.add_argument("--cf-token", help="Cloudflare API Token (optional, uses browser login if omitted)")
    parser.add_argument("--cf-account", help="Cloudflare Account ID (optional)")
    parser.add_argument("--gumroad-token", help="Gumroad API Access Token to auto-create the Gumroad listing")
    args = parser.parse_args()

    if args.gumroad_token:
        subprocess.run(
            [sys.executable, str(BASE_DIR / "scripts" / "publish_gumroad.py"), "--token", args.gumroad_token],
            check=True
        )

    deploy_cloudflare(args.project, args.cf_token, args.cf_account)


if __name__ == "__main__":
    main()
