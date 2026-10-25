# Project 3 status

## Completed in this package
- 24 monthly Excel input files preserved.
- Python validation/build pipeline added.
- Data-quality checks added: duplicate IDs, missing required fields, profit reconciliation, SLA flag reconciliation, KPI flag reconciliation.
- Management, monthly, department and exception output datasets generated under `outputs/`.
- SQL schema plus analytical queries added.
- Power Query folder-ingestion query hardened for recurring Excel files.
- Power BI DAX measure pack expanded.
- Dashboard blueprint and KPI definitions documented.
- Public UCI Online Retail source and licensing boundary documented.

## Validation result for current inputs
- 24 files
- 3,780 records
- 0 duplicate Record_ID rows
- 0 missing required fields
- 0 profit calculation mismatches
- 0 SLA flag mismatches
- 0 KPI flag mismatches
- 3,143 exception records (83.15%)

## Remaining manual step
A `.pbix` file is not generated here because Power BI Desktop's report canvas/model is a desktop application artifact. The package contains the DAX measures, Power Query M, model assumptions and exact dashboard blueprint needed to build the report in Power BI Desktop.
