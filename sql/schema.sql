-- Star Schema for Mutual Fund Analytics

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT,
    scheme_name         TEXT NOT NULL,
    category            TEXT,
    sub_category        TEXT,
    plan                TEXT,
    launch_date         TEXT,
    benchmark           TEXT,
    expense_ratio_pct   REAL,
    exit_load_pct       REAL,
    min_sip_amount      REAL,
    min_lumpsum_amount  REAL,
    fund_manager        TEXT,
    risk_category       TEXT,
    sebi_category_code  TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id     TEXT PRIMARY KEY,  -- YYYY-MM-DD
    day         INTEGER,
    month       INTEGER,
    year        INTEGER,
    quarter     INTEGER,
    is_weekend  INTEGER
);

CREATE TABLE IF NOT EXISTS fact_nav (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code   INTEGER REFERENCES dim_fund(amfi_code),
    date_id     TEXT    REFERENCES dim_date(date_id),
    nav         REAL    CHECK(nav > 0)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT,
    date_id             TEXT REFERENCES dim_date(date_id),
    amfi_code           INTEGER REFERENCES dim_fund(amfi_code),
    transaction_type    TEXT,
    amount_inr          REAL,
    state               TEXT,
    city                TEXT,
    city_tier           TEXT,
    age_group           TEXT,
    gender              TEXT,
    annual_income_lakh  REAL,
    payment_mode        TEXT,
    kyc_status          TEXT
);

CREATE TABLE IF NOT EXISTS fact_performance (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code           INTEGER REFERENCES dim_fund(amfi_code),
    scheme_name         TEXT,
    fund_house          TEXT,
    category            TEXT,
    plan                TEXT,
    return_1yr_pct      REAL,
    return_3yr_pct      REAL,
    return_5yr_pct      REAL,
    benchmark_3yr_pct   REAL,
    alpha               REAL,
    beta                REAL,
    sharpe_ratio        REAL,
    sortino_ratio       REAL,
    std_dev_ann_pct     REAL,
    max_drawdown_pct    REAL,
    aum_crore           REAL,
    expense_ratio_pct   REAL,
    morningstar_rating  INTEGER,
    risk_grade          TEXT
);
CREATE TABLE IF NOT EXISTS fact_aum (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id         TEXT REFERENCES dim_date(date_id),
    fund_house      TEXT,
    aum_lakh_crore  REAL,
    aum_crore       REAL,
    num_schemes     INTEGER
);