#!/usr/bin/env python3
"""
Automated Dev.to Publisher (`scripts/publish_devto.py`).
Publishes high-converting technical SEO articles to Dev.to with backlinks to
https://ai-roi-hub.pages.dev, the GitHub Repo, and the Gumroad Vault.
"""

import argparse
import json
import urllib.request

ARTICLES = [
    {
        "title": "The 2026 LLM API Cost Benchmark: How to Cut n8n & Make.com Token Bills by 78% Using Prompt Caching",
        "tags": ["ai", "opensource", "automation", "webdev"],
        "body_markdown": """When scaling AI automations from a prototype to 1,000+ daily webhook executions in **n8n** or **Make.com**, API token bills quickly become the #1 margin killer.

However, by combining **Prompt Caching** (90% discount on Claude 3.5 Sonnet/Haiku and 75% on Gemini 2.5) with right-sized models like **GPT-4o mini ($0.15/1M)** and **Gemini 2.0 Flash ($0.10/1M)**, most B2B workflows can run for under **$19/month**.

### 1. Run Your Numbers on the Free Interactive Calculator
We built an open benchmark tool where you can plug in your daily executions, input/output tokens, and cache hit rate across 12 flagship and fast models:

👉 **[Launch the Free LLM API Token & ROI Calculator](https://ai-roi-hub.pages.dev)**

### 2. Free JSON Schema & XML System Prompt Compilers
To avoid paying for retry loops caused by broken JSON outputs, we also released two free client-side compilers:
- **[Enterprise XML System Prompt Architect](https://ai-roi-hub.pages.dev/system-prompt-architect.html)** (structures static rules at the top of your prompt to trigger automatic cache hits)
- **[Strict JSON Schema Generator](https://ai-roi-hub.pages.dev/json-schema-builder.html)** (for OpenAI & Gemini `response_format`)
- **[B2B Automation ROI & Agency Pricing Calculator](https://ai-roi-hub.pages.dev/automation-roi-calculator.html)**

### 3. Open-Source Benchmark Repository
You can inspect the raw JSON pricing dataset and 66 head-to-head model comparisons on GitHub:
👉 **[GitHub Repository: LLM API Pricing & n8n/Make Templates](https://github.com/mateojoaquinpousa-prog/llm-api-pricing-calculator-n8n-make-templates)**

### 4. Grab the 10 Ready-to-Import n8n & Make.com JSON Blueprints
If you want to skip 40+ hours of building from scratch, we packaged our **10 production JSON blueprints**, **50 XML-structured B2B System Prompts**, and our **Agency ROI Pricing Spreadsheet** into one downloadable bundle:
👉 **[Get The Ultimate AI Agency & Automation Vault ($29)](https://mateopousa.gumroad.com/l/ai-automation-vault)**
"""
    },
    {
        "title": "How to Price AI Automation Agency (AAA) Projects in 2026: Setup Fees, Retainers & ROI Math",
        "tags": ["ai", "saas", "business", "productivity"],
        "body_markdown": """One of the biggest mistakes technical builders and freelancers make when selling **n8n** or **Make.com** workflows to B2B clients is charging by the hour instead of anchoring against **quantified annual payroll saved**.

If an automated PDF invoice extractor or inbound lead qualification workflow saves a company **80 hours per month** at a $35/hr fully-loaded wage, that single workflow unlocks **$33,600/year** in net labor savings—while costing less than **$25/month** in Gemini 2.0 Flash or GPT-4o mini API tokens.

### 1. Calculate Client ROI & Recommended Setup/Retainer Pricing Free
We built two interactive calculators to run live on discovery calls with prospects:
- 🧮 **[Business AI Automation ROI & Payroll Savings Simulator](https://ai-roi-hub.pages.dev/automation-roi-calculator.html)**
- 💼 **[AI Agency Setup & Monthly Retainer Pricing Calculator](https://ai-roi-hub.pages.dev/agency-pricing-calculator.html)**
- 🎁 **[Free Sample XML System Prompts & Workflow Previews](https://ai-roi-hub.pages.dev/free-templates.html)**

### 2. The 3-Tier Anchoring Framework (Good / Better / Best)
Instead of sending a single price quote, always present three options anchored against the client's 12-month labor cost:
1. **Option 1 (Core Pilot — $1,500 Setup + $290/mo):** 1 core workflow + Slack error alerts.
2. **Option 2 (Growth Automation — $2,950 Setup + $490/mo):** 3 integrated workflows + prompt caching optimization.
3. **Option 3 (Full AI Department — $4,800 Setup + $890/mo):** 5 workflows + custom RAG knowledge base triage.

### 3. Download Our Complete Agency Vault (10 JSON Blueprints + 50 B2B Prompts + Proposal Template)
Want our ready-to-import **n8n & Make.com JSON files**, the **Excel/Sheets ROI Calculator with formulas**, and the **50 Enterprise XML Prompt Vault**?
👉 **[Download The Ultimate AI Agency & Automation Vault ($29 USD)](https://mateopousa.gumroad.com/l/ai-automation-vault)**
"""
    }
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, help="Dev.to API key")
    args = parser.parse_args()

    for idx, art in enumerate(ARTICLES, 1):
        payload = json.dumps({"article": {"published": True, **art}}).encode("utf-8")
        req = urllib.request.Request(
            "https://dev.to/api/articles",
            data=payload,
            headers={
                "api-key": args.key,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            print(f"[SUCCESS #{idx}] Published on Dev.to: {res.get('url')}")


if __name__ == "__main__":
    main()
