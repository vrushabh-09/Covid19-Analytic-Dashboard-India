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

# Dark theme CSS with gradient backgrounds
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
