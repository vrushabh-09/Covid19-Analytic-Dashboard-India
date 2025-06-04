# pages/1_Trend_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, filter_data

st.set_page_config(layout="wide")
st.title("📈 COVID-19 Testing Trends")

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
                template='plotly_white'
            )
            fig.update_layout(
                hovermode="x unified",
                xaxis_title="Date",
                yaxis_title=available_metrics[selected_metric]
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
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

            # Show data table
            st.dataframe(
                agg_df.style.format({
                    'Total': '{:,.0f}',
                    'Average': '{:,.2f}',
                    'Peak': '{:,.0f}'
                }),
                use_container_width=True
            )
        else:
            st.error("Selected metric cannot be aggregated numerically")
    else:
        st.warning("No data available for comparison")
