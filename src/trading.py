import pandas as pd
import numpy as np

def strategy_build(df):
    """
    Identifies buy and sell signals using a simple moving average (SMA) crossover strategy.
    Updates the DataFrame with a 'signal' column indicating -1 for sell, 1 for buy, and 0 for hold.
    """
    df['SMA9'] = df['Adj Close'].rolling(window=9).mean()
    df['SMA20'] = df['Adj Close'].rolling(window=20).mean()
    df['signal'] = 0

    # Ensure signals are calculated only after both SMAs have enough data points
    df.loc[df.index[19:], 'signal'] = np.where(df['SMA9'][19:] > df['SMA20'][19:], 1, 0)
    df.loc[df.index[19:], 'signal'] = np.where(df['SMA9'][19:] < df['SMA20'][19:], -1, df['signal'][19:])

    # Debug: Print the SMA and signals
    # print(df[['SMA9', 'SMA20', 'signal']].tail(20))

    return df

class TradingExecution:
    def __init__(self, df, ticker, start_date, end_date):
        self.df = df
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.df = strategy_build(self.df)
        self.df['position'] = 0
        self.df['returns'] = 0.0

    def run(self):
        position = 0
        buy_price = 0.0

        for i in range(len(self.df)):
            if self.df['signal'].iloc[i] == 1 and position == 0:
                # Buy signal and currently not in position
                position = 1
                buy_price = self.df['Adj Close'].iloc[i]
                self.df.at[self.df.index[i], 'position'] = position

                # Debug: Print buy action
                # print(f"Buy at index {i}, price {buy_price}")

            elif self.df['signal'].iloc[i] == -1 and position == 1:
                # Sell signal and currently in position
                position = 0
                sell_price = self.df['Adj Close'].iloc[i]
                self.df.at[self.df.index[i], 'returns'] = (sell_price - buy_price) / buy_price
                self.df.at[self.df.index[i], 'position'] = position

                # Debug: Print sell action and return
                # print(f"Sell at index {i}, price {sell_price}, return {(sell_price - buy_price) / buy_price}")

            elif position == 1:
                # Implement stop loss
                current_price = self.df['Adj Close'].iloc[i]
                if (current_price - buy_price) / buy_price < -0.05:
                    position = 0
                    self.df.at[self.df.index[i], 'returns'] = (current_price - buy_price) / buy_price
                    self.df.at[self.df.index[i], 'position'] = position

                    # Debug: Print stop loss action and return
                    # print(f"Stop loss at index {i}, price {current_price}, return {(current_price - buy_price) / buy_price}")

        returns_series = self.df['returns'].copy()
        returns_series = returns_series[returns_series != 0]

        # Debug: Print the final returns series
        # print("Final returns series:")
        # print(returns_series)

        return returns_series
