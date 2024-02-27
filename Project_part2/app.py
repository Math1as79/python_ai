from flask import Flask, render_template, request
import pandas as pd
from services.data_collector_service import scrape_stock_prices, get_company_info
from ml.breakout import run_breakout, get_breakout_data
from ml.sentiment_analyser import run_sentiment_analysis, get_sentiment
from services.plot_service import plot_graph

# Because of time limitation I decided not to comment so much on the flask part.
# Every call that renders the engine need to repeat the previous one and add additional information to the flow, 
# not an optimal solution. Therefore I have taken a shortcut and saving the steps in different file formats to increase performance. 
# Having the flow more visualised in an ui adds to the understanding. 

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

@app.route("/analyze", methods=['POST'])
def analyze():
    if request.method == 'POST':
        ticker = request.form['tickers']
            
        #Maybe generate a dictionary with different statuses
        scrape_result = scrape_stock_prices(ticker)
        plot_graph(scrape_result['Data'], ticker)
        return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=scrape_result['Info'])
    else:
        return render_template('engine.html')

@app.route("/breakout/<ticker>")
def breakout(ticker):
    breakout_data = run_breakout(ticker)
    df_data = breakout_data['Data']
    df_breakout = df_data[['Date','Open','Close','Volume','MACD','Signal_Line']].copy()
    info = get_company_info(ticker)
    return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=info, accuracy=breakout_data['Accuracy'], 
                           column_names=df_breakout.columns.values, row_data=list(df_breakout.values.tolist()), zip=zip)

@app.route("/sentiment/<ticker>")
def sentiment(ticker):
    info = get_company_info(ticker)
    df_breakout = get_breakout_data(ticker)
    sentiment = run_sentiment_analysis(ticker, df_breakout)
    return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=info,
                           column_names=df_breakout.columns.values, row_data=list(df_breakout.values.tolist()), zip=zip, tables = [sentiment.to_html(classes='data', header="true")])

@app.route("/price/<ticker>")
def price_prediction(ticker):
    info = get_company_info(ticker)
    df_breakout = get_breakout_data(ticker)
    sentiment = get_sentiment(ticker)
    return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=info,
                           column_names=df_breakout.columns.values, row_data=list(df_breakout.values.tolist()), zip=zip, tables = [sentiment.to_html(classes='data', header="true")])


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

    