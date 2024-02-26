import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mplfinance as mpf
import os

def plot_graph(df_prices, ticker):
    if os.path.isfile(f'./static/images/{ticker}.png') == False:
        fig, axes = mpf.plot(df_prices,returnfig=True,volume=True,
                     figsize=(11,8),panel_ratios=(2,1),
                     title=f'\n\n{ticker}',type='candle',mav=(10,20))
    
        fig.savefig(f'./static/images/{ticker}.png')
    

    