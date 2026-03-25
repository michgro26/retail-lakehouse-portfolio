import duckdb

from retail_portfolio.config import DB_PATH


def test_gold_tables_exist():
    con = duckdb.connect(str(DB_PATH))
    required = {'dim_customer', 'dim_product', 'dim_date', 'fact_sales', 'daily_sales_metrics'}
    rows = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
    existing = {r[0] for r in rows}
    con.close()
    assert required.issubset(existing)
