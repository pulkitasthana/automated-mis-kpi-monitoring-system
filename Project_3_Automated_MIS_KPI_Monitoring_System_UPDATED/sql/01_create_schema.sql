USE [MIS_KPI_Monitoring];
GO
IF OBJECT_ID('dbo.MIS_KPI_Fact','U') IS NULL
BEGIN
CREATE TABLE dbo.MIS_KPI_Fact (
 KPI_ID INT IDENTITY(1,1) PRIMARY KEY,
 MonthDate DATE NOT NULL,
 Region NVARCHAR(100) NOT NULL,
 Department NVARCHAR(100) NOT NULL,
 Employee NVARCHAR(150) NOT NULL,
 Process NVARCHAR(150) NOT NULL,
 Revenue DECIMAL(18,2) NOT NULL,
 Tickets_Closed INT NOT NULL,
 Escalations INT NOT NULL,
 SLA_Percent DECIMAL(6,2) NOT NULL,
 Quality_Percent DECIMAL(6,2) NOT NULL,
 LoadedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
END
GO
IF OBJECT_ID('dbo.MIS_KPI_Staging','U') IS NULL
BEGIN
CREATE TABLE dbo.MIS_KPI_Staging (
 MonthDate DATE, Region NVARCHAR(100), Department NVARCHAR(100), Employee NVARCHAR(150),
 Process NVARCHAR(150), Revenue DECIMAL(18,2), Tickets_Closed INT, Escalations INT,
 SLA_Percent DECIMAL(6,2), Quality_Percent DECIMAL(6,2)
);
END
GO
CREATE OR ALTER VIEW dbo.vw_MIS_KPI_Monthly AS
SELECT MonthDate, Region, Department,
 SUM(Revenue) AS Total_Revenue,
 SUM(Tickets_Closed) AS Tickets_Closed,
 SUM(Escalations) AS Escalations,
 CAST(AVG(SLA_Percent) AS DECIMAL(6,2)) AS Avg_SLA_Percent,
 CAST(AVG(Quality_Percent) AS DECIMAL(6,2)) AS Avg_Quality_Percent,
 CAST(CASE WHEN SUM(Tickets_Closed)=0 THEN 0 ELSE 100.0*SUM(Escalations)/SUM(Tickets_Closed) END AS DECIMAL(6,2)) AS Escalation_Rate_Percent
FROM dbo.MIS_KPI_Fact
GROUP BY MonthDate, Region, Department;
GO
