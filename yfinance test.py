import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "AAPL"

df_1m = yf.download(tickers=ticker, period="1D", interval="1m")
df_1d = yf.download(tickers=ticker, period="3D", interval="1d")
total_volume = df_1m['Volume'].sum()
print(df_1m)
print(total_volume)

pd.set_option('display.max_rows', None)

print(df_1d)

# 繪製折線圖
df_1m.plot()

# 顯示圖形
plt.show()