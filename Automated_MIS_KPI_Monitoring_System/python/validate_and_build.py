from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / 'data' / 'monthly_inputs'
OUT_DIR = ROOT / 'outputs'
OUT_DIR.mkdir(exist_ok=True)

EXPECTED = [
    'Record_ID','Record_Date','Department','Region','Channel','Category','Customer_Segment',
    'Quantity','Sales','Cost','Profit','KPI_Target','KPI_Actual','SLA_Target_Hours','TAT_Hours',
    'SLA_Breach','KPI_Below_Target','Missing_Data_Flag','Duplicate_Flag','Volume_Anomaly_Flag',
    'Exception_Type','Status'
]

frames = []
file_rows = []
for f in sorted(INPUT_DIR.glob('*.xlsx')):
    df = pd.read_excel(f)
    missing_cols = [c for c in EXPECTED if c not in df.columns]
    extra_cols = [c for c in df.columns if c not in EXPECTED]
    frames.append(df)
    file_rows.append({
        'File': f.name, 'Rows': len(df), 'Missing_Columns': '; '.join(missing_cols),
        'Extra_Columns': '; '.join(extra_cols)
    })

if not frames:
    raise SystemExit('No monthly Excel files found.')

fact = pd.concat(frames, ignore_index=True)
for c in ['Record_Date']:
    fact[c] = pd.to_datetime(fact[c], errors='coerce')
for c in ['Quantity','Sales','Cost','Profit','KPI_Target','KPI_Actual','SLA_Target_Hours','TAT_Hours']:
    fact[c] = pd.to_numeric(fact[c], errors='coerce')

fact['Calculated_Profit'] = fact['Sales'] - fact['Cost']
fact['Profit_Variance'] = fact['Profit'] - fact['Calculated_Profit']
fact['SLA_Breach_Calc'] = (fact['TAT_Hours'] > fact['SLA_Target_Hours']).map({True:'Yes',False:'No'})
fact['KPI_Below_Target_Calc'] = (fact['KPI_Actual'] < fact['KPI_Target']).map({True:'Yes',False:'No'})
fact['Month'] = fact['Record_Date'].dt.to_period('M').astype(str)

duplicate_mask = fact.duplicated('Record_ID', keep=False)
required_for_record = [c for c in EXPECTED if c != 'Exception_Type']
missing_mask = fact[required_for_record].isna().any(axis=1)
profit_issue = fact['Profit_Variance'].abs() > 0.01
sla_issue = fact['SLA_Breach'].fillna('') != fact['SLA_Breach_Calc'].fillna('')
kpi_issue = fact['KPI_Below_Target'].fillna('') != fact['KPI_Below_Target_Calc'].fillna('')

quality = pd.DataFrame({
    'Metric': [
        'Input files','Input rows','Duplicate Record_ID rows','Rows with missing required fields',
        'Profit calculation mismatches','SLA flag mismatches','KPI flag mismatches','Exception rows','Exception rate %'
    ],
    'Value': [
        len(frames), len(fact), int(duplicate_mask.sum()), int(missing_mask.sum()), int(profit_issue.sum()),
        int(sla_issue.sum()), int(kpi_issue.sum()), int((fact['Status']=='Exception').sum()),
        round((fact['Status']=='Exception').mean()*100, 2)
    ]
})
quality.to_csv(OUT_DIR/'data_quality_summary.csv', index=False)
pd.DataFrame(file_rows).to_csv(OUT_DIR/'file_validation.csv', index=False)

fact.to_csv(OUT_DIR/'fact_mis_validated.csv', index=False)

exception_detail = fact.loc[fact['Status'].eq('Exception'), EXPECTED + ['Month']].copy()
exception_detail.to_csv(OUT_DIR/'exception_detail.csv', index=False)

monthly = fact.groupby('Month', as_index=False).agg(
    Records=('Record_ID','count'), Sales=('Sales','sum'), Profit=('Profit','sum'),
    Avg_TAT_Hours=('TAT_Hours','mean'), SLA_Breaches=('SLA_Breach', lambda s: (s=='Yes').sum()),
    KPI_Below_Target=('KPI_Below_Target', lambda s: (s=='Yes').sum()),
    Exceptions=('Status', lambda s: (s=='Exception').sum())
)
monthly['SLA_Compliance_%'] = (1 - monthly['SLA_Breaches']/monthly['Records'])*100
monthly['Exception_Rate_%'] = monthly['Exceptions']/monthly['Records']*100
monthly.to_csv(OUT_DIR/'monthly_kpi.csv', index=False)

dep = fact.groupby('Department', as_index=False).agg(
    Records=('Record_ID','count'), Sales=('Sales','sum'), Profit=('Profit','sum'),
    Avg_KPI_Actual=('KPI_Actual','mean'), Avg_KPI_Target=('KPI_Target','mean'),
    Avg_TAT_Hours=('TAT_Hours','mean'), SLA_Breaches=('SLA_Breach', lambda s: (s=='Yes').sum()),
    KPI_Below_Target=('KPI_Below_Target', lambda s: (s=='Yes').sum()),
    Exceptions=('Status', lambda s: (s=='Exception').sum())
)
dep['SLA_Compliance_%'] = (1 - dep['SLA_Breaches']/dep['Records'])*100
dep['KPI_Achievement_%'] = dep['Avg_KPI_Actual']/dep['Avg_KPI_Target']*100
dep['Exception_Rate_%'] = dep['Exceptions']/dep['Records']*100
dep.to_csv(OUT_DIR/'department_kpi.csv', index=False)

print('Build complete.')
print(quality.to_string(index=False))
