import yfinance as yf
row = "AAPL"
ticker = yf.Ticker("AAPL")
#df = yf.download(row, period="2y")
#print (df)
df = ticker.info
#sector = info['sector']
print(df)

#import yfinance as yf

#tickers = yf.Tickers('msft aapl goog')

# access each ticker using (example)
#aa = tickers.tickers['MSFT'].info
#print(aa)
