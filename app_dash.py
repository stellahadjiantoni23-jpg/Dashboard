import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sales.csv", parse_dates=["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

df_filtered = df[
    (df["year"].isin(year_filter)) &
    (df["category"].isin(category_filter))
]

# -----------------------------
# KPIs
# -----------------------------
total_revenue = df_filtered["revenue"].sum()
total_units = df_filtered["units_sold"].sum()
avg_order_value = df_filtered["revenue"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"£{total_revenue:,.0f}")
col2.metric("Units Sold", f"{total_units:,}")
col3.metric("Avg Order Value", f"£{avg_order_value:,.2f}")

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------

# Revenue over time
rev_trend = df_filtered.groupby("month")["revenue"].sum().reset_index()
fig_trend = px.line(rev_trend, x="month", y="revenue", title="Monthly Revenue Trend")

# Revenue by category
rev_cat = df_filtered.groupby("category")["revenue"].sum().reset_index()
fig_cat = px.bar(rev_cat, x="category", y="revenue", title="Revenue by Category")

# Top products
top_products = df_filtered.groupby("product")["revenue"].sum().nlargest(10).reset_index()
fig_top = px.bar(top_products, x="revenue", y="product", orientation="h", title="Top 10 Products")

# Layout
col4, col5 = st.columns(2)
col4.plotly_chart(fig_trend, use_container_width=True)
col5.plotly_chart(fig_cat, use_container_width=True)

st.plotly_chart(fig_top, use_container_width=True)
