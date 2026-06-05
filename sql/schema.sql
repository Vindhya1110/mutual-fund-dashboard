-- Star Schema for Mutual Fund Analytics

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code       INTEGER PRIMARY KEY,
    scheme_name     TEXT NOT NULL,
    fund_house      TEXT,
    category        TEXT,
    sub_category    TEXT,
    risk_grade      TEXT,
    expense_ratio   REAL
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
    amfi_code           INTEGER REFERENCES dim_fund(amfi_code),
    date_id             TEXT    REFERENCES dim_date(date_id),
    transaction_type    TEXT    CHECK(transaction_type IN ('SIP','Lumpsum','Redemption')),
    amount              REAL    CHECK(amount > 0),
    state               TEXT,
    kyc_status          TEXT
);

CREATE TABLE IF NOT EXISTS fact_performance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code       INTEGER REFERENCES dim_fund(amfi_code),
    return_1y       REAL,
    return_3y       REAL,
    return_5y       REAL,
    expense_ratio   REAL,
    expense_ratio_flag TEXT
);

CREATE TABLE IF NOT EXISTS fact_aum (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house  TEXT,
    date_id     TEXT REFERENCES dim_date(date_id),
    aum         REAL
);