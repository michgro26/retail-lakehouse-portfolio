from pathlib import Path
import duckdb

from retail_portfolio.config import BASE_DIR, DB_PATH


SQL_FOLDERS = ["silver", "gold"]


def run_sql_folder(con: duckdb.DuckDBPyConnection, folder_name: str) -> None:
    folder = BASE_DIR / "sql" / folder_name
    for sql_file in sorted(folder.glob("*.sql")):
        sql = sql_file.read_text(encoding="utf-8")
        print(f"Running {sql_file.name}")
        con.execute(sql)


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    for folder in SQL_FOLDERS:
        run_sql_folder(con, folder)
    con.close()
    print("Silver and gold layers built successfully")


if __name__ == "__main__":
    main()
