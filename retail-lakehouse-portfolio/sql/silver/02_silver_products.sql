CREATE OR REPLACE TABLE silver_products AS
SELECT DISTINCT
    CAST(product_id AS INTEGER) AS product_id,
    product_name,
    category,
    CAST(price AS DOUBLE) AS price
FROM bronze_products;
