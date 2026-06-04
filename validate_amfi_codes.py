import pandas as pd
import os

# Load fund master and nav history CSVs
fund_master = pd.read_csv("data/raw/fund_master.csv")   # adjust filename as needed
nav_history = pd.read_csv("data/raw/nav_history.csv")   # adjust filename as needed

master_codes = set(fund_master["scheme_code"].unique())
nav_codes = set(nav_history["scheme_code"].unique())

missing_in_nav = master_codes - nav_codes
missing_in_master = nav_codes - master_codes

print(f"Total codes in fund_master: {len(master_codes)}")
print(f"Total codes in nav_history: {len(nav_codes)}")
print(f"Codes in master but NOT in nav: {len(missing_in_nav)}")
print(f"Codes in nav but NOT in master: {len(missing_in_master)}")

# Write summary
with open("reports/data_quality_summary.md", "w") as f:
    f.write("# Data Quality Summary\n\n")
    f.write(f"- Fund master records: {len(fund_master)}\n")
    f.write(f"- NAV history records: {len(nav_history)}\n")
    f.write(f"- Codes in master not in NAV: {len(missing_in_nav)}\n")
    f.write(f"- Codes in NAV not in master: {len(missing_in_master)}\n")
    if missing_in_nav:
        f.write(f"\nMissing codes: {list(missing_in_nav)[:20]}\n")