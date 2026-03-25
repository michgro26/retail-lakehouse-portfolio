from pathlib import Path
import duckdb
import matplotlib.pyplot as plt

from retail_portfolio.config import BASE_DIR, DB_PATH

ARTIFACTS_DIR = BASE_DIR / 'artifacts'


def save_line_chart(df, x, y, title, path: Path) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(df[x], df[y])
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def save_bar_chart(df, x, y, title, path: Path) -> None:
    plt.figure(figsize=(10, 5))
    plt.bar(df[x], df[y])
    plt.title(title)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH), read_only=True)

    daily = con.execute('SELECT * FROM daily_sales_metrics ORDER BY date_key').df()
    categories = con.execute('''
        SELECT p.category, ROUND(SUM(f.net_sales), 2) AS revenue
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY 1 ORDER BY 2 DESC
    ''').df()
    campaigns = con.execute('''
        SELECT campaign_id, ROUND(SUM(net_sales), 2) AS revenue
        FROM fact_sales GROUP BY 1 ORDER BY 2 DESC
    ''').df()
    snapshot = con.execute('''
        SELECT 
            ROUND(SUM(revenue), 2) AS total_revenue,
            SUM(orders_count) AS total_orders,
            ROUND(AVG(aov), 2) AS avg_aov,
            MAX(revenue) AS best_day_revenue
        FROM daily_sales_metrics
    ''').fetchone()

    save_line_chart(daily, 'date_key', 'revenue', 'Daily Revenue', ARTIFACTS_DIR / 'daily_revenue.png')
    save_bar_chart(categories, 'category', 'revenue', 'Revenue by Category', ARTIFACTS_DIR / 'revenue_by_category.png')
    save_bar_chart(campaigns, 'campaign_id', 'revenue', 'Revenue by Campaign', ARTIFACTS_DIR / 'revenue_by_campaign.png')

    md = f'''# Retail KPI Report

## Snapshot
- Total revenue: {snapshot[0]:,.2f}
- Total orders: {int(snapshot[1]):,}
- Average AOV: {snapshot[2]:,.2f}
- Best day revenue: {snapshot[3]:,.2f}

## Included charts
- `artifacts/daily_revenue.png`
- `artifacts/revenue_by_category.png`
- `artifacts/revenue_by_campaign.png`

## Notes
This report was generated automatically from the gold layer and can be attached to the portfolio repository as evidence of business reporting on top of the warehouse.
'''
    (ARTIFACTS_DIR / 'kpi_report.md').write_text(md, encoding='utf-8')
    con.close()
    print(f'Report artifacts written to {ARTIFACTS_DIR}')


if __name__ == '__main__':
    main()
