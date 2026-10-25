USE AutomatedMIS;
GO

-- Management KPI summary
SELECT
    Department,
    COUNT(*) AS Records,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    AVG(KPI_Actual) AS Avg_KPI_Actual,
    AVG(KPI_Target) AS Avg_KPI_Target,
    100.0 * SUM(CASE WHEN SLA_Breach = 'No' THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0) AS SLA_Compliance_Pct,
    100.0 * SUM(CASE WHEN Status = 'Exception' THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0) AS Exception_Rate_Pct
FROM fact_mis
GROUP BY Department
ORDER BY Exception_Rate_Pct DESC;

-- Monthly trend
SELECT
    YEAR(Record_Date) AS Report_Year,
    MONTH(Record_Date) AS Report_Month,
    SUM(Sales) AS Sales,
    SUM(Profit) AS Profit,
    COUNT(*) AS Records,
    SUM(CASE WHEN SLA_Breach='Yes' THEN 1 ELSE 0 END) AS SLA_Breaches,
    SUM(CASE WHEN Status='Exception' THEN 1 ELSE 0 END) AS Exceptions
FROM fact_mis
GROUP BY YEAR(Record_Date), MONTH(Record_Date)
ORDER BY Report_Year, Report_Month;

-- Exception monitoring
SELECT
    Department,
    Exception_Type,
    COUNT(*) AS Exception_Count
FROM fact_mis
WHERE Status = 'Exception'
GROUP BY Department, Exception_Type
ORDER BY Exception_Count DESC;

-- Record-level data-quality checks
SELECT Record_ID, Record_Date, Department, Status, Exception_Type
FROM fact_mis
WHERE Missing_Data_Flag='Yes'
   OR Duplicate_Flag='Yes'
   OR Volume_Anomaly_Flag='Yes'
   OR SLA_Breach='Yes'
   OR KPI_Below_Target='Yes'
ORDER BY Record_Date DESC;
