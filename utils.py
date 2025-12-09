# utils.py (Complete Version)
import pandas as pd
import streamlit as st
import numpy as np
from datetime import date, datetime
from typing import Tuple, List, Dict, Any
import warnings
warnings.filterwarnings('ignore')

@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    """Load and preprocess COVID-19 testing data with comprehensive cleaning"""
    try:
        # Read CSV with explicit NA values handling
        df = pd.read_csv(
            "StatewiseTestingDetails.csv",
            na_values=['', 'None', 'none', 'NONE',
                       'null', 'NULL', 'NaN', 'nan', ' ', '-', 'NA'],
            keep_default_na=True,
            encoding='utf-8'
        )
        
        # Standardize column names
        df.columns = df.columns.str.strip().str.replace(' ', '').str.replace('-', '')
        
        # Rename columns to standard format
        column_mapping = {
            'State': 'State',
            'Date': 'Date',
            'TotalSamples': 'TotalSamples',
            'Negative': 'Negative',
            'Positive': 'Positive',
            'positive': 'Positive',
            'negative': 'Negative',
            'totalsamples': 'TotalSamples',
            'state': 'State',
            'date': 'Date',
            'total': 'TotalSamples'
        }
        
        df = df.rename(columns={col: column_mapping.get(col, col) for col in df.columns})
        
        # Ensure required columns exist
        required_columns = ['State', 'Date', 'TotalSamples', 'Negative', 'Positive']
        for col in required_columns:
            if col not in df.columns:
                # Try to find similar columns
                possible_matches = [c for c in df.columns if col.lower() in c.lower()]
                if possible_matches:
                    df = df.rename(columns={possible_matches[0]: col})
                else:
                    # Create placeholder column if missing
                    df[col] = np.nan
        
        # Convert date column with error handling
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            # Drop rows with invalid dates
            df = df.dropna(subset=['Date'])
            # Convert to date only
            df['Date'] = df['Date'].dt.date
        
        # Clean State names
        if 'State' in df.columns:
            df['State'] = df['State'].astype(str).str.strip().str.title()
            # Remove invalid state names
            invalid_states = ['Nan', 'Na', 'None', 'Null', '', ' ', 'Unknown', 'Unspecified']
            df = df[~df['State'].isin(invalid_states)]
        
        # Process numeric columns
        numeric_cols = ['TotalSamples', 'Negative', 'Positive']
        for col in numeric_cols:
            if col in df.columns:
                # Convert to string first to handle various formats
                df[col] = df[col].astype(str)
                # Remove commas, spaces, and other non-numeric characters
                df[col] = df[col].str.replace(',', '').str.replace(' ', '')
                # Convert to numeric, forcing errors to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Replace negative values with 0
                df[col] = df[col].clip(lower=0)
                # Fill NaN with 0 for counts
                df[col] = df[col].fillna(0).astype(int)
        
        # Calculate PositiveRatio safely
        if all(col in df.columns for col in ['Positive', 'TotalSamples']):
            df['PositiveRatio'] = np.where(
                (df['TotalSamples'] > 0) & (df['Positive'].notna()),
                df['Positive'] / df['TotalSamples'],
                0
            ).round(4)
        
        # Remove duplicates (same state and date)
        df = df.drop_duplicates(subset=['State', 'Date'], keep='last')
        
        # Sort by date and state
        df = df.sort_values(['State', 'Date'])
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Log success
        st.success(f"✅ Data loaded successfully: {len(df)} records, {df['State'].nunique()} states")
        
        return df
        
    except FileNotFoundError:
        st.error("❌ Data file 'StatewiseTestingDetails.csv' not found!")
        st.info("📁 Please ensure the CSV file is in the same directory as the app.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()

def filter_data(
    df: pd.DataFrame,
    states: List[str] = None,
    date_range: Tuple[date, date] = None,
    positive_range: Tuple[int, int] = None
) -> pd.DataFrame:
    """Filter data by states, date range, and positive cases range"""
    try:
        if df.empty:
            return pd.DataFrame()
        
        filtered_df = df.copy()
        
        # Filter by states
        if states and len(states) > 0:
            filtered_df = filtered_df[filtered_df['State'].isin(states)]
        
        # Filter by date range
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['Date'] >= start_date) & 
                (filtered_df['Date'] <= end_date)
            ]
        
        # Filter by positive range
        if positive_range and 'Positive' in filtered_df.columns:
            min_positive, max_positive = positive_range
            filtered_df = filtered_df[
                (filtered_df['Positive'] >= min_positive) &
                (filtered_df['Positive'] <= max_positive)
            ]
        
        return filtered_df.sort_values(['State', 'Date'], ascending=[True, False])
        
    except Exception as e:
        st.error(f"❌ Filtering error: {str(e)}")
        return pd.DataFrame()

def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Get comprehensive data summary"""
    if df.empty:
        return {}
    
    summary = {
        'total_records': len(df),
        'total_states': df['State'].nunique(),
        'date_range': {
            'start': df['Date'].min().strftime('%Y-%m-%d'),
            'end': df['Date'].max().strftime('%Y-%m-%d')
        },
        'total_samples': int(df['TotalSamples'].sum()),
        'total_positive': int(df['Positive'].sum()),
        'total_negative': int(df['Negative'].sum()),
        'avg_positive_ratio': float(df['PositiveRatio'].mean()),
        'peak_positive_day': {
            'date': df.loc[df['Positive'].idxmax(), 'Date'].strftime('%Y-%m-%d'),
            'value': int(df['Positive'].max()),
            'state': df.loc[df['Positive'].idxmax(), 'State']
        } if 'Positive' in df.columns else None,
        'states_with_highest_positivity': df.groupby('State')['PositiveRatio'].mean().nlargest(3).to_dict()
    }
    
    return summary

def create_sample_data() -> pd.DataFrame:
    """Create sample COVID-19 testing data for demo purposes"""
    dates = pd.date_range(start='2020-01-01', end='2021-12-31', freq='D')
    states = [
        'Maharashtra', 'Delhi', 'Kerala', 'Karnataka', 'Tamil Nadu',
        'Uttar Pradesh', 'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'West Bengal',
        'Bihar', 'Andhra Pradesh', 'Telangana', 'Assam', 'Odisha',
        'Punjab', 'Chhattisgarh', 'Haryana', 'Jharkhand', 'Uttarakhand'
    ]
    
    data = []
    for date in dates:
        for state in states:
            # Base values with some randomness
            base_samples = np.random.randint(1000, 5000)
            # Add seasonality and trends
            month_factor = 1 + (date.month - 1) * 0.1  # Increase over months
            state_factor = 0.5 + (states.index(state) % 10) * 0.1
            
            total_samples = int(base_samples * month_factor * state_factor)
            positive_rate = 0.01 + (np.sin(date.month * 0.5) * 0.005)  # Seasonal variation
            positive = int(total_samples * positive_rate)
            negative = total_samples - positive
            
            data.append({
                'State': state,
                'Date': date.date(),
                'TotalSamples': total_samples,
                'Positive': positive,
                'Negative': negative,
                'PositiveRatio': positive / total_samples
            })
    
    df = pd.DataFrame(data)
    return df
