# Automated MIS & KPI Monitoring System

A portfolio project that demonstrates an end-to-end MIS/KPI reporting pipeline using **Python, SQL Server, and Power BI**.

> **Data note:** The included July–September 2026 MIS records are synthetic/generated sample data created for demonstrating the workflow. They are not real company performance data.

## 1. Project Objective

Build a repeatable MIS workflow that takes monthly Excel operational inputs, validates and loads them into SQL Server, exposes management-ready KPI aggregations through a SQL view, and connects those outputs to a Power BI dashboard.

The project is designed to demonstrate practical skills in:

- Excel-based MIS input handling
- Python ETL and data validation
- SQL Server staging and fact-table design
- KPI aggregation and reporting views
- Power BI dashboard development
- Basic data-quality and reconciliation checks

## 2. Architecture

```text
Monthly Excel MIS Files
        |
        v
Python ETL + Validation
        |
        v
SQL Server
  |-- MIS_KPI_Staging
  |-- MIS_KPI_Fact
  `-- vw_MIS_KPI_Monthly
        |
        v
Power BI Desktop
        |
        v
4-page MIS & KPI Dashboard
```

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Input | Microsoft Excel (.xlsx) |
| ETL | Python 3.13.15, pandas, SQLAlchemy, pyodbc, openpyxl |
| Database | SQL Server 2025 Developer, database `MIS_KPI_Monitoring` |
| Query/Validation | T-SQL / SQL Server Management Studio |
| BI | Power BI Desktop |
| Authentication | Windows Authentication by default |

## 4. Input Data

The project contains three monthly sample files:

- `input_data/MIS_Input_2026-07.xlsx`
- `input_data/MIS_Input_2026-08.xlsx`
- `input_data/MIS_Input_2026-09.xlsx`

Required columns:

`Month`, `Region`, `Department`, `Employee`, `Process`, `Revenue`, `Tickets_Closed`, `Escalations`, `SLA_Percent`, `Quality_Percent`

## 5. Python ETL Workflow

`python/etl_pipeline.py` performs the following steps:

1. Discovers all `MIS_Input_*.xlsx` files in `input_data/`.
2. Checks that all required columns exist.
3. Converts the month to a date and KPI fields to numeric values.
4. Rejects blank/invalid values.
5. Rejects negative ticket/escalation counts.
6. Validates SLA and Quality percentages are between 0 and 100.
7. Combines the monthly files and removes duplicate rows.
8. Truncates and reloads `dbo.MIS_KPI_Staging`.
9. Merges staging records into `dbo.MIS_KPI_Fact` using the business-key combination of month, region, department, employee and process.

The verified run processed **15 rows successfully**.

## 6. SQL Server Layer

Database:

`MIS_KPI_Monitoring`

### `dbo.MIS_KPI_Staging`

Temporary landing table used by the ETL process before the records are merged into the fact table.

### `dbo.MIS_KPI_Fact`

Persistent operational fact table containing:

- MonthDate
- Region
- Department
- Employee
- Process
- Revenue
- Tickets_Closed
- Escalations
- SLA_Percent
- Quality_Percent
- LoadedAt

### `dbo.vw_MIS_KPI_Monthly`

Management reporting view grouped by `MonthDate`, `Region`, and `Department`.

It exposes:

- Total Revenue
- Tickets Closed
- Escalations
- Average SLA %
- Average Quality %
- Escalation Rate %

Escalation Rate is calculated as:

`Escalations / Tickets Closed × 100`

with a zero-ticket safeguard.

## 7. Verified Sample Results

For the included synthetic July–September 2026 sample:

| KPI | Result |
|---|---:|
| Rows processed by ETL | 15 |
| Total Revenue | 632,000 |
| Tickets Closed | 613 |
| Escalations | 41 |
| Average SLA % across the 15 grouped records | 96.51% |

These values describe the included demonstration data only and should not be interpreted as real business performance.

## 8. Power BI Dashboard

The PBIX file is included at the project root:

`Automated_MIS_KPI_Monitoring_System.pbix`

The report contains four analytical pages:

### Page 1 — Executive MIS Overview

Executive KPI cards and high-level views for:

- Total Revenue
- Tickets Closed
- Escalations
- Average SLA %
- Revenue by Department
- Monthly Revenue Trend
- Escalation Rate by Department
- Tickets Closed by Department
- Average SLA % by Department

### Page 2 — Regional & Department Performance

Compares performance across regions and departments using revenue, tickets, escalation rate, SLA and matrix-based analysis.

### Page 3 — KPI & Service Quality

Focuses on SLA, quality, escalation trends and department-level KPI monitoring.

### Page 4 — Detailed MIS Monitoring

Provides row-level MIS analysis with employee, process, region, department and month filtering.

## 9. Setup & Run

### Prerequisites

- Python 3.13.x
- SQL Server 2025 Developer or compatible SQL Server instance
- SQL Server Management Studio
- ODBC Driver 18 for SQL Server
- Power BI Desktop

### Install Python dependencies

```powershell
pip install -r python/requirements.txt
```

### Create the database objects

Open SSMS, create/select the `MIS_KPI_Monitoring` database and run:

```text
sql/01_create_schema.sql
```

### Run the ETL

From the project root:

```powershell
python python/etl_pipeline.py
```

### Validate the load

Run:

```text
sql/03_validation_queries.sql
```

### Connect Power BI

In Power BI Desktop:

`Home → Get Data → SQL Server`

Server:

`localhost`

Database:

`MIS_KPI_Monitoring`

Use `dbo.vw_MIS_KPI_Monthly` for the management-level report and `dbo.MIS_KPI_Fact` for detailed analysis.

See `docs/POWER_BI_CONNECTION.md` for the connection notes.

## 10. Folder Structure

```text
Project_3_Automated_MIS_KPI_Monitoring_System_UPDATED/
├── Automated_MIS_KPI_Monitoring_System.pbix
├── config/
│   └── .env.example
├── docs/
│   ├── POWER_BI_CONNECTION.md
│   ├── PROJECT_DOCUMENTATION.md
│   └── SETUP_GUIDE.md
├── input_data/
│   ├── MIS_Input_2026-07.xlsx
│   ├── MIS_Input_2026-08.xlsx
│   └── MIS_Input_2026-09.xlsx
├── python/
│   ├── etl_pipeline.py
│   ├── regenerate_inputs.py
│   └── requirements.txt
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_merge_staging.sql
│   └── 03_validation_queries.sql
├── README.md
└── VERIFY.txt
```

## 11. Portfolio Talking Points

This project can be discussed in interviews as an end-to-end MIS automation example:

- Built a Python ETL pipeline to process recurring Excel MIS files.
- Added programmatic data-quality validation before database loading.
- Used SQL Server staging and fact tables with a reporting view for KPI consumption.
- Connected Power BI directly to SQL Server for management reporting.
- Designed a four-page dashboard covering executive KPIs, regional/department performance, service quality and detailed MIS monitoring.
- Implemented a repeatable workflow rather than manually consolidating monthly Excel reports.

## 12. Limitations

- The included records are synthetic demonstration data.
- The sample covers only July–September 2026.
- The dashboard demonstrates the workflow but does not represent a real organization's SLA, quality or revenue performance.
- The current SQL reporting view uses simple averages for SLA and Quality at the grouped-record level; it is not a ticket-weighted SLA calculation.
- No production scheduler/orchestrator is included; the ETL is executed manually from Python.

## 13. Project Status

**Core project: Complete.**

The repository/package contains the source data, Python ETL, SQL objects/scripts, Power BI report, connection documentation and validation materials required to reproduce the demonstrated workflow.
