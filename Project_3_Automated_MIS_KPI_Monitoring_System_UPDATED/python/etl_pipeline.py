from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / 'input_data'
REQUIRED = ['Month','Region','Department','Employee','Process','Revenue','Tickets_Closed','Escalations','SLA_Percent','Quality_Percent']

def engine():
    server=os.getenv('SQL_SERVER','localhost')
    db=os.getenv('SQL_DATABASE','MIS_KPI_Monitoring')
    driver=os.getenv('SQL_DRIVER','ODBC Driver 18 for SQL Server')
    trusted=os.getenv('SQL_TRUSTED_CONNECTION','yes').lower()=='yes'
    if trusted:
        odbc=f'DRIVER={{{driver}}};SERVER={server};DATABASE={db};Trusted_Connection=yes;TrustServerCertificate=yes;'
    else:
        user=os.environ['SQL_USER']; password=os.environ['SQL_PASSWORD']
        odbc=f'DRIVER={{{driver}}};SERVER={server};DATABASE={db};UID={user};PWD={password};TrustServerCertificate=yes;'
    return create_engine('mssql+pyodbc:///?odbc_connect='+quote_plus(odbc), fast_executemany=True)

def validate(df, name):
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError(f'{name}: missing columns {missing}')
    df=df[REQUIRED].copy()
    df['Month']=pd.to_datetime(df['Month'],errors='coerce').dt.date
    for c in ['Revenue','Tickets_Closed','Escalations','SLA_Percent','Quality_Percent']:
        df[c]=pd.to_numeric(df[c],errors='coerce')
    if df.isna().any().any(): raise ValueError(f'{name}: blank/invalid values found')
    if (df[['Tickets_Closed','Escalations']]<0).any().any(): raise ValueError(f'{name}: negative count')
    if ((df[['SLA_Percent','Quality_Percent']]<0)|(df[['SLA_Percent','Quality_Percent']]>100)).any().any(): raise ValueError(f'{name}: percentage outside 0-100')
    return df

def main():
    files=sorted(INPUT_DIR.glob('MIS_Input_*.xlsx'))
    if not files: raise FileNotFoundError('No MIS_Input_*.xlsx files found')
    frames=[validate(pd.read_excel(f),f.name) for f in files]
    df=pd.concat(frames,ignore_index=True).drop_duplicates()
    e=engine()
    with e.begin() as c: c.execute(text('TRUNCATE TABLE dbo.MIS_KPI_Staging'))
    df.rename(columns={'Month':'MonthDate'}).to_sql('MIS_KPI_Staging',e,schema='dbo',if_exists='append',index=False)
    merge='''MERGE dbo.MIS_KPI_Fact AS T USING dbo.MIS_KPI_Staging AS S ON T.MonthDate=S.MonthDate AND T.Region=S.Region AND T.Department=S.Department AND T.Employee=S.Employee AND T.Process=S.Process WHEN MATCHED THEN UPDATE SET T.Revenue=S.Revenue,T.Tickets_Closed=S.Tickets_Closed,T.Escalations=S.Escalations,T.SLA_Percent=S.SLA_Percent,T.Quality_Percent=S.Quality_Percent,T.LoadedAt=SYSUTCDATETIME() WHEN NOT MATCHED THEN INSERT (MonthDate,Region,Department,Employee,Process,Revenue,Tickets_Closed,Escalations,SLA_Percent,Quality_Percent) VALUES (S.MonthDate,S.Region,S.Department,S.Employee,S.Process,S.Revenue,S.Tickets_Closed,S.Escalations,S.SLA_Percent,S.Quality_Percent);'''
    with e.begin() as c: c.execute(text(merge))
    print(f'ETL completed successfully. Rows processed: {len(df)}')

if __name__=='__main__': main()
