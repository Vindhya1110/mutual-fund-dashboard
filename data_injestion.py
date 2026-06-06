import pandas as pd
import os
import glob

# ── CONFIG ──────────────────────────────────────────────
RAW_DIR = "data/raw"
anomalies = []

# ── LOAD ALL CSVs ────────────────────────────────────────
csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

if not csv_files:
    print("No CSV files found in data/raw/")
    exit()

for filepath in csv_files:
    filename = os.path.basename(filepath)
    print("=" * 60)
    print(f"📄 FILE: {filename}")
    print("=" * 60)

    try:
        df = pd.read_csv(filepath)

        print(f"\nShape: {df.shape}")
        print(f"\nData Types:\n{df.dtypes}")
        print(f"\nFirst 5 rows:\n{df.head()}")

        # ── ANOMALY CHECKS ───────────────────────────────
        # Check for missing values
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        if not missing_cols.empty:
            anomalies.append(f"{filename}: Missing values in → {missing_cols.to_dict()}")
            print(f"\nMissing values found:\n{missing_cols}")

        # Check for duplicate rows
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            anomalies.append(f"{filename}: {dup_count} duplicate rows found")
            print(f"\nDuplicate rows: {dup_count}")

        # Check for completely empty columns
        empty_cols = [col for col in df.columns if df[col].isnull().all()]
        if empty_cols:
            anomalies.append(f"{filename}: Empty columns → {empty_cols}")
            print(f"\nCompletely empty columns: {empty_cols}")

    except Exception as e:
        anomalies.append(f"{filename}: ERROR reading file → {e}")
        print(f"\nError reading {filename}: {e}")

    print()

# ── ANOMALY SUMMARY ──────────────────────────────────────
print("\n" + "=" * 60)
print("DATA QUALITY ANOMALY SUMMARY")
print("=" * 60)
if anomalies:
    for a in anomalies:
        print(f"  {a}")
else:
    print("No anomalies found across all files!")

# ── FUND MASTER EXPLORATION ──────────────────────────────
print("\n" + "=" * 60)
print(" FUND MASTER EXPLORATION")
print("=" * 60)

fund_master_path = os.path.join(RAW_DIR, "fund_master.csv")  # adjust filename if different

if os.path.exists(fund_master_path):
    fm = pd.read_csv(fund_master_path)

    # Print column names to understand the structure
    print(f"\nColumns: {fm.columns.tolist()}")

    # Adjust column names below to match your actual CSV headers
    try:
        print(f"\nUnique Fund Houses ({fm['fund_house'].nunique()}):")
        print(fm['fund_house'].unique())
    except KeyError:
        print("⚠️  Column 'fund_house' not found — check your column names above")

    try:
        print(f"\nUnique Categories: {fm['category'].unique()}")
    except KeyError:
        pass

    try:
        print(f"\nUnique Sub-categories: {fm['sub_category'].unique()}")
    except KeyError:
        pass

    try:
        print(f"\nUnique Risk Grades: {fm['risk_grade'].unique()}")
    except KeyError:
        pass

    # ── AMFI CODE VALIDATION ─────────────────────────────
    nav_history_path = os.path.join(RAW_DIR, "nav_history.csv")  # adjust if needed

    if os.path.exists(nav_history_path):
        nav = pd.read_csv(nav_history_path)
        print(f"\n{'='*60}")
        print(" AMFI CODE VALIDATION")
        print(f"{'='*60}")

        # Adjust column names to match your actual CSVs
        fm_codes = set(fm['scheme_code'].astype(str))       # fund_master AMFI codes
        nav_codes = set(nav['scheme_code'].astype(str))     # nav_history AMFI codes

        missing_in_nav = fm_codes - nav_codes
        extra_in_nav   = nav_codes - fm_codes

        print(f"\nTotal codes in fund_master : {len(fm_codes)}")
        print(f"Total codes in nav_history : {len(nav_codes)}")
        print(f"Codes in fund_master but NOT in nav_history: {len(missing_in_nav)}")
        print(f"Codes in nav_history but NOT in fund_master: {len(extra_in_nav)}")

        if missing_in_nav:
            print(f"\n⚠️  Missing codes (first 10): {list(missing_in_nav)[:10]}")
        else:
            print("\n✅ All fund_master codes exist in nav_history!")

        # Write data quality summary to file
        with open("reports/data_quality_summary.txt", "w") as f:
            f.write("DATA QUALITY SUMMARY — Day 1\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"fund_master codes : {len(fm_codes)}\n")
            f.write(f"nav_history codes : {len(nav_codes)}\n")
            f.write(f"Codes missing from nav_history: {len(missing_in_nav)}\n")
            f.write(f"Extra codes in nav_history    : {len(extra_in_nav)}\n\n")
            if anomalies:
                f.write("CSV Anomalies:\n")
                for a in anomalies:
                    f.write(f"  - {a}\n")
            else:
                f.write("No CSV anomalies found.\n")
        print("\n	 Data quality summary saved to reports/data_quality_summary.txt")
    else:
        print("⚠️  nav_history.csv not found — skipping AMFI validation")
else:
    print("⚠️  fund_master.csv not found — skipping fund master exploration")