import matplotlib.pyplot as plt

def plot_closing_prices(data, symbol):
    """
    Plot the closing prices of the stock.
    
    Parameters:
    data (DataFrame): Historical price data.
    symbol (str): symbol symbol of the stock.
    
    Objective:
    To visualize the closing prices of the stock over time.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label='Closing Price')
    plt.title(f'Closing Prices of {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (INR)')
    plt.legend()
    plt.grid(True)
    plt.show()