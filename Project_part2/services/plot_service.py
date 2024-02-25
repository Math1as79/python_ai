import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mplfinance as mpf


def plot_graph(df_prices, ticker):
    fig, axes = mpf.plot(df_prices,returnfig=True,volume=True,
                     figsize=(11,8),panel_ratios=(2,1),
                     title=f'\n\n{ticker}',type='candle',mav=(10,20))
    
    
    fig.savefig(f'./static/images/{ticker}.png')
    

    