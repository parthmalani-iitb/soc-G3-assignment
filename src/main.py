# import matplotlib.pyplot as plt
# import pandas as pd
# from datetime import datetime
# from data_fetch import download_historical_data 
# from performance import plot_closing_prices

# def main():
#     # Download historical price data
#     symbol = 'RELIANCE.NS'
#     start_date = '2024-06-01'
#     end_date = datetime.today().strftime('%Y-%m-%d')
#     data = download_historical_data(symbol, start_date, end_date)
    
#     data = pd.DataFrame(data)
#     df=data.head(10)
#     print(df.to_string())
#     # Plot closing prices
#     plot_closing_prices(data, symbol)

# if __name__ == '__main__':
#     main()


from datetime import datetime
from data import DataPreprocessing

def main():
    symbol = 'RELIANCE.NS'
    start_date = '2024-06-01'
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    data_preprocessor = DataPreprocessing(symbol, start_date, end_date)
    
    # Display data characteristics
    characteristics = data_preprocessor.data_characteristics()
    for key, value in characteristics.items():
        print(f"{key}: {value}")
    
    # Handle missing values
    data_preprocessor.handle_missing_values(method='ffill')
    
    # Plot cumulative returns against Nifty Index
    data_preprocessor.calculate_cumulative_returns()
    
    # Plot closing prices
    data_preprocessor.plot_closing_prices()

if __name__ == '__main__':
    main()
