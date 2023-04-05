from yahooquery import Ticker
import pandas as pd
import time

# Compare downloads for all companies within the S&P500
tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sp500 = tables[0]['Symbol'].tolist()
sp500 = [symbol.replace(".", "-") for symbol in sp500]
# sp500 = sp500[:3]

print(sp500)

df_ticker = pd.read_excel("Tickers.xlsx", sheet_name="US", usecols=[0])
us_tickers = df_ticker.iloc[:, 0].tolist()
# us_tickers = us_tickers[:500]
us_tickers_length = len(us_tickers)

start_time = time.time()  # 记录开始时间
tickers = Ticker(us_tickers, asynchronous=True)
print(tickers)
yq_data = tickers.history(period='3y', interval='1d')
print(yq_data)

end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算运行时间

type(yq_data)
yq_data.shape
yq_data.head()
print(yq_data.index.names)

mmm_data = yq_data.loc['MMM']
print(mmm_data)
print(f"Elapsed time: {elapsed_time} seconds")

