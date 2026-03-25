CREATE OR REPLACE TABLE dim_date AS
SELECT DISTINCT
    order_date AS date_key,
    EXTRACT(year FROM order_date) AS year_nr,
    EXTRACT(month FROM order_date) AS month_nr,
    EXTRACT(dayofweek FROM order_date) AS day_of_week
FROM silver_orders;
