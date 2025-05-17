import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

# --- Inject Live Background (Particles.js) ---
st.markdown("""
    <style>
    /* Ensure full transparency for the body */
    body {
        margin: 0;
        padding: 0;
        background: transparent !important;
    }

    /* Make the particles.js background fixed and full-screen */
    #particles-js {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        background-color: transparent !important;
    }

    /* Set the background of HTML and body elements to transparent */
    html, body, [class*="css"] {
        background-color: transparent !important;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }

    /* Transparent Streamlit main container */
    .stApp {
        background: transparent !important;
    }

    /* Styling headings */
    h1, h2, h3, .stTitle, .stHeader {
        color: #00bcd4 !important;
    }

    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #00ffff, #00bcd4);
        color: #121212;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 255, 255, 0.2);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #00bcd4, #00ffff);
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 255, 255, 0.3);
    }

    /* Sidebar styling */
    .stSidebar {
        background-color: transparent !important;
    }

    /* Hide default footer, header, and menu */
    footer, header, #MainMenu {
        visibility: hidden;
    }
    </style>

    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script>
    window.addEventListener('load', () => {
        particlesJS("particles-js", {
            "particles": {
                "number": {"value": 80,"density": {"enable": true,"value_area": 800}},
                "color": {"value": "#00bcd4"},
                "shape": {"type": "circle"},
                "opacity": {"value": 0.5,"random": true},
                "size": {"value": 3,"random": true},
                "line_linked": {"enable": true,"distance": 150,"color": "#00bcd4","opacity": 0.4,"width": 1},
                "move": {"enable": true,"speed": 2,"out_mode": "out"}
            },
            "interactivity": {
                "events": {"onhover": {"enable": true,"mode": "grab"}},
                "modes": {"grab": {"distance": 140,"line_linked": {"opacity": 1}}}
            },
            "retina_detect": true
        });
    });
    </script>
""", unsafe_allow_html=True)

# --- Load and Cache Data ---
@st.cache_data
def load_data():
    return pd.read_csv("DF_cleaned_data.csv", parse_dates=["date"])

try:
    df = load_data()
    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# --- UI Title ---
st.title("📊 Item Family Statistics Dashboard")
st.markdown("Analyze sales trends for a selected item family over the past week.")

# --- Required Columns Check ---
required_columns = {"item_family", "date", "price", "is_holiday"}
if not required_columns.issubset(df.columns):
    st.error(f"❌ The dataset must include columns: {required_columns}")
    st.stop()

# --- Date Filtering (Last 7 Days) ---
latest_date = df["date"].max()
one_week_ago = latest_date - timedelta(days=7)

# --- Item Family Dropdown ---
item_families = df["item_family"].dropna().unique()
item_family = st.selectbox("Select Item Family:", sorted(item_families))

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Options")

# Holiday Type Filter
holiday_type_options = ["All", "Holiday Type 0", "Holiday Type 1", "Holiday Type 2"]
selected_holiday_type = st.sidebar.selectbox("Holiday Type:", holiday_type_options)

# Sales on Promotion Filter
sales_on_promotion_options = ["All", "On Promotion", "Not on Promotion"]
selected_sales_on_promotion = st.sidebar.selectbox("Sales on Promotion:", sales_on_promotion_options)

# Store Type Filter
store_type_options = ["All", "Store Type 0", "Store Type 1", "Store Type 2"]
selected_store_type = st.sidebar.selectbox("Store Type:", store_type_options)

# --- Apply Filters ---
filtered_df = df[(df["item_family"] == item_family) & (df["date"] >= one_week_ago)]

if selected_holiday_type != "All":
    filtered_df = filtered_df[filtered_df[f"holiday_type_{selected_holiday_type.split()[-1]}"] == 1]

if selected_sales_on_promotion == "On Promotion":
    filtered_df = filtered_df[filtered_df["onpromotion"] == 1]
elif selected_sales_on_promotion == "Not on Promotion":
    filtered_df = filtered_df[filtered_df["onpromotion"] == 0]

if selected_store_type != "All":
    filtered_df = filtered_df[filtered_df[f"store_type_{selected_store_type.split()[-1]}"] == 1]

# --- Show Output ---
if not filtered_df.empty:
    st.subheader(f"📈 Summary for '{item_family}' (Last 7 Days)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Unique Dates", filtered_df["date"].nunique())
    with col2:
        st.metric("Average Price", f"${filtered_df['price'].mean():.2f}")
    with col3:
        st.metric("Total Records", len(filtered_df))

    # --- Line Chart ---
    price_trend = filtered_df.groupby(filtered_df["date"].dt.date)["price"].mean().reset_index()
    fig = px.line(price_trend, x="date", y="price", title="📉 Average Price Trend (Last 7 Days)")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No records found with the selected filters for the past 7 days.")
