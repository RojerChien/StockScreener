import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "1456.TW"
ticker2 = yf.Ticker("1456.TW")
df_1m = yf.download(tickers=ticker, period="3D", interval="1m")
df_1d = yf.download(tickers=ticker, period="5D", interval="1d")
hist = ticker2.history(start="2023-03-02", end="2023-03-09")
total_volume = df_1m['Volume'].sum()
#print(df_1m)
print(total_volume)

pd.set_option('display.max_rows', None)
print(df_1m)
print(hist)
print(df_1d)

# 繪製折線圖
df_1m.plot()

# 顯示圖形
plt.show()