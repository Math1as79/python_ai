from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt

# Use a pipeline fitted for sentiment analysis 
sentiment_classifier = pipeline("sentiment-analysis")

def __return_sentiment(tweet):
    # return label from output label
    sentiment = sentiment_classifier(tweet)[0]['label']
    return(sentiment_classifier(tweet)[0]['label'])


def main(ticker):
    df_tweets = pd.read_csv(f'./data/sentiment/{ticker}_nonlabeled.csv', nrows=10)

    df_tweets['sentiment'] = df_tweets['Tweet'].apply(__return_sentiment)
    #Save to csv
    sentiment, plot = plt.subplots(nrows=1, ncols = 3, figsize=(10,4))
    sentiment.suptitle(f'Sentiment analysis via Bert of {ticker} Tweets')

    sentiment_grouped =df_tweets.groupby('sentiment').size()
    sentiment_grouped.plot(kind='bar', ax=plot[0], color=['crimson', 'lightblue', 'green'])
    sentiment.show()
    #df_tweets.head(10)
    print(df_tweets)
main('TSLA')