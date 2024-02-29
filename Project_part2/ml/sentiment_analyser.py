from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
import os 
import re

# Use a pipeline fitted for sentiment analysis 
sentiment_classifier = pipeline("sentiment-analysis")

def __clean_tweet(text):
    # Lowercasing
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove mentions and hashtags
    text = re.sub(r'@[\w]+', '', text)
    text = re.sub(r'#', '', text)
    
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-z\s]', '', text)
    
    return text

def __return_sentiment(tweet):
    # return label from output label
    sentiment = sentiment_classifier(tweet)[0]['label']
    return(sentiment_classifier(tweet)[0]['label'])


def run_sentiment_analysis(ticker, df_breakout):
    if os.path.isfile(f'./data/sentiment/{ticker}_sa.csv') == True:
        return get_sentiment(ticker)
    else:
        sentiment = []
        if os.path.isfile(f'./data/sentiment/{ticker}_nonlabeled.csv') == True:
            df_tweets = pd.read_csv(f'./data/sentiment/{ticker}_nonlabeled.csv')
            df_tweets['Date'] = pd.to_datetime(df_tweets['Date'])
            for i, row in df_breakout.iterrows():
                # Run sentiment analyzis starting 3 days before breakout (due to performance and speed of analysing)
                tweets_in_scope = (df_tweets['Date'] > (pd.to_datetime(row['Date']) - pd.Timedelta(3, unit='D'))) & ((df_tweets['Date']) < pd.to_datetime(row['Date']))
                df_tweets = df_tweets.loc[tweets_in_scope]
                
                if df_tweets.empty == False:
                    df_tweets['Tweet'] = df_tweets['Tweet'].apply(__clean_tweet)
                    df_tweets['sentiment'] = df_tweets['Tweet'].apply(__return_sentiment)
                    positive = df_tweets['sentiment'].value_counts()['POSITIVE']
                    negative = df_tweets['sentiment'].value_counts()['NEGATIVE']
                    total = positive + negative
                    # Add the sentiment stats on a given date that has been labeled with breakout
                    sentiment.append({'Date': row['Date'], 'Status':'Tweets analysed', 'Postive':positive / total,'Negative':negative / total,'Number of tweets':total})

                else:
                    sentiment.append({'Date': row['Date'],'Status':'No sentiment to analyze in period', 'Postive':0,'Negative':0, 'Number of tweets':0})
        else:
            sentiment.append({'Date': '','Status':f'No sentiment to analyze on {ticker} ', 'Postive':0,'Negative':0, 'Number of tweets':0})

        df_sentiment = pd.DataFrame(sentiment)
        df_sentiment.to_csv(f'./data/sentiment/{ticker}_sa.csv')

        return df_sentiment

def get_sentiment(ticker):
    df = pd.read_csv(f'./data/sentiment/{ticker}_sa.csv') 
    print(df)
    return df    
        
#df_breakout = pd.read_csv('./data/breakout/TSLA.csv')

#s=run_sentiment_analysis('TSLA',df_breakout)
#print(s)