CREATE OR REPLACE TABLE silver_order_items AS
SELECT DISTINCT
    CAST(order_item_id AS INTEGER) AS order_item_id,
    CAST(order_id AS INTEGER) AS order_id,
    CAST(product_id AS INTEGER) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(discount_amount AS DOUBLE) AS discount_amount
FROM bronze_order_items;
