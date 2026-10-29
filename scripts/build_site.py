#!/usr/bin/env python3
"""
Programmatic SEO Static Site Builder for "AI ROI & Automation Hub" (Ruta A).
Generates:
- 6 Interactive Micro-SaaS Calculators & Generators (Home/Token Calculator, Automation ROI Calculator,
  System Prompt Architect, JSON Schema Builder, Agency Pricing Calculator, Directory)
- 36+ Programmatic Head-to-Head Model Comparison Pages (e.g., /compare/gpt-4o-vs-claude-3-5-sonnet.html)
- 6 Automation Blueprint Landing Pages (e.g., /blueprints/lead-qualification-enrichment.html)
- Gumroad SVG Cover Asset, Sitemap.xml, and Robots.txt
"""

import itertools
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = BASE_DIR / "site"
DATA_FILE = BASE_DIR / "data" / "models_and_tools.json"
CONFIG_FILE = BASE_DIR / "config.json"


def load_data():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return data, config


def write_styles_and_assets(config):
    (SITE_DIR / "assets").mkdir(parents=True, exist_ok=True)
    css = """
:root {
  --bg: #0b0f19;
  --bg-card: #111827;
  --bg-elevated: #1f2937;
  --border: #374151;
  --text: #f9fafb;
  --text-muted: #9ca3af;
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --accent: #10b981;
  --warning: #f59e0b;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Inter, sans-serif;
  background-color: var(--bg);
  color: var(--text);
  line-height: 1.6;
}
a { color: #818cf8; text-decoration: none; transition: 0.15s; }
a:hover { color: #a5b4fc; }
.container { max-width: 1180px; margin: 0 auto; padding: 0 1.25rem; }
.navbar {
  background: rgba(17, 24, 39, 0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 0.85rem 0;
}
.nav-inner { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
.brand { font-weight: 800; font-size: 1.2rem; color: #fff; display: flex; align-items: center; gap: 0.5rem; }
.brand span { background: linear-gradient(135deg, #6366f1, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav-links { display: flex; gap: 1.1rem; flex-wrap: wrap; align-items: center; font-size: 0.92rem; }
.nav-links a { color: var(--text-muted); font-weight: 500; }
.nav-links a:hover, .nav-links a.active { color: #fff; }
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 0.45rem;
  padding: 0.6rem 1.15rem; border-radius: 0.5rem; font-weight: 600; font-size: 0.92rem;
  cursor: pointer; border: none; transition: 0.2s;
}
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { background: var(--primary-hover); color: #fff; transform: translateY(-1px); }
.btn-accent { background: var(--accent); color: #052e16; font-weight: 700; }
.btn-accent:hover { background: #34d399; color: #052e16; transform: translateY(-1px); }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
.btn-outline:hover { background: var(--bg-elevated); color: #fff; }
.hero { padding: 3.2rem 0 2rem; text-align: center; }
.badge {
  display: inline-block; padding: 0.3rem 0.85rem; border-radius: 999px;
  background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.4);
  color: #a5b4fc; font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem;
}
.hero h1 { font-size: clamp(1.9rem, 4vw, 3rem); font-weight: 800; line-height: 1.18; margin-bottom: 0.9rem; }
.hero p { color: var(--text-muted); max-width: 720px; margin: 0 auto 1.5rem; font-size: 1.08rem; }
.grid { display: grid; gap: 1.25rem; }
.grid-2 { grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
.grid-3 { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 0.85rem; padding: 1.5rem;
}
.card h2, .card h3 { margin-bottom: 0.65rem; color: #fff; }
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.86rem; font-weight: 600; color: var(--text-muted); margin-bottom: 0.35rem; }
.input, select, textarea {
  width: 100%; padding: 0.65rem 0.85rem; border-radius: 0.5rem;
  background: var(--bg-elevated); border: 1px solid var(--border);
  color: #fff; font-size: 0.95rem; font-family: inherit;
}
.input:focus, select:focus, textarea:focus { outline: 2px solid var(--primary); border-color: transparent; }
.table-wrap { overflow-x: auto; margin-top: 1rem; }
table { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
th, td { padding: 0.85rem 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }
th { color: var(--text-muted); font-weight: 600; background: rgba(31, 41, 55, 0.5); }
tr:hover td { background: rgba(255, 255, 255, 0.02); }
.kpi-box {
  background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 0.75rem; padding: 1.15rem; text-align: center;
}
.kpi-val { font-size: 1.8rem; font-weight: 800; color: #34d399; }
.kpi-lbl { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.vault-banner {
  margin: 2.5rem 0; padding: 2rem; border-radius: 1rem;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.18), rgba(16, 185, 129, 0.14));
  border: 1px solid rgba(99, 102, 241, 0.45);
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.5rem;
}
.vault-banner h3 { font-size: 1.4rem; margin-bottom: 0.4rem; color: #fff; }
.vault-banner p { color: #d1d5db; max-width: 680px; font-size: 0.96rem; }
.price-tag { font-size: 1.5rem; font-weight: 800; color: #34d399; }
.price-strike { text-decoration: line-through; color: var(--text-muted); font-size: 1rem; margin-right: 0.4rem; }
pre.code-out {
  background: #050811; border: 1px solid var(--border); border-radius: 0.6rem;
  padding: 1rem; overflow-x: auto; font-family: 'Consolas', monospace; font-size: 0.86rem; color: #a7f3d0;
  white-space: pre-wrap;
}
footer {
  margin-top: 4rem; padding: 2.5rem 0; border-top: 1px solid var(--border);
  color: var(--text-muted); font-size: 0.88rem;
}
"""
    (SITE_DIR / "assets" / "style.css").write_text(css.strip(), encoding="utf-8")

    cover_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19"/>
      <stop offset="50%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#bg)"/>
  <rect x="60" y="60" width="1160" height="600" rx="24" fill="none" stroke="url(#accent)" stroke-width="3" opacity="0.6"/>
  <rect x="110" y="120" width="430" height="44" rx="22" fill="#1f2937" stroke="#6366f1" stroke-width="1.5"/>
  <text x="325" y="148" fill="#a5b4fc" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle">INSTANT DOWNLOAD • B2B AUTOMATION VAULT</text>
  <text x="110" y="245" fill="#ffffff" font-family="Arial, sans-serif" font-size="56" font-weight="bold">The Ultimate AI Agency</text>
  <text x="110" y="315" fill="#34d399" font-family="Arial, sans-serif" font-size="56" font-weight="bold">&amp; Automation Vault (2026)</text>
  <text x="110" y="385" fill="#d1d5db" font-family="Arial, sans-serif" font-size="24">• 10 Ready-to-Import n8n &amp; Make.com JSON Blueprints</text>
  <text x="110" y="430" fill="#d1d5db" font-family="Arial, sans-serif" font-size="24">• 50 XML-Structured Enterprise B2B Prompt Systems</text>
  <text x="110" y="475" fill="#d1d5db" font-family="Arial, sans-serif" font-size="24">• Client ROI &amp; Retainer Pricing Calculator Spreadsheet</text>
  <text x="110" y="520" fill="#d1d5db" font-family="Arial, sans-serif" font-size="24">• 3-Tier High-Ticket B2B Proposal &amp; Sprint Playbook</text>
  <rect x="110" y="560" width="320" height="64" rx="14" fill="#10b981"/>
  <text x="270" y="601" fill="#052e16" font-family="Arial, sans-serif" font-size="26" font-weight="bold" text-anchor="middle">ONLY ${config['gumroad']['price_standard']} USD (Save 70%)</text>
</svg>"""
    (SITE_DIR / "assets" / "gumroad-cover.svg").write_text(cover_svg, encoding="utf-8")


def render_layout(title, description, canonical_path, body_html, config, schema_json=None):
    domain = config["brand"]["domain"].rstrip("/")
    canonical_url = f"{domain}/{canonical_path.lstrip('/')}"
    prefix = "../" if "/" in canonical_path.strip("/") else ""
    schema_block = ""
    if schema_json:
        schema_block = f'<script type="application/ld+json">{json.dumps(schema_json)}</script>'

    g_Config = config["gumroad"]
    aff = config["affiliates"]

    vault_cta = f"""
    <section class="vault-banner">
      <div>
        <span class="badge">{g_Config['badge_text']}</span>
        <h3>🚀 Skip 40 Hours of Setup: Get The Ultimate AI Automation Vault</h3>
        <p>Download <strong>10 ready-to-import n8n &amp; Make.com JSON workflows</strong>, <strong>50 XML B2B Prompt Systems</strong>, and our <strong>Agency ROI &amp; Pricing Spreadsheet</strong>.</p>
      </div>
      <div style="text-align:right">
        <div style="margin-bottom:0.5rem">
          <span class="price-strike">${g_Config['price_original']}</span>
          <span class="price-tag">${g_Config['price_standard']} USD</span>
        </div>
        <a href="{g_Config['product_url']}" target="_blank" rel="noopener" class="btn btn-accent">Download Complete Vault &rarr;</a>
      </div>
    </section>
    """

    affiliate_strip = f"""
    <section class="card" style="margin-top:1.5rem">
      <h3>🔥 Recommended AI Automation Stack (Verified Free Tiers &amp; High ROI)</h3>
      <div class="grid grid-3" style="margin-top:1rem">
        <div style="padding:1rem; background:var(--bg-elevated); border-radius:0.6rem;">
          <strong>{aff['make']['name']}</strong>
          <p style="font-size:0.86rem; color:var(--text-muted); margin:0.4rem 0 0.8rem">{aff['make']['tagline']}</p>
          <a href="{aff['make']['url']}" target="_blank" rel="noopener sponsored" class="btn btn-primary" style="width:100%">{aff['make']['cta_text']}</a>
        </div>
        <div style="padding:1rem; background:var(--bg-elevated); border-radius:0.6rem;">
          <strong>{aff['n8n']['name']}</strong>
          <p style="font-size:0.86rem; color:var(--text-muted); margin:0.4rem 0 0.8rem">{aff['n8n']['tagline']}</p>
          <a href="{aff['n8n']['url']}" target="_blank" rel="noopener sponsored" class="btn btn-primary" style="width:100%">{aff['n8n']['cta_text']}</a>
        </div>
        <div style="padding:1rem; background:var(--bg-elevated); border-radius:0.6rem;">
          <strong>{aff['customgpt']['name']}</strong>
          <p style="font-size:0.86rem; color:var(--text-muted); margin:0.4rem 0 0.8rem">{aff['customgpt']['tagline']}</p>
          <a href="{aff['customgpt']['url']}" target="_blank" rel="noopener sponsored" class="btn btn-primary" style="width:100%">{aff['customgpt']['cta_text']}</a>
        </div>
      </div>
    </section>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  {schema_block}
</head>
<body>
  <header class="navbar">
    <div class="container nav-inner">
      <a href="{prefix}index.html" class="brand">⚡ <span>{config['brand']['name']}</span></a>
      <nav class="nav-links">
        <a href="{prefix}index.html">LLM Cost Calculator</a>
        <a href="{prefix}automation-roi-calculator.html">Automation ROI</a>
        <a href="{prefix}system-prompt-architect.html">Prompt Architect</a>
        <a href="{prefix}json-schema-builder.html">JSON Schema</a>
        <a href="{prefix}agency-pricing-calculator.html">Agency Pricing</a>
        <a href="{prefix}industries.html">15 Industries</a>
        <a href="{prefix}free-templates.html">Free Templates</a>
        <a href="{prefix}comparisons.html">Model Benchmarks</a>
        <a href="{g_Config['product_url']}" target="_blank" rel="noopener" class="btn btn-accent" style="padding:0.4rem 0.85rem; font-size:0.84rem">Get B2B Vault (${g_Config['price_standard']})</a>
      </nav>
    </div>
  </header>

  <main class="container">
    {body_html}
    {vault_cta}
    {affiliate_strip}
  </main>

  <footer>
    <div class="container" style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:1rem">
      <div>
        <strong>{config['brand']['name']}</strong> — {config['brand']['tagline']}<br>
        <span>Updated for 2026 LLM API Pricing (OpenAI, Anthropic, Google Gemini, DeepSeek, Meta).</span>
      </div>
      <div style="display:flex; gap:1.25rem; flex-wrap:wrap">
        <a href="{prefix}index.html">Token Calculator</a>
        <a href="{prefix}automation-roi-calculator.html">ROI Calculator</a>
        <a href="{prefix}comparisons.html">All 66 Model Comparisons</a>
        <a href="{prefix}sitemap.xml">Sitemap</a>
      </div>
    </div>
  </footer>
</body>
</html>"""


def build_index_page(data, config):
    models_json = json.dumps(data["models"])
    rows_html = ""
    for m in data["models"]:
        rows_html += f"""
        <tr data-model-id="{m['id']}">
          <td><strong>{m['name']}</strong><br><span style="font-size:0.78rem; color:var(--text-muted)">{m['provider']} • {m['tier']}</span></td>
          <td>${m['input_per_1m']:.3f}</td>
          <td>${m['cached_input_per_1m']:.3f}</td>
          <td>${m['output_per_1m']:.2f}</td>
          <td>{m['context_window']:,}</td>
          <td class="calc-monthly" style="font-weight:700; color:#34d399">$0.00</td>
        </tr>"""

    body = f"""
    <section class="hero">
      <span class="badge">LIVE 2026 API PRICING BENCHMARK</span>
      <h1>LLM API Token &amp; Monthly Cost Calculator</h1>
      <p>Compare real-time monthly API costs across <strong>GPT-4o, Claude 3.5 Sonnet, Gemini 2.5 Pro, DeepSeek V3 &amp; R1</strong> with prompt caching discounts.</p>
    </section>

    <div class="grid grid-2">
      <div class="card">
        <h2>1. Configure Your Workload</h2>
        <div class="form-group">
          <label for="runsPerDay">Workflow Executions / API Calls per Day</label>
          <input type="number" id="runsPerDay" class="input" value="1000" min="1">
        </div>
        <div class="form-group">
          <label for="inputTokens">Average Input Tokens per Call (System Prompt + Context)</label>
          <input type="number" id="inputTokens" class="input" value="2500" min="1">
        </div>
        <div class="form-group">
          <label for="outputTokens">Average Output Tokens per Call (Response)</label>
          <input type="number" id="outputTokens" class="input" value="600" min="1">
        </div>
        <div class="form-group">
          <label for="cacheHitPct">Prompt Cache Hit Rate (% of Input Tokens Cached)</label>
          <input type="range" id="cacheHitPct" min="0" max="95" value="50" style="width:100%">
          <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:var(--text-muted)">
            <span>0% (No Caching)</span>
            <strong id="cacheHitLabel" style="color:#fff">50% Cached</strong>
            <span>95% Cached</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>2. Instant Cost Optimization Summary</h2>
        <div class="grid grid-2" style="margin-top:0.8rem">
          <div class="kpi-box">
            <div class="kpi-lbl">Lowest Cost Model</div>
            <div class="kpi-val" id="cheapestName">Gemini 2.0 Flash</div>
            <div id="cheapestCost" style="font-size:0.9rem; color:#d1d5db">$0.00 / mo</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-lbl">Monthly Token Volume</div>
            <div class="kpi-val" id="totalMonthlyTokens">93.0M</div>
            <div style="font-size:0.9rem; color:#d1d5db">Input + Output / 30 days</div>
          </div>
        </div>
        <div style="margin-top:1.25rem; padding:1rem; background:var(--bg-elevated); border-radius:0.65rem; font-size:0.9rem">
          <strong>💡 Pro Tip for n8n &amp; Make.com Users:</strong> Structure your static instructions at the top of your prompt to unlock up to <strong>90% prompt caching discounts</strong> on Claude 3.5 and Gemini 2.5, or download our <strong>50 XML Prompt Vault</strong> below.
        </div>
      </div>
    </div>

    <div class="card" style="margin-top:1.5rem">
      <h2>3. Full Model-by-Model Monthly Cost Breakdown (30 Days)</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Model &amp; Provider</th>
              <th>Input / 1M</th>
              <th>Cached Input / 1M</th>
              <th>Output / 1M</th>
              <th>Context Window</th>
              <th>Est. Monthly Cost (USD)</th>
            </tr>
          </thead>
          <tbody id="pricingTableBody">
            {rows_html}
          </tbody>
        </table>
      </div>
    </div>

    <script>
      const MODELS = {models_json};
      function recalc() {{
        const runs = Math.max(1, parseFloat(document.getElementById('runsPerDay').value) || 0);
        const inTok = Math.max(0, parseFloat(document.getElementById('inputTokens').value) || 0);
        const outTok = Math.max(0, parseFloat(document.getElementById('outputTokens').value) || 0);
        const cachePct = (parseFloat(document.getElementById('cacheHitPct').value) || 0) / 100;
        document.getElementById('cacheHitLabel').textContent = Math.round(cachePct * 100) + '% Cached';

        const monthlyRuns = runs * 30;
        const totalInM = (monthlyRuns * inTok) / 1e6;
        const totalOutM = (monthlyRuns * outTok) / 1e6;
        const totalTokensM = totalInM + totalOutM;
        document.getElementById('totalMonthlyTokens').textContent = totalTokensM.toFixed(1) + 'M';

        let cheapestModel = null;
        let cheapestVal = Infinity;

        MODELS.forEach(m => {{
          const uncachedInCost = totalInM * (1 - cachePct) * m.input_per_1m;
          const cachedInCost = totalInM * cachePct * m.cached_input_per_1m;
          const outCost = totalOutM * m.output_per_1m;
          const total = uncachedInCost + cachedInCost + outCost;

          const row = document.querySelector(`tr[data-model-id="${{m.id}}"] .calc-monthly`);
          if (row) row.textContent = '$' + total.toFixed(2) + '/mo';

          if (total < cheapestVal) {{
            cheapestVal = total;
            cheapestModel = m.name;
          }}
        }});

        if (cheapestModel) {{
          document.getElementById('cheapestName').textContent = cheapestModel;
          document.getElementById('cheapestCost').textContent = '$' + cheapestVal.toFixed(2) + ' / month';
        }}
      }}
      ['runsPerDay', 'inputTokens', 'outputTokens', 'cacheHitPct'].forEach(id => {{
        document.getElementById(id).addEventListener('input', recalc);
      }});
      recalc();
    </script>
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "LLM API Token & Monthly Cost Calculator",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }
    html = render_layout(
        "LLM API Pricing & Token Cost Calculator (2026) — OpenAI, Claude, Gemini, DeepSeek",
        "Free interactive LLM API token cost calculator. Compare monthly pricing with prompt caching across GPT-4o, Claude 3.5 Sonnet, Gemini 2.5 Pro, and DeepSeek.",
        "index.html",
        body,
        config,
        schema
    )
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")


def build_automation_roi_page(data, config):
    use_cases_html = ""
    for uc in data["automation_use_cases"]:
        use_cases_html += f"""
        <div class="card">
          <span class="badge">{uc['platform'].upper()} BLUEPRINT</span>
          <h3><a href="blueprints/{uc['slug']}.html">{uc['title']}</a></h3>
          <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:1rem">{uc['description']}</p>
          <div style="font-size:0.85rem; margin-bottom:1rem">
            ⏱️ Manual: <strong>{uc['manual_minutes_per_task']} min/task</strong> • Volume: <strong>{uc['tasks_per_month']}/mo</strong>
          </div>
          <a href="blueprints/{uc['slug']}.html" class="btn btn-outline" style="width:100%">Calculate Specific ROI &rarr;</a>
        </div>"""

    body = f"""
    <section class="hero">
      <span class="badge">B2B AUTOMATION ROI SIMULATOR</span>
      <h1>Business AI Automation ROI &amp; Labor Savings Calculator</h1>
      <p>Calculate exactly how much manual payroll your company or agency clients save every year by migrating repetitive processes to <strong>n8n / Make.com + LLM APIs</strong>.</p>
    </section>

    <div class="grid grid-2">
      <div class="card">
        <h2>1. Manual Process Inputs</h2>
        <div class="form-group">
          <label for="tasksMonth">Number of Tasks Executed per Month</label>
          <input type="number" id="tasksMonth" class="input" value="800" min="1">
        </div>
        <div class="form-group">
          <label for="minsPerTask">Manual Minutes per Task</label>
          <input type="number" id="minsPerTask" class="input" value="15" min="1">
        </div>
        <div class="form-group">
          <label for="hourlyWage">Team Member Fully-Loaded Hourly Cost ($ USD)</label>
          <input type="number" id="hourlyWage" class="input" value="35" min="1">
        </div>
        <div class="form-group">
          <label for="automationPct">% of Task Automated by AI Agent</label>
          <input type="number" id="automationPct" class="input" value="85" min="10" max="100">
        </div>
      </div>

      <div class="card">
        <h2>2. Verified Annual ROI Breakdown</h2>
        <div class="grid grid-2" style="margin-top:0.8rem">
          <div class="kpi-box">
            <div class="kpi-lbl">Net Annual Dollar Savings</div>
            <div class="kpi-val" id="annualSavings">$71,100</div>
            <div style="font-size:0.85rem; color:#d1d5db">After API &amp; Make/n8n Costs</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-lbl">Hours Reclaimed / Year</div>
            <div class="kpi-val" id="hoursSaved">2,040 hrs</div>
            <div style="font-size:0.85rem; color:#d1d5db">Equivalent to 1.0 FTE Staff</div>
          </div>
        </div>
        <div style="margin-top:1.25rem; padding:1rem; background:var(--bg-elevated); border-radius:0.65rem">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem">
            <span>Current Manual Monthly Cost:</span>
            <strong id="manualMonthly">$7,000/mo</strong>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem">
            <span>Est. Make.com / n8n + LLM API Cost:</span>
            <strong id="aiMonthlyCost" style="color:#34d399">$29/mo</strong>
          </div>
          <div style="display:flex; justify-content:space-between">
            <span>Net Monthly Profit Impact:</span>
            <strong id="netMonthly" style="color:#34d399">$5,921/mo</strong>
          </div>
        </div>
      </div>
    </div>

    <section style="margin-top:2.5rem">
      <h2 style="margin-bottom:1rem">Pre-Built Industry Automation ROI Benchmarks</h2>
      <div class="grid grid-3">
        {use_cases_html}
      </div>
    </section>

    <script>
      function calcRoi() {{
        const tasks = parseFloat(document.getElementById('tasksMonth').value) || 0;
        const mins = parseFloat(document.getElementById('minsPerTask').value) || 0;
        const wage = parseFloat(document.getElementById('hourlyWage').value) || 0;
        const pct = (parseFloat(document.getElementById('automationPct').value) || 85) / 100;

        const monthlyHours = (tasks * mins) / 60;
        const manualCost = monthlyHours * wage;
        const savedHoursMo = monthlyHours * pct;
        const grossSavedMo = manualCost * pct;
        const estApiCost = Math.max(19, Math.round(tasks * 0.025));
        const netMo = Math.max(0, grossSavedMo - estApiCost);
        const netYear = netMo * 12;

        document.getElementById('manualMonthly').textContent = '$' + Math.round(manualCost).toLocaleString() + '/mo';
        document.getElementById('aiMonthlyCost').textContent = '$' + estApiCost.toLocaleString() + '/mo';
        document.getElementById('netMonthly').textContent = '$' + Math.round(netMo).toLocaleString() + '/mo';
        document.getElementById('annualSavings').textContent = '$' + Math.round(netYear).toLocaleString();
        document.getElementById('hoursSaved').textContent = Math.round(savedHoursMo * 12).toLocaleString() + ' hrs';
      }}
      ['tasksMonth', 'minsPerTask', 'hourlyWage', 'automationPct'].forEach(id => {{
        document.getElementById(id).addEventListener('input', calcRoi);
      }});
      calcRoi();
    </script>
    """
    html = render_layout(
        "AI Automation ROI & Labor Cost Savings Calculator (2026)",
        "Calculate annual payroll savings, hours reclaimed, and net ROI from deploying Make.com, n8n, and LLM API automations.",
        "automation-roi-calculator.html",
        body,
        config
    )
    (SITE_DIR / "automation-roi-calculator.html").write_text(html, encoding="utf-8")


def build_prompt_architect_page(config):
    body = """
    <section class="hero">
      <span class="badge">XML &amp; JSON PROMPT COMPILER</span>
      <h1>Enterprise System Prompt Architect</h1>
      <p>Generate token-optimized, XML-tagged system prompts for <strong>OpenAI, Claude 3.5, and Gemini</strong> that prevent hallucinations and enforce deterministic JSON outputs.</p>
    </section>

    <div class="grid grid-2">
      <div class="card">
        <h2>1. Define Agent Specification</h2>
        <div class="form-group">
          <label for="agentRole">Agent Role &amp; Persona</label>
          <input type="text" id="agentRole" class="input" value="Senior B2B RevOps & Lead Qualification Analyst">
        </div>
        <div class="form-group">
          <label for="agentGoal">Primary Objective</label>
          <textarea id="agentGoal" rows="3" class="input">Analyze incoming prospect webhook data, score ICP fit from 0-100, identify primary operational pain point, and draft a 2-sentence personalized cold outreach icebreaker.</textarea>
        </div>
        <div class="form-group">
          <label for="jsonKeys">Required JSON Output Keys (comma-separated)</label>
          <input type="text" id="jsonKeys" class="input" value="icp_score, buyer_persona, urgency_tier, core_pain_point, personalized_opener">
        </div>
        <div class="form-group">
          <label for="guardrails">Strict Guardrails &amp; Constraints</label>
          <input type="text" id="guardrails" class="input" value="Zero buzzwords, never fabricate metrics, return strict RFC8259 JSON only">
        </div>
        <button class="btn btn-primary" onclick="copyPrompt()" style="width:100%">📋 Copy Production System Prompt</button>
      </div>

      <div class="card">
        <h2>2. Compiled Production System Prompt (Cache-Ready)</h2>
        <pre class="code-out" id="promptOutput"></pre>
      </div>
    </div>

    <script>
      function buildPrompt() {
        const role = document.getElementById('agentRole').value.trim();
        const goal = document.getElementById('agentGoal').value.trim();
        const keys = document.getElementById('jsonKeys').value.split(',').map(k => k.trim()).filter(Boolean);
        const guards = document.getElementById('guardrails').value.trim();

        const schemaObj = {};
        keys.forEach(k => { schemaObj[k] = "<string_or_number_value>"; });

        const out = `<role>\\nYou are a ${role}.\\n</role>\\n\\n<objective>\\n${goal}\\n</objective>\\n\\n<operational_guardrails>\\n- ${guards}\\n- Place static instructions first to maximize LLM API prompt caching discounts.\\n- Never output markdown code fences around the JSON payload.\\n</operational_guardrails>\\n\\n<output_json_schema>\\n${JSON.stringify(schemaObj, null, 2)}\\n</output_json_schema>`;
        document.getElementById('promptOutput').textContent = out;
      }
      function copyPrompt() {
        navigator.clipboard.writeText(document.getElementById('promptOutput').textContent);
      }
      ['agentRole', 'agentGoal', 'jsonKeys', 'guardrails'].forEach(id => {
        document.getElementById(id).addEventListener('input', buildPrompt);
      });
      buildPrompt();
    </script>
    """
    html = render_layout(
        "Enterprise System Prompt Architect — XML & JSON Prompt Generator",
        "Free system prompt generator for OpenAI, Anthropic Claude, and Google Gemini. Build XML-structured prompts for n8n and Make.com workflows.",
        "system-prompt-architect.html",
        body,
        config
    )
    (SITE_DIR / "system-prompt-architect.html").write_text(html, encoding="utf-8")


def build_json_schema_page(config):
    body = """
    <section class="hero">
      <span class="badge">OPENAI &amp; GEMINI STRUCTURED OUTPUTS</span>
      <h1>JSON Schema Builder for AI Agents</h1>
      <p>Instantly generate strict <code>response_format</code> JSON Schemas for <strong>OpenAI Structured Outputs, Gemini 2.5, and n8n HTTP nodes</strong>.</p>
    </section>

    <div class="grid grid-2">
      <div class="card">
        <h2>1. Define Schema Fields</h2>
        <div class="form-group">
          <label for="schemaName">Schema Name</label>
          <input type="text" id="schemaName" class="input" value="lead_enrichment_response">
        </div>
        <div class="form-group">
          <label for="fieldDefs">Fields (Format: <code>field_name:type:description</code>, one per line)</label>
          <textarea id="fieldDefs" rows="7" class="input">icp_score:number:Fit score from 0 to 100
is_qualified:boolean:True if score is 70 or above
buyer_persona:string:Target executive role title
pain_points:array:List of top 3 operational bottlenecks
personalized_icebreaker:string:Two-sentence tailored email opener</textarea>
        </div>
        <button class="btn btn-primary" onclick="copySchema()" style="width:100%">📋 Copy OpenAI / Gemini JSON Schema</button>
      </div>

      <div class="card">
        <h2>2. Strict JSON Schema Payload</h2>
        <pre class="code-out" id="schemaOutput"></pre>
      </div>
    </div>

    <script>
      function updateSchema() {
        const name = document.getElementById('schemaName').value.trim() || 'structured_output';
        const lines = document.getElementById('fieldDefs').value.split('\\n').map(l => l.trim()).filter(Boolean);
        const properties = {};
        const required = [];

        lines.forEach(line => {
          const parts = line.split(':');
          const key = (parts[0] || '').trim();
          const typeRaw = (parts[1] || 'string').trim().toLowerCase();
          const desc = parts.slice(2).join(':').trim() || 'Extracted value';
          if (!key) return;
          required.push(key);
          if (typeRaw === 'array') {
            properties[key] = { type: 'array', items: { type: 'string' }, description: desc };
          } else {
            properties[key] = { type: typeRaw, description: desc };
          }
        });

        const payload = {
          type: "json_schema",
          json_schema: {
            name: name,
            strict: true,
            schema: {
              type: "object",
              properties: properties,
              required: required,
              additionalProperties: false
            }
          }
        };
        document.getElementById('schemaOutput').textContent = JSON.stringify(payload, null, 2);
      }
      function copySchema() {
        navigator.clipboard.writeText(document.getElementById('schemaOutput').textContent);
      }
      ['schemaName', 'fieldDefs'].forEach(id => {
        document.getElementById(id).addEventListener('input', updateSchema);
      });
      updateSchema();
    </script>
    """
    html = render_layout(
        "JSON Schema Generator for OpenAI & Gemini Structured Outputs",
        "Free visual JSON Schema generator for OpenAI response_format, Google Gemini Structured Outputs, and n8n/Make AI workflows.",
        "json-schema-builder.html",
        body,
        config
    )
    (SITE_DIR / "json-schema-builder.html").write_text(html, encoding="utf-8")


def build_agency_pricing_page(config):
    body = """
    <section class="hero">
      <span class="badge">AI AUTOMATION AGENCY (AAA) PRICING ENGINE</span>
      <h1>AI Agency Setup &amp; Retainer Pricing Calculator</h1>
      <p>Price your AI automation projects based on <strong>quantified client ROI</strong> instead of trading hours for dollars.</p>
    </section>

    <div class="grid grid-2">
      <div class="card">
        <h2>1. Client Project Parameters</h2>
        <div class="form-group">
          <label for="clientSavedMo">Estimated Client Monthly Labor Savings ($ USD)</label>
          <input type="number" id="clientSavedMo" class="input" value="4200" min="100">
        </div>
        <div class="form-group">
          <label for="workflowCount">Number of Make / n8n Workflows to Deploy</label>
          <input type="number" id="workflowCount" class="input" value="3" min="1" max="20">
        </div>
        <div class="form-group">
          <label for="complexityMult">Integration Complexity</label>
          <select id="complexityMult" class="input">
            <option value="1.0">Standard (Webhooks, CRM, Email, Slack)</option>
            <option value="1.35" selected>Intermediate (Custom RAG, Vision OCR, Multi-Agent)</option>
            <option value="1.75">Enterprise (Voice AI, Custom ERP SQL, SOC2 Guardrails)</option>
          </select>
        </div>
      </div>

      <div class="card">
        <h2>2. Recommended 3-Tier Proposal Pricing</h2>
        <div class="grid grid-2" style="margin-top:0.8rem">
          <div class="kpi-box">
            <div class="kpi-lbl">Recommended Setup Fee</div>
            <div class="kpi-val" id="recSetup">$2,850</div>
            <div style="font-size:0.82rem; color:#d1d5db">One-Time Implementation</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-lbl">Monthly Retainer</div>
            <div class="kpi-val" id="recRetainer">$590/mo</div>
            <div style="font-size:0.82rem; color:#d1d5db">Monitoring &amp; Prompt Tuning</div>
          </div>
        </div>
        <div style="margin-top:1.25rem; padding:1rem; background:var(--bg-elevated); border-radius:0.65rem; font-size:0.9rem">
          <div>Client Annual Savings: <strong id="clientAnnual" style="color:#34d399">$50,400/yr</strong></div>
          <div>Client Payback Period: <strong id="paybackDays" style="color:#fff">21 Days</strong></div>
          <div>Your Gross Margin after API costs: <strong style="color:#34d399">94%+</strong></div>
        </div>
      </div>
    </div>

    <script>
      function calcAgency() {
        const savedMo = parseFloat(document.getElementById('clientSavedMo').value) || 1000;
        const wf = parseFloat(document.getElementById('workflowCount').value) || 1;
        const mult = parseFloat(document.getElementById('complexityMult').value) || 1.0;

        const baseSetup = (savedMo * 0.45) + (wf * 350);
        const setup = Math.round((baseSetup * mult) / 50) * 50;
        const retainer = Math.round(((savedMo * 0.12) + (wf * 45)) / 10) * 10;
        const payback = Math.max(5, Math.round((setup / savedMo) * 30));

        document.getElementById('recSetup').textContent = '$' + setup.toLocaleString();
        document.getElementById('recRetainer').textContent = '$' + retainer.toLocaleString() + '/mo';
        document.getElementById('clientAnnual').textContent = '$' + (savedMo * 12).toLocaleString() + '/yr';
        document.getElementById('paybackDays').textContent = payback + ' Days';
      }
      ['clientSavedMo', 'workflowCount', 'complexityMult'].forEach(id => {
        document.getElementById(id).addEventListener('input', calcAgency);
      });
      calcAgency();
    </script>
    """
    html = render_layout(
        "AI Automation Agency (AAA) Pricing & Retainer Calculator",
        "Calculate setup fees, monthly retainers, and client payback periods for Make.com and n8n AI automation projects.",
        "agency-pricing-calculator.html",
        body,
        config
    )
    (SITE_DIR / "agency-pricing-calculator.html").write_text(html, encoding="utf-8")


def build_programmatic_comparison_pages(data, config):
    comp_dir = SITE_DIR / "compare"
    comp_dir.mkdir(parents=True, exist_ok=True)
    models = data["models"]
    links = []

    for m1, m2 in itertools.combinations(models, 2):
        slug = f"{m1['id']}-vs-{m2['id']}.html"
        rel_path = f"compare/{slug}"

        in_diff_ratio = m1["input_per_1m"] / m2["input_per_1m"] if m2["input_per_1m"] else 1
        cheaper = m1 if m1["input_per_1m"] + m1["output_per_1m"] <= m2["input_per_1m"] + m2["output_per_1m"] else m2
        pricier = m2 if cheaper["id"] == m1["id"] else m1
        savings_pct = round((1 - ((cheaper["input_per_1m"] + cheaper["output_per_1m"]) / (pricier["input_per_1m"] + pricier["output_per_1m"]))) * 100)

        # Sample 1,000 runs/day (2,500 in, 600 out)
        m1_mo = ((30000 * 2500 / 1e6) * m1["input_per_1m"]) + ((30000 * 600 / 1e6) * m1["output_per_1m"])
        m2_mo = ((30000 * 2500 / 1e6) * m2["input_per_1m"]) + ((30000 * 600 / 1e6) * m2["output_per_1m"])

        body = f"""
        <section class="hero">
          <span class="badge">2026 HEAD-TO-HEAD API BENCHMARK</span>
          <h1>{m1['name']} vs {m2['name']}: API Pricing, Context &amp; Automation ROI</h1>
          <p>Switching from <strong>{pricier['name']}</strong> to <strong>{cheaper['name']}</strong> cuts token costs by <strong>{savings_pct}%</strong> on compatible workflows. Compare exact token pricing and speed below.</p>
        </section>

        <div class="card">
          <h2>Side-by-Side Technical &amp; Cost Comparison</h2>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>{m1['name']} ({m1['provider']})</th>
                  <th>{m2['name']} ({m2['provider']})</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Input Cost (per 1M tokens)</strong></td>
                  <td>${m1['input_per_1m']:.3f}</td>
                  <td>${m2['input_per_1m']:.3f}</td>
                </tr>
                <tr>
                  <td><strong>Cached Input Cost (per 1M)</strong></td>
                  <td>${m1['cached_input_per_1m']:.3f}</td>
                  <td>${m2['cached_input_per_1m']:.3f}</td>
                </tr>
                <tr>
                  <td><strong>Output Cost (per 1M tokens)</strong></td>
                  <td>${m1['output_per_1m']:.2f}</td>
                  <td>${m2['output_per_1m']:.2f}</td>
                </tr>
                <tr>
                  <td><strong>Max Context Window</strong></td>
                  <td>{m1['context_window']:,} tokens</td>
                  <td>{m2['context_window']:,} tokens</td>
                </tr>
                <tr>
                  <td><strong>Throughput Speed</strong></td>
                  <td>~{m1['speed_tps']} tokens/sec</td>
                  <td>~{m2['speed_tps']} tokens/sec</td>
                </tr>
                <tr>
                  <td><strong>Monthly Cost (1,000 runs/day)</strong></td>
                  <td><strong style="color:#34d399">${m1_mo:.2f} / month</strong></td>
                  <td><strong style="color:#34d399">${m2_mo:.2f} / month</strong></td>
                </tr>
                <tr>
                  <td><strong>Best Automation Use Case</strong></td>
                  <td>{m1['best_for']}</td>
                  <td>{m2['best_for']}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="grid grid-2" style="margin-top:1.5rem">
          <div class="card">
            <h3>When to Choose {m1['name']}</h3>
            <p style="color:var(--text-muted); margin-bottom:0.8rem">{m1['best_for']}</p>
            <ul style="padding-left:1.2rem; color:#d1d5db">
              {''.join(f'<li>{s}</li>' for s in m1['strengths'])}
            </ul>
          </div>
          <div class="card">
            <h3>When to Choose {m2['name']}</h3>
            <p style="color:var(--text-muted); margin-bottom:0.8rem">{m2['best_for']}</p>
            <ul style="padding-left:1.2rem; color:#d1d5db">
              {''.join(f'<li>{s}</li>' for s in m2['strengths'])}
            </ul>
          </div>
        </div>
        """

        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"Is {m1['name']} cheaper than {m2['name']}?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"{cheaper['name']} is {savings_pct}% cheaper than {pricier['name']} per million combined tokens ({m1['name']} is ${m1['input_per_1m']}/1M input vs {m2['name']} at ${m2['input_per_1m']}/1M input)."
                    }
                }
            ]
        }

        html = render_layout(
            f"{m1['name']} vs {m2['name']}: API Pricing & Token Cost Calculator (2026)",
            f"Compare {m1['name']} vs {m2['name']} API token pricing, prompt caching discounts, context window, and monthly costs for n8n and Make.com workflows.",
            rel_path,
            body,
            config,
            faq_schema
        )
        (comp_dir / slug).write_text(html, encoding="utf-8")
        links.append((f"{m1['name']} vs {m2['name']}", rel_path, f"Save {savings_pct}% with {cheaper['name']}"))

    # Build directory page of all 66 comparisons
    cards = "".join(
        f'<div class="card"><h3><a href="{href}">{label}</a></h3><p style="color:var(--text-muted); font-size:0.88rem">{sub}</p></div>'
        for label, href, sub in links
    )
    dir_body = f"""
    <section class="hero">
      <span class="badge">{len(links)} HEAD-TO-HEAD LLM BENCHMARKS</span>
      <h1>All LLM Model Cost &amp; ROI Comparisons</h1>
      <p>Select any two AI models below to inspect side-by-side API token costs, caching discounts, and automation benchmarks.</p>
    </section>
    <div class="grid grid-3">{cards}</div>
    """
    (SITE_DIR / "comparisons.html").write_text(
        render_layout(
            "All 66 LLM API Pricing Comparisons (GPT-4o, Claude 3.5, Gemini 2.5, DeepSeek)",
            "Directory of 66 head-to-head LLM API cost and performance comparisons for automation builders.",
            "comparisons.html",
            dir_body,
            config
        ),
        encoding="utf-8"
    )
    return [r[1] for r in links]


def build_blueprint_pages(data, config):
    bp_dir = SITE_DIR / "blueprints"
    bp_dir.mkdir(parents=True, exist_ok=True)
    paths = []

    for uc in data["automation_use_cases"]:
        slug_file = f"{uc['slug']}.html"
        rel_path = f"blueprints/{slug_file}"
        manual_hrs_mo = (uc["tasks_per_month"] * uc["manual_minutes_per_task"]) / 60
        manual_cost_mo = manual_hrs_mo * uc["hourly_rate_usd"]
        annual_savings = round((manual_cost_mo - 24) * 12)
        aff_info = config["affiliates"].get(uc["platform"], config["affiliates"]["make"])

        body = f"""
        <section class="hero">
          <span class="badge">VERIFIED {uc['platform'].upper()} WORKFLOW BLUEPRINT</span>
          <h1>{uc['title']}</h1>
          <p>{uc['description']}</p>
        </section>

        <div class="grid grid-3">
          <div class="kpi-box">
            <div class="kpi-lbl">Annual Payroll Saved</div>
            <div class="kpi-val">${annual_savings:,}</div>
            <div style="font-size:0.82rem; color:#d1d5db">Based on {uc['tasks_per_month']} tasks/mo</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-lbl">Hours Saved / Month</div>
            <div class="kpi-val">{manual_hrs_mo:.0f} hrs</div>
            <div style="font-size:0.82rem; color:#d1d5db">At {uc['manual_minutes_per_task']} mins/task</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-lbl">Optimal LLM Model</div>
            <div class="kpi-val">{uc['recommended_model']}</div>
            <div style="font-size:0.82rem; color:#d1d5db">~{uc['avg_input_tokens']} in / {uc['avg_output_tokens']} out tokens</div>
          </div>
        </div>

        <div class="card" style="margin-top:1.5rem">
          <h2>How This Automated Architecture Works</h2>
          <ol style="padding-left:1.25rem; color:#d1d5db; margin-top:0.75rem; display:grid; gap:0.5rem">
            <li><strong>Webhook / Event Trigger:</strong> Captures incoming payload automatically inside <a href="{aff_info['url']}" target="_blank" rel="noopener sponsored">{aff_info['name']}</a>.</li>
            <li><strong>Structured LLM Processing:</strong> Calls <code>{uc['recommended_model']}</code> with an XML-guarded system prompt and strict JSON Schema validation.</li>
            <li><strong>Confidence Router &amp; Sync:</strong> Routes high-confidence outputs directly to your CRM/ERP and flags edge cases in Slack.</li>
          </ol>
          <div style="margin-top:1.25rem; display:flex; gap:1rem; flex-wrap:wrap">
            <a href="{config['gumroad']['product_url']}" target="_blank" rel="noopener" class="btn btn-accent">Download This Ready-to-Import JSON Blueprint ($29 Vault) &rarr;</a>
            <a href="{aff_info['url']}" target="_blank" rel="noopener sponsored" class="btn btn-primary">{aff_info['cta_text']}</a>
          </div>
        </div>
        """

        html = render_layout(
            f"{uc['title']} — AI Automation ROI & JSON Blueprint",
            uc["description"],
            rel_path,
            body,
            config
        )
        (bp_dir / slug_file).write_text(html, encoding="utf-8")
        paths.append(rel_path)

    return paths


def build_sitemap_and_robots(all_paths, config):
    domain = config["brand"]["domain"].rstrip("/")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    url_entries = []
    for p in all_paths:
        loc = f"{domain}/{p.lstrip('/')}"
        prio = "1.0" if p == "index.html" else ("0.9" if "/" not in p else "0.8")
        url_entries.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(url_entries) + "\n</urlset>"
    (SITE_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    robots = f"User-agent: *\nAllow: /\nSitemap: {domain}/sitemap.xml\n"
    (SITE_DIR / "robots.txt").write_text(robots, encoding="utf-8")


def main():
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    data, config = load_data()
    write_styles_and_assets(config)
    build_index_page(data, config)
    build_automation_roi_page(data, config)
    build_prompt_architect_page(config)
    build_json_schema_page(config)
    build_agency_pricing_page(config)
    comp_paths = build_programmatic_comparison_pages(data, config)
    bp_paths = build_blueprint_pages(data, config)

    core_pages = [
        "index.html",
        "automation-roi-calculator.html",
        "system-prompt-architect.html",
        "json-schema-builder.html",
        "agency-pricing-calculator.html",
        "free-templates.html",
        "comparisons.html"
    ]
    all_pages = core_pages + comp_paths + bp_paths
    build_sitemap_and_robots(all_pages, config)
    print(f"Static site built successfully! Total SEO pages generated: {len(all_pages)}")


if __name__ == "__main__":
    main()
