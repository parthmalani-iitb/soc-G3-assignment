from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


def fetch_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    nifty_data = yf.download('^NSEI', start=start_date, end=end_date)
    return stock_data, nifty_data


def data_characteristics(data):
    summary = {
        "Data Size": data.shape,
        "Missing Values": data.isnull().sum().sum(),
        "Mean": data.mean().to_dict(),
        "Median": data.median().to_dict(),
        "Standard Deviation": data.std().to_dict()
    }
    return summary


def handle_missing_values(data, method='ffill'):
    if method == 'ffill':
        data.fillna(method='ffill', inplace=True)
    elif method == 'bfill':
        data.fillna(method='bfill', inplace=True)
    elif method == 'interpolate':
        data.interpolate(method='linear', inplace=True)
    else:
        raise ValueError(
            "Invalid method. Use 'ffill', 'bfill', or 'interpolate'.")
    return data


def plot_cumulative_return(stock_data, nifty_data, ticker):
    stock_data['Cumulative Return'] = (
        1 + stock_data['Adj Close'].pct_change()).cumprod()
    nifty_data['Cumulative Return'] = (
        1 + nifty_data['Adj Close'].pct_change()).cumprod()

    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Cumulative Return'],
             label=f'{ticker} Cumulative Return')
    plt.plot(nifty_data['Cumulative Return'],
             label='Nifty Index Cumulative Return')
    plt.title(f'{ticker} vs Nifty Index Cumulative Return')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return plot_url


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        stock_data, nifty_data = fetch_data(ticker, start_date, end_date)
        stock_data = handle_missing_values(stock_data, method='interpolate')

        statistics = data_characteristics(stock_data)
        plot_url = plot_cumulative_return(stock_data, nifty_data, ticker)

        return render_template('index.html',
                               statistics=statistics,
                               plot_url=plot_url)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
