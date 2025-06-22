import streamlit as st
import pandas as pd
import json
from datetime import date
from utils import load_data

# Apply dark theme CSS
st.markdown("""
<style>
    /* ===== DARK THEME COLORS ===== */
    /* Base text color for all elements */
    body, .stApp, [data-testid="stAppViewContainer"], 
    [data-testid="stSidebar"], .stMarkdown, .stMarkdown p,
    .stMarkdown div, .stMarkdown span, .st-emotion-cache-10trblm {
        color: #e0e7ff !important;
    }
    
    /* Headings color */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .metric-card h3, .header-container h3,
    .st-emotion-cache-10trblm, .st-emotion-cache-16idsys {
        color: #ffffff !important;
    }
    
    /* Secondary text color */
    .stMarkdown p, .metric-card p, .header-container p,
    .footer, .stHelp, .stDateInput, .stSelectbox,
    .stRadio, .stMultiselect, .stMetricLabel,
    .st-emotion-cache-p5msec, .st-emotion-cache-q8sbsg {
        color: #a3b3cc !important;
    }

    /* ===== SPECIFIC ELEMENT STYLES ===== */
    /* Main Page Gradient - Dark Blue/Purple */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* Sidebar Gradient - Dark Blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 1px solid #2a3a5a;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebarNav"] ul {
        padding-left: 1rem;
    }
    
    [data-testid="stSidebarNav"] a {
        color: #e0e7ff !important;
        font-weight: 600;
        padding: 0.5rem 0;
        display: block;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        color: #ffffff !important;
        transform: translateX(3px);
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
    }

    /* Widget Containers */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiselect,
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] .stDateInput {
        background-color: rgba(26, 32, 58, 0.8);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 1.25rem;
        border: 1px solid #2a3a5a;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
    }

    /* Widget Labels */
    [data-testid="stSidebar"] label {
        color: #a3b3cc !important;
        font-weight: 600;
    }

    /* Widget Values */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stMultiselect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #e0e7ff !important;
    }

    /* Widget Hover Effects */
    [data-testid="stSidebar"] .stSelectbox:hover,
    [data-testid="stSidebar"] .stMultiselect:hover,
    [data-testid="stSidebar"] .stRadio:hover,
    [data-testid="stSidebar"] .stDateInput:hover {
        background-color: rgba(30, 38, 70, 0.9);
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        border-color: #3a4a7a;
    }

    /* Header Container - Dark Green Gradient */
    .data-header {
        background: linear-gradient(135deg, #1a5d38 0%, #0d3b22 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        border: 1px solid rgba(50, 150, 100, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .data-header h1 {
        color: #FFD700 !important;  /* Gold color for contrast */
        margin-bottom: 0;
        text-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
        font-size: 2.5rem;
        letter-spacing: 0.5px;
    }
    
    .data-header p {
        color: #c8f0d8 !important;
        margin-bottom: 0;
        font-size: 1.1rem;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(145deg, #1a5d38, #0d3b22) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(145deg, #2a6d48, #1d4b32) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4) !important;
    }

    /* Data Table Styling */
    .stDataFrame {
        background: rgba(20, 25, 45, 0.6) !important;
        border-radius: 10px;
        border: 1px solid rgba(80, 90, 150, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stDataFrame th {
        background: rgba(30, 35, 60, 0.8) !important;
        color: #ffffff !important;
    }
    
    .stDataFrame td {
        background: rgba(25, 30, 50, 0.6) !important;
        color: #e0e7ff !important;
    }
    
    .stDataFrame tr:hover {
        background: rgba(40, 45, 75, 0.7) !important;
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        }
        
        .data-header h1 {
            font-size: 2rem;
        }
    }

    /* Smooth Scrollbar */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 8px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: #0f1320;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: #3a4a7a;
        border-radius: 4px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {
        background: #4a5a8a;
    }
</style>
""", unsafe_allow_html=True)

# Custom header with contrasting h1 color
st.markdown("""
<div class="data-header">
    <h1>🔍 Data Explorer</h1>
    <p>Filter and export detailed testing data</p>
</div>
""", unsafe_allow_html=True)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# Load data
df = load_data()
if df.empty:
    st.stop()

# Sidebar Filters
st.sidebar.header("Data Filters")
state = st.sidebar.selectbox(
    "Select State",
    options=sorted(df['State'].unique()),
    index=10
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[df['Date'].min(), df['Date'].max()],
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Filter Data
filtered_data = df[
    (df['State'] == state) &
    (df['Date'].between(*date_range))
].sort_values('Date', ascending=False)

# Main Display
st.subheader(f"🧮 {state} Testing Data")
st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Date": st.column_config.DateColumn(format="YYYY-MM-DD"),
        "Positive": st.column_config.NumberColumn(format="%,d"),
        "TotalSamples": st.column_config.NumberColumn(format="%,d")
    }
)

# Export Options
st.subheader("📤 Export Data")
col1, col2 = st.columns(2)
with col1:
    st.download_button(
        label="💾 Download CSV",
        data=filtered_data.to_csv(index=False).encode('utf-8'),
        file_name=f"{state}_covid_data.csv",
        mime='text/csv'
    )
with col2:
    st.download_button(
        label="📥 Download JSON",
        data=json.dumps(
            filtered_data.to_dict(orient='records'),
            cls=DateTimeEncoder,
            indent=2
        ),
        file_name=f"{state}_covid_data.json",
        mime='application/json'
    )
