import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

# -- Load the dataset safely --
@st.cache_data
def load_data():
    return pd.read_csv("DF_cleaned_data.csv", parse_dates=["date"])

# Load data
try:
    df = load_data()
    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# -- UI Title --
st.title("📊 Item Family Statistics Dashboard")
st.markdown("Analyze sales trends for a selected item family over the past week.")

# -- Required columns check --
required_columns = {"item_family", "date", "price", "is_holiday"}
if not required_columns.issubset(df.columns):
    st.error(f"❌ The dataset must include columns: {required_columns}")
    st.stop()

# -- Date filtering: last 7 days --
latest_date = df["date"].max()
one_week_ago = latest_date - timedelta(days=7)

# -- Required Input: item_family --
item_families = df["item_family"].dropna().unique()
item_family = st.selectbox("Select Item Family:", sorted(item_families))

# -- Sidebar Filters --
st.sidebar.header("🔎 Filter Options")

# Holiday Type filter
holiday_type_options = ["All", "Holiday Type 0", "Holiday Type 1", "Holiday Type 2"]
selected_holiday_type = st.sidebar.selectbox("Holiday Type:", holiday_type_options)

# Sales on Promotion filter
sales_on_promotion_options = ["All", "On Promotion", "Not on Promotion"]
selected_sales_on_promotion = st.sidebar.selectbox("Sales on Promotion:", sales_on_promotion_options)

# Store Type filter
store_type_options = ["All", "Store Type 0", "Store Type 1", "Store Type 2"]
selected_store_type = st.sidebar.selectbox("Store Type:", store_type_options)

# -- Apply core filters --
filtered_df = df[(df["item_family"] == item_family) & (df["date"] >= one_week_ago)]

# Apply holiday type filter
if selected_holiday_type != "All":
    filtered_df = filtered_df[filtered_df[f"holiday_type_{selected_holiday_type.split()[-1]}"] == 1]

# Apply sales on promotion filter
if selected_sales_on_promotion == "On Promotion":
    filtered_df = filtered_df[filtered_df["onpromotion"] == 1]
elif selected_sales_on_promotion == "Not on Promotion":
    filtered_df = filtered_df[filtered_df["onpromotion"] == 0]

# Apply store type filter
if selected_store_type != "All":
    filtered_df = filtered_df[filtered_df[f"store_type_{selected_store_type.split()[-1]}"] == 1]

# -- Display Results --
if not filtered_df.empty:
    st.subheader(f"📈 Summary for '{item_family}' (Last 7 Days)")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Unique Dates", filtered_df["date"].nunique())
    with col2:
        st.metric("Average Price", f"${filtered_df['price'].mean():.2f}")
    with col3:
        st.metric("Total Records", len(filtered_df))

    # -- Line Chart: Average Price --
    price_trend = filtered_df.groupby(filtered_df["date"].dt.date)["price"].mean().reset_index()
    fig = px.line(price_trend, x="date", y="price", title="📉 Average Price Trend (Last 7 Days)")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No records found with the selected filters for the past 7 days.")
