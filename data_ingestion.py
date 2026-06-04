import pandas as pd
import os
import glob

# ── CONFIG ──────────────────────────────────────────────
RAW_DIR = "data/raw"
anomalies = []

# ── LOAD ALL CSVs ────────────────────────────────────────
csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))

if not csv_files:
    print("❌ No CSV files found in data/raw/")
    exit()

for filepath in csv_files:
    filename = os.path.basename(filepath)
    print("=" * 60)
    print(f"📄 FILE: {filename}")
    print("=" * 60)

    try:
        df = pd.read_csv(filepath)

        print(f"\n🔹 Shape: {df.shape}")
        print(f"\n🔹 Data Types:\n{df.dtypes}")
        print(f"\n🔹 First 5 rows:\n{df.head()}")

        # ── ANOMALY CHECKS ───────────────────────────────
        # Check for missing values
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        if not missing_cols.empty:
            anomalies.append(f"{filename}: Missing values in → {missing_cols.to_dict()}")
            print(f"\n⚠️  Missing values found:\n{missing_cols}")

        # Check for duplicate rows
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            anomalies.append(f"{filename}: {dup_count} duplicate rows found")
            print(f"\n⚠️  Duplicate rows: {dup_count}")

        # Check for completely empty columns
        empty_cols = [col for col in df.columns if df[col].isnull().all()]
        if empty_cols:
            anomalies.append(f"{filename}: Empty columns → {empty_cols}")
            print(f"\n⚠️  Completely empty columns: {empty_cols}")

    except Exception as e:
        anomalies.append(f"{filename}: ERROR reading file → {e}")
        print(f"\n❌ Error reading {filename}: {e}")

    print()

# ── ANOMALY SUMMARY ──────────────────────────────────────
print("\n" + "=" * 60)
print("📊 DATA QUALITY ANOMALY SUMMARY")
print("=" * 60)
if anomalies:
    for a in anomalies:
        print(f"  ⚠️  {a}")
else:
    print("  ✅ No anomalies found across all files!")