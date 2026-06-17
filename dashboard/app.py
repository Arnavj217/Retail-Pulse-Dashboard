import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# =====================================================
# CUSTOM MODERN & HIGH-CONTRAST CSS (THEME-AWARE)
# =====================================================
sidebar_width = "250px" if st.session_state.sidebar_open else "70px"

st.markdown(f"""
<style>
/* Hide default boilerplate elements */
#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

/* High-contrast and reactive modern metric cards */
.metric-card {{
    background-color: var(--background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 15px;
}}

.metric-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
    border-color: #3B82F6;
}}

/* Bold Titles & Subtitles with stark contrast */
.dashboard-title {{
    font-size: 38px;
    font-weight: 800;
    color: var(--text-color);
    letter-spacing: -0.5px;
    margin-bottom: 5px;
}}

.dashboard-subtitle {{
    color: #3B82F6; /* High contrast energetic blue */
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 25px;
}}

/* Custom styled Large Sidebar Components */
.sidebar-title {{
    color: #FFFFFF !important;
    text-align: center;
    font-size: 34px; /* Increased size */
    font-weight: 800;
    letter-spacing: 0.5px;
}}

.sidebar-subtitle {{
    color: #60A5FA !important; /* Vivid light blue */
    text-align: center;
    font-size: 15px; /* Increased size */
    font-weight: 600;
    margin-top: 5px;
}}

/* Dynamic Sidebar Sizing */
[data-testid="stSidebar"] {{
    background-color:#1E293B !important;
    min-width:{sidebar_width} !important;
    max-width:{sidebar_width} !important;
    transition:all .35s ease;
}}

.main .block-container {{
    transition:all .35s ease;
}}

/* Enhancing Streamlit native Radio font sizing in Sidebar */
[data-testid="stSidebar"] .stRadio label {{
    font-size: 17px !important; /* Larger text for navigation */
    font-weight: 500 !important;
    color: #F3F4F6 !important;
    padding: 8px 0px;
}}

/* Status Indicator Colors */
.text-high-risk {{ color: #EF4444 !important; font-weight: bold; font-size: 20px; }}
.text-med-risk {{ color: #F59E0B !important; font-weight: bold; font-size: 20px; }}
.text-safe {{ color: #10B981 !important; font-weight: bold; font-size: 20px; }}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DATA LOADING (with error protection)
# =====================================================
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data"

@st.cache_data
def load_data():
    cleaned_df = pd.read_csv(DATA_PATH / "cleaned_retail.csv")
    segments = pd.read_csv(DATA_PATH / "customer_segments.csv")
    churn = pd.read_csv(DATA_PATH / "customer_churn.csv")
    forecast = pd.read_csv(DATA_PATH / "sales_forecast.csv")
    inventory = pd.read_csv(DATA_PATH / "inventory_recommendations.csv")

    cleaned_df["InvoiceDate"] = pd.to_datetime(cleaned_df["InvoiceDate"])

    return cleaned_df, segments, churn, forecast, inventory

# Load datasets
cleaned_df, segments, churn, forecast, inventory = load_data()

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
col1, col2 = st.columns([1, 15])

with col1:
    # Hamburger Button
    if st.button("☰"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

st.sidebar.markdown(
"""
<div class='sidebar-title'>📊 RetailPulse</div>
<br><hr style="border-color: rgba(255,255,255,0.15)">
""",
unsafe_allow_html=True
)

with st.sidebar:
    if st.session_state.sidebar_open:
        page = st.radio(
            "Navigation",
            [
                "🏠 Executive Summary",
                "📈 Sales Analytics",
                "👥 Customer Segmentation",
                "🔮 Demand Forecasting",
                "⚠️ Churn Prediction",
                "📦 Inventory Optimization"
            ]
        )
    else:
        page = st.radio(
            "",
            [
                "🏠",
                "📈",
                "👥",
                "🔮",
                "⚠️",
                "📦"
            ]
        )

    page_map = {
        "🏠": "🏠 Executive Summary",
        "📈": "📈 Sales Analytics",
        "👥": "👥 Customer Segmentation",
        "🔮": "🔮 Demand Forecasting",
        "⚠️": "⚠️ Churn Prediction",
        "📦": "📦 Inventory Optimization",
        "🏠 Executive Summary": "🏠 Executive Summary",
        "📈 Sales Analytics": "📈 Sales Analytics",
        "👥 Customer Segmentation": "👥 Customer Segmentation",
        "🔮 Demand Forecasting": "🔮 Demand Forecasting",
        "⚠️ Churn Prediction": "⚠️ Churn Prediction",
        "📦 Inventory Optimization": "📦 Inventory Optimization"
    }

    page = page_map[page]

    if st.session_state.sidebar_open:
        st.sidebar.markdown("""
        <div class='sidebar-subtitle'>AI-Powered Analytics Suite</div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style='text-align:center;font-size:30px'>
        📊
        </div>
        """, unsafe_allow_html=True)
        
    st.sidebar.markdown("<br><hr style='border-color: rgba(255,255,255,0.15)'>", unsafe_allow_html=True)
    st.sidebar.success("RetailPulse Engine Active🌍")

# Helper function to inject responsive Plotly template styles
def get_plotly_layout():
    return dict(
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================
if page == "🏠 Executive Summary":
    st.markdown("<div class='dashboard-title'>RetailPulse Hub</div><div class='dashboard-subtitle'>Enterprise Business Analytics Dashboard</div>", unsafe_allow_html=True)

    total_revenue = cleaned_df["Revenue"].sum()
    total_customers = cleaned_df["Customer ID"].nunique()
    total_orders = cleaned_df["Invoice"].nunique()
    total_countries = cleaned_df["Country"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px; text-transform:uppercase; font-weight:600;'>Total Revenue</p><h2 style='margin:5px 0 0 0; font-weight:800; color:#10B981;'>${total_revenue:,.0f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px; text-transform:uppercase; font-weight:600;'>Active Customers</p><h2 style='margin:5px 0 0 0; font-weight:800; color:#3B82F6;'>{total_customers:,}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px; text-transform:uppercase; font-weight:600;'>Processed Orders</p><h2 style='margin:5px 0 0 0; font-weight:800; color:#F59E0B;'>{total_orders:,}</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px; text-transform:uppercase; font-weight:600;'>Global Markets</p><h2 style='margin:5px 0 0 0; font-weight:800; color:#8B5CF6;'>{total_countries}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Line Chart
    monthly = cleaned_df.groupby(cleaned_df["InvoiceDate"].dt.to_period("M"))["Revenue"].sum().reset_index()
    monthly["InvoiceDate"] = monthly["InvoiceDate"].astype(str)
    
    fig = px.line(monthly, x="InvoiceDate", y="Revenue", markers=True, title="Monthly Revenue Momentum", template="plotly_dark" if st.get_option("theme.base") == "dark" else "ggplot2")
    fig.update_layout(height=400, **get_plotly_layout())
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    colA, colB = st.columns(2)

    with colA:
        top_country = cleaned_df.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index()
        fig_country = px.bar(top_country, x="Country", y="Revenue", title="Top 10 Global Revenue Contributors", color="Revenue", color_continuous_scale="Viridis")
        fig_country.update_layout(height=400, **get_plotly_layout())
        st.plotly_chart(fig_country, use_container_width=True)

    with colB:
        top_products = cleaned_df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index()
        fig_products = px.bar(top_products, y="Description", x="Revenue", title="Top 10 High-Performing Stock Items", orientation='h', color="Revenue", color_continuous_scale="Cividis")
        fig_products.update_layout(height=400, **get_plotly_layout())
        st.plotly_chart(fig_products, use_container_width=True)

# =====================================================
# SALES ANALYTICS PAGE
# =====================================================
elif page == "📈 Sales Analytics":
    st.markdown("<div class='dashboard-title'>Sales Analytics Suite</div><div class='dashboard-subtitle'>Deep Dive Revenue Performance Mapping</div>", unsafe_allow_html=True)

    country_filter = st.selectbox("🌎 Select Regional Filter Focus", ["All"] + sorted(cleaned_df["Country"].dropna().unique().tolist()))
    sales_df = cleaned_df.copy()

    if country_filter != "All":
        sales_df = sales_df[sales_df["Country"] == country_filter]

    sales_df["Month"] = sales_df["InvoiceDate"].dt.to_period("M").astype(str)
    monthly_sales = sales_df.groupby("Month")["Revenue"].sum().reset_index()

    fig_monthly = px.area(monthly_sales, x="Month", y="Revenue", title=f"Revenue Growth Curve: {country_filter}", markers=True)
    fig_monthly.update_layout(height=400, **get_plotly_layout())
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        country_sales = sales_df.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index()
        fig_country = px.bar(country_sales, x="Country", y="Revenue", title="Filtered Target Regional Sales", color_discrete_sequence=['#3B82F6'])
        fig_country.update_layout(height=380, **get_plotly_layout())
        st.plotly_chart(fig_country, use_container_width=True)

    with col2:
        product_sales = sales_df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index()
        fig_products = px.bar(product_sales, x="Revenue", y="Description", orientation='h', title="Filtered Top Generating Stock Elements", color_discrete_sequence=['#60A5FA'])
        fig_products.update_layout(height=380, **get_plotly_layout())
        st.plotly_chart(fig_products, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Granular Ledger (Top 100 Records)")
    st.dataframe(sales_df.head(100), use_container_width=True)

# =====================================================
# CUSTOMER SEGMENTATION PAGE
# =====================================================
elif page == "👥 Customer Segmentation":
    st.markdown("<div class='dashboard-title'>Customer Cohort Intelligence</div><div class='dashboard-subtitle'>Behavioral Profiling and Segment Structuring</div>", unsafe_allow_html=True)

    if "Segment" in segments.columns:
        segment_counts = segments["Segment"].value_counts()
        col1, col2 = st.columns(2)

        with col1:
            fig_segment = px.pie(values=segment_counts.values, names=segment_counts.index, hole=0.55, title="Cohort Share Ratios", color_discrete_sequence=px.colors.qualitative.Bold)
            fig_segment.update_layout(height=400, **get_plotly_layout())
            st.plotly_chart(fig_segment, use_container_width=True)

        with col2:
            fig_bar = px.bar(x=segment_counts.index, y=segment_counts.values, title="Cohort Total Volume Metrics", color=segment_counts.values, color_continuous_scale="Plasma")
            fig_bar.update_layout(height=400, **get_plotly_layout())
            st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("🎯 Average RFM Benchmark Key Metrics")

    if all(col in segments.columns for col in ["Recency", "Frequency", "Monetary"]):
        colA, colB, colC = st.columns(3)
        with colA:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px;'>Avg Recency (Days Out)</p><h2 style='margin:5px 0 0 0; color:#60A5FA;'>{segments['Recency'].mean():.1f} d</h2></div>", unsafe_allow_html=True)
        with colB:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px;'>Avg Frequency (Order Counts)</p><h2 style='margin:5px 0 0 0; color:#8B5CF6;'>{segments['Frequency'].mean():.1f} txn</h2></div>", unsafe_allow_html=True)
        with colC:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px;'>Avg Monetary Valuation</p><h2 style='margin:5px 0 0 0; color:#10B981;'>${segments['Monetary'].mean():,.2f}</h2></div>", unsafe_allow_html=True)

        st.write("<br>", unsafe_allow_html=True)
        fig_rfm = px.scatter(segments, x="Frequency", y="Monetary", color="Segment", size="Monetary", title="3-Dimensional RFM Behavioral Spread Mapping", hover_name="Segment", log_x=True)
        fig_rfm.update_layout(height=500, **get_plotly_layout())
        st.plotly_chart(fig_rfm, use_container_width=True)

    st.markdown("---")
    st.download_button(label="⬇️ Export Structural Cohort Dataset (CSV)", data=segments.to_csv(index=False), file_name="customer_segments.csv", mime="text/csv")
    st.dataframe(segments.head(100), use_container_width=True)

# =====================================================
# DEMAND FORECASTING PAGE
# =====================================================
elif page == "🔮 Demand Forecasting":
    st.markdown("<div class='dashboard-title'>Predictive Demand Engine</div><div class='dashboard-subtitle'>AI Machine Learning Multi-Day Forecast Framework</div>", unsafe_allow_html=True)

    if "yhat" in forecast.columns:
        forecast_total = round(forecast["yhat"].tail(30).sum())
        forecast_avg = round(forecast["yhat"].tail(30).mean())

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px;'>Forecast Accumulation (Next 30 Days)</p><h2 style='margin:5px 0 0 0; color:#8B5CF6;'>{forecast_total:,} Units</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px;'>Expected Baseline Daily Run-Rate</p><h2 style='margin:5px 0 0 0; color:#3B82F6;'>{forecast_avg:,} Units/Day</h2></div>", unsafe_allow_html=True)

    st.markdown("---")
    fig_forecast = px.line(forecast, x="ds", y="yhat", title="Forward Look: 30-Day Predictive Sales Path Trendline", labels={'ds': 'Date Timeline', 'yhat': 'Predicted Units Requested'})
    fig_forecast.update_traces(line_color='#8B5CF6', line_width=3)
    fig_forecast.update_layout(height=450, **get_plotly_layout())
    st.plotly_chart(fig_forecast, use_container_width=True)

    st.markdown("---")
    st.download_button(label="⬇️ Export Complete Demand Ledger File", data=forecast.to_csv(index=False), file_name="sales_forecast.csv", mime="text/csv")
    st.dataframe(forecast.tail(50), use_container_width=True)

# =====================================================
# CHURN PREDICTION PAGE
# =====================================================
elif page == "⚠️ Churn Prediction":
    st.markdown("<div class='dashboard-title'>At-Risk Churn Intelligence</div><div class='dashboard-subtitle'>Early Warning Mitigation Profiling Engine</div>", unsafe_allow_html=True)

    if "Churn_Probability" in churn.columns:
        risky = churn[churn["Churn_Probability"] > 0.80]
        medium = churn[(churn["Churn_Probability"] > 0.50) & (churn["Churn_Probability"] <= 0.80)]
        safe = churn[churn["Churn_Probability"] <= 0.50]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px; text-transform:uppercase;'>🔴 High Action Alert</p><h2 class='text-high-risk'>{len(risky)} Accounts</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px; text-transform:uppercase;'>🟠 Medium Retention Warning</p><h2 class='text-med-risk'>{len(medium)} Accounts</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px; text-transform:uppercase;'>🟢 Normalized Health Stable</p><h2 class='text-safe'>{len(safe)} Accounts</h2></div>", unsafe_allow_html=True)

        st.markdown("---")
        churn_chart = pd.DataFrame({
            "Risk Tier": ["Critical Churn Target", "Medium Attrition Risk", "Healthy Retention State"],
            "Volumetrics": [len(risky), len(medium), len(safe)]
        })

        fig_churn = px.pie(churn_chart, values="Volumetrics", names="Risk Tier", hole=0.5, color="Risk Tier", color_discrete_map={"Critical Churn Target": "#EF4444", "Medium Attrition Risk": "#F59E0B", "Healthy Retention State": "#10B981"}, title="Enterprise Health Stability Share Breakdown")
        fig_churn.update_layout(height=420, **get_plotly_layout())
        st.plotly_chart(fig_churn, use_container_width=True)

        st.markdown("---")
        st.subheader("🔴 Immediate Outreach Priorities: Critical Action Tracker")
        st.dataframe(risky.sort_values(by="Churn_Probability", ascending=False).head(100), use_container_width=True)
        st.download_button(label="⬇️ Export Complete Risk Assessment Report", data=churn.to_csv(index=False), file_name="customer_churn.csv", mime="text/csv")

# =====================================================
# INVENTORY OPTIMIZATION PAGE
# =====================================================
elif page == "📦 Inventory Optimization":
    st.markdown("<div class='dashboard-title'>Adaptive Stock Optimization</div><div class='dashboard-subtitle'>Algorithmic Procurement & Restocking Metrics</div>", unsafe_allow_html=True)

    if "ReorderQuantity" in inventory.columns:
        total_reorder = inventory["ReorderQuantity"].sum()
        max_reorder = inventory["ReorderQuantity"].max()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px;'>Target Pipeline Restock Cumulative Units</p><h2 style='margin:5px 0 0 0; color:#10B981;'>{round(total_reorder):,} Units</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><p style='margin:0; font-size:14px;'>Single-Item Peak Restock Limit Need</p><h2 style='margin:5px 0 0 0; color:#EF4444;'>{round(max_reorder):,} Units Max</h2></div>", unsafe_allow_html=True)

    st.markdown("---")
    fig_inventory = px.bar(inventory.sort_values(by="ReorderQuantity", ascending=False).head(30), x="StockCode", y="ReorderQuantity", title="Top 30 Urgent Procurement Directives", color="ReorderQuantity", color_continuous_scale="Turbo")
    fig_inventory.update_layout(height=450, **get_plotly_layout())
    st.plotly_chart(fig_inventory, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Recommended Replenishment Schedule Matrix")
    st.dataframe(inventory, use_container_width=True)
    st.download_button(label="⬇️ Export Strategic Procurement Manifest", data=inventory.to_csv(index=False), file_name="inventory_recommendations.csv", mime="text/csv")

# =====================================================
# HIGH-CONTRAST ENTERPRISE FOOTER
# =====================================================
st.markdown("<br><hr style='border-color: rgba(128,128,128,0.25)'><br>", unsafe_allow_html=True)
st.markdown(
"""
<div style='text-align: center;'>
    <h3 style='font-weight:700; letter-spacing:0.5px;'>📊 RetailPulse Enterprise Platform</h3>
    <p style='color: #3B82F6; font-size:14px; font-weight:600; margin-top:-5px;'>AI-Generated Operational Insights & Predictive Optimization Suite</p>
    <p style='font-size:12px; opacity:0.75;'>Engineered using Streamlit Architecture • Dynamic Plotly • Deep Learning Frameworks</p>
</div>
""",
unsafe_allow_html=True
)
