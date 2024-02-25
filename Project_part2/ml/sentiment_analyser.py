from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt

# Use a pipeline fitted for sentiment analysis 
sentiment_classifier = pipeline("sentiment-analysis")

def __return_sentiment(tweet):
    # return label from output label
    sentiment = sentiment_classifier(tweet)[0]['label']
    return(sentiment_classifier(tweet)[0]['label'])


def run_sentiment_analyzis(ticker, df_breakout):
    df_tweets = pd.read_csv(f'./data/sentiment/{ticker}_nonlabeled.csv')
    df_tweets['Date'] = pd.to_datetime(df_tweets['Date'])
    for i, row in df_breakout.iterrows():
        if row['Date'] == '2022-04-20 00:00:00-04:00':
            print('Should be hit')

        # Run sentiment analyzis starting 10 days before breakout 
        tweets_in_scope = (df_tweets['Date'] > (pd.to_datetime(row['Date']) - pd.Timedelta(10, unit='D'))) & ((df_tweets['Date']) < pd.to_datetime(row['Date']))
        print(tweets_in_scope)
        df_tweets = df_tweets.loc[tweets_in_scope]
        print(df_tweets)
        if df_tweets.empty == False:
            
            df_tweets['sentiment'] = df_tweets['Tweet'].apply(__return_sentiment)

            #Save to csv
            sentiment, plot = plt.subplots(nrows=1, ncols = 3, figsize=(10,4))
            sentiment.suptitle(f'Sentiment analysis via Bert of {ticker} Tweets')

            sentiment_grouped =df_tweets.groupby('sentiment').size()
            sentiment_grouped.plot(kind='bar', ax=plot[0], color=['crimson', 'lightblue', 'green'])
            sentiment.show()
            #df_tweets.head(10)
        else:
            print('Missing sentiment data')

        
        
#df_breakout = pd.read_csv('./data/breakout/TSLA.csv')

#run_sentiment_analyzis('TSLA',df_breakout)