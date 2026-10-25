USE [MIS_KPI_Monitoring];
GO
TRUNCATE TABLE dbo.MIS_KPI_Staging;
GO
MERGE dbo.MIS_KPI_Fact AS T
USING dbo.MIS_KPI_Staging AS S
ON T.MonthDate=S.MonthDate AND T.Region=S.Region AND T.Department=S.Department AND T.Employee=S.Employee AND T.Process=S.Process
WHEN MATCHED THEN UPDATE SET T.Revenue=S.Revenue,T.Tickets_Closed=S.Tickets_Closed,T.Escalations=S.Escalations,T.SLA_Percent=S.SLA_Percent,T.Quality_Percent=S.Quality_Percent,T.LoadedAt=SYSUTCDATETIME()
WHEN NOT MATCHED THEN INSERT (MonthDate,Region,Department,Employee,Process,Revenue,Tickets_Closed,Escalations,SLA_Percent,Quality_Percent)
VALUES (S.MonthDate,S.Region,S.Department,S.Employee,S.Process,S.Revenue,S.Tickets_Closed,S.Escalations,S.SLA_Percent,S.Quality_Percent);
GO
