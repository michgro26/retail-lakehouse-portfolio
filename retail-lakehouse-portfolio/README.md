# Retail Lakehouse Portfolio

Gotowy, rozbudowany projekt portfolio pod role:
- Big Data / Data Engineer
- Hurtownia danych / Analytics Engineer
- ML / AI Engineer
- LLM / GenAI

To jest **działająca platforma end-to-end dla retail analytics**. Projekt generuje dane demo, ładuje je do warstwy bronze, buduje silver i gold, wykonuje quality checks, trenuje model forecastingu, generuje raport KPI oraz udostępnia aplikację Streamlit z warstwą analytics assistant.

## Co zostało zaimplementowane

### 1. Data generation i ingestion
- syntetyczne dane klientów, produktów, kampanii, zamówień i pozycji zamówień,
- zapis do `data/raw/*.csv`,
- ładowanie do DuckDB jako tabele bronze.

### 2. Hurtownia danych
- warstwa **silver** z czyszczeniem i typowaniem,
- warstwa **gold** z modelowaniem faktów i wymiarów,
- metryki dzienne gotowe do BI i ML.

### 3. Data quality
- walidacja pustych tabel,
- sprawdzanie kluczy unikalnych,
- kontrola osieroconych rekordów w tabeli faktów,
- kontrola nieujemnego przychodu.

### 4. ML
- model forecastingu dziennego revenue,
- zapis predykcji do tabeli `sales_forecast`,
- prosty split train/test i metryka MAE.

### 5. Reporting
- automatycznie generowane wykresy PNG,
- raport Markdown z KPI,
- artefakty do wrzucenia na GitHub lub do portfolio.

### 6. Warstwa LLM / analytics assistant
- aplikacja Streamlit,
- pytania do KPI i danych,
- lokalny mechanizm odpowiedzi oparty o dokumentację KPI i dane z hurtowni,
- miejsce przygotowane pod integrację z OpenAI API lub lokalnym LLM.

## Architektura

```text
raw CSV -> bronze tables -> silver cleansing -> gold warehouse -> ML forecast -> KPI report -> Streamlit analytics assistant
```

## Struktura repo

```text
retail-lakehouse-portfolio/
├── artifacts/
│   ├── daily_revenue.png
│   ├── revenue_by_campaign.png
│   ├── revenue_by_category.png
│   └── kpi_report.md
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── sql/
│   ├── silver/
│   └── gold/
├── src/retail_portfolio/
│   ├── config.py
│   ├── pipelines/
│   │   ├── generate_sample_data.py
│   │   ├── ingest_raw.py
│   │   ├── build_warehouse.py
│   │   └── run_all.py
│   ├── quality/
│   │   └── validate_warehouse.py
│   ├── ml/
│   │   └── train_forecast.py
│   ├── reporting/
│   │   └── generate_report.py
│   └── llm/
│       ├── app.py
│       └── kpi_definitions.md
└── tests/
```

## Jak uruchomić

### Instalacja

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Uruchomienie całego pipeline'u

```bash
python -m retail_portfolio.pipelines.run_all
```

### Uruchomienie aplikacji

```bash
streamlit run src/retail_portfolio/llm/app.py
```

## Tabele końcowe

### Bronze
- `bronze_customers`
- `bronze_products`
- `bronze_campaigns`
- `bronze_orders`
- `bronze_order_items`

### Silver
- `silver_customers`
- `silver_products`
- `silver_orders`
- `silver_order_items`

### Gold
- `dim_customer`
- `dim_product`
- `dim_date`
- `fact_sales`
- `daily_sales_metrics`
- `sales_forecast`

## Artefakty portfolio

Po uruchomieniu pipeline'u powstają:
- baza `data/processed/retail_portfolio.duckdb`,
- wykresy w katalogu `artifacts/`,
- raport `artifacts/kpi_report.md`.


## Rozszerzenia
- dbt,
- Airflow / Prefect,
- Delta Lake / Parquet,
- PySpark,
- MLflow,
- RAG nad dokumentacją i słownikiem danych,
- ewaluacja odpowiedzi LLM,
- dashboard w Power BI / Superset.
