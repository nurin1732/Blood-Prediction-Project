import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Config
st.set_page_config(page_title="Blood Donation Forecast", layout="wide")
st.title(" Blood Donation Prediction Dashboard")

# 2. Load Data
@st.cache_data
def load_data():
    # Get the directory where the current script (dashboard.py) is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go one level up to the root folder, then into the 'data' folder
    file_path = os.path.join(script_dir, '..', 'data', 'final_dashboard_data.csv')
    
    return pd.read_csv(file_path)

df = load_data()

# 3. Sidebar Filters
state = st.sidebar.selectbox("Select State", df['state'].unique())
filtered_df = df[df['state'] == state]

# 4. Display Charts
st.subheader(f"Donation Trends for {state}")
fig = px.line(filtered_df, x='date', y=['actual_donations', 'predicted_donations'], 
              title="Actual vs Predicted Daily Donations")
st.plotly_chart(fig, use_container_width=True)

# 5. Highlight "Festive Dips"
anomalies = filtered_df[filtered_df['annotation'] == 'Festive Dip/Anomaly']
st.write("### Detected Festive Dips/Anomalies")
st.dataframe(anomalies)