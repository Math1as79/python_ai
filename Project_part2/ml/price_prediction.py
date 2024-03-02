import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import joblib

def run_price_prediction(ticker, df_breakout):
    #existing_model = joblib.load(f'./models/{ticker}_breakout.joblib')
    
    # Needs to be the same parameters that are used during breakout training otherwise it will fail.
    #breakout_features = df_breakout[['Open_Close','MA20','OC-%-MA20','MaxOC_Prev10','MA20_Volume','Volume-%-MA20_Volume']]
    
    #predictions = existing_model.predict(breakout_features)

    clustering_features = df_breakout[['Open_Close','MA20','OC-%-MA20','MaxOC_Prev10','MA20_Volume','Volume-%-MA20_Volume','Breakout']]

    # Use K-Means to cluster historical price movements
    num_clusters = 2
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    
    kmeans_clusters = kmeans.fit_predict(clustering_features)

    # Visualize the K-Means clusters
    plt.scatter(df_breakout['Open_Close'], df_breakout['MA20'], c=kmeans_clusters, cmap='viridis')
    plt.xlabel('Daily returns')
    plt.ylabel('MA20')
    plt.title('K-Means Clustering of Daily Reurns and Volume')
    plt.savefig(f'./static/images/{ticker}_price.png')
    #plt.show()
    plt.close()

    breakout_cluster =kmeans.predict(clustering_features)

    similar_periods = df_breakout[kmeans_clusters == breakout_cluster[0]]

    average_future_price_movement = similar_periods['Open_Close'].mean()

    print(average_future_price_movement)

    """ plt.scatter(df_breakout['Date'], df_breakout['Open_Close'], c=breakout_cluster, cmap='viridis')
    plt.xlabel('Date')
    plt.ylabel('Daily Returns')
    plt.title('K-Means Clustering of Daily Returns')
    plt.savefig(f'./static/images/{ticker}_price.png')
    #plt.show()
    plt.close() """
        
    

    # Find historical periods with a similar cluster
    
    # Calculate the average future price movement for the identified cluster
    #average_future_price_movement = similar_periods['FuturePrice'].mean()

    #print(f'Predicted Average Future Price Movement: {average_future_price_movement}')

