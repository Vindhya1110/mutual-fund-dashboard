import requests
import pandas as pd
import os
from datetime import datetime

RAW_DIR = "data/raw"

# ── SCHEME LIST ──────────────────────────────────────────
schemes = {
    "HDFC_Top_100_Direct":    125497,   # NOTE: actual API returns SBI Small Cap for this code
    "SBI_Bluechip":           119551,
    "ICICI_Bluechip":         120503,
    "Nippon_Large_Cap":       118632,
    "Axis_Bluechip":          119092,
    "Kotak_Bluechip":         120841,
}

BASE_URL = "https://api.mfapi.in/mf/"

def fetch_and_save(scheme_name, scheme_code):
    url = f"{BASE_URL}{scheme_code}"
    print(f"\n📡 Fetching: {scheme_name} (Code: {scheme_code})")
    print(f"   URL: {url}")

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print(f"    Failed! Status code: {response.status_code}")
        return

    data = response.json()
    meta = data["meta"]
    nav_data = data["data"]

    print(f"    Fund House : {meta['fund_house']}")
    print(f"    Scheme Name: {meta['scheme_name']}")
    print(f"    Category   : {meta['scheme_category']}")
    print(f"    Records    : {len(nav_data)}")

    # Convert to DataFrame
    df = pd.DataFrame(nav_data)
    df["scheme_code"] = scheme_code
    df["scheme_name"] = meta["scheme_name"]
    df["fund_house"] = meta["fund_house"]
    df["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to CSV
    filename = f"{scheme_name}_{scheme_code}_nav.csv"
    filepath = os.path.join(RAW_DIR, filename)
    df.to_csv(filepath, index=False)
    print(f"    Saved to: {filepath}")

    # Show latest 3 NAV values
    print(f"\n   Latest NAV values:")
    print(df.head(3).to_string(index=False))

# ── MAIN ─────────────────────────────────────────────────
print("=" * 60)
print(" LIVE NAV FETCHER — mfapi.in")
print("=" * 60)

for name, code in schemes.items():
    fetch_and_save(name, code)

print("\n" + "=" * 60)
print(" All NAV data fetched and saved to data/raw/")
print("=" * 60)