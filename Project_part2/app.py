from flask import Flask, render_template, request
import pandas as pd
from services.data_collector_service import scrape_stock_prices, get_company_info
from ml.breakout import run_breakout, get_breakout_data, get_accuracy
from ml.sentiment_analyser import run_sentiment_analysis, get_sentiment
from ml.price_prediction import run_price_prediction
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
        scrape_result = scrape_stock_prices(ticker)
        if scrape_result['Status'] == True:
            plot_graph(scrape_result['Data'], ticker)
            return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=scrape_result['Info'], 
               menu1='accordion-collapse collapse show', menu2='accordion-collapse collapse', menu3='accordion-collapse collapse', menu4='accordion-collapse collapse')
        
    else:
        return render_template('engine.html')

@app.route("/breakout/<ticker>")
def breakout(ticker):
    breakout_data = run_breakout(ticker)
    df_breakout = breakout_data['Data']
    df_breakout = df_breakout[df_breakout['Breakout'] == True]
    df_breakout = df_breakout[['Date','Open','Close','Volume','Breakout']].copy()
    info = get_company_info(ticker)
    return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=info, accuracy=breakout_data['Accuracy'], 
                           column_names=df_breakout.columns.values, row_data=list(df_breakout.values.tolist()), zip=zip,
                           menu1='accordion-collapse collapse show', menu2='accordion-collapse collapse show', menu3='accordion-collapse collapse', menu4='accordion-collapse collapse')

@app.route("/sentiment/<ticker>")
def sentiment(ticker):
    info = get_company_info(ticker)
    df_breakout = get_breakout_data(ticker)
    df_breakout = df_breakout[df_breakout['Breakout'] == True]
    df_breakout = df_breakout[['Date','Open','Close','Volume','Breakout']].copy()
    sentiment = run_sentiment_analysis(ticker, df_breakout)
    return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=info, accuracy=get_accuracy(ticker),
                           column_names=df_breakout.columns.values, row_data=list(df_breakout.values.tolist()), zip=zip, tables = [sentiment.to_html(classes='data', header="true", index = False)],
                           menu1='accordion-collapse collapse', menu2='accordion-collapse collapse show', menu3='accordion-collapse collapse show', menu4='accordion-collapse collapse')
                           

@app.route("/prediction/<ticker>")
def prediction(ticker):
    info = get_company_info(ticker)
    df_breakout = get_breakout_data(ticker)
    prediction = run_price_prediction(ticker, df_breakout)
    df_breakout = df_breakout[df_breakout['Breakout'] == True]
    df_breakout = df_breakout[['Date','Open','Close','Volume','Breakout']].copy()
    sentiment = get_sentiment(ticker)
    return render_template('engine.html', graph=f'images/{ticker}.png', ticker=ticker, company_info=info,accuracy=get_accuracy(ticker),
                           column_names=df_breakout.columns.values, row_data=list(df_breakout.values.tolist()), zip=zip, tables = [sentiment.to_html(classes='data', header="true", index = False)],
                           prediction=prediction, prediction_img=f'images/{ticker}_predictions.png',
                           menu1='accordion-collapse collapse', menu2='accordion-collapse collapse', menu3='accordion-collapse collapse show', menu4='accordion-collapse collapse show')


@app.route("/engine")
def engine():
    return render_template('engine.html')


    