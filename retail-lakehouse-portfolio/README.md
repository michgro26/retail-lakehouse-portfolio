# Retail Lakehouse Portfolio

To jest mój projekt portfolio, który przygotowałem pod role związane z:
- Data Engineering / Big Data
- Hurtownią danych / Analytics Engineering
- ML / AI
- LLM / GenAI

Chciałem zbudować coś, co pokazuje nie tylko sam model albo sam dashboard, ale cały przepływ danych end-to-end — od surowych danych, przez warstwy hurtowni, aż po prostą warstwę ML i aplikację do zadawania pytań o dane.

Projekt jest osadzony w scenariuszu retail / e-commerce i obejmuje:
- generowanie danych demo,
- ingestion do warstwy bronze,
- transformacje do silver i gold,
- quality checks,
- forecasting sprzedaży,
- raport KPI,
- prostą aplikację Streamlit działającą jako analytics assistant.

## Cel projektu

Celem było zbudowanie spójnego projektu, który pokazuje:
- pracę z danymi w kilku warstwach,
- modelowanie hurtowni danych,
- podejście do jakości danych,
- prosty pipeline ML,
- sposób połączenia analityki z warstwą LLM / assistant.

Zależało mi na tym, żeby projekt dało się uruchomić lokalnie i żeby miał sens biznesowy, a nie był tylko zbiorem luźnych skryptów.

## Co tutaj zrobiłem

### 1. Generowanie i załadowanie danych
Przygotowałem syntetyczne dane dotyczące:
- klientów,
- produktów,
- kampanii marketingowych,
- zamówień,
- pozycji zamówień.

Dane są zapisywane do `data/raw/*.csv`, a następnie ładowane do DuckDB jako warstwa bronze.

### 2. Budowa warstw silver i gold
Na danych surowych buduję kolejne warstwy:
- **bronze** – surowy zrzut danych,
- **silver** – oczyszczone i ujednolicone dane,
- **gold** – warstwa analityczna z faktami, wymiarami i metrykami.

W gold przygotowałem model z tabelami typu:
- `fact_sales`
- `dim_customer`
- `dim_product`
- `dim_date`

Dodatkowo powstaje tabela dziennych metryk sprzedażowych, którą można wykorzystać dalej w BI albo ML.

### 3. Kontrole jakości danych
Dodałem prostą warstwę quality checks, żeby projekt był bardziej zbliżony do realnego pipeline’u. Sprawdzane są m.in.:
- czy tabele nie są puste,
- czy klucze mają unikalne wartości tam, gdzie powinny,
- czy nie ma osieroconych rekordów w tabeli faktów,
- czy revenue nie schodzi poniżej zera.

### 4. Część ML
Na danych z warstwy gold trenuję prosty model forecastingu dziennego revenue.  
Model zapisuje predykcje do tabeli `sales_forecast`.

To nie jest projekt stricte badawczy, tylko bardziej pokazanie, jak można podpiąć model ML pod wcześniej przygotowaną hurtownię danych.

### 5. Raportowanie
Na końcu pipeline generuje:
- wykresy PNG,
- raport KPI w Markdown,
- gotowe artefakty, które można pokazać w repo albo wykorzystać w portfolio.

### 6. Prosty analytics assistant
Dodałem też aplikację Streamlit, która pozwala zadawać pytania o dane i KPI.  
Na ten moment działa to jako lekka warstwa analytics assistant oparta o lokalną logikę i definicje KPI, ale projekt jest przygotowany tak, żeby można go było łatwo rozwinąć np. o OpenAI API, RAG albo lokalny model.

---

## Architektura

```text
raw CSV -> bronze -> silver -> gold -> ML forecast -> KPI report -> Streamlit analytics assistant