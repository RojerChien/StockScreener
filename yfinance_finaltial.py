import yfinance as yf
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
data_org = yf.download("AAPL", period="3y", progress=False)
# 重置索引以将'symbol'级别移除
# data_org = data_org.reset_index(level='symbol')

# 将'date'列设置为新的索引
# ata_org = data_org.set_index('date')
temp = data_org.head(3)
print(temp)
