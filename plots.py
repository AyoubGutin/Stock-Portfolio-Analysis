import plotly.express as px
import pandas as pd

def price_change(stock_data, ticker):
    """
    Plots line chart for stock price (closing price)

    Parameters:
    stock_data (pd.DataFrame): The stock data for the selected ticker. 
    ticker (str): The stock ticker symbol (e.g., 'GOOG', 'AAPL').

    Returns:
    plotly.graph_objects.Figure: A Plotly figure containing the line chart for the closing 
                                 price and bar chart for the trading volume.
    """
    # create line chart 
    fig = px.line(stock_data, x=stock_data.index, y=f"Close", title=f"{ticker} Stock Price")

    return fig