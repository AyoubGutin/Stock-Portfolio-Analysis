import yfinance as yf
import pandas as pd
import streamlit as st
import datetime 
from plots import price_change

# get ytd 
today = datetime.datetime.today().date()

 # streamlit input form 
st.title("Stock Analysis")

# sidebar for ticket selection 
ticker = st.text_input("Enter a stock ticker (e.g., AAPL)", "AAPL")

# submit button
if st.button("Analyse Stock"):
    try:
        # fetch stock data from yahoo finance api 
        stock_data = yf.download(ticker, end=today)

        # clean data frame
        stock_data.columns = stock_data.columns.get_level_values(0)  
        stock_data.columns = stock_data.columns.str.strip()

        # generate plot for stock data - this needs fixing 
        fig = price_change(stock_data, ticker)
        st.plotly_chart(fig)

        # performance metrics
        st.write("### Performance Metrics")
        stock_data["Daily Return"] = stock_data["Close"].pct_change() * 100

        max_price = max(stock_data["High"])
        min_price = min(stock_data["Low"])
        max_price_date = stock_data["High"].idxmax()
        min_price_date = stock_data["Low"].idxmin() 

        years = (stock_data.index[-1] - stock_data.index[0]).days / 365.25
        cagr = (stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) ** (1 / years) - 1

        volatility = stock_data['Daily Return'].std()

        st.write(f"##### Return Metrics:\n- Average Daily Return: {stock_data['Daily Return'].mean().round(2)}%\n- Annualized Return (CAGR): {cagr * 100:.2f}%")
        st.write(f"##### Price Metrics:\n- Maximum Price: ${max_price:.2f} on {max_price_date.strftime('%Y-%m-%d')}\n- Lowest Price: ${min_price:.2f} on {min_price_date.strftime('%Y-%m-%d')}")
        st.write(f"- Volatility (Standard Deviation of Daily Return): {volatility:.2f}%")


        # save to csv
        stock_data.to_csv(f"data/{ticker}_stock_data.csv")

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")

