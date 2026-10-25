from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "data" / "monthly_inputs"
OUTPUT_DIR = BASE_DIR / "data" / "etl_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = OUTPUT_DIR / "automated_mis.db"

REQUIRED_COLUMNS = [
    "Record_ID", "Record_Date", "Department", "Region", "Channel",
    "Category", "Customer_Segment", "Quantity", "Sales", "Cost", "Profit",
    "KPI_Target", "KPI_Actual", "SLA_Target_Hours", "TAT_Hours",
    "SLA_Breach", "KPI_Below_Target", "Missing_Data_Flag", "Duplicate_Flag",
    "Volume_Anomaly_Flag", "Exception_Type", "Status"
]

NUMERIC_COLUMNS = [
    "Quantity", "Sales", "Cost", "Profit", "KPI_Target", "KPI_Actual",
    "SLA_Target_Hours", "TAT_Hours"
]


def extract_excel_files():
    files = sorted(INPUT_DIR.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No Excel files found in {INPUT_DIR}")

    frames = []
    for file in files:
        df = pd.read_excel(file)
        df["Source_File"] = file.name
        frames.append(df)

    return pd.concat(frames, ignore_index=True), files


def validate_data(df):
    errors = []

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
        return errors

    duplicate_count = int(df["Record_ID"].duplicated().sum())
    if duplicate_count:
        errors.append(f"Duplicate Record_IDs: {duplicate_count}")

    for column in ["Record_ID", "Record_Date", "Department", "Sales", "Cost", "Profit"]:
        count = int(df[column].isna().sum())
        if count:
            errors.append(f"{column}: {count} missing values")

    for column in NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[column], errors="coerce")
        invalid = int(converted.isna().sum() - df[column].isna().sum())
        if invalid:
            errors.append(f"{column}: {invalid} non-numeric values")

    profit_diff = (df["Sales"] - df["Cost"] - df["Profit"]).abs()
    failures = int((profit_diff > 0.01).sum())
    if failures:
        errors.append(f"Profit reconciliation failures: {failures}")

    expected_sla = df["TAT_Hours"] > df["SLA_Target_Hours"]
    actual_sla = df["SLA_Breach"].astype(str).str.upper().eq("YES")
    mismatches = int((expected_sla != actual_sla).sum())
    if mismatches:
        errors.append(f"SLA flag mismatches: {mismatches}")

    expected_kpi = df["KPI_Actual"] < df["KPI_Target"]
    actual_kpi = df["KPI_Below_Target"].astype(str).str.upper().eq("YES")
    mismatches = int((expected_kpi != actual_kpi).sum())
    if mismatches:
        errors.append(f"KPI flag mismatches: {mismatches}")

    return errors


def transform_data(df):
    df = df.copy().dropna(how="all")
    df.columns = df.columns.str.strip().str.replace(" ", "_", regex=False)
    df["Record_Date"] = pd.to_datetime(df["Record_Date"], errors="coerce")
    df = df.drop_duplicates()

    text_columns = [
        "Department", "Region", "Channel", "Category",
        "Customer_Segment", "Status"
    ]
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    return df


def load_to_sqlite(df):
    with sqlite3.connect(DATABASE_PATH) as connection:
        df.to_sql("fact_mis", connection, if_exists="replace", index=False)

        department_summary = (
            df.groupby("Department", dropna=False)
            .agg(
                Records=("Record_ID", "count"),
                Total_Sales=("Sales", "sum"),
                Total_Cost=("Cost", "sum"),
                Total_Profit=("Profit", "sum"),
                Average_KPI=("KPI_Actual", "mean"),
            )
            .reset_index()
        )
        department_summary.to_sql(
            "department_kpi_summary", connection, if_exists="replace", index=False
        )

        exceptions = df[
            (df["SLA_Breach"].astype(str).str.upper() == "YES")
            | (df["KPI_Below_Target"].astype(str).str.upper() == "YES")
            | (df["Exception_Type"].notna())
        ]
        exceptions.to_sql(
            "mis_exceptions", connection, if_exists="replace", index=False
        )


def write_validation_report(file_count, record_count, errors):
    status = "PASSED" if not errors else "FAILED"
    report = pd.DataFrame([{
        "Files_Processed": file_count,
        "Records_Processed": record_count,
        "Validation_Status": status,
        "Error_Count": len(errors),
        "Errors": " | ".join(errors),
    }])
    report.to_csv(OUTPUT_DIR / "validation_report.csv", index=False)


def main():
    print("=== Automated MIS & KPI Monitoring System ===")
    df, files = extract_excel_files()
    errors = validate_data(df)
    write_validation_report(len(files), len(df), errors)

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(" -", error)
        raise SystemExit(1)

    clean_df = transform_data(df)
    clean_df.to_csv(OUTPUT_DIR / "consolidated_validated.csv", index=False)
    load_to_sqlite(clean_df)

    print(f"VALIDATION PASSED | files={len(files)} | records={len(clean_df)}")
    print(f"SQLite database: {DATABASE_PATH}")


if __name__ == "__main__":
    main()
