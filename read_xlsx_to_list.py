import pandas as pd
### 從Tickers.xlsx，去讀取不同的sheet，然後設成ticker list ###
# 讀取 Excel 檔案，選取 TW 工作表中的第一欄資料
df_tw = pd.read_excel("Tickers.xlsx", sheet_name="TW", usecols=[0])
df_us = pd.read_excel("Tickers.xlsx", sheet_name="US", usecols=[0])
df_etf = pd.read_excel("Tickers.xlsx", sheet_name="ETF", usecols=[0])
# 將讀取到的資料轉換為 list，並存入 tw_tickers 變數中
tw_tickers = df_tw.iloc[:, 0].tolist()
us_tickers = df_us.iloc[:, 0].tolist()
etf_tickers = df_etf.iloc[:, 0].tolist()

tw_tickers_length = len(tw_tickers)
us_tickers_length = len(us_tickers)
etf_tickers_length = len(etf_tickers)

print("Total TW Tickers:",tw_tickers_length)
print("Total US Tickers:",us_tickers_length)
print("Total ETF Tickers:",etf_tickers_length)