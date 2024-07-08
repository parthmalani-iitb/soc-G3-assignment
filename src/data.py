import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class DataPreprocessing:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.fetch_data()

    def fetch_data(self):
        data = yf.download(self.symbol, self.start_date, self.end_date)
        return data

    def data_characteristics(self):
        summary = {
            'Data Size': self.data.shape,
            'Number of Missing Values': self.data.isnull().sum().sum(),
            'Mean': self.data.mean(),
            'Median': self.data.median(),
            'Standard Deviation': self.data.std()
        }
        return summary

    def handle_missing_values(self, method='ffill'):
        if method == 'ffill':
            self.data = self.data.ffill()
        elif method == 'bfill':
            self.data = self.data.bfill()
        elif method == 'drop':
            self.data = self.data.dropna()
        else:
            raise ValueError("Method not recognized. Use 'ffill', 'bfill', or 'drop'.")

    def calculate_cumulative_returns(self, benchmark_symbol='^NSEI'):
        self.data['Cumulative Returns'] = (1 + self.data['Adj Close'].pct_change()).cumprod()

        benchmark_data = yf.download(benchmark_symbol, self.start_date, self.end_date)
        benchmark_data['Cumulative Returns'] = (1 + benchmark_data['Adj Close'].pct_change()).cumprod()

        plt.figure(figsize=(10, 6))
        plt.plot(self.data['Cumulative Returns'], label=self.symbol)
        plt.plot(benchmark_data['Cumulative Returns'], label='Nifty Index')
        plt.title('Cumulative Returns')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.show()

    def plot_closing_prices(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.data['Adj Close'], label=self.symbol)
        plt.title('Closing Prices')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
