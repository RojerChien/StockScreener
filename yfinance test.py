import yfinance as yf

tickers = yf.Ticker.symbols_available
print(tickers)