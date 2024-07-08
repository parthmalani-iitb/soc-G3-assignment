# from datetime import datetime
# from data import DataPreprocessing

# def main():
#     symbol = 'RELIANCE.NS'
#     start_date = '2024-06-01'
#     end_date = datetime.today().strftime('%Y-%m-%d')
    
#     data_preprocessor = DataPreprocessing(symbol, start_date, end_date)
    
#     # Display data characteristics
#     characteristics = data_preprocessor.data_characteristics()
#     for key, value in characteristics.items():
#         print(f"{key}: {value}")
    
#     # Handle missing values
#     data_preprocessor.handle_missing_values(method='ffill')
    
#     # Plot cumulative returns against Nifty Index
#     data_preprocessor.calculate_cumulative_returns()
    
#     # Plot closing prices
#     data_preprocessor.plot_closing_prices()

# if __name__ == '__main__':
#     main()


from datetime import datetime
from data import DataPreprocessing
from trading import TradingExecution

def main():
    symbol = 'RELIANCE.NS'
    start_date = '2024-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')

    data_preprocessor = DataPreprocessing(symbol, start_date, end_date)

    # Handle missing values
    data_preprocessor.handle_missing_values(method='ffill')

    # Initialize TradingExecution with preprocessed data
    trading_executor = TradingExecution(data_preprocessor.data, symbol, start_date, end_date)
    
    # Run the trading execution
    returns_series = trading_executor.run()
    print(returns_series)

if __name__ == '__main__':
    main()
