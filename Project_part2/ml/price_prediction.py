import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

def run_price_prediction(ticker):
    df_breakout = pd.read_csv(f'./data/breakout/{ticker}.csv')
    loaded_model = joblib.load(f'./models/{ticker}.joblib')

    # Loop breakout data for each breakout date 
    for row in df_breakout.iterrows():
        features_for_prediction = df_breakout[['Short_MA', 'Long_MA', 'MACD', 'Signal_Line']].values
        # Make a price prediction
        prediction = loaded_model.predict(features_for_prediction)[0]

    # Display the result
    print(f"For the breakout date {breakout_date}, the model predicts {'Increase' if prediction else 'No Increase'} in stock price.")


""" 
#new_data = yf.download(symbol, start="2022-01-01", end="2022-02-01")
new_features = pd.DataFrame(new_data['Close'])
new_features_scaled = scaler.transform(new_features)

# Use the trained model to predict the percentage change
predicted_percentage_change = model.predict(new_features_scaled)
print(f'Predicted Percentage Change: {predicted_percentage_change}') """