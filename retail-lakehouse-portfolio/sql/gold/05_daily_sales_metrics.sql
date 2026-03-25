CREATE OR REPLACE TABLE daily_sales_metrics AS
SELECT
    f.date_key,
    d.day_of_week,
    d.month_nr,
    COUNT(DISTINCT f.order_id) AS orders_count,
    COUNT(DISTINCT f.customer_id) AS unique_customers,
    SUM(f.net_sales) AS revenue,
    SUM(f.net_sales) / COUNT(DISTINCT f.order_id) AS aov
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY 1, 2, 3
ORDER BY 1;
