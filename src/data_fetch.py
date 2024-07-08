import yfinance as yf
import pandas as pd

def download_historical_data (symbol , start_date , end_date , timeframe = '1D'):
    data = yf.download(symbol , start_date , end_date , timeframe)
    return data