from pathlib import Path
import numpy as np
import pandas as pd

from retail_portfolio.config import RAW_DIR


rng = np.random.default_rng(42)


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(n: int = 500) -> pd.DataFrame:
    signup_dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    df = pd.DataFrame(
        {
            "customer_id": range(1, n + 1),
            "city": rng.choice(["Warsaw", "Krakow", "Wroclaw", "Gdansk", "Poznan"], size=n),
            "segment": rng.choice(["new", "returning", "vip"], size=n, p=[0.5, 0.4, 0.1]),
            "signup_date": rng.choice(signup_dates, size=n),
        }
    )
    return df


def generate_products(n: int = 80) -> pd.DataFrame:
    categories = ["electronics", "home", "beauty", "sports", "fashion"]
    df = pd.DataFrame(
        {
            "product_id": range(1, n + 1),
            "product_name": [f"product_{i}" for i in range(1, n + 1)],
            "category": rng.choice(categories, size=n),
            "price": np.round(rng.uniform(20, 800, size=n), 2),
        }
    )
    return df


def generate_campaigns() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "campaign_id": [1, 2, 3, 4],
            "campaign_name": ["brand_search", "social_paid", "newsletter", "affiliate"],
            "channel": ["search", "social", "email", "partner"],
        }
    )


def generate_orders(customers: pd.DataFrame, campaigns: pd.DataFrame, n: int = 4000) -> tuple[pd.DataFrame, pd.DataFrame]:
    order_dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")

    orders = pd.DataFrame(
        {
            "order_id": range(1, n + 1),
            "customer_id": rng.choice(customers["customer_id"], size=n),
            "order_date": rng.choice(order_dates, size=n),
            "campaign_id": rng.choice(campaigns["campaign_id"], size=n),
            "status": rng.choice(["completed", "completed", "completed", "cancelled"], size=n),
        }
    ).sort_values("order_date")

    item_rows = []
    item_id = 1
    for order_id in orders["order_id"]:
        num_items = int(rng.integers(1, 5))
        for _ in range(num_items):
            product_id = int(rng.integers(1, 81))
            quantity = int(rng.integers(1, 4))
            discount = float(np.round(rng.uniform(0, 20), 2))
            item_rows.append(
                {
                    "order_item_id": item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "discount_amount": discount,
                }
            )
            item_id += 1

    order_items = pd.DataFrame(item_rows)
    return orders, order_items


def main() -> None:
    ensure_dirs()
    customers = generate_customers()
    products = generate_products()
    campaigns = generate_campaigns()
    orders, order_items = generate_orders(customers, campaigns)

    customers.to_csv(RAW_DIR / "customers.csv", index=False)
    products.to_csv(RAW_DIR / "products.csv", index=False)
    campaigns.to_csv(RAW_DIR / "campaigns.csv", index=False)
    orders.to_csv(RAW_DIR / "orders.csv", index=False)
    order_items.to_csv(RAW_DIR / "order_items.csv", index=False)

    print(f"Sample data written to {RAW_DIR}")


if __name__ == "__main__":
    main()
