-- 1. Top 5 funds by AUM
SELECT fund_house, SUM(aum) as total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;

-- 2. Average NAV per month per fund
SELECT amfi_code,
       strftime('%Y-%m', date_id) as month,
       ROUND(AVG(nav), 4) as avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- 3. SIP YoY Growth
WITH yearly AS (
    SELECT
        strftime('%Y', date_id) AS year,
        SUM(amount) AS sip_amount
    FROM fact_transactions
    WHERE transaction_type = 'SIP'
    GROUP BY year
)
SELECT
    year,
    ROUND(sip_amount, 2) AS sip_amount,
    ROUND(
        (sip_amount - LAG(sip_amount) OVER (ORDER BY year)) * 100.0
        / LAG(sip_amount) OVER (ORDER BY year),
        2
    ) AS yoy_growth_pct
FROM yearly;

-- 4. Transactions by state
SELECT state,
       COUNT(*) as transaction_count,
       ROUND(SUM(amount), 2) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. Funds with expense_ratio < 1%
SELECT amfi_code, expense_ratio
FROM fact_performance
WHERE expense_ratio < 1.0
ORDER BY expense_ratio ASC;

-- 6. Top 5 funds by 1-year return
SELECT amfi_code, return_1y
FROM fact_performance
ORDER BY return_1y DESC
LIMIT 5;

-- 7. Monthly SIP inflow trend
SELECT strftime('%Y-%m', date_id) as month,
       ROUND(SUM(amount), 2) as sip_inflow
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY month
ORDER BY month;

-- 8. Redemption vs SIP ratio
SELECT transaction_type,
       COUNT(*) as count,
       ROUND(SUM(amount), 2) as total
FROM fact_transactions
GROUP BY transaction_type;

-- 9. Funds with highest 5Y return and low expense ratio
SELECT amfi_code, return_5y, expense_ratio
FROM fact_performance
WHERE expense_ratio < 1.0
ORDER BY return_5y DESC
LIMIT 10;

-- 10. KYC status breakdown
SELECT kyc_status, COUNT(*) as count
FROM fact_transactions
GROUP BY kyc_status;