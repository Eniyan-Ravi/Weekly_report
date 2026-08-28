import streamlit as st
import sqlite3
import pandas as pd

connection = sqlite3.connect("data/warehouse/novacart.db")
# Dashboard title

st.set_page_config(page_title="Novacart",layout="wide")
st.title("Novacart")

#1. Total Revenue
query = """
SELECT SUM(net_revenue) AS total_revenue FROM fact_sales
"""

result = pd.read_sql_query(query,connection)
total_revenue = result["total_revenue"].iloc[0]

#-----------------------------------------------------------------------
#2. Return Rate
query_return_rate = """
SELECT AVG(is_returned) * 100 AS return_rate FROM fact_sales
"""

return_rate_df = pd.read_sql_query(query_return_rate,connection)
return_rate = (return_rate_df["return_rate"].iloc[0])

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Revenue",f"${total_revenue:,.2f}")
with col2:
    st.metric("Return Rate",f"{return_rate:.2f}%")
#----------------------------------------------------------------------------------------------
#3.Revenue by Price Tier
st.subheader("Revenue by Price Tier")

query_price_tier = """
SELECT price_tier, SUM(net_revenue) AS revenue FROM fact_sales
GROUP BY price_tier ORDER BY revenue DESC
"""

revenue_by_tier = pd.read_sql_query(query_price_tier,connection)
st.bar_chart(revenue_by_tier,x="price_tier",y="revenue")

#---------------------------------------------------------
#4.Revenue by Country
st.subheader("Revenue by Country")

query_country = """SELECT c.country, SUM(f.net_revenue) AS revenue FROM fact_sales AS f
JOIN dim_customers AS c ON f.customer_id = c.customer_id
GROUP BY c.country
ORDER BY revenue DESC
"""

revenue_by_country = pd.read_sql_query(query_country,connection)
st.bar_chart(revenue_by_country,x="country",y="revenue")

#-------------------------------------------------------------------------------------
#5.Revenue Over Time
st.subheader("Revenue Over Time")

query_revenue_time = """
SELECT order_date, SUM(net_revenue) AS revenue FROM fact_sales
GROUP BY order_date
ORDER BY order_date
"""

revenue_over_time = pd.read_sql_query(query_revenue_time,connection)
revenue_over_time["order_date"] = pd.to_datetime(revenue_over_time["order_date"])

st.line_chart(revenue_over_time,x="order_date",y="revenue")

connection.close()
