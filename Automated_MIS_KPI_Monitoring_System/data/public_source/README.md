# Public source dataset

The public-data reference for this portfolio project is the **UCI Online Retail** dataset.

Official source: https://archive.ics.uci.edu/dataset/352/online-retail

Dataset facts: 541,909 transaction records covering 01/12/2010–09/12/2011 for a UK-based non-store online retailer. Core fields include InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID and Country.

License: Creative Commons Attribution 4.0 International (CC BY 4.0).

Citation:
Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. DOI: 10.24432/C5BW33.

## Important project boundary
The monthly `data/monthly_inputs/` files in this portfolio are **synthetic operational records** created to demonstrate MIS controls that are not present in the UCI transaction schema, such as department, SLA target, TAT and KPI target.

Do not describe those operational fields as coming from UCI. The correct portfolio description is: **public retail transaction source + synthetic MIS control layer**.
