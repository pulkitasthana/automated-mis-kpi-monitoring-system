# Power BI Dashboard Blueprint

## Data model
- `fact_mis`: one row per operational record.
- `dim_kpi_targets`: department KPI target reference.
- `Calendar`: dedicated date table related to `fact_mis[Record_Date]`.

## Page 1 — Management MIS
Cards: Total Sales, Total Profit, Profit Margin %, Total Records, Exception Rate %, SLA Compliance %.
Visuals: Monthly Sales/Profit trend, Department Target vs Actual, Department summary matrix, Exception mix, slicers for Date/Department/Region/Channel.

## Page 2 — Department Performance
Cards: Avg KPI Actual, Avg KPI Target, Target Achievement %, Avg TAT Hours.
Visuals: department comparison, monthly KPI trend, regional performance, top/bottom categories.

## Page 3 — SLA / TAT Monitoring
Cards: SLA Compliance %, SLA Breaches, Avg TAT Hours.
Visuals: TAT by department, monthly breach trend, SLA breach by region/channel, breach detail table.

## Page 4 — Exception Monitoring
Cards: Exceptions, KPI Below Target, Missing Data, Duplicates, Volume Anomalies.
Visuals: exception trend, exception type by department, exception detail table, record-level drill-through.

## Recommended interactions
- Date slicer filters all pages.
- Department/Region/Channel slicers should cross-filter all relevant visuals.
- Exception detail page should be filterable by Status and Exception Type.
- Keep KPI cards as measures, not raw columns.
