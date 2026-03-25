import duckdb

from retail_portfolio.config import DB_PATH, PROCESSED_DIR, RAW_DIR


TABLES = {
    "bronze_customers": "customers.csv",
    "bronze_products": "products.csv",
    "bronze_campaigns": "campaigns.csv",
    "bronze_orders": "orders.csv",
    "bronze_order_items": "order_items.csv",
}


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))

    for table_name, file_name in TABLES.items():
        file_path = RAW_DIR / file_name
        con.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.execute(
            f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path.as_posix()}', header=True)"
        )
        row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Loaded {table_name}: {row_count} rows")

    con.close()
    print(f"Bronze tables created in {DB_PATH}")


if __name__ == "__main__":
    main()
