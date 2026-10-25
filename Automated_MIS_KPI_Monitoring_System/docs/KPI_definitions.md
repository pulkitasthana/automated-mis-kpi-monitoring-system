# KPI and control definitions

| KPI / Control | Definition | Interpretation |
|---|---|---|
| Total Sales | Sum of Sales | Revenue volume in the operational simulation |
| Total Profit | Sum of Profit | Sales minus recorded Cost |
| Profit Margin % | Profit / Sales | Profitability ratio |
| SLA Compliance % | 1 - SLA breaches / records | Share of records within SLA |
| Avg TAT Hours | Average TAT_Hours | Average turnaround time |
| Target Achievement % | Avg KPI Actual / Avg KPI Target | Actual performance relative to target |
| Exception Rate % | Exception records / total records | Share requiring attention |
| Missing Data | Records with Missing_Data_Flag = Yes | Data-quality issue |
| Duplicate Records | Records with Duplicate_Flag = Yes | Duplicate-key issue |
| Volume Anomalies | Records with Volume_Anomaly_Flag = Yes | Unusual volume movement |

## Exception categories
- KPI below target
- SLA breach
- Missing data
- Duplicate record
- Volume anomaly

## Important limitation
The SLA, TAT, KPI target and exception fields are portfolio simulation controls, not fields from the public UCI dataset.
