from flask import Flask, render_template, request
import pandas as pd
from services.data_collector_service import scrape_stock_prices
from ml.breakout import run_breakout 
from services.plot_service import plot_graph
from flask import g

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

@app.route("/analyze", methods=['POST'])
def analyze():
    if request.method == 'POST':
        ticker = request.form['tickers']
            
        #Maybe generate a dictionary with different statuses
        scrape_result = scrape_stock_prices(ticker)
        #plot_graph(scrape_result['Data'], ticker)
        #, company_info=scrape_result['Info']
        return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=scrape_result['Info'])
    else:
        return render_template('engine.html')

@app.route("/breakout/<ticker>")
def breakout(ticker):
    breakout_data = run_breakout(ticker) 
    return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, accuracy=breakout_data['Accuracy'], breakouts=breakout_data['Data'])

@app.route("/sentiment/<ticker>")
def sentiment(ticker):
    return render_template('engine.html')


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

    