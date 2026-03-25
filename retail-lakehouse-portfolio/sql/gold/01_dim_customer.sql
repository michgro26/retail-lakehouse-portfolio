CREATE OR REPLACE TABLE dim_customer AS
SELECT
    customer_id,
    city,
    segment,
    signup_date
FROM silver_customers;
