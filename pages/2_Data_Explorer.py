import streamlit as st
import pandas as pd
import json
from datetime import date
import sys
import os
from utils import load_data

# Custom header
st.markdown("""
<style>
    .data-header {
        background: linear-gradient(135deg, #1cc88a 0%, #13855c 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .data-header h1 {
        color: white;
        margin-bottom: 0;
    }
</style>
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


st.title("🔍 Data Explorer Pro")

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
