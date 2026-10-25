CREATE DATABASE AutomatedMIS;
GO
USE AutomatedMIS;
GO

CREATE TABLE fact_mis (
    Record_ID VARCHAR(50) PRIMARY KEY,
    Record_Date DATE NOT NULL,
    Department VARCHAR(50),
    Region VARCHAR(20),
    Channel VARCHAR(30),
    Category VARCHAR(50),
    Customer_Segment VARCHAR(30),
    Quantity INT,
    Sales DECIMAL(18,2),
    Cost DECIMAL(18,2),
    Profit DECIMAL(18,2),
    KPI_Target DECIMAL(18,2),
    KPI_Actual DECIMAL(18,2),
    SLA_Target_Hours INT,
    TAT_Hours INT,
    SLA_Breach VARCHAR(3),
    KPI_Below_Target VARCHAR(3),
    Missing_Data_Flag VARCHAR(3),
    Duplicate_Flag VARCHAR(3),
    Volume_Anomaly_Flag VARCHAR(3),
    Exception_Type VARCHAR(255),
    Status VARCHAR(20)
);

CREATE TABLE dim_kpi_targets (
    Department VARCHAR(50),
    KPI_Name VARCHAR(100),
    Target_Value DECIMAL(18,2),
    Unit VARCHAR(20),
    Definition VARCHAR(255)
);