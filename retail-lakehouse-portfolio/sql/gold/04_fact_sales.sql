CREATE OR REPLACE TABLE fact_sales AS
SELECT
    o.order_id,
    o.order_date AS date_key,
    o.customer_id,
    oi.product_id,
    oi.quantity,
    p.price AS unit_price,
    oi.discount_amount,
    (oi.quantity * p.price) AS gross_sales,
    ((oi.quantity * p.price) - oi.discount_amount) AS net_sales,
    o.campaign_id
FROM silver_orders o
JOIN silver_order_items oi ON o.order_id = oi.order_id
JOIN silver_products p ON oi.product_id = p.product_id;
