import duckdb
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from retail_portfolio.config import DB_PATH


FEATURE_QUERY = """
SELECT
    date_key,
    day_of_week,
    month_nr,
    orders_count,
    unique_customers,
    revenue
FROM daily_sales_metrics
ORDER BY date_key
"""


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    df = con.execute(FEATURE_QUERY).df()

    if len(df) < 30:
        raise ValueError("Not enough data to train the forecasting model.")

    features = ["day_of_week", "month_nr", "orders_count", "unique_customers"]
    target = "revenue"

    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(train_df[features], train_df[target])

    test_df["predicted_revenue"] = model.predict(test_df[features])
    mae = mean_absolute_error(test_df[target], test_df["predicted_revenue"])
    print(f"MAE: {mae:.2f}")

    con.execute("DROP TABLE IF EXISTS sales_forecast")
    con.register("forecast_df", test_df[["date_key", target, "predicted_revenue"]])
    con.execute(
        """
        CREATE TABLE sales_forecast AS
        SELECT
            date_key,
            revenue AS actual_revenue,
            predicted_revenue
        FROM forecast_df
        """
    )
    con.close()
    print("Forecast written to sales_forecast table")


if __name__ == "__main__":
    main()
