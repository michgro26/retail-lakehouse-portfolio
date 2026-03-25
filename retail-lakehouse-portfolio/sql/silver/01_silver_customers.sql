CREATE OR REPLACE TABLE silver_customers AS
SELECT DISTINCT
    CAST(customer_id AS INTEGER) AS customer_id,
    city,
    segment,
    CAST(signup_date AS DATE) AS signup_date
FROM bronze_customers;
