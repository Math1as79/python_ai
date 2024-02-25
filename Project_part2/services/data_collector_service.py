import yfinance as yf
from datetime import date
import os

import pandas as pd

def scrape_stock_prices(ticker, range="1y"):
    try:
        # Control if File already exist
        current_date = date.today()
        path = f'./data/prices/{current_date.strftime("%d%m%Y")}_{ticker}_{range}.csv'
        if os.path.isfile(path) == True:
            df_prices = pd.read_csv(path)
        else:
            tickers = yf.Tickers(ticker)
            df_prices = tickers.tickers[ticker].history(period=range)
            df_info = tickers.tickers[ticker].basic_info()
            df_prices.to_csv(path)

        return {'Status': True, 'Message': 'Prices collected', 'Data': df_prices, 'Info': df_info}
    except Exception as e:
        return {'Status': False, 'Message':'Prices could not be collected due to: ' + e.message}




    