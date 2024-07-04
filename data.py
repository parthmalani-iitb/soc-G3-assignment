import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class StockData:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.fetch_data()

    def fetch_data(self):
        stock_data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        nifty_data = yf.download('^NSEI', start=self.start_date, end=self.end_date)  
        return stock_data, nifty_data

    def data_characteristics(self):
        stock_data, _ = self.data
        data_summary = {
            "Data Size": stock_data.shape,
            "Missing Values": stock_data.isnull().sum().sum(),
            "Mean": stock_data.mean(),
            "Median": stock_data.median(),
            "Standard Deviation": stock_data.std()
        }
        return data_summary

    def missing_values_handler(self, method='ffill'):
        stock_data, nifty_data = self.data
        if method == 'ffill':
            stock_data.fillna(method='ffill', inplace=True)
            nifty_data.fillna(method='ffill', inplace=True)
        elif method == 'bfill':
            stock_data.fillna(method='bfill', inplace=True)
            nifty_data.fillna(method='bfill', inplace=True)
        elif method == 'interpolate':
            stock_data.interpolate(method='linear', inplace=True)
            nifty_data.interpolate(method='linear', inplace=True)
        else:
            raise ValueError("Invalid method. Use 'ffill', 'bfill', or 'interpolate'.")
        self.data = (stock_data, nifty_data)
        return self.data

    def performance_analysis(self):
        stock_data, nifty_data = self.data
        stock_data['Cumulative Return'] = (1 + stock_data['Adj Close'].pct_change()).cumprod()
        nifty_data['Cumulative Return'] = (1 + nifty_data['Adj Close'].pct_change()).cumprod()

        plt.figure(figsize=(10, 6))
        plt.plot(stock_data['Cumulative Return'], label=f'{self.ticker} Cumulative Return')
        plt.plot(nifty_data['Cumulative Return'], label='Nifty Index Cumulative Return')
        plt.title(f'{self.ticker} vs Nifty Index Cumulative Return')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.grid(True)
        plt.show()


