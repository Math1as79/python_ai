import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import joblib

def run_price_prediction(ticker, df_breakout):
    # Load Model that was saved during breakout training if accuracy above 75%
    df_breakout = df_breakout[df_breakout['Breakout'] == True]

    # Need at least as many entries as we have clusters otherwise clustering will fail 
    if len(df_breakout) >= 3:
        existing_model = joblib.load(f'./models/{ticker}_breakout.joblib')
        
        # Needs to be the same parameters that are used during breakout training otherwise it will fail.
        breakout_features = df_breakout[['Open_Close','MA20','OC-%-MA20','MaxOC_Prev10','MA20_Volume','Volume-%-MA20_Volume']]
        
        existing_model_predictions = existing_model.predict(breakout_features)

        # Use K-Means to cluster historical price movements
        num_clusters = 3
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        
        kmeans.fit(breakout_features)

        breakout_cluster =kmeans.predict(breakout_features)
        
        similar_periods = df_breakout[kmeans.labels_ == breakout_cluster[0]]

        # Mutliple breakouts will give a more fair cluster picture of what the future price of the breakout might be
        average_future_price_movement = similar_periods['Open_Close'].mean()

        # Combine predictions 
        combined_predictions = (existing_model_predictions + breakout_cluster) / 2

        # Visualize Combined Predictions
        plt.plot(df_breakout['Date'], existing_model_predictions, label='Existing Model Predictions')
        plt.scatter(df_breakout['Date'], combined_predictions, c='red', label='Combined Predictions', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Predictions')
        plt.title('Combined Predictions Over Time')
        plt.legend()

        plt.savefig(f'./static/images/{ticker}_predictions.png')
        plt.close()

        f = open(f'./data/predictions/{ticker}_future_price.txt', "w")
        f.write(str(average_future_price_movement))
        f.close()

        combined_predictions_df = pd.DataFrame({'Date': df_breakout['Date'], 'CombinedPredictions': combined_predictions})
        combined_predictions_df.to_csv('./data/predictions/combined_predictions.csv', index=False) 

        return average_future_price_movement

    
    
        
    

    
    
    

