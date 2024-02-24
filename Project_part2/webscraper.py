import yfinance as yf
from datetime import date
import matplotlib as plt
import mplfinance as mpf
import pandas as pd

def scrape_stock_prices(ticker, range="1y"):
    try:
        tickers = yf.Tickers(ticker)
        df_prices = tickers.tickers[ticker].history(period=range)
        __plot_chart(df_prices, ticker)
        current_date = date.today()
        df_prices.to_csv(f'./data/prices/{current_date.strftime("%d%m%Y")}_{ticker}_{range}.csv')
        return {'Status': True, 'Message': 'Prices collected'}
    except Exception as e:
        return {'Status': False, 'Message':'Prices could not be collected due to: ' + e.message}

#https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask

def __plot_chart(df_prices, ticker):
    fig, axes = mpf.plot(df_prices,returnfig=True,volume=True,
                     figsize=(11,8),panel_ratios=(2,1),
                     title=f'\n\n{ticker}',type='candle',mav=(10,20))
    ax1 = axes[0]
    ax2 = axes[2]

    #./static/images/
    mpf.plot(df_prices,ax=ax1,volume=ax2, type='candle',mav=(10,20), savefig=f'{ticker}.png')
    #mpf.show() 
     # display the plot
    