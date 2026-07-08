# Customer Support Operations Intelligence Platform
## Product Requirements Document (PRD) — v1.0 (Source of Truth)

**Status:** Finalized — architectural baseline. Changes after this point require explicit re-approval, not incremental drift.

---

## 1. Project Overview

The Customer Support Operations Intelligence Platform is a data platform that helps customer support managers and operations leaders make better operational decisions using data — not a customer support chatbot, and not an AI-first product.

The platform ingests customer support ticket data, models it through a proper data warehouse (staging → intermediate → marts), and surfaces insight through SQL analysis, BI dashboards, and — starting at v1.5 — predictive analytics and forecasting. AI/ML is used only where it demonstrably creates business value on top of a solid analytics foundation, never as the centerpiece of the project.

This project is built to demonstrate the skill set of a **Data Analyst / Business Intelligence Analyst / Operations Analyst**, using engineering practices (data modeling, testing, documentation, layered pipelines) consistent with how a real software company would build an internal operations intelligence tool.

---

## 2. Business Problem

Customer support organizations generate large volumes of operational data (tickets, agent activity, SLAs, escalations, customer feedback) but frequently lack the analytics infrastructure to answer basic operational questions reliably:

- Support managers can't easily see which issue categories are driving volume or escalations.
- Workload is distributed unevenly across agents with no visibility into capacity vs. load.
- SLA breaches are discovered reactively instead of anticipated.
- Root causes of poor customer satisfaction are anecdotal, not data-driven.
- Leadership lacks a single, trustworthy view of support performance.

This platform solves that by building the underlying data infrastructure and analytics layer that a real support operations team would need — the same problem BI/Analytics/Ops teams solve at any company with a support function.

---

## 3. Goals

1. Build a defensible, well-modeled data warehouse for customer support operations.
2. Answer the core operational business questions directly and reliably using SQL/BI — no ML dependency for core reporting.
3. Demonstrate correct use of dbt, star schema modeling, and layered pipeline architecture.
4. Add predictive analytics (classification, sentiment, escalation risk, forecasting) only where it creates clear, explainable business value.
5. Demonstrate awareness of production-grade patterns (human-in-the-loop governance, decision support) without over-building them into a second product.
6. Produce a portfolio artifact that reads as an internal enterprise data platform, not a tutorial project.

---

## 4. Users (Personas)

| Persona | Needs |
|---|---|
| **Support Operations Manager** | Daily/weekly view of volume, backlog, SLA compliance, agent workload; wants to know where to intervene today. |
| **Team Lead / Shift Supervisor** | Agent-level workload and capacity visibility; needs to rebalance queues in real time. |
| **CX / Support Director (Executive)** | High-level KPIs, trends, forecasted risk; needs a trustworthy single source of truth for reporting upward. |
| **Data/Analytics Engineer (secondary persona: you, the builder)** | Needs the platform to be maintainable, tested, and documented — the "user" of the codebase itself. |

---

## 5. Success Metrics

Since this is a portfolio project rather than a live production system, success is measured by **capability and rigor demonstrated**, not live business KPIs:

- All 10 core business questions (Section 7) are answerable directly from the marts layer via documented SQL, with no manual data manipulation.
- dbt project has staging/intermediate/marts layering with test coverage (`not_null`, `unique`, relationship tests) on all key/foreign-key columns.
- Dashboards load from marts only — no dashboard-side business logic.
- Synthetic data exhibits realistic, intentional correlations (validated via `tests/test_generator.py` distribution checks), not pure randomness.
- v1.5 ML models report standard, appropriate evaluation metrics (precision/recall/AUC for classification; MAPE/MAE with walk-forward validation for forecasting) — not just "it works."
- Every major design decision is documented in `docs/design_decisions.md` with rationale, not just implemented silently.

---

## 6. Business Questions (Core Requirements)

The platform must be able to answer, at minimum:

1. Which ticket categories are driving the most support volume?
2. Which issues create the highest escalation risk?
3. Which agents are overloaded, and who has capacity?
4. Which categories take the longest to resolve?
5. How should work be distributed among agents?
6. How can response times and SLA compliance be improved?
7. Which agents are handling the most escalations?
8. How can we balance workload better?
9. What root causes are hurting customer satisfaction?
10. How can leadership monitor support performance over time (trend + forecast)?

---

## 7. Final Module List

### V1 — Operations Intelligence Platform (core; zero ML dependency)
| Module | Description |
|---|---|
| Data Foundation | Synthetic data generator, ingestion, PostgreSQL warehouse, dbt project, star schema |
| Ticket Category Analytics | SQL/BI analysis of volume, escalation rate, and resolution time by category, using ground-truth labels |
| Workforce Operations Analytics | Agent load, capacity, utilization, idle time — answers "who is overloaded / who has capacity" |
| Daily Ticket Volume Aggregation | Dedicated mart aggregating tickets by date/category; feeds both v1 dashboards and v1.5 forecasting |
| Operational Reporting | Delivered via dbt docs + documented analytical SQL against marts — not a separate build |
| Executive Dashboard (Basic) | Volume, resolution time, first response time, SLA compliance, escalation rate, CSAT, agent utilization, backlog, category/root-cause breakdown |

### V1.5 — Predictive & Forecasting Analytics
| Module | Description |
|---|---|
| Ticket Auto-Classification | ML: predict category from ticket text |
| Priority Prediction | ML: predict priority from ticket text/category |
| Sentiment Analysis | ML: sentiment label + score from ticket text |
| Escalation Risk Prediction | ML: probability of escalation from ticket/customer/agent features |
| **Forecasting Analytics** | Time-series forecast of ticket volume (Holt-Winters primary, Prophet evaluated as alternative); derived staffing requirement and expected SLA breaches computed from forecasted volume + historical operational ratios |
| Executive Dashboard (Predictive KPIs) | Adds predicted escalations, forecasted volume, staffing forecast, expected SLA breaches on top of the basic dashboard |

### V2 — AI Decision Support (optional stretch, explicitly scoped down from original vision)
| Module | Description |
|---|---|
| Similar Ticket Retrieval | Embedding-based similarity search over resolved tickets — no fabricated knowledge base, no RAG generation step |
| Knowledge Intelligence / Continuous Learning | Documented production pattern + small demo (e.g., resolved-ticket root-cause tagging feeding future matching) |
| Decision Support Recommendations | Rule-based agent assignment logic (expertise + lowest load + SLA target), optionally informed by v1.5 escalation risk scores |
| Human Review & Governance | Architectural pattern: ML outputs stored as suggestions only, never auto-applied; optional minimal Streamlit approve/reject demo |

**Design principle preserved throughout:** every module in the original long-term vision is retained — none deleted — but re-sequenced so the platform is analytics-first and defensible at every stage, with AI-adjacent scope (RAG, workflow engines) explicitly bounded and optional.

---

## 8. Final Phase Roadmap

| Phase | Deliverables |
|---|---|
| **Phase 0 — Project Setup** | Repo scaffold, Docker Compose (Postgres), README skeleton, environment config |
| **Phase 1 — Data Foundation** | Synthetic data generator (with parameterized correlation config), ingestion scripts, data quality checks, dbt project init, star schema (dims + facts) |
| **Phase 2 — Operational Analytics** | Ticket Category Analytics, Workforce Operations Analytics, Daily Ticket Volume mart, documented analytical SQL answering all 10 business questions, Basic Executive Dashboard |
| **Phase 3 — Predictive & Forecasting Analytics** | Ticket Auto-Classification, Priority Prediction, Sentiment Analysis, Escalation Risk Prediction, Forecasting Analytics (volume/staffing/SLA breach), Predictive KPI dashboard enhancements |
| **Phase 4 — AI Decision Support** | Similar Ticket Retrieval, rule-based Decision Support Recommendations, Human Review & Governance pattern (+ optional demo) |
| **Phase 5 — Continuous Improvement & Polish** | Knowledge Management/continuous learning loop, dashboard refinement, documentation finalization, architecture diagram polish |

---

## 9. Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Database / Warehouse | PostgreSQL | Real SQL surface (window functions, CTEs, indexing) vs. SQLite's limitations |
| Transformation | dbt | Industry-standard analytics engineering layer; testing, documentation, lineage built in |
| Ingestion / Scripting / ML | Python | pandas/polars for data work, scikit-learn for ML, statsmodels/Prophet for forecasting |
| BI / Dashboards | Power BI / Tableau | Recognized BI tooling for Analyst-track hiring; connects directly to marts schema |
| Orchestration | Makefile / CLI scripts (no Airflow/Dagster in v1) | Dataset scale doesn't warrant an orchestrator; explicitly deferred to Future Roadmap to show deliberate scoping, not a gap in knowledge |
| Optional serving layer (v2) | FastAPI | Only if demonstrating "AI as a service" pattern for prediction scores |
| Optional decision-support demo (v2) | Streamlit | Minimal human-review demo only, not a full application |
| Containerization | Docker Compose | Reproducible local environment (Postgres + optional pgAdmin) |

---

## 10. Data Architecture

```
[Python Data Generator] — parameterized, correlated, seasonal synthetic data
        ↓
   raw CSV/Parquet ("source system export" simulation)
        ↓
[Python Ingestion] → Postgres schema: raw
        ↓
[dbt staging] — 1:1 with raw, typed/cleaned/renamed, no business logic
        ↓
[dbt intermediate] — business logic: SLA breach flags, escalation flags,
                      agent daily load calculations, derived joins
        ↓
[dbt marts] — final star schema: dim_*, fact_* tables, tested & documented
        ↓
        ├──→ Power BI / Tableau (direct connection to marts)
        │
        └──→ Python ML/forecasting (v1.5) → schema: predictions
                      ↓
              joins back to marts for BI consumption
              (optional FastAPI serving layer, v2)
```

**Layering rationale:** each layer has one responsibility (staging = cleaning, intermediate = business logic, marts = consumption-ready), so when a number looks wrong, the layer responsible is immediately identifiable. ML and forecasting are downstream consumers of the marts layer, writing to their own `predictions` schema — never mutating operational fact tables directly, preserving the human-in-the-loop governance principle from Module list Section 7 (V2).

**Synthetic data must encode deliberate, documented correlations**, including:
- Category → escalation rate and resolution time
- Agent seniority → resolution speed and reopen rate
- Agent load → response time and CSAT degradation (models the "overload" business question)
- Priority → SLA target, with breach probability rising under agent overload
- Customer segment → routing speed and complexity
- CSAT as a function of resolution time, escalation occurrence, and reopens (not independent noise)
- Time seasonality (weekday/weekend, post-holiday spikes) — required input for the forecasting module

All correlation strengths live in a version-controlled config file (`data_generator/config/correlations.yaml`), not hardcoded, so assumptions are inspectable and tunable.

---

## 11. Database Design

**Modeling pattern:** Kimball star schema, with an **accumulating snapshot fact** for ticket lifecycle plus a **transaction fact** for discrete status-change events — two grains for two distinct classes of question.

### Dimensions
| Table | Grain | Key attributes |
|---|---|---|
| `dim_date` | 1 row/day | day, week, month, quarter, is_weekend, fiscal_period |
| `dim_customer` | 1 row/customer | segment (Free/Pro/Enterprise), region, signup_date, plan_tier |
| `dim_agent` | 1 row/agent | name, team, seniority_level, hire_date, shift, employment_status |
| `dim_category` | 1 row/category | category_name, parent_category, default_complexity_score |
| `dim_sla_policy` | 1 row/(priority × category) | target_response_minutes, target_resolution_minutes |
| `dim_channel` | 1 row/channel | email, chat, phone, social |

### Facts
| Table | Grain | Key measures |
|---|---|---|
| `fact_ticket` (accumulating snapshot) | 1 row/ticket | created_at, first_response_at, escalated_at, resolved_at, closed_at, priority, csat_score, reopened_count, sla_response_breached, sla_resolution_breached |
| `fact_ticket_event` (transaction fact) | 1 row/status-change event | ticket_id, event_type, event_timestamp, from_agent_id, to_agent_id, from_status, to_status |
| `fact_agent_daily_capacity` | 1 row/agent/day | scheduled_hours, tickets_open_at_start_of_day, tickets_assigned_that_day — required to distinguish "busy" from "under-resourced" |
| `fact_daily_ticket_volume` | 1 row/date × category | ticket_count — dedicated aggregation feeding dashboard trend charts and v1.5 forecasting |

### Predictions schema (v1.5+, separate from marts)
| Table | Grain | Notes |
|---|---|---|
| `predictions.ticket_scores` | 1 row/ticket | predicted_category, predicted_priority, sentiment_label, sentiment_score, escalation_probability — written by ML, never overwrites ground truth |
| `predictions.volume_forecast` | 1 row/date | forecasted_ticket_count, forecasted_staffing_requirement, expected_sla_breaches |

Free-text fields (`subject`, `description`) are included on tickets from the start (template-generated, sentiment-varied by category) to support v1.5 NLP without retrofitting.

---

## 12. Repository Structure

```
support-ops-intelligence-platform/
├── README.md
├── docker-compose.yml
├── Makefile
├── .env.example
│
├── data_generator/
│   ├── config/correlations.yaml
│   ├── generators/{customers,agents,tickets,text_templates}.py
│   ├── main.py
│   └── output/
│
├── ingestion/
│   ├── load_raw.py
│   └── data_quality_checks.py
│
├── warehouse/                      # dbt project
│   ├── dbt_project.yml
│   ├── models/{staging,intermediate,marts}/
│   ├── tests/
│   └── docs/
│
├── ml/
│   ├── features/build_features.py
│   ├── models/{train_escalation_model,train_priority_model,sentiment_scoring,forecast_volume}.py
│   ├── evaluation/model_metrics.py
│   └── serving/app.py              # v2, optional
│
├── analysis/sql/                   # documented ad-hoc SQL answering the 10 business questions
│
├── dashboards/{powerbi|tableau}/
│   └── screenshots/
│
├── docs/
│   ├── architecture_diagram.png
│   ├── data_dictionary.md
│   └── design_decisions.md         # ADR-style rationale log
│
└── tests/
    ├── test_generator.py
    └── test_dbt_models.py
```

---

## 13. Future Roadmap (explicitly out of scope, documented for credibility)

Items deliberately excluded from v1/v1.5/v2, noted to show scope was a decision, not a gap:

- **Orchestration (Airflow/Dagster):** unnecessary at this data scale; would be adopted if scheduling/dependency complexity grew.
- **Full RAG/generative knowledge assistant:** rejected as out-of-positioning for an analytics-first platform; scoped down to similarity retrieval only (V2).
- **Full human-review workflow application:** a real approve/modify/reject system would be a separate full-stack product; only the architectural pattern + optional minimal demo is in scope.
- **Real-time/streaming ingestion:** current design is batch-oriented, appropriate for the data volume and reporting cadence; would be revisited if sub-hourly latency became a requirement.
- **Multi-tenant / multi-org support:** single support-org design is sufficient for the platform's purpose.
- **Cloud deployment:** local Docker Compose is sufficient for a portfolio demo; cloud deployment (AWS/GCP/Azure) noted as a possible infrastructure extension.

---

## Change Control

This document is the project's source of truth as of finalization. Any change to module scope, phase sequencing, database design, or technology stack after implementation begins should be treated as a deliberate architectural decision, recorded in `docs/design_decisions.md`, not an ad-hoc deviation.
