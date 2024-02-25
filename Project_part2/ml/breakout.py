import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def generate_breakout_feauters(df_prices, volume=False):
    # quite generous breakout conditions
    df_prices['SMA50'] = df_prices['Close'].rolling(window=50).mean()
    df_prices['SMA200'] = df_prices['Close'].rolling(window=200).mean()
    df_prices['Price_vs_SMA50'] = df_prices['Close'] - df_prices['SMA50']
    df_prices['Price_vs_SMA200'] = df_prices['Close'] - df_prices['SMA200']
    df_prices['Volume_vs_SMA50'] = df_prices['Volume'].rolling(window=50).mean()
    df_prices['Volume_vs_SMA200'] = df_prices['Volume'].rolling(window=200).mean()

    if volume == True:
        df_prices['Breakout'] = (df_prices['Price_vs_SMA50'] > 0) & (df_prices['Price_vs_SMA200'] > 0) & (df_prices['Volume_vs_SMA50'] > 0) & (df_prices['Volume_vs_SMA200'] > 0)
    else:
        df_prices['Breakout'] = (df_prices['Price_vs_SMA50'] > 0) & (df_prices['Price_vs_SMA200'] > 0)

    return df_prices.dropna()
    

def run_breakout(ticker):
    #Read in prices from ticker dataframe
    df_prices = pd.read_csv(f'./data/prices/{ticker}.csv')
    df_breakout = generate_breakout_feauters(df_prices, True)

    df_breakout.to_csv(f'./data/breakout/{ticker}.csv')
    
    X = df_breakout[['SMA50', 'SMA200', 'Price_vs_SMA50', 'Price_vs_SMA200', 'Volume_vs_SMA50', 'Volume_vs_SMA200']]
    y = df_breakout['Breakout'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a decision tree classifier
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = clf.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    
    return accuracy * 100

#run_breakout('TSLA')
