import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import alpha_vantage
from alpha_vantage.fundamentaldata import FundamentalData

API_KEY = 'W3UMK39W1AOA7MZD'

# code from here
st.title('Stock Dashboard')

ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

try:
    data = yf.download(ticker, start=start_date, end=end_date)
    if not data.empty:
        fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
        st.plotly_chart(fig)
    else:
        st.warning("No data available for the specified parameters.")
except ValueError as ve:
    error_message = str(ve)
    if "API rate limit" in error_message:
        st.warning("API rate limit exceeded. Please try again later or consider subscribing to a premium plan.")
    else:
        st.warning("An error occurred: {}".format(error_message))

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")



pricing_data, fundamental_data = st.tabs(["Pricing Data", "Fundamental Data"])

with pricing_data:
    st.header('Price Movements')
    data = yf.download(ticker, start=start_date, end=end_date)
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1)-1
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100
    st.write('Annual Return is ',annual_return,'%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is ',stdev*100,'%')
    st.write('Risk Adj. Return is ',annual_return/(stdev*100))

with fundamental_data:
    fd = FundamentalData(API_KEY, output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)
