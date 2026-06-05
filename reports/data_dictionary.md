# Data Dictionary — Mutual Fund Analytics

## 01_fund_master
| Column | Type | Description |
|---|---|---|
| amfi_code | int | Unique AMFI scheme code |
| scheme_name | str | Full name of the mutual fund scheme |
| fund_house | str | AMC / fund house name |
| category | str | Broad category (Equity, Debt, Hybrid) |
| sub_category | str | Sub-category (Large Cap, ELSS etc.) |
| risk_grade | str | Risk level (Low/Moderate/High) |

## 02_nav_history
| Column | Type | Description |
|---|---|---|
| amfi_code | int | Foreign key to fund_master |
| date | date | NAV date (forward-filled for holidays) |
| nav | float | Net Asset Value in INR |

## 07_scheme_performance
| Column | Type | Description |
|---|---|---|
| amfi_code | int | Foreign key to fund_master |
| return_1y | float | 1-year trailing return (%) |
| return_3y | float | 3-year trailing return (%) |
| return_5y | float | 5-year trailing return (%) |
| expense_ratio | float | Annual expense ratio (%) valid range 0.1–2.5 |
| expense_ratio_flag | str | 'anomaly' if outside valid range, else 'ok' |

## 08_investor_transactions
| Column | Type | Description |
|---|---|---|
| amfi_code | int | Foreign key to fund_master |
| date | date | Transaction date |
| transaction_type | str | SIP / Lumpsum / Redemption |
| amount | float | Transaction amount in INR (must be > 0) |
| state | str | Investor's state |
| kyc_status | str | KYC Verified / Pending / Rejected |