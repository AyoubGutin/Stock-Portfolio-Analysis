import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime 
from plots import price_change



# GLOBAL VARIABLES 

# get ytd 
today = datetime.today().date()


# streamlit input form 
st.title("Stock Analysis")
# sidebar for ticket selection 
ticker = st.text_input("Enter a stock ticker (e.g., AAPL)", "AAPL")


# FUNCTIONS
def handle_fetch_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(F"Error fetching data: {str(e)}")
            return None 
    return wrapper

@handle_fetch_error
def fetch_stock_data(ticker, end: datetime): 
    """
    Parameters: 
    1) ticker: ticker name for the stock
    2) end: end of stock's price history 

    Returns:
    A dataframe of the price history of the selected stock
    """
    return yf.download(ticker, end=end)

@handle_fetch_error
def fetch_spx_data(start: datetime, end: datetime): 
    """
    Parameters: 
    1) start: start of stock's price history - this will be the start of the stock it is being compared to.
    2) end: end of stock's price history 

    Returns:
    A dataframe of the price history of the selected stock
    """
    return yf.download("SPX", start=start, end=end)

def clean_stock_data(stock_data): 
    """
    Parameters:
    1) stock_data: dataframe of stock price history

    Returns:
    A cleaned dataframe 
    """
    stock_data.columns = stock_data.columns.get_level_values(0)  
    stock_data.columns = stock_data.columns.str.strip()

    return stock_data



# when button is submitted, run code below 
if st.button("Analyse Stock"):
    stock_data = fetch_stock_data(ticker, end=today)
    stock_data = clean_stock_data(stock_data)

    # generate plot for stock data - this needs fixing 
    st.write("Fetching stock data from an API - this might take a minute.... ")
    fig = price_change(stock_data, ticker)
    st.plotly_chart(fig)


    # calculate metrics

    # performance metrics
    st.write("### General Performance Metrics")
    # return metrics
    stock_data["Daily Return"] = stock_data["Close"].pct_change() * 100
    years = (stock_data.index[-1] - stock_data.index[0]).days / 365.25
    cagr = (stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) ** (1 / years) - 1
    # price metrics
    max_price = max(stock_data["High"])
    min_price = min(stock_data["Low"])
    max_price_date = stock_data["High"].idxmax()
    min_price_date = stock_data["Low"].idxmin() 
    # risk metrics
    volatility = stock_data['Daily Return'].std() # simple standard deviation calculation for volatility
    start_date = stock_data.index[0]
    spx_data = fetch_spx_data(start=start_date, end=today)
    spx_data = clean_stock_data(spx_data)
    spx_data["Daily Return"] = spx_data["Close"].pct_change() * 100 # percent change
    corr = stock_data["Daily Return"].corr(spx_data["Daily Return"])
    
    st.write(f"##### Return Metrics:\n- Average Daily Return: {stock_data['Daily Return'].mean().round(2)}%\n- Annualized Return (CAGR): {cagr * 100:.2f}%")
    st.write(f"##### Price Metrics:\n- Maximum Price: ${max_price:.2f} on {max_price_date.strftime('%Y-%m-%d')}\n- Lowest Price: ${min_price:.2f} on {min_price_date.strftime('%Y-%m-%d')}")
    st.write(f"##### Risk Metrics:\n- Volatility (Standard Deviation of Daily Return): {volatility:.2f}%\n- Correlation with S&P 500: {corr:.2f}")

    # save to csv
    #stock_data.to_csv(f"data/{ticker}_stock_data.csv")



