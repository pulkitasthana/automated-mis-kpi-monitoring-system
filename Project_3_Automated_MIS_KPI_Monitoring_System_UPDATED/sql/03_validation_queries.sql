USE [MIS_KPI_Monitoring];
GO
SELECT COUNT(*) AS Total_Rows FROM dbo.MIS_KPI_Fact;
SELECT * FROM dbo.vw_MIS_KPI_Monthly ORDER BY MonthDate, Region, Department;
GO
