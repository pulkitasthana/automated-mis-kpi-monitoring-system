# Automated MIS & KPI Monitoring System

## Final architecture

**Excel Raw Files → Python ETL & Validation → SQL Database → Power BI MIS Dashboard**

### Python role
- Reads all `.xlsx` files from `data/monthly_inputs/`
- Consolidates department/monthly files
- Checks required columns, missing values and duplicates
- Validates numeric fields
- Reconciles `Sales - Cost = Profit`
- Validates SLA breach and KPI-below-target flags
- Cleans and standardizes the validated dataset
- Loads the result into SQL-compatible tables
- Writes a validation report

### Local database
The included `python/etl_pipeline.py` uses SQLite for local verification so the complete pipeline can run without a SQL Server installation. The resulting database contains:
- `fact_mis`
- `department_kpi_summary`
- `mis_exceptions`

For a production-style deployment, replace the SQLite load function with SQL Server/ODBC connection details and point Power BI to the SQL Server database.

### Run
From the project root:

```bash
pip install pandas openpyxl
python python/etl_pipeline.py
```

The input Excel files are synthetic operational data used to simulate a real MIS process; they are not claimed to be data from a real company.
