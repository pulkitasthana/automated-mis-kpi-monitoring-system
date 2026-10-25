# Project Documentation — Automated MIS & KPI Monitoring System

## Purpose

This project demonstrates how a recurring Excel-based MIS process can be converted into a structured reporting pipeline using Python, SQL Server and Power BI.

## Business Workflow

```text
Monthly MIS Excel Inputs
        ↓
Data Validation
        ↓
SQL Server Staging
        ↓
Fact Table / Upsert
        ↓
KPI Reporting View
        ↓
Power BI
        ↓
Management Dashboard
```

## Data Contract

Each monthly workbook is expected to contain these fields:

- Month
- Region
- Department
- Employee
- Process
- Revenue
- Tickets_Closed
- Escalations
- SLA_Percent
- Quality_Percent

The Python validation layer checks column presence, numeric conversion, missing values, non-negative counts and percentage ranges.

## Database Design

### Staging

`dbo.MIS_KPI_Staging` is the landing layer populated by Python before the merge operation.

### Fact

`dbo.MIS_KPI_Fact` stores the persistent operational records. `KPI_ID` is the identity primary key and `LoadedAt` records the load timestamp.

### Reporting View

`dbo.vw_MIS_KPI_Monthly` groups the fact data by month, region and department and calculates management KPIs.

## ETL Logic

The ETL reads every file matching `MIS_Input_*.xlsx`, validates each file, concatenates the records, removes exact duplicates, loads staging and merges into the fact table.

The merge key is:

`MonthDate + Region + Department + Employee + Process`

Existing records are updated and new records are inserted.

## Dashboard Design

### Page 1 — Executive MIS Overview

Purpose: high-level management snapshot.

### Page 2 — Regional & Department Performance

Purpose: compare revenue and operational KPIs across regions and departments.

### Page 3 — KPI & Service Quality

Purpose: monitor SLA, quality and escalation behaviour.

### Page 4 — Detailed MIS Monitoring

Purpose: provide employee/process-level operational detail with filtering.

## Validation Evidence

The demonstrated ETL run completed successfully with 15 processed rows. SQL validation returned the loaded fact records and the monthly reporting view returned 15 grouped records for July–September 2026.

For the included synthetic sample, the resulting totals are:

- Revenue: 632,000
- Tickets Closed: 613
- Escalations: 41
- Average SLA across the 15 grouped records: 96.51%

## Reproducibility

1. Install the required Python packages.
2. Ensure SQL Server and ODBC Driver 18 are available.
3. Create the database objects using the schema script.
4. Run the ETL from the project root.
5. Run the SQL validation queries.
6. Open the PBIX file and refresh the SQL data source if required.

## Interpretation Rules

The included metrics are examples for a synthetic MIS environment. They should not be presented as real organizational results. KPI relationships should be described as observations from the sample data rather than causal findings.
