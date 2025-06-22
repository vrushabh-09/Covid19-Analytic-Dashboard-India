# Home.py (Main Entry)
# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime

# Config - Set first
st.set_page_config(
    page_title="COVID-19 Analytics Pro",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with consistent text colors
st.markdown("""
<style>
    /* Global Text Colors */
    body, .stApp, [data-testid="stAppViewContainer"], 
    [data-testid="stSidebar"], .stMarkdown, .stMarkdown p {
        color: #2c3e50 !important; /* Base text color */
    }
    
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .metric-card h3, .header-container h3,
    [data-testid="stSidebar"] .sidebar-title {
        color: #1a3d7c !important; /* Headings color */
    }
    
    .stMarkdown p, .metric-card p, .header-container p,
    .footer, .stMetric, .stHelp {
        color: #4a6580 !important; /* Secondary text color */
    }

    /* Main Page Gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #e0ebff 0%, #f5f9ff 100%);
    }

    /* Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #dde5f0 0%, #e9f0ff 100%) !important;
        border-right: 1px solid #ced4da;
    }

    /* Sidebar Title */
    [data-testid="stSidebar"] .sidebar-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }

    /* Widget Containers */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiselect,
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] .stDateInput {
        background-color: rgba(255,255,255,0.9);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 1.25rem;
        border: 1px solid #ced4da;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }

    /* Widget Labels */
    [data-testid="stSidebar"] label {
        color: #1a3d7c !important;
        font-weight: 600;
    }

    /* Widget Hover Effects */
    [data-testid="stSidebar"] .stSelectbox:hover,
    [data-testid="stSidebar"] .stMultiselect:hover,
    [data-testid="stSidebar"] .stRadio:hover,
    [data-testid="stSidebar"] .stDateInput:hover {
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #adb5bd;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f1f7ff 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card h3 {
        color: #1a3d7c !important;
        margin-top: 0;
    }

    .metric-card p {
        color: #4a6580 !important;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        border-color: #dee2e6;
    }

    /* Header Container */
    .header-container {
        background: linear-gradient(145deg, #e0ebff 0%, #d0e0ff 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #c6d4f5;
    }

    /* Footer Styling */
    .footer {
        color: #4a6580 !important;
    }

    /* Metric Values */
    .stMetric {
        color: #1a3d7c !important;
        font-weight: 700;
    }

    /* Help Text */
    .stHelp {
        color: #4a6580 !important;
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #dde5f0 0%, #e9f0ff 100%) !important;
        }
        
        .metric-card {
            padding: 16px;
        }
        
        [data-testid="stSidebar"] .sidebar-title {
            font-size: 1.25rem;
        }
    }

    /* Smooth Scrollbar */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: #f1f3f5;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: #a1b4d0;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Main Content
st.title("🦠 COVID-19 Testing Analytics Dashboard")
st.markdown("""
<div class="header-container">
    <h3>Advanced Analytics for India's Pandemic Response</h3>
    <p>Visualize testing trends, compare states, and export clean datasets.</p>
</div>
""", unsafe_allow_html=True)

# Metrics Overview
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total States Covered", "36", help="Includes all states/UTs")
with col2:
    st.metric("Data Timeframe", "2020-2021", help="Jan 2020 - Dec 2021")
with col3:
    st.metric("Last Updated", datetime.now().strftime(
        "%d %b %Y"), help="Auto-refreshes daily")

# Features Grid
st.subheader("🚀 Key Features")
features = [
    {"icon": "📈", "name": "Multi-State Trend Analysis",
        "desc": "Compare testing metrics across states"},
    {"icon": "🔍", "name": "Granular Data Explorer",
        "desc": "Filter by date ranges and states"},
    {"icon": "📊", "name": "Interactive Visualizations",
        "desc": "Hover-enabled charts"},
    {"icon": "💾", "name": "Data Export", "desc": "Download CSV/JSON"}
]

cols = st.columns(4)
for idx, feature in enumerate(features):
    with cols[idx]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{feature['icon']} {feature['name']}</h3>
            <p>{feature['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<small class="footer">
    Built with ♥ using Streamlit | Data Source: Ministry of Health & Family Welfare, India
</small>
""", unsafe_allow_html=True)
