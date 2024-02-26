import yfinance as yf
from datetime import date
import os

import pandas as pd
#https://pypi.org/project/yfinance/
def scrape_stock_prices(ticker, range="1y"):
    try:
        # Control if file already exist
        #{current_date.strftime("%Y%m%d")}_
        current_date = date.today()
        path = f'./data/prices/{ticker}.csv'
        if os.path.isfile(path) == True:
            df_prices = pd.read_csv(path)
            f = open(f'./data/ticker_info/{ticker}.txt', "r")
            company_info = f.read()
        else:
            tickers = yf.Tickers(ticker)
            if ticker == 'TSLA':
                df_prices = df_prices = tickers.tickers[ticker].history(start='2021-09-30',end='2022-09-30')
            else:
                df_prices = tickers.tickers[ticker].history(period=range)
                
            df_prices.to_csv(path)
            info = tickers.tickers[ticker].info
            company_info = info['longBusinessSummary']
            f = open(f'./data/ticker_info/{ticker}.txt', "w")
            f.write(company_info)
            f.close()
        
        return {'Status': True, 'Message': 'Prices collected', 'Data': df_prices, 'Info': company_info}
    except Exception as e:
        return {'Status': False, 'Message':'Prices could not be collected due to: ' + str(e)}

#scrape_stock_prices('TSLA', '5y')

def get_company_info(ticker):
    f = open(f'./data/ticker_info/{ticker}.txt', "r")
    return f.read()