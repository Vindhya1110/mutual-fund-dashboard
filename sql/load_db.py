import pandas as pd
from sqlalchemy import create_engine
import os

PROCESSED = "data/processed"
DB_PATH = "bluestock_mf.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

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
    df.to_sql(table, engine, if_exists="replace", index=False)
    # Verify row count
    result = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", engine)
    print(f"✅ {table}: {result['count'][0]} rows loaded")

print("\n🎉 Database ready: bluestock_mf.db")