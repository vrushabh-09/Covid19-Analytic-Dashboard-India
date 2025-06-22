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

# Enhanced CSS with gradient backgrounds
st.markdown("""
<style>
    /* Main Page Gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #e6f0ff 0%, #f8f9fa 100%);
    }

    /* Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #e9ecef 0%, #d1e0ff 100%) !important;
        border-right: 1px solid #ced4da;
    }

    /* Sidebar Header */
    [data-testid="stSidebar"] .sidebar-header {
        color: #212529;
        font-size: 1.25rem;
        font-weight: 600;
        padding: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #ced4da;
        background: rgba(255,255,255,0.7);
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

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        border-color: #dee2e6;
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e9ecef 0%, #d1e0ff 100%) !important;
        }
        
        .metric-card {
            padding: 16px;
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
        background: #adb5bd;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Main Content
st.title("🦠 COVID-19 Testing Analytics Dashboard")
st.markdown("""
<div style="background:#f0f2f6;padding:20px;border-radius:10px;margin-bottom:20px;">
    <h3 style="color:#2c3e50;">Advanced Analytics for India's Pandemic Response</h3>
    <p style="color:#7f8c8d;">Visualize testing trends, compare states, and export clean datasets.</p>
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
<small>
    Built with ♥ using Streamlit | Data Source: Ministry of Health & Family Welfare, India
</small>
""", unsafe_allow_html=True)
