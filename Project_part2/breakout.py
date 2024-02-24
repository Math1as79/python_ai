import pandas as pd

# Code logic for manual breakout

# How many candles do we have 
def __estimate_dataframe(df):
    df.hist()

def __add_columns_to_dataframe(df_prices):
    # Add difference between closing price and opening price
    
    # Open-to-Close is the length of the candle's body
    df_prices['Open_to_Close'] = df_prices['Close'] - df_prices['Open']

    # Add 20-Day moving average for Open-to-Close column, could have added MA50 and MA10 as well
    df_prices['MA20'] = df_prices['Open_to_Close'].rolling(20).mean()

    # Calculate the % change of the current day's Open-to-Close relative to the moving average
    df_prices['Change_op_ma20'] = 100*(df_prices['Open-to-Close'] - df_prices['MA20'])/df_prices['MA20']

    # Get the maximum Open Close compared to the recent 10 candles (including the current candle)
    df_prices['MaxOC_Prev10'] = df_prices['O-to-C'].rolling(10).max()

    #  Volume columns
    # Add 20-Day moving average for volume 
    df_prices['Volume-MA20'] = df_prices['volume'].rolling(20).mean()

    # Calculate the % change of the current volume relative to the moving average
    df_prices['Volume-%-from-20D-Mean'] = 100*(df_prices['volume'] - df_prices['Volume-MA20'])/df_prices['Volume-MA20']

def run_breakout(ticker):
    #Find files with that ticker take the latest one
    df_prices = pd.read_csv(f'./data/prices/{ticker}.csv')

