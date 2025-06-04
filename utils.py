# utils.py
import pandas as pd
import streamlit as st
import numpy as np
from datetime import date
from typing import Tuple, List


@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    """Load and preprocess COVID-19 testing data with empty cell handling"""
    try:
        # Read CSV with explicit NA values handling
        df = pd.read_csv(
            "StatewiseTestingDetails.csv",
            na_values=['', 'None', 'none', 'NONE',
                       'null', 'NULL', 'NaN', 'nan', ' ', '-'],
            keep_default_na=True
        )

        # Convert date and handle invalid dates
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
        df = df.dropna(subset=['Date', 'State'])

        # Process numeric columns
        numeric_cols = ['TotalSamples', 'Negative', 'Positive']
        for col in numeric_cols:
            if col in df.columns:
                # Ensure numeric type and non-negative
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].clip(lower=0)  # Replace negatives with 0

        # Calculate PositiveRatio safely
        if all(col in df.columns for col in ['Positive', 'TotalSamples']):
            df['PositiveRatio'] = np.where(
                (df['TotalSamples'] > 0) & df['Positive'].notna(),
                df['Positive'] / df['TotalSamples'],
                np.nan
            ).round(4)

        return df

    except FileNotFoundError:
        st.error(
            "❌ Data file not found. Please ensure 'StatewiseTestingDetails.csv' exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()


def filter_data(
    df: pd.DataFrame,
    states: List[str],
    date_range: Tuple[date, date]
) -> pd.DataFrame:
    """Filter data by states and date range"""
    try:
        if df.empty:
            return pd.DataFrame()

        if not states:
            states = df['State'].unique().tolist()

        return df[
            (df['State'].isin(states)) &
            (df['Date'].between(*date_range))
        ].sort_values('Date')

    except Exception as e:
        st.error(f"❌ Filtering error: {str(e)}")
        return pd.DataFrame()
