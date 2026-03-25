# Architektura projektu

## Cel

Celem projektu jest pokazanie jednego, spójnego case study portfolio, które łączy:
- data engineering,
- hurtownię danych,
- ML,
- LLM / analytics assistant.

## Warstwy danych

### 1. Raw
Pliki wejściowe CSV generowane lub pobierane z zewnętrznych źródeł.

### 2. Bronze
Minimalnie przetworzone dane źródłowe zapisane do DuckDB.

### 3. Silver
Dane oczyszczone:
- poprawione typy,
- usunięte duplikaty,
- podstawowe reguły jakości.

### 4. Gold
Model analityczny:
- tabele wymiarów,
- tabela faktów,
- gotowe agregaty KPI.

## Model hurtowni

### Fakty
- `fact_sales`

Miary:
- quantity
- gross_sales
- discount_amount
- net_sales

### Wymiary
- `dim_customer`
- `dim_product`
- `dim_date`

## ML

Model bazowy przewiduje sprzedaż dzienną na podstawie:
- dnia tygodnia,
- miesiąca,
- liczby zamówień,
- liczby klientów,
- wartości sprzedaży historycznej.

## LLM

Aplikacja ma dwa zadania:
1. odpowiadać na pytania o KPI i definicje,
2. w kolejnej iteracji generować insighty na podstawie danych z warstwy gold.

## Rozszerzenia produkcyjne
- orkiestracja Airflow,
- incremental loads,
- data quality checks,
- CI/CD,
- testy SQL i Python,
- konteneryzacja,
- monitoring pipeline.
