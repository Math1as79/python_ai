import pandas as pd

# Code logic for manual breakout

# How many candles do we have 

def __estimate_dataframe(df):
    df.hist()

def __add_columns_to_dataframe(df_prices):
    # Add difference between closing price and opening price
    # NOTE: O-to-C is the length of the candle's body
    df_prices['Open_to_Close'] = df_prices['Close'] - df_prices['Open']

    # Add 20-Day moving average for Open-to-Close column
    df_prices['MA20'] = df_prices['Open_to_Close'].rolling(20).mean()

def run_breakout(ticker):
    df_prices = pd.read_csv(f'./data/prices/{ticker}.csv')

