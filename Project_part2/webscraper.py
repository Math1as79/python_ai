import yfinance as yf
from datetime import date

def scrape_stock_prices(ticker, range="1y"):
    try:
        tickers = yf.Tickers(ticker)
        df_prices = tickers.tickers[ticker].history(period=range)
        current_date = date.today()
        df_prices.to_csv(f'./data/prices/{current_date.strftime("%d%m%Y")}_{ticker}_{range}.csv')
        return {'Status': True, 'Message': 'Prices collected'}
    except Exception as e:
        return {'Status': False, 'Message':'Prices could not be collected due to: ' + e}
