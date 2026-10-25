# Setup Guide

## 1. SQL Server

Create or select the database:

`MIS_KPI_Monitoring`

Run:

`sql/01_create_schema.sql`

This creates/updates:

- `dbo.MIS_KPI_Fact`
- `dbo.MIS_KPI_Staging`
- `dbo.vw_MIS_KPI_Monthly`

## 2. Python

From the project root:

```powershell
pip install -r python/requirements.txt
python python/etl_pipeline.py
```

The ETL expects SQL Server to be available at `localhost` by default and uses Windows Authentication.

Environment variables can override the defaults. See `config/.env.example`.

## 3. Validation

Run:

`sql/03_validation_queries.sql`

Confirm that `dbo.MIS_KPI_Fact` contains the expected rows and that `dbo.vw_MIS_KPI_Monthly` returns the management-level aggregation.

## 4. Power BI

Open:

`Automated_MIS_KPI_Monitoring_System.pbix`

For the SQL Server connection, use:

- Server: `localhost`
- Database: `MIS_KPI_Monitoring`
- Main reporting object: `dbo.vw_MIS_KPI_Monthly`
- Detailed object: `dbo.MIS_KPI_Fact`

If the SQL Server instance is not running when the PBIX is opened or refreshed, the SQL data source will not be available.

## 5. Regenerating Sample Inputs

`python/regenerate_inputs.py` can be used when additional demonstration months are required. Any generated data remains synthetic sample data and should be labelled accordingly.
