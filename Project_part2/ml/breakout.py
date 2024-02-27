import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Function to train the RandomForestClassifier
def train_model(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, accuracy

#https://python.plainenglish.io/coding-stock-breakouts-in-python-a-step-by-step-guide-592211e36774
def __generate_breakout_feauters(df_prices, volume=False):
    df_prices['Short_MA'] = df_prices['Close'].ewm(span=12, adjust=False).mean()
    df_prices['Long_MA'] = df_prices['Close'].ewm(span=26, adjust=False).mean()
    df_prices['MACD'] = df_prices['Short_MA'] - df_prices['Long_MA']
    df_prices['Signal_Line'] = df_prices['MACD'].ewm(span=9, adjust=False).mean()
    
    df_prices['Volume_MA'] = df_prices['Volume'].ewm(span=12, adjust=False).mean()
    df_prices['Volume_Ratio'] = df_prices['Volume'] / df_prices['Volume_MA']
    
    return df_prices.dropna()

def __generate_breakout_labels(df_breakout, threshold=0):
    df_breakout['Breakout'] = (df_breakout['MACD'] > threshold) & (df_breakout['Signal_Line'] > threshold) 
    return df_breakout

def run_breakout(ticker):
    #Read in prices from ticker dataframe
    df_prices = pd.read_csv(f'./data/prices/{ticker}.csv')
    # Drop some columns that are not needed
    df_prices =df_prices.drop(['High'],['Low'])
    df_breakout = __generate_breakout_feauters(df_prices, True)
    # Need to tweak threshold/model and analyse it more to be able to hit breakpoints that I deem to be interesting
    df_breakout = __generate_breakout_labels(df_breakout, 10)
    
    # Split the dataset into what we want to train and what we want to predict
    features = df_breakout[['Short_MA', 'Long_MA', 'MACD', 'Signal_Line', 'Volume_Ratio']]
    labels = df_breakout['Breakout']

    # Only save entries where breakout = true
    df_breakout = df_breakout[df_breakout['Breakout'] == True]
    df_breakout.to_csv(f'./data/breakout/{ticker}.csv')

    trained_model, accuracy = train_model(features, labels)
    
    # The model seems to be overfitting, the accuracy is to high
    if accuracy > 0.75:
        # Saving the model, so that going foward it can be feed 
        joblib.dump(trained_model, f'./models/{ticker}_breakout.joblib')

    return {'Accuracy':accuracy * 100,'Data':df_breakout }

def get_breakout_data(ticker):
    df_data = pd.read_csv(f'./data/breakout/{ticker}.csv')
    df_breakout = df_data[['Date','Open','Close','Volume','MACD','Signal_Line']].copy()
    return df_breakout 

#run_breakout('TSLA')
