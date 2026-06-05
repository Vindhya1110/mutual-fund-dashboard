import pandas as pd
import numpy as np
import os

RAW = "data/raw"
PROCESSED = "data/processed"
os.makedirs(PROCESSED, exist_ok=True)

# ── 1. fund_master ────────────────────────────────────────
df = pd.read_csv(f"{RAW}/01_fund_master.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
df.dropna(subset=["amfi_code"], inplace=True)
df.to_csv(f"{PROCESSED}/01_fund_master_clean.csv", index=False)
print(f"fund_master: {df.shape}")

# ── 2. nav_history ────────────────────────────────────────
df = pd.read_csv(f"{RAW}/02_nav_history.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
df.dropna(subset=["date"], inplace=True)

df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
df = df[df["nav"] > 0]

df.sort_values(["amfi_code", "date"], inplace=True)
df = df.drop_duplicates(subset=["amfi_code", "date"])

# Forward-fill missing NAV for holidays/weekends
df = (
    df.set_index("date")
      .groupby("amfi_code", group_keys=False)
      .apply(lambda x: x.resample("D").ffill())
      .reset_index()
)

df.to_csv(f"{PROCESSED}/02_nav_history_clean.csv", index=False)
print(f"nav_history: {df.shape}")

# ── 3. aum_by_fund_house ──────────────────────────────────
df = pd.read_csv(f"{RAW}/03_aum_by_fund_house.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
df["aum_crore"] = pd.to_numeric(df["aum_crore"], errors="coerce")
df.dropna(subset=["aum_crore"], inplace=True)
df.to_csv(f"{PROCESSED}/03_aum_by_fund_house_clean.csv", index=False)
print(f"aum_by_fund_house: {df.shape}")

# ── 4. monthly_sip_inflows ────────────────────────────────
df = pd.read_csv(f"{RAW}/04_monthly_sip_inflows.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
df.to_csv(f"{PROCESSED}/04_monthly_sip_inflows_clean.csv", index=False)
print(f"monthly_sip_inflows: {df.shape}")

# ── 5. category_inflows ───────────────────────────────────
df = pd.read_csv(f"{RAW}/05_category_inflows.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
df.to_csv(f"{PROCESSED}/05_category_inflows_clean.csv", index=False)
print(f"category_inflows: {df.shape}")

# ── 6. industry_folio_count ───────────────────────────────
df = pd.read_csv(f"{RAW}/06_industry_folio_count.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
df.to_csv(f"{PROCESSED}/06_industry_folio_count_clean.csv", index=False)
print(f"industry_folio_count: {df.shape}")

# ── 7. scheme_performance ─────────────────────────────────
df = pd.read_csv(f"{RAW}/07_scheme_performance.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
# Validate return columns are numeric
return_cols = [c for c in df.columns if "return" in c]
for col in return_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
# Validate expense_ratio range
if "expense_ratio" in df.columns:
    df["expense_ratio"] = pd.to_numeric(df["expense_ratio"], errors="coerce")
    anomalies = df[(df["expense_ratio"] < 0.1) | (df["expense_ratio"] > 2.5)]
    print(f"     expense_ratio anomalies: {len(anomalies)} rows")
    df["expense_ratio_flag"] = df["expense_ratio"].apply(
        lambda x: "anomaly" if pd.notna(x) and (x < 0.1 or x > 2.5) else "ok"
    )
df.to_csv(f"{PROCESSED}/07_scheme_performance_clean.csv", index=False)
print(f"scheme_performance: {df.shape}")

# ── 8. investor_transactions ──────────────────────────────
df = pd.read_csv(f"{RAW}/08_investor_transactions.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=True, errors="coerce")
df["annual_income_lakh"] = pd.to_numeric(df["annual_income_lakh"], errors="coerce")
df = df[df["annual_income_lakh"] > 0]
# Standardise transaction_type
type_map = {
    "sip": "SIP", "lumpsum": "Lumpsum", "lump sum": "Lumpsum",
    "redemption": "Redemption", "redeem": "Redemption"
}
if "transaction_type" in df.columns:
    df["transaction_type"] = df["transaction_type"].str.strip().str.lower().map(
        lambda x: type_map.get(x, x.title()) if isinstance(x, str) else x
    )
# Validate KYC
if "kyc_status" in df.columns:
    valid_kyc = ["KYC Verified", "Pending", "Rejected"]
    df["kyc_status"] = df["kyc_status"].str.strip()
    print(f"   KYC values: {df['kyc_status'].unique()}")
df.to_csv(f"{PROCESSED}/08_investor_transactions_clean.csv", index=False)
print(f"investor_transactions: {df.shape}")

# ── 9. portfolio_holdings ─────────────────────────────────
df = pd.read_csv(f"{RAW}/09_portfolio_holdings.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(inplace=True)
df.to_csv(f"{PROCESSED}/09_portfolio_holdings_clean.csv", index=False)
print(f"portfolio_holdings: {df.shape}")

# ── 10. benchmark_indices ─────────────────────────────────
df = pd.read_csv(f"{RAW}/10_benchmark_indices.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
df.drop_duplicates(inplace=True)
df.to_csv(f"{PROCESSED}/10_benchmark_indices_clean.csv", index=False)
print(f"benchmark_indices: {df.shape}")

print("\nAll 10 CSVs cleaned and saved to data/processed/")