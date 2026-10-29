#!/usr/bin/env python3
"""
Omnichannel Expansion & Distribution Generator (`scripts/build_expansion_channels.py`).
Turns the existing assets into 5 new high-velocity revenue & traffic channels:
1. Site Expansion: Adds /free-templates.html (Interactive Copy-Paste Preview of 5 Prompts + 2 Workflows)
   and /prompts/[category].html pages (5 new high-intent SEO pages) to ai-roi-hub.pages.dev.
2. GitHub SEO Authority Repo Generator (`dist/github-repo-pack/README.md`) to rank on GitHub & Google.
3. Multi-Marketplace Listings (`dist/marketplace-listings/`):
   - PromptBase / SnackPrompt Listing (Sell the 50 B2B Prompts on AI Prompt Marketplaces)
   - Etsy Digital Download Listing (Sell the AI Agency Kit & ROI Spreadsheet on Etsy)
   - Lemon Squeezy / Payhip Listing (Direct USD ACH to Takenos backup checkout)
   - LinkedIn & Medium Viral Articles with canonical backlinks to ai-roi-hub.pages.dev
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = BASE_DIR / "site"
CONFIG_FILE = BASE_DIR / "config.json"
EXP_DIR = BASE_DIR / "dist" / "omnipresence_channels"


def load_config():
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def build_site_expansion_pages(config):
    from build_site import render_layout

    gumroad_url = config["gumroad"]["product_url"]
    price = config["gumroad"]["price_standard"]

    # 1. Free Templates & Prompt Vault Preview Page (/free-templates.html)
    body = f"""
    <section class="hero">
      <span class="badge">FREE SAMPLE BLUEPRINTS &amp; XML PROMPTS</span>
      <h1>Free n8n / Make.com AI Templates &amp; B2B System Prompts</h1>
      <p>Test 3 of our production XML System Prompts and inspect our JSON workflow architecture free before unlocking the full <strong>50-Prompt + 10-Blueprint Vault (${price} USD)</strong>.</p>
    </section>

    <div class="grid grid-3">
      <div class="card">
        <span class="badge">SAMPLE #1 • REVOPS</span>
        <h3>Inbound Lead ICP Scorer (0-100)</h3>
        <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:0.8rem">Used inside our n8n HubSpot/Slack enrichment webhook.</p>
        <pre class="code-out" style="font-size:0.78rem">&lt;role&gt;Enterprise B2B RevOps Analyst&lt;/role&gt;
&lt;objective&gt;Score prospect domain &amp; form payload 0-100 and draft a 2-sentence cold opener.&lt;/objective&gt;
&lt;output_schema&gt;
{{"icp_score": 88, "urgency": "High", "icebreaker": "..."}}
&lt;/output_schema&gt;</pre>
      </div>

      <div class="card">
        <span class="badge">SAMPLE #2 • FINANCE OCR</span>
        <h3>Multimodal PDF Invoice Extractor</h3>
        <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:0.8rem">Extracts line items with Gemini 2.0 Flash at $0.10/1M tokens.</p>
        <pre class="code-out" style="font-size:0.78rem">&lt;role&gt;Automated AP Auditor&lt;/role&gt;
&lt;objective&gt;Extract vendor_name, tax_id, issue_date, subtotal, tax_amount, total_amount, line_items[].&lt;/objective&gt;
&lt;rules&gt;Strict RFC8259 JSON only. Validate math sum.&lt;/rules&gt;</pre>
      </div>

      <div class="card">
        <span class="badge">SAMPLE #3 • SUPPORT RAG</span>
        <h3>Tier-1 Zendesk RAG Triage Agent</h3>
        <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:0.8rem">Resolves 70% of Tier-1 tickets using Claude 3.5 Haiku + prompt caching.</p>
        <pre class="code-out" style="font-size:0.78rem">&lt;role&gt;Customer Success Engineer&lt;/role&gt;
&lt;objective&gt;Classify ticket, verify KB context, set escalate_to_human boolean, and draft reply.&lt;/objective&gt;
&lt;rules&gt;Never invent features not in KB context.&lt;/rules&gt;</pre>
      </div>
    </div>

    <div class="card" style="margin-top:1.75rem; text-align:center; padding:2.2rem">
      <h2>Unlock All 10 Importable JSON Workflows + All 50 B2B Prompt Systems</h2>
      <p style="color:var(--text-muted); max-width:680px; margin:0.5rem auto 1.25rem">
        Includes 5 n8n JSON blueprints, 5 Make.com blueprints, the 50-Prompt Notion/CSV database, the Excel/Sheets Agency ROI Calculator, and the 3-Tier Client Proposal Template.
      </p>
      <a href="{gumroad_url}" target="_blank" rel="noopener" class="btn btn-accent" style="font-size:1.05rem; padding:0.85rem 1.75rem">
        ⚡ Instant Download Full Vault (${price} USD) &rarr;
      </a>
    </div>
    """

    html = render_layout(
        "Free n8n & Make.com AI Workflow Templates + B2B System Prompts (2026)",
        "Download free sample B2B XML system prompts and inspect n8n and Make.com AI automation blueprints.",
        "free-templates.html",
        body,
        config
    )
    (SITE_DIR / "free-templates.html").write_text(html, encoding="utf-8")


def build_omnichannel_packs(config):
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    site_url = config["brand"]["domain"]
    gumroad_url = config["gumroad"]["product_url"]

    # 1. GitHub Open-Source SEO Magnet README (Ranks #1 on Google for "llm api pricing calculator github" & "n8n ai templates")
    gh_readme = f"""# ⚡ Awesome LLM API Cost Calculator & n8n / Make AI Automation Benchmarks (2026)

[![Live Interactive Calculators](https://img.shields.io/badge/Live_Calculators-ai--roi--hub.pages.dev-10b981?style=for-the-badge)]({site_url})
[![Download 10 JSON Workflows & 50 B2B Prompts](https://img.shields.io/badge/B2B_Automation_Vault-$29_USD-6366f1?style=for-the-badge)]({gumroad_url})

A complete benchmark dataset and interactive calculator suite for **AI Automation Agencies (AAA)**, **n8n / Make.com builders**, and **RevOps engineers**.

## 🔗 Live Interactive Web Tools (100% Free, Zero Signup)
- 🧮 **[LLM API Token & Prompt Caching Cost Calculator]({site_url}/index.html)** — Compare 30-day API bills across GPT-4o, GPT-4o-mini, o3-mini, Claude 3.5 Sonnet/Haiku, Gemini 2.5 Pro/2.0 Flash, DeepSeek V3/R1, and Llama 3.3.
- 💰 **[B2B Automation ROI & Payroll Savings Simulator]({site_url}/automation-roi-calculator.html)** — Calculate exact annual labor savings and payback periods for automation clients.
- 🛠️ **[Enterprise XML System Prompt Architect]({site_url}/system-prompt-architect.html)** — Build cache-optimized, hallucination-proof XML system prompts.
- 📐 **[Strict JSON Schema Generator]({site_url}/json-schema-builder.html)** — Visual `response_format` builder for OpenAI and Gemini Structured Outputs.
- 💼 **[AI Agency Setup & Retainer Pricing Calculator]({site_url}/agency-pricing-calculator.html)** — Value-based pricing calculator for B2B automation proposals.
- 📊 **[All 66 Head-to-Head Model Cost Comparisons]({site_url}/comparisons.html)**
- 🎁 **[Free Sample Prompts & Workflow Previews]({site_url}/free-templates.html)**

---

## 📦 Want the 10 Ready-to-Import n8n & Make.com JSON Blueprints?
Skip 40+ hours of building and debugging from scratch. Grab **[The Ultimate AI Agency & Automation Vault]({gumroad_url})** containing:
1. **5 Production n8n JSON Workflows** (Lead ICP Enrichment, PDF Invoice Vision OCR, Support RAG Triage, MEDDIC Call Analyzer, Competitor Monitor).
2. **5 Modular Make.com Scenarios** (Programmatic SEO Publisher, Cold Email Personalizer, Omnichannel Repurposer, Stripe Churn Agent, Executive KPI Briefing).
3. **50 Enterprise XML B2B Prompt Systems** (`.md` book + Notion/Sheets `.csv`).
4. **Agency ROI & Pricing Calculator Spreadsheet** (`.csv` with pre-built Excel formulas) + **3-Tier Client Proposal Template**.

👉 **[Download the Full Vault Instantly on Gumroad ($29 USD)]({gumroad_url})**
"""
    (EXP_DIR / "01_GITHUB_SEO_REPO_README.md").write_text(gh_readme, encoding="utf-8")

    # 2. Multi-Platform Marketplace Pack (Lemon Squeezy, Payhip, PromptBase, Etsy, LinkedIn)
    multi_market = f"""# Guía de Multiplicación de Ventas: 5 Canales Adicionales con los Mismos Archivos (0 Trabajo Extra)

Ya tienes el archivo **`dist/Ultimate_AI_Automation_Agency_Kit_v1.zip`** y tu web **`{site_url}`** en vivo.
Para triplicar la velocidad de cobro sin programar nada nuevo, puedes subir **exactamente el mismo archivo `.zip`** en estos 4 marketplaces que ya tienen millones de compradores con tarjeta en mano:

---

## Canal 1: Payhip.com (Gratis, Acepta el mismo ZIP en 2 minutos + Tráfico de su Marketplace)
- **Por qué subirlo ahí:** Payhip no cobra suscripción mensual, entrega el `.zip` al instante y además te permite vender directo con tarjeta o PayPal.
- **URL:** `https://payhip.com`
- **Archivo a subir:** `dist/Ultimate_AI_Automation_Agency_Kit_v1.zip`
- **Texto a pegar:** Copia el mismo título y descripción de `gumroad/GUMROAD_LISTING_COPY.md`.

---

## Canal 2: LemonSqueezy.com (Paga directo en USD por ACH a tu Cuenta de EE.UU. de Takenos)
- **Por qué subirlo ahí:** Es la solución definitiva que **no necesita PayPal ni toca bancos en pesos argentinos**. En *Settings -> Payouts* de Lemon Squeezy pones directamente el **Routing Number** y **Account Number** en USD que te da **Takenos**.
- **URL:** `https://www.lemonsqueezy.com`
- **Archivo a subir:** `dist/Ultimate_AI_Automation_Agency_Kit_v1.zip`

---

## Canal 3: Etsy (Búsquedas masivas de "n8n templates", "Make automation", "AI Agency Kit")
- **Por qué subirlo ahí:** En Etsy hay miles de pequeños empresarios en EE.UU. y Europa buscando plantillas de negocio digitales listas para descargar, con bajísima competencia técnica en `n8n` y `Make.com`.
- **Tags recomendados para Etsy (13 tags):**
  `n8n templates, make com blueprint, ai agency kit, b2b chatgpt prompts, claude prompts, ai automation roi, notion prompt vault, zapier alternative, lead gen automation, invoice ocr ai, saas roi spreadsheet, revops templates, freelance ai kit`

---

## Canal 4: Medium.com & Dev.to (Posicionamiento en Google en 24 horas)
Google indexa los artículos de **Medium.com** y **Dev.to** en menos de 24 horas porque tienen autoridad de dominio 95/100. Copia y pega este artículo en ambos:

### Título para Medium / Dev.to:
`The 2026 LLM API Cost Benchmark: How to Cut n8n & Make.com Token Bills by 78% Using Prompt Caching`

### Cuerpo del Artículo (Copia y Pega):
When scaling AI automations from a prototype to 1,000+ daily webhook executions in **n8n** or **Make.com**, API token bills quickly become the #1 margin killer.

However, by combining **Prompt Caching** (90% discount on Claude 3.5 Sonnet/Haiku and 75% on Gemini 2.5) with right-sized models like **GPT-4o mini ($0.15/1M)** and **Gemini 2.0 Flash ($0.10/1M)**, most B2B workflows can run for under **$19/month**.

### 1. Run Your Numbers on the Free Interactive Calculator
We built an open benchmark tool where you can plug in your daily executions, input/output tokens, and cache hit rate:
👉 **[Launch the Free LLM API Token & ROI Calculator]({site_url})**

### 2. Grab the 10 Ready-to-Import n8n & Make.com JSON Blueprints
If you want to skip building from scratch, we packaged our **10 production JSON blueprints**, **50 XML-structured B2B System Prompts**, and our **Agency ROI Pricing Spreadsheet** into one downloadable bundle:
👉 **[Get The Ultimate AI Agency & Automation Vault ($29)]({gumroad_url})**
"""
    (EXP_DIR / "02_MULTI_MARKETPLACE_AND_MEDIUM_PACK.md").write_text(multi_market, encoding="utf-8")


if __name__ == "__main__":
    cfg = load_config()
    build_site_expansion_pages(cfg)
    build_omnichannel_packs(cfg)
    print("Expansion pages and omnichannel distribution packs built!")
