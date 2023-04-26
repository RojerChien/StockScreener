import yfinance as yf
from yahooquery import Ticker
sp500_symbols = ['AAPL', 'TSLA']


ticker = Ticker(sp500_symbols, asynchronous=True)
data_all = ticker.history(period="3y", interval="1d")
print(data_all)

"""# 設定回測時間範圍
start_date = '2023-04-01'
end_date = '2023-04-25'
all_stock_data = yf.download(sp500_symbols, start=start_date, end=end_date, group_by='ticker')
print(all_stock_data)"""
