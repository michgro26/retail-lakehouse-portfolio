from __future__ import annotations
from pathlib import Path
import re
import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

from retail_portfolio.config import DB_PATH


st.set_page_config(page_title='Retail Analytics Assistant', layout='wide')
st.title('Retail Analytics Assistant')
st.caption('Portfolio demo: warehouse + ML + analytics Q&A layer')

kpi_file = Path(__file__).with_name('kpi_definitions.md')
kpi_text = kpi_file.read_text(encoding='utf-8')

con = duckdb.connect(str(DB_PATH), read_only=True)
metrics = con.execute(
    '''
    SELECT date_key, revenue, orders_count, unique_customers, aov
    FROM daily_sales_metrics
    ORDER BY date_key
    '''
).df()


def retrieve_kpi_context(question: str) -> str:
    blocks = [b.strip() for b in kpi_text.split('\n## ') if b.strip()]
    q_terms = set(re.findall(r'[a-zA-Z_]+', question.lower()))
    scored = []
    for block in blocks:
        terms = set(re.findall(r'[a-zA-Z_]+', block.lower()))
        score = len(q_terms & terms)
        scored.append((score, block))
    scored.sort(reverse=True, key=lambda x: x[0])
    return '\n\n'.join(block for score, block in scored[:2] if score > 0) or kpi_text[:800]


def answer_question(question: str) -> tuple[str, pd.DataFrame | None]:
    q = question.lower()
    if 'aov' in q:
        avg_aov = metrics['aov'].mean()
        return f'AOV means average order value. In this dataset the average daily AOV is {avg_aov:,.2f}.\n\nContext:\n{retrieve_kpi_context(question)}', None
    if 'revenue' in q and ('trend' in q or 'over time' in q or 'daily' in q):
        return 'Here is the daily revenue trend from the gold layer.', metrics[['date_key', 'revenue']]
    if 'best day' in q or 'highest revenue' in q:
        row = metrics.sort_values('revenue', ascending=False).iloc[0]
        return f"The highest revenue day was {row['date_key']} with revenue {row['revenue']:,.2f}.", None
    if 'orders' in q:
        total_orders = int(metrics['orders_count'].sum())
        return f'Total completed orders in the warehouse: {total_orders:,}.', None
    if 'customers' in q:
        total_customers = int(metrics['unique_customers'].sum())
        return f'Total daily unique customers aggregated across all days: {total_customers:,}.', None
    if 'forecast' in q or 'prediction' in q:
        exists = con.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'sales_forecast'").fetchone()[0] > 0
        if exists:
            forecast = con.execute('SELECT * FROM sales_forecast ORDER BY date_key').df()
            latest = forecast.iloc[-1]
            return f"Latest forecast date is {latest['date_key']}. Predicted revenue: {latest['predicted_revenue']:,.2f}.", forecast
        return 'Forecast table is not available yet. Run the ML pipeline first.', None
    return (
        'I matched your question against KPI documentation and warehouse outputs. '\
        f"\n\nRelevant context:\n{retrieve_kpi_context(question)}\n\n"\
        'For a production version, this block can be replaced with OpenAI API or a local LLM plus SQL generation and evals.',
        None,
    )


left, right = st.columns([2, 1])

with left:
    st.subheader('Trend sprzedaży')
    fig = px.line(metrics, x='date_key', y='revenue', title='Daily Revenue')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('KPI definitions')
    st.markdown(kpi_text)

with right:
    st.subheader('Snapshot')
    st.metric('Revenue', f"{metrics['revenue'].sum():,.0f}")
    st.metric('Orders', f"{metrics['orders_count'].sum():,.0f}")
    st.metric('Unique customers', f"{metrics['unique_customers'].sum():,.0f}")

    question = st.text_area(
        'Ask a business question',
        placeholder='Np. What is AOV and how is it calculated? / Show revenue trend / What is the highest revenue day?',
        height=120,
    )

    if st.button('Generate answer'):
        if not question.strip():
            st.warning('Enter a question first.')
        else:
            answer, maybe_df = answer_question(question)
            st.markdown(answer)
            if maybe_df is not None and {'date_key', 'revenue'}.issubset(maybe_df.columns):
                st.plotly_chart(px.line(maybe_df, x='date_key', y='revenue', title='Requested view'), use_container_width=True)
            elif maybe_df is not None and {'date_key', 'actual_revenue', 'predicted_revenue'}.issubset(maybe_df.columns):
                chart_df = maybe_df.melt(id_vars=['date_key'], value_vars=['actual_revenue', 'predicted_revenue'])
                st.plotly_chart(px.line(chart_df, x='date_key', y='value', color='variable', title='Forecast vs actual'), use_container_width=True)

forecast_exists = con.execute(
    """
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_name = 'sales_forecast'
    """
).fetchone()[0] > 0

if forecast_exists:
    st.subheader('Forecast vs actual')
    forecast = con.execute('SELECT * FROM sales_forecast ORDER BY date_key').df()
    chart_df = forecast.melt(id_vars=['date_key'], value_vars=['actual_revenue', 'predicted_revenue'])
    fig2 = px.line(chart_df, x='date_key', y='value', color='variable', title='Actual vs Predicted Revenue')
    st.plotly_chart(fig2, use_container_width=True)
