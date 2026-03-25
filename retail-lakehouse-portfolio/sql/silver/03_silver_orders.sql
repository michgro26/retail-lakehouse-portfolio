CREATE OR REPLACE TABLE silver_orders AS
SELECT DISTINCT
    CAST(order_id AS INTEGER) AS order_id,
    CAST(customer_id AS INTEGER) AS customer_id,
    CAST(campaign_id AS INTEGER) AS campaign_id,
    CAST(order_date AS DATE) AS order_date,
    status
FROM bronze_orders
WHERE status = 'completed';
