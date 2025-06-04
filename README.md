## 🦠 COVID-19 Statewise Dashboard (India) 
## Live at:https://covid-analytic-vrushabh.streamlit.app/

## An interactive analytical dashboard for tracking COVID-19 testing metrics across Indian states with visualization and data export capabilities.

🚀 Key Features

📊 **Visualization**
- Multi-state trend comparison charts
- Interactive date range selection
- Metric toggles (Positive/Negative/Total Samples)
- Positive ratio calculations
- Animated transitions between views

🔍 **Data Exploration**
- State-wise data filtering
- CSV/JSON export functionality
- Tabular data preview with sorting
- Responsive mobile-friendly design

⚙️ **Technical Highlights**
- Modular page architecture
- Cached data loading (300% faster performance)
- Error-resistant data processing
- Production-ready deployment setup

## 📂 Project Structure

covid19-dashboard/
├── Home.py                 # Main application entry point
├── utils.py                # Data processing utilities
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version specification
├── StatewiseTestingDetails.csv  # Primary dataset
└── pages/                  # Multi-page components
    ├── 1_Trend_Analysis.py # Time-series visualization
    └── 2_Data_Explorer.py  # Data filtering/export


## 🛠 Technology Stack

| Category        | Technologies Used         |
|----------------|--------------------------|
| **Core Framework** | Python 3.9+, Streamlit 1.28+ |
| **Data Processing** | Pandas 2.0+, NumPy 1.24+ |
| **Visualization** | Plotly 6.1+, Matplotlib 3.7+ |
| **Deployment** | Streamlit Cloud, GitHub Actions |

## 🚀 Getting Started

### Local Development

```bash
# Clone repository
git clone https://github.com/vrushabh-09/covid19-dashboard.git
cd covid19-dashboard

# Setup environment (Windows)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run application
streamlit run Home.py
```

### ☁️ Cloud Deployment

1. Push to your GitHub repository
2. Connect at [Streamlit Cloud](https://streamlit.io/cloud)
3. Configure:
   - Main file: `Home.py`
   - Python version: 3.9
4. Deploy with one click!

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

## 📊 Dataset Specification

**File:** `StatewiseTestingDetails.csv`

| Column        | Type    | Description                     | Example Value      |
|--------------|---------|--------------------------------|--------------------|
| Date         | Date    | Testing date (DD-MM-YYYY)      | 15-08-2021        |
| State        | String  | Indian state/UT name           | Maharashtra        |
| TotalSamples | Integer | Total samples tested           | 45,326,814        |
| Negative     | Integer | Negative test results          | 42,891,207        |
| Positive     | Integer | Confirmed positive cases       | 2,435,607         |


## ✉ Contact

**Developer:** Vrushabh Patil  
**Email:** [vrushabhpatil97711@gmail.com](mailto:vrushabhpatil97711@gmail.com)  
**GitHub:** [https://github.com/vrushabh-09/](https://github.com/vrushabh-09/)  
