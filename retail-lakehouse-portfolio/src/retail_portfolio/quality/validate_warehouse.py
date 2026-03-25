import duckdb

from retail_portfolio.config import DB_PATH


CHECKS = {
    'bronze_customers_not_empty': "SELECT COUNT(*) > 0 FROM bronze_customers",
    'bronze_orders_not_empty': "SELECT COUNT(*) > 0 FROM bronze_orders",
    'fact_sales_not_empty': "SELECT COUNT(*) > 0 FROM fact_sales",
    'fact_sales_non_negative_revenue': "SELECT COUNT(*) = 0 FROM fact_sales WHERE net_sales < 0",
    'unique_customer_keys': "SELECT COUNT(*) = COUNT(DISTINCT customer_id) FROM dim_customer",
    'unique_product_keys': "SELECT COUNT(*) = COUNT(DISTINCT product_id) FROM dim_product",
    'no_orphan_fact_customer': "SELECT COUNT(*) = 0 FROM fact_sales f LEFT JOIN dim_customer d ON f.customer_id = d.customer_id WHERE d.customer_id IS NULL",
    'no_orphan_fact_product': "SELECT COUNT(*) = 0 FROM fact_sales f LEFT JOIN dim_product d ON f.product_id = d.product_id WHERE d.product_id IS NULL",
    'daily_metrics_not_empty': "SELECT COUNT(*) > 0 FROM daily_sales_metrics",
}


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    failed = []
    for name, sql in CHECKS.items():
        ok = con.execute(sql).fetchone()[0]
        print(f"{'PASS' if ok else 'FAIL'}: {name}")
        if not ok:
            failed.append(name)
    con.close()
    if failed:
        raise ValueError(f'Data quality checks failed: {failed}')


if __name__ == '__main__':
    main()
