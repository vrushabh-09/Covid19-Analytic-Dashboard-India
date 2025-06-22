# pages/1_Trend_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, filter_data

st.set_page_config(layout="wide")
st.title("📈 COVID-19 Testing Trends")

# Apply the same dark theme CSS as home page
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

    /* Metric Cards - Glassmorphism Effect */
    .metric-card {
        background: rgba(30, 30, 60, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border: 1px solid rgba(100, 100, 200, 0.2);
        transition: all 0.3s ease;
    }

    .metric-card h3 {
        color: #ffffff !important;
        margin-top: 0;
        font-size: 1.2rem;
    }

    .metric-card p {
        color: #a3b3cc !important;
        margin-bottom: 0;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        background: rgba(40, 40, 80, 0.5);
        border-color: rgba(120, 120, 220, 0.3);
    }

    /* Header Container */
    .header-container {
        background: rgba(20, 25, 45, 0.6);
        backdrop-filter: blur(5px);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid rgba(80, 90, 150, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .header-container h3 {
        color: #ffffff !important;
        margin-top: 0;
    }

    .header-container p {
        color: #a3b3cc !important;
        margin-bottom: 0;
    }

    /* Footer Styling */
    .footer {
        color: #a3b3cc !important;
    }

    /* Metric Values */
    .stMetric {
        color: #ffffff !important;
        font-weight: 700;
        font-size: 1.5rem !important;
        text-shadow: 0 0 10px rgba(100, 150, 255, 0.5);
    }

    /* Metric Labels */
    .stMetricLabel {
        color: #a3b3cc !important;
        font-size: 0.9rem !important;
        font-weight: 600;
    }

    /* Help Text */
    .stHelp {
        color: #7987a5 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(145deg, #3a3a8a, #2a2a6a) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(145deg, #4a4a9a, #3a3a7a) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4) !important;
    }

    /* Tabs Styling */
    .stTabs [role="tablist"] {
        background: rgba(20, 25, 45, 0.6) !important;
        border-radius: 8px;
        padding: 5px;
        margin-bottom: 1rem;
    }
    
    .stTabs [role="tab"] {
        background: transparent !important;
        color: #a3b3cc !important;
        border: none !important;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(145deg, #3a3a8a, #2a2a6a) !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    
    .stTabs [role="tab"]:hover {
        background: rgba(40, 40, 80, 0.4) !important;
        color: #ffffff !important;
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
        
        .metric-card {
            padding: 16px;
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

# Load data with progress indicator
with st.spinner('Loading data...'):
    df = load_data()
    if df.empty:
        st.error("No valid data available. Please check your data file.")
        st.stop()

# Sidebar Filters
st.sidebar.header("Filter Options")
available_states = sorted(df['State'].dropna().unique())
states = st.sidebar.multiselect(
    "Select States",
    options=available_states,
    default=available_states[:3],
    help="Select states to compare"
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=[df['Date'].min(), df['Date'].max()],
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Metric selection with availability check
available_metrics = {
    'TotalSamples': 'Total Samples',
    'Positive': 'Positive Cases',
    'Negative': 'Negative Cases',
    'PositiveRatio': 'Positive Rate'
}
selected_metric = st.sidebar.selectbox(
    "Select Metric",
    options=list(available_metrics.keys()),
    format_func=lambda x: available_metrics[x]
)

# Data Processing
filtered_df = filter_data(df, states, date_range)

# Visualization Tabs
tab1, tab2 = st.tabs(["Trend Analysis", "State Comparison"])

with tab1:
    if not filtered_df.empty:
        # Drop rows where selected metric is NA
        plot_df = filtered_df.dropna(subset=[selected_metric])

        if not plot_df.empty:
            fig = px.line(
                plot_df,
                x='Date',
                y=selected_metric,
                color='State',
                title=f"{available_metrics[selected_metric]} Over Time",
                labels={selected_metric: available_metrics[selected_metric]},
                height=600,
                template='plotly_dark'  # Use dark theme for plotly
            )
            fig.update_layout(
                hovermode="x unified",
                xaxis_title="Date",
                yaxis_title=available_metrics[selected_metric],
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e7ff')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(
                f"No valid {available_metrics[selected_metric]} data for selected filters")
    else:
        st.warning("No data available for selected filters")

with tab2:
    if not filtered_df.empty:
        # Ensure we have valid numeric data
        if pd.api.types.is_numeric_dtype(filtered_df[selected_metric]):
            agg_df = filtered_df.groupby('State', observed=True).agg(
                Total=pd.NamedAgg(column=selected_metric, aggfunc='sum'),
                Average=pd.NamedAgg(column=selected_metric, aggfunc='mean'),
                Peak=pd.NamedAgg(column=selected_metric, aggfunc='max')
            ).reset_index()

            fig = px.bar(
                agg_df,
                x='State',
                y='Total',
                color='State',
                title=f"Total {available_metrics[selected_metric]} by State",
                text_auto='.2s',
                height=500,
                template='plotly_dark'  # Use dark theme for plotly
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e7ff')
            )
            st.plotly_chart(fig, use_container_width=True)

            # Show data table
            st.dataframe(
                agg_df.style.format({
                    'Total': '{:,.0f}',
                    'Average': '{:,.2f}',
                    'Peak': '{:,.0f}'
                }).applymap(lambda x: 'color: #e0e7ff'),
                use_container_width=True
            )
        else:
            st.error("Selected metric cannot be aggregated numerically")
    else:
        st.warning("No data available for comparison")
