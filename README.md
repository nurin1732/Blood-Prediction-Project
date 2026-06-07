# Blood Donation Forecasting Dashboard

## Short Project Description
This project is an interactive time-series forecasting dashboard designed to predict daily blood donation levels by state.

## Prerequisites 
Ensure you have **Python 3.8+** installed. 
You will need to install the dependenciesin bash:
pip install -r requirements.txt
Ensure there is a virtual environment active to avoid errors while downloading the requirements.txt

## How to run the dashboard in the virtual environment
1. Navigate to the project root directory in your terminal.
2. Ensure your data file is located at model/data/final_dashboard_data.csv
3. Execute the following command in the terminal : streamlit run dashboard/dashboard.py
4. Access the dashboard in your web browser at the local URL provided

## Additional information on the columns of the dataset
daily: The actual number of blood donations recorded for that day.
predicted_daily: The value forecasted by the model for that specific date.
