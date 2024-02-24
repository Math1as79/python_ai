from flask import Flask, render_template, request
import pandas as pd
from webscraper import scrape_stock_prices
from breakout import run_breakout 

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True) 

@app.route("/")
def index():
    df_tickers = pd.read_csv('./data/tickers.csv')
    df_tickers = df_tickers[df_tickers['Ticker'].isin(['TSLA','MSFT','AAPL','META','NVDA','NFLX','AMZN'])]
    df_tickers = df_tickers.assign(Sentiment=False)
    df_tickers.loc[df_tickers['Ticker'] == 'TSLA', 'Sentiment'] = True
    df_tickers = df_tickers.assign(Analyze=False)
    return render_template('index.html', column_names=df_tickers.columns.values, row_data=list(df_tickers.values.tolist()), zip=zip)

#@app.route("/tickers")

@app.route("/anayze", methods=['POST'])
def analyze():
    if request.method == 'POST':
        ticker = request.form['tickers']
        #Maybe generate a dictionary with different statuses
        scrape_result = scrape_stock_prices(ticker)
        run_breakout(ticker)

@app.route("/engine")
def engine():
    
    return render_template('engine.html')


""" if ticker in ['TSLA','MSFT','AAPL','META']:
    print(f'Webscarping via Yahoo finance started for {ticker}')
    scrape_status = scrape_stock_prices(ticker)
    print(scrape_status['Message'])
    if scrape_status['Status'] == True:
        print('Retriving historical breakout patterns')
        #run_breakout(ticker)
        print('How is the sentiment leading up to the breakout')
        print('Display dates of potential break outs - apply machine learning, does it become a breakout or not when we have identified it?')
        print('Run sentiment analysis (only supported for Tesla at the moment(historicaly)) Take sentiment of the consolidation period')
    else:
        print('Please try another ticker.') """

    