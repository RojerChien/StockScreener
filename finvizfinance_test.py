from finvizfinance.screener.overview import Overview

def get_finviz_screener_tickers():
    foverview = Overview()
    filters_dict = {'20-Day Simple Moving Average':'SMA20 above SMA50',
                    '50-Day Simple Moving Average':'SMA50 above SMA200',
                    'Change':'Up 3%'}
    foverview.set_filter(filters_dict=filters_dict)
    df = foverview.screener_view()
    print(df)
    tickers = df['Ticker'].tolist()
    return tickers


tickers = get_finviz_screener_tickers()
print(tickers)
"""foverview = Overview()
filters_dict = {'20-Day Simple Moving Average':'SMA20 above SMA50','50-Day Simple Moving Average':'SMA50 above SMA200','Change':'Up 3%'}
#filters_dict = {'Performance':'Today +5%'}
#filters_dict = {'Exchange':'AMEX','Sector':'Basic Materials'}
foverview.set_filter(filters_dict=filters_dict)
df = foverview.screener_view()
#df.set_option('display.max_rows', None)

print(df)
ticker = df['Ticker'].tolist()
print(ticker)"""