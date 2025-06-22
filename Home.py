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

# Custom CSS for Pro UI with gradient backgrounds
st.markdown("""
<style>
    /* Full Page Gradient Background */
    body {
        background: linear-gradient(135deg, #f0f2f6, #dfe9f3);
    }
    .block-container {
        background: linear-gradient(135deg, #f0f4f8, #f5f7fa);
        padding: 2rem 2rem 2rem 2rem;
        border-radius: 12px;
    }

    /* Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #dbeafe 0%, #f0f4f8 50%, #e0e7ff 100%);
        border-right: 1px solid #cbd5e1;
    }

    /* Sidebar Header */
    [data-testid="stSidebar"] .sidebar-header {
        color: #1e293b;
        font-size: 1.25rem;
        font-weight: 600;
        padding: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #cbd5e1;
        background: rgba(255,255,255,0.75);
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
        border: 1px solid #94a3b8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }

    /* Widget Hover Effects */
    [data-testid="stSidebar"] .stSelectbox:hover,
    [data-testid="stSidebar"] .stMultiselect:hover,
    [data-testid="stSidebar"] .stRadio:hover,
    [data-testid="stSidebar"] .stDateInput:hover {
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #60a5fa;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
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
            background: linear-gradient(180deg, #f0f4f8 0%, #e0e7ff 100%);
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
        background: #94a3b8;
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
    st.metric("Last Updated", datetime.now().strftime("%d %b %Y"), help="Auto-refreshes daily")

# Features Grid
st.subheader("🚀 Key Features")
features = [
    {"icon": "📈", "name": "Multi-State Trend Analysis", "desc": "Compare testing metrics across states"},
    {"icon": "🔍", "name": "Granular Data Explorer", "desc": "Filter by date ranges and states"},
    {"icon": "📊", "name": "Interactive Visualizations", "desc": "Hover-enabled charts"},
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
