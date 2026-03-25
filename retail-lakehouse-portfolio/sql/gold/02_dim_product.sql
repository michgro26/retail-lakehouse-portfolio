CREATE OR REPLACE TABLE dim_product AS
SELECT
    product_id,
    product_name,
    category,
    price
FROM silver_products;
