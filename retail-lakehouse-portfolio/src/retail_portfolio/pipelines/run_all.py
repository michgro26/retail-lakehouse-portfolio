from retail_portfolio.pipelines import generate_sample_data, ingest_raw, build_warehouse
from retail_portfolio.ml import train_forecast
from retail_portfolio.quality import validate_warehouse
from retail_portfolio.reporting import generate_report


def main() -> None:
    print('1/6 Generating sample data...')
    generate_sample_data.main()
    print('2/6 Loading bronze tables...')
    ingest_raw.main()
    print('3/6 Building silver and gold layers...')
    build_warehouse.main()
    print('4/6 Running data quality checks...')
    validate_warehouse.main()
    print('5/6 Training forecasting model...')
    train_forecast.main()
    print('6/6 Generating KPI report...')
    generate_report.main()
    print('Pipeline finished successfully.')


if __name__ == '__main__':
    main()
