from pathlib import Path
import pandas as pd, random
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/'input_data'; OUT.mkdir(exist_ok=True)
regions=['North','West','South','East']; depts=['Sales','Support','Operations']; employees=['Amit','Neha','Rahul','Priya','Karan','Riya','Arjun','Simran']; processes=['MIS Reporting','Customer Support','Operations']
for month in pd.date_range('2026-07-01','2026-12-01',freq='MS'):
    rows=[]
    for _ in range(12): rows.append({'Month':month.date(),'Region':random.choice(regions),'Department':random.choice(depts),'Employee':random.choice(employees),'Process':random.choice(processes),'Revenue':random.randint(30000,60000),'Tickets_Closed':random.randint(25,55),'Escalations':random.randint(0,6),'SLA_Percent':round(random.uniform(90,99),2),'Quality_Percent':round(random.uniform(85,98),2)})
    pd.DataFrame(rows).to_excel(OUT/f'MIS_Input_{month:%Y-%m}.xlsx',index=False)
print('Monthly sample inputs generated.')
