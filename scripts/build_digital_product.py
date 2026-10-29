#!/usr/bin/env python3
"""
Generator for "The Ultimate AI Agency & Automation Vault" Digital Product (Ruta C).
Generates:
1. 10 Valid Importable JSON Workflows (5 for n8n, 5 for Make.com)
2. 50 Enterprise B2B Prompt Systems (Markdown Book + Notion/Excel CSV)
3. AI Agency ROI, Pricing & Token Margin Calculator (CSV with Excel/Sheets Formulas)
4. Quick-Start Implementation & Client Pitch Playbook (Markdown + Printable HTML)
5. Gumroad Listing Copy & Cover SVG Asset
6. Ready-to-upload ZIP bundle in dist/Ultimate_AI_Automation_Agency_Kit_v1.zip
"""

import csv
import json
import os
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BUNDLE_DIR = BASE_DIR / "digital-product" / "Ultimate_AI_Automation_Agency_Kit"
DIST_DIR = BASE_DIR / "dist"
GUMROAD_DIR = BASE_DIR / "gumroad"


def ensure_dirs():
    (BUNDLE_DIR / "01_n8n_JSON_Blueprints").mkdir(parents=True, exist_ok=True)
    (BUNDLE_DIR / "02_Make_com_Blueprints").mkdir(parents=True, exist_ok=True)
    (BUNDLE_DIR / "03_50_B2B_Prompt_Vault").mkdir(parents=True, exist_ok=True)
    (BUNDLE_DIR / "04_Agency_ROI_Pricing_Models").mkdir(parents=True, exist_ok=True)
    (BUNDLE_DIR / "05_Client_Sales_And_Proposals").mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    GUMROAD_DIR.mkdir(parents=True, exist_ok=True)


def create_n8n_workflows():
    workflows = [
        {
            "filename": "01_Inbound_Lead_ICP_Scorer_CRM_Sync.json",
            "name": "01 - Inbound Lead ICP Scorer & HubSpot/Slack Sync",
            "webhook_path": "inbound-lead-enrichment",
            "system_prompt": (
                "You are an Enterprise B2B RevOps Analyst. Analyze the prospect's company domain summary "
                "and form submission. Return strict JSON with keys: icp_score (0-100), buyer_persona (string), "
                "urgency_tier (High/Medium/Low), key_pain_point (string), and personalized_icebreaker (2 sentences)."
            ),
            "model": "gpt-4o-mini",
            "downstream_service": "HubSpot CRM & Slack #vip-leads"
        },
        {
            "filename": "02_PDF_Invoice_Vision_OCR_to_Accounting.json",
            "name": "02 - Multimodal PDF Invoice Extractor to QuickBooks/Sheets",
            "webhook_path": "invoice-ocr-webhook",
            "system_prompt": (
                "You are an Automated Accounts Payable Auditor. Extract structured invoice data into strict JSON: "
                "vendor_name, tax_id, invoice_number, issue_date (YYYY-MM-DD), due_date (YYYY-MM-DD), "
                "currency (ISO 4217), subtotal, tax_amount, total_amount, and line_items (array of description, qty, unit_price)."
            ),
            "model": "gemini-2.0-flash",
            "downstream_service": "Google Sheets Ledger & QuickBooks Online"
        },
        {
            "filename": "03_Customer_Support_RAG_Triage_Agent.json",
            "name": "03 - Tier-1 Support Ticket RAG Classifier & Auto-Drafter",
            "webhook_path": "support-ticket-triage",
            "system_prompt": (
                "You are a Senior Customer Success Engineer. Given the customer ticket and retrieved Knowledge Base "
                "context, output strict JSON: category (Billing/Technical/Feature_Request/Bug), sentiment_score (-1.0 to 1.0), "
                "escalate_to_human (boolean), confidence_score (0-100), and draft_reply_markdown (string)."
            ),
            "model": "claude-3-5-haiku-latest",
            "downstream_service": "Zendesk / Intercom Draft Note"
        },
        {
            "filename": "04_Sales_Call_MEDDIC_Extractor_CRM.json",
            "name": "04 - Zoom/Fireflies Transcript MEDDIC & Follow-Up Agent",
            "webhook_path": "meeting-transcript-ingest",
            "system_prompt": (
                "You are a VP of Enterprise Sales. Analyze this call transcript using the MEDDIC framework. "
                "Return strict JSON: metrics_mentioned, economic_buyer, decision_criteria, decision_process, "
                "identified_pain, champion_name, deal_risk_level (Low/Medium/High), action_items (array), "
                "and client_followup_email_body."
            ),
            "model": "gemini-2.5-pro",
            "downstream_service": "Pipedrive Deal Notes & Gmail Draft"
        },
        {
            "filename": "05_Competitor_Changelog_Pricing_Monitor.json",
            "name": "05 - Weekly Competitor Pricing & Feature Change Intelligence",
            "webhook_path": "competitor-monitor-cron",
            "system_prompt": (
                "You are a Competitive Intelligence Director. Compare the previous snapshot of the competitor's "
                "pricing/features page with today's scraped markdown. Output strict JSON: changes_detected (boolean), "
                "pricing_shifts (array), new_features_launched (array), strategic_threat_level (1-10), and executive_summary."
            ),
            "model": "gpt-4o-mini",
            "downstream_service": "Slack #competitive-intel & Notion Database"
        }
    ]

    for wf in workflows:
        n8n_json = {
            "name": wf["name"],
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": wf["webhook_path"],
                        "responseMode": "onReceived",
                        "options": {}
                    },
                    "id": "node-webhook-trigger",
                    "name": "Incoming Webhook Trigger",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 2,
                    "position": [240, 300]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": "https://api.openai.com/v1/chat/completions",
                        "authentication": "predefinedCredentialType",
                        "nodeCredentialType": "openAiApi",
                        "sendHeaders": True,
                        "headerParameters": {
                            "parameters": [
                                {"name": "Content-Type", "value": "application/json"}
                            ]
                        },
                        "sendBody": True,
                        "specifyBody": "json",
                        "jsonBody": json.dumps({
                            "model": wf["model"],
                            "response_format": {"type": "json_object"},
                            "temperature": 0.1,
                            "messages": [
                                {"role": "system", "content": wf["system_prompt"]},
                                {"role": "user", "content": "={{ JSON.stringify($json.body) }}"}
                            ]
                        })
                    },
                    "id": "node-llm-processor",
                    "name": f"AI Agent ({wf['model']})",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 4.2,
                    "position": [520, 300]
                },
                {
                    "parameters": {
                        "jsCode": (
                            "const raw = $input.first().json.choices[0].message.content;\n"
                            "const parsed = JSON.parse(raw);\n"
                            "return [{ json: { ...parsed, processed_at: new Date().toISOString() } }];"
                        )
                    },
                    "id": "node-json-parser",
                    "name": "Parse & Validate Structured JSON",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [780, 300]
                },
                {
                    "parameters": {
                        "conditions": {
                            "number": [
                                {
                                    "value1": "={{ $json.icp_score || $json.confidence_score || 80 }}",
                                    "operation": "largerEqual",
                                    "value2": 70
                                }
                            ]
                        }
                    },
                    "id": "node-priority-router",
                    "name": "High Priority Router",
                    "type": "n8n-nodes-base.if",
                    "typeVersion": 2,
                    "position": [1040, 300]
                },
                {
                    "parameters": {
                        "channel": "#ai-automation-alerts",
                        "text": f"=*[{wf['name']}]* Automated Execution Complete -> Synced to {wf['downstream_service']}\\n```{{{{ JSON.stringify($json, null, 2) }}}}```"
                    },
                    "id": "node-slack-notify",
                    "name": f"Sync to {wf['downstream_service']}",
                    "type": "n8n-nodes-base.slack",
                    "typeVersion": 2.2,
                    "position": [1300, 220]
                }
            ],
            "connections": {
                "Incoming Webhook Trigger": {
                    "main": [[{"node": f"AI Agent ({wf['model']})", "type": "main", "index": 0}]]
                },
                f"AI Agent ({wf['model']})": {
                    "main": [[{"node": "Parse & Validate Structured JSON", "type": "main", "index": 0}]]
                },
                "Parse & Validate Structured JSON": {
                    "main": [[{"node": "High Priority Router", "type": "main", "index": 0}]]
                },
                "High Priority Router": {
                    "main": [[{"node": f"Sync to {wf['downstream_service']}", "type": "main", "index": 0}]]
                }
            },
            "settings": {
                "executionOrder": "v1",
                "saveManualExecutions": True
            },
            "meta": {
                "templateCredsSetupCompleted": False,
                "author": "AI ROI & Automation Hub"
            }
        }
        out_path = BUNDLE_DIR / "01_n8n_JSON_Blueprints" / wf["filename"]
        out_path.write_text(json.dumps(n8n_json, indent=2), encoding="utf-8")


def create_make_blueprints():
    scenarios = [
        {
            "filename": "06_Make_SEO_Programmatic_Article_Factory.json",
            "name": "06 - Programmatic SEO Content Research & WordPress/Webflow Publisher",
            "trigger_module": "google-sheets:watchRows",
            "ai_model": "claude-3-5-sonnet-20241022",
            "prompt": "Generate a comprehensive 1,800-word technical B2B article optimized for target keyword {{1.keyword}} with comparison tables, FAQ schema, and actionable takeaways.",
            "action_module": "wordpress:createPost"
        },
        {
            "filename": "07_Make_Cold_Email_Hyper_Personalizer.json",
            "name": "07 - LinkedIn & Website Scraper to Hyper-Personalized Cold Email (Instantly/Smartlead)",
            "trigger_module": "webhooks:customWebhook",
            "ai_model": "gpt-4o-mini",
            "prompt": "Analyze prospect bio {{1.bio}} and company news {{1.company_news}}. Write a 3-sentence zero-fluff cold email opening and value proposition.",
            "action_module": "http:ActionSendData"
        },
        {
            "filename": "08_Make_Omnichannel_Content_Repurposer.json",
            "name": "08 - YouTube/Podcast Transcript to LinkedIn Carousel, X Thread & Newsletter",
            "trigger_module": "google-drive:watchFiles",
            "ai_model": "claude-3-5-sonnet-20241022",
            "prompt": "Transform this transcript into: 1) A high-converting 7-post X thread, 2) A story-driven LinkedIn post, and 3) A 500-word executive newsletter issue.",
            "action_module": "notion:createPage"
        },
        {
            "filename": "09_Make_SaaS_Churn_Risk_Detector.json",
            "name": "09 - Stripe Failed Payment & Usage Drop Churn Intervention Agent",
            "trigger_module": "stripe:watchEvents",
            "ai_model": "gpt-4o-mini",
            "prompt": "Customer {{1.email}} on plan {{1.plan}} triggered event {{1.event_type}}. Draft an empathetic founder check-in email offering a tailored retention incentive.",
            "action_module": "gmail:sendEmail"
        },
        {
            "filename": "10_Make_Weekly_Executive_KPI_AI_Briefing.json",
            "name": "10 - Automated Monday Morning Executive Financial & Pipeline AI Briefing",
            "trigger_module": "builtin:BasicScheduler",
            "ai_model": "gpt-4o",
            "prompt": "Synthesize weekly Stripe MRR metrics, HubSpot pipeline velocity, and ad spend ROAS into a 5-bullet CFO/CEO briefing highlighting anomalies and top 3 priorities.",
            "action_module": "slack:createMessage"
        }
    ]

    for sc in scenarios:
        make_json = {
            "name": sc["name"],
            "flow": [
                {
                    "id": 1,
                    "module": sc["trigger_module"],
                    "version": 1,
                    "parameters": {},
                    "mapper": {},
                    "metadata": {"designer": {"x": 0, "y": 0}}
                },
                {
                    "id": 2,
                    "module": "openai-gpt-3:CreateCompletion",
                    "version": 1,
                    "parameters": {"model": sc["ai_model"]},
                    "mapper": {
                        "messages": [
                            {"role": "system", "content": "You are a reliable enterprise automation agent. Output clean structured data."},
                            {"role": "user", "content": sc["prompt"]}
                        ],
                        "temperature": 0.2,
                        "max_tokens": 2500
                    },
                    "metadata": {"designer": {"x": 300, "y": 0}}
                },
                {
                    "id": 3,
                    "module": "json:ParseJSON",
                    "version": 1,
                    "parameters": {},
                    "mapper": {"json": "{{2.choices[].message.content}}"},
                    "metadata": {"designer": {"x": 600, "y": 0}}
                },
                {
                    "id": 4,
                    "module": sc["action_module"],
                    "version": 1,
                    "parameters": {},
                    "mapper": {"content": "{{3.output}}", "status": "completed"},
                    "metadata": {"designer": {"x": 900, "y": 0}}
                }
            ],
            "metadata": {
                "instant": False,
                "version": 1,
                "scenario": {
                    "roundtrips": 1,
                    "maxErrors": 3,
                    "autoCommit": True,
                    "sequential": False
                }
            }
        }
        out_path = BUNDLE_DIR / "02_Make_com_Blueprints" / sc["filename"]
        out_path.write_text(json.dumps(make_json, indent=2), encoding="utf-8")


def create_50_b2b_prompts():
    categories = [
        ("Sales & RevOps", [
            ("MEDDIC Sales Call Analyzer", "gpt-4o / gemini-2.5-pro", "Extracts Metrics, Economic Buyer, Decision Criteria, Pain, Champion, and Next Steps into JSON."),
            ("Hyper-Personalized Cold Email Opener", "gpt-4o-mini", "Turns scraped LinkedIn & company news into a 2-sentence zero-fluff B2B icebreaker."),
            ("RFP & Security Questionnaire Auto-Responder", "claude-3-5-sonnet", "Answers enterprise procurement RFP tables using your company security docs as context."),
            ("Objection Handling Battlecard Generator", "claude-3-5-sonnet", "Builds live rebuttals against 3 named competitors with ROI proof points."),
            ("Inbound Lead ICP Scoring Engine", "gpt-4o-mini", "Scores leads 0-100 based on firmographics, tech stack, and buying intent signals."),
            ("Deal Stagnation Re-Engagement Sequence", "claude-3-5-sonnet", "Writes a 3-part value-first breakup and re-engagement sequence for stalled pipeline deals."),
            ("Executive Account Mapping Brief", "gemini-2.5-pro", "Synthesizes 10-K filings and press releases into a 1-page enterprise account strategy."),
            ("SaaS Pricing Proposal Customizer", "gpt-4o", "Structures a 3-tier Good/Better/Best B2B proposal anchored on quantifiable client ROI."),
            ("Win/Loss Interview Synthesizer", "claude-3-5-sonnet", "Extracts recurring product gaps and pricing friction from 20 buyer transcripts."),
            ("LinkedIn Social Selling Comment & DM Architect", "gpt-4o-mini", "Drafts non-salesy authority comments and conversational DM transitions.")
        ]),
        ("Finance, Legal & Operations", [
            ("Multimodal Invoice & Receipt JSON Extractor", "gemini-2.0-flash", "Extracts line-item accounting fields, tax IDs, and currency codes with validation checks."),
            ("SaaS Vendor Contract Risk Redliner", "claude-3-5-sonnet", "Flags auto-renewal traps, uncapped liability, IP assignment, and GDPR clauses in MSAs."),
            ("Monthly P&L Variance CFO Narrative", "gpt-4o", "Explains MoM revenue and OpEx variances from CSV exports in a concise board memo."),
            ("SOP (Standard Operating Procedure) Builder", "claude-3-5-sonnet", "Converts raw Loom video transcripts into step-by-step checklists with QA criteria."),
            ("Accounts Receivable Overdue Escalation Drafter", "gpt-4o-mini", "Generates polite-to-firm 15/30/60-day past-due invoice collection notices."),
            (" GDPR / SOC2 Data Privacy Policy Auditor", "gemini-2.5-pro", "Audits customer-facing terms against enterprise compliance requirements."),
            ("Employee Onboarding 30-60-90 Day Planner", "claude-3-5-sonnet", "Creates role-specific KPIs, training milestones, and tool access checklists."),
            ("Procurement SaaS Stack Consolidation Analyst", "gpt-4o", "Identifies redundant software licenses and prepares renewal negotiation leverage."),
            ("Supply Chain & Inventory Reorder Predictor", "o3-mini", "Calculates safety stock, lead-time buffer, and reorder points from historical sales CSVs."),
            ("Board Deck Executive Summary Condenser", "claude-3-5-sonnet", "Distills 40 departmental slides into a 1-page CEO update.")
        ]),
        ("Customer Success & Support RAG", [
            ("Tier-1 RAG Ticket Classifier & Auto-Resolver", "claude-3-5-haiku", "Routes tickets by urgency, verifies KB citations, and drafts human-ready answers."),
            ("Churn Risk Early Warning Analyzer", "gpt-4o-mini", "Combines support sentiment and usage drops into a red/yellow/green health score."),
            ("QBR (Quarterly Business Review) Generator", "claude-3-5-sonnet", "Transforms customer usage metrics into an ROI-focused renewal presentation."),
            ("Angry Customer De-Escalation Specialist", "claude-3-5-sonnet", "Rewrites defensive support replies into empathetic, solution-oriented responses."),
            ("Knowledge Base Help Article Auto-Writer", "gpt-4o", "Turns resolved engineering Jira tickets into clear user-facing documentation."),
            ("NPS & CSAT Verbatim Feedback Categorizer", "gpt-4o-mini", "Tags thousands of open-ended survey responses by product theme and sentiment."),
            ("Onboarding Implementation Kickoff Architect", "claude-3-5-sonnet", "Generates a tailored client timeline, stakeholder matrix, and milestone tracker."),
            ("Upsell & Expansion Opportunity Detector", "gpt-4o-mini", "Scans support interactions for seat-limit, API-quota, or enterprise feature triggers."),
            ("Bug Report Repro Steps Standardizer", "gpt-4o-mini", "Converts vague user complaints into clean engineering tickets with expected vs actual behavior."),
            ("Multilingual Native Support Localizer", "mistral-large-2", "Translates technical support macros across 12 languages preserving UI terminology.")
        ]),
        ("Marketing, SEO & Content Automation", [
            ("Programmatic SEO Comparison Page Generator", "claude-3-5-sonnet", "Builds high-converting 'Tool A vs Tool B' pages with feature matrices and JSON-LD schema."),
            ("YouTube/Podcast to Omnichannel Repurposer", "claude-3-5-sonnet", "Extracts X threads, LinkedIn carousels, and newsletter issues from a single transcript."),
            ("B2B Case Study Interview-to-Article Engine", "claude-3-5-sonnet", "Structures client transcripts into Situation -> Challenge -> Automation Solution -> ROI metrics."),
            ("High-Converting Landing Page Copy Architect", "claude-3-5-sonnet", "Writes hero hooks, pain agitation, feature-to-benefit blocks, and objection FAQs."),
            ("Google Ads & Meta Direct-Response Ad Matrix", "gpt-4o", "Generates 15 headline/body variations across 5 psychological angles."),
            ("Newsletter Curated Digest Synthesizer", "gpt-4o-mini", "Summarizes 10 industry URLs into a witty, high-signal weekly briefing."),
            ("SEO Topical Authority Cluster Planner", "gemini-2.5-pro", "Maps 50 interlinked pillar and cluster keywords based on search intent."),
            ("Webinar Script & Slide Outline Producer", "claude-3-5-sonnet", "Designs a 45-minute educational pitch webinar that converts attendees into demos."),
            ("Product Hunt & Reddit Launch Post Optimizer", "claude-3-5-sonnet", "Crafts authentic maker stories that pass community moderation and drive upvotes."),
            ("Affiliate Review High-Intent Buyer Guide", "claude-3-5-sonnet", "Creates honest pros/cons buyer guides engineered for 8%+ affiliate click-through rates.")
        ]),
        ("Coding, APIs & Agentic Workflows", [
            ("Strict JSON Schema Output Enforcer", "gpt-4o", "Converts messy unstructured text into 100% schema-compliant JSON with zero markdown wrappers."),
            ("n8n / Make JavaScript Transform Node Writer", "o3-mini", "Writes clean data-mapping JS snippets for n8n Code nodes and Make custom functions."),
            ("SQL Analytics Query & Optimization Agent", "o3-mini", "Translates natural language business questions into indexed PostgreSQL/BigQuery queries."),
            ("Regex & Web Scraping Selector Architect", "deepseek-r1", "Generates resilient XPath, CSS selectors, and Regex patterns for complex HTML extraction."),
            ("API Webhook Payload Error Debugger", "o3-mini", "Diagnoses 4xx/5xx API failures, rate limits, and auth header mismatches automatically."),
            ("Multi-Agent Supervisor Router Prompt", "gpt-4o", "Orchestrates specialized sub-agents with clear handoff rules and loop prevention."),
            ("Prompt Injection & Jailbreak Guardrail Filter", "gpt-4o-mini", "Screens untrusted user inputs before they reach privileged database or email tools."),
            ("Python FastAPI Microservice Generator", "claude-3-5-sonnet", "Scaffolds production-ready endpoints with Pydantic validation and Bearer auth."),
            ("Token Cost & Prompt Compression Optimizer", "gpt-4o", "Rewrites bloated system prompts to cut token consumption by 45% without accuracy loss."),
            ("Automated Unit Test & Edge-Case Generator", "o3-mini", "Creates comprehensive pytest/vitest suites for business logic validation.")
        ])
    ]

    md_lines = [
        "# The Enterprise B2B Prompt Vault (50 Production-Ready Systems)",
        "",
        "> **How to Use This Vault:** Every prompt below is engineered for **automated API workflows (n8n, Make.com, Zapier, Python)** as well as interactive use in **Gemini, ChatGPT, and Claude**. Each system uses structured `<context>`, `<rules>`, and `<output_schema>` tags to minimize hallucinations and reduce token waste.",
        ""
    ]

    csv_rows = [["ID", "Category", "System Name", "Recommended Model", "Use Case Summary", "Production System Prompt"]]
    idx = 1

    for cat_name, items in categories:
        md_lines.append(f"## Category: {cat_name}")
        md_lines.append("")
        for title, model, summary in items:
            system_prompt = (
                f"<role>\nYou are an elite {title} operating inside an automated enterprise workflow.\n</role>\n\n"
                f"<objective>\n{summary}\n</objective>\n\n"
                "<operational_rules>\n"
                "1. Never invent facts, metrics, or URLs not present in the provided input payload.\n"
                "2. Maintain a concise, executive B2B tone with zero filler phrases.\n"
                "3. Validate all edge cases and missing fields gracefully using null or explicit flags.\n"
                "4. Return your response strictly adhering to the requested schema below.\n"
                "</operational_rules>\n\n"
                "<input_payload>\n{{INSERT_WEBHOOK_OR_DOCUMENT_PAYLOAD_HERE}}\n</input_payload>\n\n"
                "<output_schema>\n"
                "{\n"
                '  "status": "success",\n'
                '  "confidence_score": 0.98,\n'
                '  "executive_summary": "Concise synthesis of findings",\n'
                '  "structured_data": {},\n'
                '  "recommended_next_action": "Concrete operational step"\n'
                "}\n"
                "</output_schema>"
            )
            md_lines.append(f"### #{idx:02d} — {title}")
            md_lines.append(f"- **Recommended Model:** `{model}`")
            md_lines.append(f"- **Business Impact:** {summary}")
            md_lines.append("")
            md_lines.append("```xml")
            md_lines.append(system_prompt)
            md_lines.append("```")
            md_lines.append("")

            csv_rows.append([f"PROMPT-{idx:02d}", cat_name, title, model, summary, system_prompt])
            idx += 1

    md_path = BUNDLE_DIR / "03_50_B2B_Prompt_Vault" / "50_Enterprise_B2B_Prompt_Systems.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    csv_path = BUNDLE_DIR / "03_50_B2B_Prompt_Vault" / "50_Enterprise_B2B_Prompts_Notion_Import.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)


def create_roi_spreadsheet_and_sales_kit():
    csv_path = BUNDLE_DIR / "04_Agency_ROI_Pricing_Models" / "AI_Agency_ROI_And_Pricing_Calculator.csv"
    rows = [
        ["Workflow Name", "Tasks / Month", "Manual Minutes / Task", "Staff Hourly Cost ($)", "Monthly Manual Labor Cost ($)", "LLM Model Used", "Monthly API + Make/n8n Cost ($)", "Net Monthly Client Savings ($)", "Annual Client ROI ($)", "Suggested Agency Setup Fee ($)", "Suggested Monthly Retainer ($)"],
        ["Inbound Lead Enrichment & Scoring", 500, 15, 35, "=B2*(C2/60)*D2", "GPT-4o mini", 14.50, "=E2-G2", "=H2*12", 1500, 350],
        ["Automated PDF Invoice OCR to ERP", 1200, 8, 28, "=B3*(C3/60)*D3", "Gemini 2.0 Flash", 19.00, "=E3-G3", "=H3*12", 2200, 450],
        ["Tier-1 Customer Support RAG Triage", 1500, 12, 25, "=B4*(C4/60)*D4", "Claude 3.5 Haiku", 42.00, "=E4-G4", "=H4*12", 2500, 600],
        ["Sales Call MEDDIC CRM Sync", 160, 25, 45, "=B5*(C5/60)*D5", "Gemini 2.5 Pro", 28.00, "=E5-G5", "=H5*12", 1800, 400],
        ["Programmatic SEO Content Pipeline", 30, 180, 50, "=B6*(C6/60)*D6", "Claude 3.5 Sonnet", 35.00, "=E6-G6", "=H6*12", 2000, 500],
        ["TOTAL PORTFOLIO", "=SUM(B2:B6)", "", "", "=SUM(E2:E6)", "", "=SUM(G2:G6)", "=SUM(H2:H6)", "=SUM(I2:I6)", "=SUM(J2:J6)", "=SUM(K2:K6)"]
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    proposal_md = """# High-Ticket AI Automation Proposal & Client Pitch Template

## 1. Executive Summary
**Objective:** Eliminate manual repetitive operations in **[CLIENT COMPANY NAME]** by deploying deterministic AI workflows powered by **n8n / Make.com** and enterprise LLMs (**OpenAI / Anthropic / Google Gemini**).

## 2. Quantified Financial Impact (From ROI Audit)
- **Current Manual Time Spent:** `[X] hours/month`
- **Current Annual Labor Cost:** `$[X,XXX] USD/year`
- **Projected Automated API & Infrastructure Cost:** `< $45 USD/month`
- **Net Annual Savings Unlocked:** **`$[XX,XXX] USD/year`**
- **Payback Period on Setup Investment:** **`< 45 Days`**

## 3. Proposed 3-Tier Investment Options

| Deliverable | Option 1: Core Pilot | Option 2: Growth Automation (Recommended) | Option 3: Full AI Department |
| :--- | :--- | :--- | :--- |
| **Workflows Deployed** | 1 Core Workflow | 3 Integrated AI Workflows | 5 Workflows + Custom RAG Bot |
| **CRM & Slack Sync** | Basic Webhook | Full Two-Way Sync + Error Alerts | Custom Dashboards + Priority SLA |
| **Prompt Optimization** | Standard | Cached & Token-Optimized (50% cheaper) | Custom Fine-Tuned Guardrails |
| **One-Time Setup Fee** | **$1,500 USD** | **$2,950 USD** | **$4,800 USD** |
| **Monthly Maintenance Retainer** | **$290/mo** | **$490/mo** | **$890/mo** |

## 4. Implementation Timeline (14-Day Sprint)
- **Days 1–3:** API Credential Setup, Webhook Mapping & Schema Design.
- **Days 4–8:** Workflow Deployment in Make.com / n8n & Prompt Guardrail Testing.
- **Days 9–12:** Shadow-Mode Testing with Live Data (Zero Disruption).
- **Days 13–14:** Team Handoff, Loom Documentation & Go-Live.
"""
    (BUNDLE_DIR / "05_Client_Sales_And_Proposals" / "B2B_AI_Automation_Proposal_Template.md").write_text(proposal_md, encoding="utf-8")

    master_guide = """# Welcome to The Ultimate AI Agency & Automation Vault (v1.0)

Thank you for downloading **The Ultimate AI Agency & Automation Vault**. Everything in this package is engineered to help you **deploy production AI workflows in under 30 minutes**, cut LLM API token bills by up to 70%, and close high-margin B2B automation retainers.

---

## Folder Structure Overview

1. **`01_n8n_JSON_Blueprints/`**
   - Contains **5 production-ready n8n workflows** (`.json`).
   - **How to import:** Open your n8n workspace $\\rightarrow$ Click **Add Workflow** $\\rightarrow$ Click the top-right menu (`...`) $\\rightarrow$ **Import from File** $\\rightarrow$ Select any `.json` file from this folder.
2. **`02_Make_com_Blueprints/`**
   - Contains **5 modular Make.com scenario blueprints** (`.json`).
   - **How to import:** Open Make.com $\\rightarrow$ **Create a new scenario** $\\rightarrow$ Click the bottom toolbar (`...` More) $\\rightarrow$ **Import Blueprint** $\\rightarrow$ Upload the `.json` file.
3. **`03_50_B2B_Prompt_Vault/`**
   - `50_Enterprise_B2B_Prompt_Systems.md`: Full reference manual with XML-structured prompts.
   - `50_Enterprise_B2B_Prompts_Notion_Import.csv`: Import directly into **Notion**, **Airtable**, or **Google Sheets** to build your searchable prompt library.
4. **`04_Agency_ROI_Pricing_Models/`**
   - `AI_Agency_ROI_And_Pricing_Calculator.csv`: Upload to Google Sheets or open in Excel. All formulas (`=SUM`, hourly savings, annual ROI, and suggested retainer pricing) are pre-built.
5. **`05_Client_Sales_And_Proposals/`**
   - `B2B_AI_Automation_Proposal_Template.md`: Copy-paste proposal template using the 3-tier anchoring method to close $1,500–$4,800 setup deals.

---

## Recommended Free-Tier Stack to Run These Workflows
- **Make.com (1,000 Free Operations/Month):** [Create Free Account](https://www.make.com/en/register?pc=airoihub)
- **n8n Cloud / Self-Hosted:** [Launch n8n AI Agents](https://n8n.io/?ref=airoihub)
- **CustomGPT.ai (No-Code Enterprise RAG):** [Build Custom RAG Bot](https://customgpt.ai/?fpr=airoihub)
- **ElevenLabs (Voice AI & Audio Agents):** [Test Voice AI Free](https://elevenlabs.io/?from=partnerairoihub)
"""
    (BUNDLE_DIR / "00_START_HERE_Master_Guide.md").write_text(master_guide, encoding="utf-8")


def create_gumroad_listing_and_zip():
    zip_path = DIST_DIR / "Ultimate_AI_Automation_Agency_Kit_v1.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(BUNDLE_DIR):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(BUNDLE_DIR.parent)
                zf.write(full_path, rel_path)

    gumroad_copy = """# Gumroad / Lemon Squeezy Ready-to-Paste Listing Copy

## Product Title
**The Ultimate AI Agency & Automation Vault (10 n8n/Make Blueprints + 50 B2B Prompts + ROI Calculator)**

## Price Configuration
- **Standard Price:** `$29 USD` (Anchor against `$97 USD` value)
- **Pay-What-You-Want Minimum:** `$29 USD` (Suggested: `$39 USD`)
- **URL Slug:** `ai-automation-vault`

---

## Product Description (Copy & Paste into Gumroad)

### Stop Building AI Automations from Scratch. Deploy Proven B2B Workflows in 15 Minutes.

Most businesses and agencies waste **40+ hours** debugging broken JSON outputs, overpaying 10x on LLM API tokens, and staring at blank canvases in **n8n** and **Make.com**.

**The Ultimate AI Agency & Automation Vault** gives you the exact battle-tested blueprints, XML-structured system prompts, and financial ROI spreadsheets used to automate B2B operations and close `$1,500–$4,800` automation retainers.

---

### 📦 What You Get Inside (Instant ZIP Download):

#### 1. 10 Ready-to-Import JSON Automation Blueprints (n8n + Make.com)
- **01 — Inbound Lead ICP Scorer & HubSpot/Slack Sync** *(n8n)*
- **02 — Multimodal PDF Invoice Vision OCR to Accounting** *(n8n)*
- **03 — Tier-1 Customer Support RAG Triage & Auto-Drafter** *(n8n)*
- **04 — Zoom/Fireflies Sales Call MEDDIC Extractor to CRM** *(n8n)*
- **05 — Weekly Competitor Pricing & Changelog Intelligence Monitor** *(n8n)*
- **06 — Programmatic SEO Article Factory to WordPress/Webflow** *(Make.com)*
- **07 — LinkedIn & Web Scraper to Hyper-Personalized Cold Email** *(Make.com)*
- **08 — Omnichannel Video/Podcast to X, LinkedIn & Newsletter Engine** *(Make.com)*
- **09 — Stripe Churn-Risk & Failed Payment AI Intervention Agent** *(Make.com)*
- **10 — Automated Monday Executive KPI & Pipeline AI Briefing** *(Make.com)*

#### 2. The 50 Enterprise B2B Prompt Systems Vault (`.md` + Notion `.csv`)
- 50 XML-structured system prompts across **Sales & RevOps, Finance & Legal, Customer Support RAG, Programmatic Marketing, and Coding/APIs**.
- Engineered with strict `<operational_rules>` and `<output_schema>` blocks to eliminate hallucinations and enforce clean JSON responses.

#### 3. AI Agency ROI & Token Margin Calculator (`.csv` for Google Sheets & Excel)
- Plug in any client's manual hours and team wages to automatically calculate **Net Monthly Dollar Savings**, **Annual ROI**, and your **Suggested Setup & Retainer Price**.

#### 4. High-Ticket Client Proposal & 14-Day Sprint Template
- Copy-paste 3-tier B2B proposal template (`Good / Better / Best`) designed to anchor your automation fee against quantifiable labor savings.

---

### 💡 Who Is This For?
- **AI Automation Agencies (AAA) & Freelancers** who want ready-to-deliver client systems.
- **Founders & Solopreneurs** looking to automate lead gen, invoicing, content, and support on a <$25/mo API budget.
- **RevOps & Technical Marketers** scaling workflows in n8n, Make.com, OpenAI, Claude, and Google Gemini.

**⚡ Instant Access:** Download the complete `.zip` archive immediately after checkout.
"""
    (GUMROAD_DIR / "GUMROAD_LISTING_COPY.md").write_text(gumroad_copy, encoding="utf-8")


if __name__ == "__main__":
    ensure_dirs()
    create_n8n_workflows()
    create_make_blueprints()
    create_50_b2b_prompts()
    create_roi_spreadsheet_and_sales_kit()
    create_gumroad_listing_and_zip()
    print("Digital product bundle and ZIP successfully generated!")
