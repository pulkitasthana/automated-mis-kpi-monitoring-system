"""Fetch the official UCI Online Retail dataset.

Requires: pip install ucimlrepo
The project intentionally does not redistribute the 22.6 MB source file in Git.
"""
from pathlib import Path
from ucimlrepo import fetch_ucirepo

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'data' / 'public_source'
out.mkdir(exist_ok=True)

dataset = fetch_ucirepo(id=352)
df = dataset.data.features.copy()
out_file = out / 'uci_online_retail.csv'
df.to_csv(out_file, index=False)
print(f'Saved {len(df):,} rows to {out_file}')
