# Stock analysis

This a an application combining a Flask UI with difference machine learning models. 

## Run application

Either via the debug in Visual studio code or via terminal: python -m flask run --no-debugger --no-reload

## Application flow

Choose a ticker => run breakout and train a ml model to be able to identify breakout => run a sentiment anlysis of tweets occuring 3 days before and up to breakout date => run a price prediction to see how much the stock might increase

## Authors and acknowledgment

Mathias Medin