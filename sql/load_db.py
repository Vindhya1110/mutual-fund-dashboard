import pandas as pd
from sqlalchemy import create_engine, text
import os

PROCESSED = "data/processed"
DB_PATH = "bluestock_mf.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

# ── Step 1: Create schema statement by statement ──────────
schema = open("sql/schema.sql").read()
statements = [s.strip() for s in schema.split(";") if s.strip() and not s.strip().startswith("--")]
with engine.begin() as conn:
    for stmt in statements:
        conn.execute(text(stmt))
print("✅ Schema created")

# ── Step 2: Generate dim_date ─────────────────────────────
dates = pd.date_range(start="2015-01-01", end="2026-12-31")
dim_date = pd.DataFrame({
    "date_id":    dates.strftime("%Y-%m-%d"),
    "day":        dates.day,
    "month":      dates.month,
    "year":       dates.year,
    "quarter":    dates.quarter,
    "is_weekend": (dates.weekday >= 5).astype(int)
})
dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
print(f"✅ dim_date: {len(dim_date)} rows loaded")

# ── Step 3: Load tables ───────────────────────────────────
files = {
    "dim_fund":          "01_fund_master_clean.csv",
    "fact_nav":          "02_nav_history_clean.csv",
    "fact_aum":          "03_aum_by_fund_house_clean.csv",
    "fact_performance":  "07_scheme_performance_clean.csv",
    "fact_transactions": "08_investor_transactions_clean.csv",
}

for table, filename in files.items():
    path = os.path.join(PROCESSED, filename)
    df = pd.read_csv(path)

    # Rename any date column to date_id
    for col in ["date", "month", "transaction_date"]:
        if col in df.columns:
            df.rename(columns={col: "date_id"}, inplace=True)
            break

    # Standardise date_id format to YYYY-MM-DD
    if "date_id" in df.columns:
        df["date_id"] = pd.to_datetime(
            df["date_id"], dayfirst=True, errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    df.to_sql(table, engine, if_exists="append", index=False)

    db_count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", engine)["count"][0]
    csv_count = len(df)
    status = "✅" if csv_count == db_count else "❌ MISMATCH"
    print(f"{status} {table}: CSV={csv_count}, DB={db_count}")

print("\n🎉 Database ready: bluestock_mf.db")