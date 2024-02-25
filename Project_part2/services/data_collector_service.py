import yfinance as yf
from datetime import date
import os

import pandas as pd
#https://pypi.org/project/yfinance/
def scrape_stock_prices(ticker, range="1y"):
    try:
        # Control if File already exist
        current_date = date.today()
        path = f'./data/prices/{current_date.strftime("%Y%m%d")}_{ticker}.csv'
        if os.path.isfile(path) == True:
            df_prices = pd.read_csv(path)
            info = pd.read_csv(f'./data/ticker_info/{ticker}.csv').to_dict()
        else:
            tickers = yf.Tickers(ticker)
            if ticker == 'TSLA':
                df_prices = df_prices = tickers.tickers[ticker].history(start='2021-09-30',end='2022-09-30')
            else:
                df_prices = tickers.tickers[ticker].history(period=range)
                
            df_prices.to_csv(path)
            info = tickers.tickers[ticker].info
            df_info = pd.DataFrame(info)
            df_info.to_csv(f'./data/ticker_info/{ticker}.csv') 
        
        return {'Status': True, 'Message': 'Prices collected', 'Data': df_prices, 'Info': info['longBusinessSummary']}
    except Exception as e:
        return {'Status': False, 'Message':'Prices could not be collected due to: ' + str(e)}

#scrape_stock_prices('TSLA', '5y')


    