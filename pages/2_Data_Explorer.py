# pages/2_Data_Explorer.py
import streamlit as st
import pandas as pd
import json
import numpy as np
from datetime import date
from utils import load_data

st.set_page_config(
    page_title="Data Explorer",
    page_icon="🔍",
    layout="wide"
)

# Apply dark theme CSS (consistent with homepage)
st.markdown("""
<style>
    /* ===== DARK THEME COLORS ===== */
    body, .stApp, [data-testid="stAppViewContainer"], 
    [data-testid="stSidebar"], .stMarkdown, .stMarkdown p,
    .stMarkdown div, .stMarkdown span, .st-emotion-cache-10trblm {
        color: #e0e7ff !important;
    }
    
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #ffffff !important;
    }
    
    .stMarkdown p, .metric-card p, .header-container p {
        color: #a3b3cc !important;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid #2a3a5a;
    }
    
    .data-header {
        background: linear-gradient(135deg, #1a5d38 0%, #0d3b22 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        border: 1px solid rgba(50, 150, 100, 0.3);
    }
    
    .data-header h1 {
        color: #FFD700 !important;
        margin-bottom: 0;
        font-size: 2.5rem;
    }
    
    .stDataFrame {
        background: rgba(20, 25, 45, 0.6) !important;
        border-radius: 10px;
        border: 1px solid rgba(80, 90, 150, 0.3) !important;
    }
    
    .stDataFrame th {
        background: rgba(30, 35, 60, 0.8) !important;
        color: #ffffff !important;
    }
    
    .stDataFrame td {
        background: rgba(25, 30, 50, 0.6) !important;
        color: #e0e7ff !important;
    }
    
    .stButton>button {
        background: linear-gradient(145deg, #1a5d38, #0d3b22) !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(145deg, #2a6d48, #1d4b32) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
<div class="data-header">
    <h1>🔍 Data Explorer</h1>
    <p>Filter, explore, and export detailed COVID-19 testing data</p>
</div>
""", unsafe_allow_html=True)

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for date serialization"""
    def default(self, obj):
        if isinstance(obj, (date, pd.Timestamp)):
            return obj.isoformat()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# Load data with caching
@st.cache_data
def load_cached_data():
    return load_data()

# Load and display data info
with st.spinner('Loading data...'):
    df = load_cached_data()
    
if df.empty:
    st.error("❌ No data available. Please check the data file.")
    st.stop()

# Display data overview
st.subheader("📊 Data Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", f"{len(df):,}")
with col2:
    st.metric("States/UTs", f"{df['State'].nunique()}")
with col3:
    st.metric("Date Range", f"{df['Date'].min()} to {df['Date'].max()}")
with col4:
    total_samples = df['TotalSamples'].sum() if 'TotalSamples' in df.columns else 0
    st.metric("Total Samples", f"{total_samples:,}")

# Sidebar Filters
st.sidebar.header("🔧 Filter Options")

# State selection
state_options = sorted(df['State'].dropna().unique())
selected_state = st.sidebar.selectbox(
    "Select State",
    options=state_options,
    index=0,
    help="Choose a state/UT to analyze"
)

# Date range selection
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[df['Date'].min(), df['Date'].max()],
    min_value=df['Date'].min(),
    max_value=df['Date'].max(),
    help="Select start and end dates"
)

# Additional filters
st.sidebar.subheader("Additional Filters")

# Positive cases filter
if 'Positive' in df.columns:
    positive_min, positive_max = st.sidebar.slider(
        "Positive Cases Range",
        min_value=int(df['Positive'].min()),
        max_value=int(df['Positive'].max()),
        value=(int(df['Positive'].min()), int(df['Positive'].max())),
        help="Filter by number of positive cases"
    )

# Show sample count
st.sidebar.markdown("---")
st.sidebar.info(f"**Available Records:** {len(df)}")

# Filter Data
try:
    filtered_data = df[
        (df['State'] == selected_state) &
        (df['Date'].between(*date_range))
    ]
    
    if 'Positive' in df.columns:
        filtered_data = filtered_data[
            (filtered_data['Positive'] >= positive_min) &
            (filtered_data['Positive'] <= positive_max)
        ]
    
    filtered_data = filtered_data.sort_values('Date', ascending=False)
    
    # Display filtered results summary
    st.subheader(f"📋 {selected_state} - Filtered Results")
    
    if filtered_data.empty:
        st.warning(f"No data found for {selected_state} in the selected date range.")
    else:
        # Show summary metrics
        st.info(f"**Found {len(filtered_data)} records** from {filtered_data['Date'].min()} to {filtered_data['Date'].max()}")
        
        # Display data table
        st.dataframe(
            filtered_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.DateColumn(
                    format="YYYY-MM-DD",
                    help="Test date"
                ),
                "State": st.column_config.TextColumn(
                    help="State/Union Territory"
                ),
                "TotalSamples": st.column_config.NumberColumn(
                    format="%,d",
                    help="Total samples tested"
                ),
                "Positive": st.column_config.NumberColumn(
                    format="%,d",
                    help="Positive cases detected"
                ),
                "Negative": st.column_config.NumberColumn(
                    format="%,d",
                    help="Negative test results"
                ),
                "PositiveRatio": st.column_config.NumberColumn(
                    format="%.4f",
                    help="Positive ratio (Positive/TotalSamples)"
                )
            },
            height=400
        )
        
        # Export Options
        st.subheader("📤 Export Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = filtered_data.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"{selected_state}_covid_data_{date_range[0]}_to_{date_range[1]}.csv",
                mime="text/csv",
                help="Download filtered data as CSV file"
            )
        
        with col2:
            json_data = json.dumps(
                filtered_data.to_dict(orient='records'),
                cls=DateTimeEncoder,
                indent=2
            )
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"{selected_state}_covid_data_{date_range[0]}_to_{date_range[1]}.json",
                mime="application/json",
                help="Download filtered data as JSON file"
            )
        
        with col3:
            # Statistics summary
            stats_summary = {
                "state": selected_state,
                "date_range": f"{date_range[0]} to {date_range[1]}",
                "total_records": len(filtered_data),
                "total_samples": int(filtered_data['TotalSamples'].sum()),
                "total_positive": int(filtered_data['Positive'].sum()),
                "total_negative": int(filtered_data['Negative'].sum()),
                "avg_positivity": float(filtered_data['PositiveRatio'].mean()),
                "max_daily_samples": int(filtered_data['TotalSamples'].max()),
                "min_daily_samples": int(filtered_data['TotalSamples'].min()),
                "data_generated": str(date.today())
            }
            
            stats_json = json.dumps(stats_summary, indent=2, cls=DateTimeEncoder)
            st.download_button(
                label="📊 Download Summary Stats",
                data=stats_json,
                file_name=f"{selected_state}_stats_summary.json",
                mime="application/json",
                help="Download summary statistics"
            )
        
        # Display quick statistics
        st.subheader("📈 Quick Statistics")
        
        if len(filtered_data) > 1:
            cols = st.columns(4)
            with cols[0]:
                st.metric(
                    "Avg Daily Samples",
                    f"{filtered_data['TotalSamples'].mean():,.0f}"
                )
            with cols[1]:
                st.metric(
                    "Avg Daily Positive",
                    f"{filtered_data['Positive'].mean():,.0f}"
                )
            with cols[2]:
                st.metric(
                    "Peak Positivity Day",
                    filtered_data.loc[filtered_data['PositiveRatio'].idxmax(), 'Date'].strftime("%b %d, %Y")
                    if 'PositiveRatio' in filtered_data.columns else "N/A"
                )
            with cols[3]:
                st.metric(
                    "Max Daily Positive",
                    f"{filtered_data['Positive'].max():,.0f}"
                )
        
        # Data preview in different formats
        with st.expander("👁️ Data Preview", expanded=False):
            tab1, tab2, tab3 = st.tabs(["Raw Data", "Top 10 Days", "Monthly Aggregation"])
            
            with tab1:
                st.dataframe(filtered_data.head(20), use_container_width=True)
            
            with tab2:
                top_days = filtered_data.nlargest(10, 'Positive')
                st.dataframe(top_days[['Date', 'TotalSamples', 'Positive', 'Negative', 'PositiveRatio']], 
                           use_container_width=True)
            
            with tab3:
                if len(filtered_data) > 30:
                    # Create monthly aggregation
                    filtered_data['Month'] = pd.to_datetime(filtered_data['Date']).dt.to_period('M')
                    monthly_stats = filtered_data.groupby('Month').agg({
                        'TotalSamples': 'sum',
                        'Positive': 'sum',
                        'Negative': 'sum'
                    }).reset_index()
                    monthly_stats['Month'] = monthly_stats['Month'].astype(str)
                    monthly_stats['PositiveRatio'] = monthly_stats['Positive'] / monthly_stats['TotalSamples']
                    st.dataframe(monthly_stats, use_container_width=True)
        
except Exception as e:
    st.error(f"❌ Error processing data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<small style="color: #a3b3cc;">
    💡 Tip: Use the sidebar filters to narrow down your data. Export options are available below the table.
</small>
""", unsafe_allow_html=True)
