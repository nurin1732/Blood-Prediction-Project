import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import time

# Page Configuration
st.set_page_config(page_title="Blood Donation Forecast", layout="wide")
st.title("Blood Donation Prediction Dashboard")

# Data Loading
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', 'model', 'data', 'final_dashboard_data.csv')
    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'])
    return data

df = load_data()

# Sidebar Controls
state = st.sidebar.selectbox("Select State", df['state'].unique())
state_df = df[df['state'] == state].sort_values('date')
view_months = st.sidebar.selectbox("View Horizon (Months)", [1, 3, 5])
total_days = view_months * 30
max_offset = max(0, len(state_df) - total_days)

# --- meant for demo use only ---------
is_paused = st.sidebar.checkbox("Pause Live Feed", value=False)
# ------------------------------------

start_idx = st.session_state.window_offset
end_idx = start_idx + total_days

if end_idx <= len(state_df):
    current_window = state_df.iloc[start_idx:end_idx].copy()
    
    # Slice Data
    actuals = current_window.iloc[:10][['date', 'daily']]
    hist_pred = current_window.iloc[:10][['date', 'predicted_daily']]
    future_pred = current_window.iloc[10:][['date', 'predicted_daily']]

    # Create Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actuals['date'], y=actuals['daily'], name='Actual', line=dict(color='#1f77b4', width=3)))
    fig.add_trace(go.Scatter(x=hist_pred['date'], y=hist_pred['predicted_daily'], name='Historical Prediction', 
                             line=dict(color='#ff7f0e', width=3, dash='dash'), opacity=0.6)) 
    fig.add_trace(go.Scatter(x=future_pred['date'], y=future_pred['predicted_daily'], name='Future Forecast', 
                             line=dict(color='#ff7f0e', width=3, dash='solid')))

    # Logic for Alerts
    volatility = future_pred['predicted_daily'].std()
    min_drop_magnitude = future_pred['predicted_daily'].mean() * 0.15 
    threshold = max(min_drop_magnitude, volatility * 2.5)
    
    trend_val = future_pred['predicted_daily'].iloc[min(6, len(future_pred)-1)] - future_pred['predicted_daily'].iloc[0]
    condition = "Increasing" if trend_val > (threshold/1.5) else "Dropping" if trend_val < -(threshold/1.5) else "Stable"
    
    drop_idx = None
    for i in range(len(future_pred) - 1):
        if (future_pred.iloc[i]['predicted_daily'] - future_pred.iloc[i+1]['predicted_daily']) > threshold:
            drop_idx = i + 1
            break

    if drop_idx is not None:
        fig.add_trace(go.Scatter(x=[future_pred.iloc[drop_idx]['date']], y=[future_pred.iloc[drop_idx]['predicted_daily']],
            mode='markers+text', marker=dict(color='red', size=14, symbol='x'), name='Significant Drop', 
            text=["ALERT"], textposition="top center"))

    fig.update_layout(title="Actual vs. Predicted Performance", xaxis_title="Date", yaxis_title="Donations")
    fig.update_xaxes(dtick=5 * 86400000.0, tickformat="%b %d")
    st.plotly_chart(fig, use_container_width=True, key="live_forecast_chart")

    # Dashboard Insights
    st.divider()
    st.subheader("Dashboard Insights")
    action = " EMERGENCY: Initiate blood drive." if condition == "Dropping" else \
             " SURPLUS: Optimize storage." if condition == "Increasing" else \
             " STABLE: Continue standard schedule."
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Condition", condition)
    col2.metric("Next Significant Drop", future_pred.iloc[drop_idx]['date'].strftime('%b %d') if drop_idx is not None else "None")
    col3.info(f"Recommended Action: {action}")

    #---1s Live Update meant for demo----
    if not is_paused and st.session_state.window_offset < max_offset:
        time.sleep(1)
        st.session_state.window_offset += 1
        st.rerun()
else:
    st.write("End of dataset reached.")
    #----------------------------------