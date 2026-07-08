# Customer Support Operations Intelligence Platform

An enterprise-grade operations intelligence data platform designed to help support managers and customer experience (CX) leaders make data-driven staffing and operational decisions.

---

## 🚀 Project Overview

The platform ingests customer support ticket data, transforms and models it through a structured data warehouse schema (staging → intermediate → marts), and exposes insights through SQL analysis and business intelligence reporting. 

Starting in later phases, the platform adds predictive analytics (escalation risk, priority classification, sentiment analysis) and workload/volume forecasting (using statsmodels/Prophet) to anticipate SLA breaches and recommend optimal agent allocations.

This project is built to demonstrate analytics engineering, database design, and pipeline orchestration practices consistent with how real software organizations build internal operations intelligence platforms.

---

## 🛠️ Technology Stack

- **Database / Warehouse:** PostgreSQL 18
- **Data Transformation:** dbt (Data Build Tool)
- **Ingestion & Data Science:** Python (Pandas, Polars, Scikit-Learn, Statsmodels, Prophet)
- **Containerization:** Docker Compose
- **Orchestration / Devops:** Makefile & CLI Scripts

---

## 📁 Repository Structure

```text
support-ops-intelligence-platform/
├── README.md
├── docker-compose.yml
├── Makefile
├── .env.example
├── requirements.txt
│
├── data_generator/                 # Phase 1: Synthetic data generator
│   ├── config/correlations.yaml
│   ├── generators/                 # Custom generator modules
│   └── main.py
│
├── ingestion/                      # Ingestion pipeline scripts
│   ├── load_raw.py
│   └── data_quality_checks.py
│
├── warehouse/                      # dbt Project
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   └── tests/
│
├── ml/                             # Phase 3: ML & Forecasting
│   ├── features/
│   ├── models/
│   └── evaluation/
│
├── analysis/sql/                   # Analytical queries for PRD business questions
│
├── dashboards/                     # BI Dashboards & screenshots
│
├── docs/                           # Documentation and Design Decisions (ADRs)
│   ├── PRD.md
│   └── design_decisions.md
│
└── tests/                          # Integration & verification tests
```

---

## ⚙️ Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.11+
- Docker and Docker Compose
- `make` (optional, for easier workflow commands)

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Michael-web698/Customer-support-operations-intelligence-platform
   cd Customer-support-operations-intelligence-platform
   ```

2. **Initialize Environment Variables:**
   Copy the example environment file and customize if necessary:
   ```bash
   cp .env.example .env
   ```

3. **Start the Database:**
   Spin up the PostgreSQL container using the Makefile:
   ```bash
   make db-up
   ```
   *This will start the database and wait until it is fully healthy and accepting connections.*

4. **Install Python Environment:**
   Initialize the virtual environment and install the required libraries:
   ```bash
   make install
   ```
   *Remember to activate the virtual environment:*
   ```bash
   source venv/bin/activate
   ```

### Makefile Commands

- `make db-up` - Spin up the database container.
- `make db-down` - Terminate the database container.
- `make db-status` - Check the database container's health.
- `make db-shell` - Open an interactive `psql` session inside the database.
- `make db-clean` - Stop database container and wipe database volumes.
- `make clean` - Remove python cache files and virtual environment.

---

## 📄 Documentation

- Refer to the full [Product Requirements Document (PRD)](file:///Users/joseph/Customer Support Operations Intelligence Platform/Customer-support-operations-intelligence-platform/docs/PRD.md) for data architectures, schema tables, goals, and business questions.
- Design decisions and logic variations will be tracked in `docs/design_decisions.md`.
