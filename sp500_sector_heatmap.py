import pandas as pd
import numpy as np
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# 获取SP500公司列表
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_data = pd.read_html(sp500_url)
sp500_table = sp500_data[0]

# 获取每个sector的股票列表
sectors = sp500_table['GICS Sector'].unique()
stocks_by_sector = {sector: sp500_table[sp500_table['GICS Sector'] == sector]['Symbol'].tolist() for sector in sectors}

# 将BRK.B替换为BRK-B
for sector in stocks_by_sector:
    stocks_by_sector[sector] = [stock.replace(".", "-") for stock in stocks_by_sector[sector]]

# 计算每个sector的股票表现
start_date = '2022-01-01'
end_date = '2022-12-31'
performance_by_sector = {}

for sector, stocks in stocks_by_sector.items():
    stock_data = yf.download(stocks, start=start_date, end=end_date, group_by='ticker')
    sector_performance = []
    for stock in stocks:
        stock_close = stock_data[stock]['Close']
        stock_close = stock_close.resample('W').last()  # 按周重新采样
        stock_return = stock_close.pct_change()  # 计算每周收益率
        sector_performance.append(stock_return)
    performance_by_sector[sector] = pd.concat(sector_performance, axis=1).mean(axis=1)

# 创建热力图
performance_df = pd.DataFrame(performance_by_sector)
performance_df.index = performance_df.index.strftime('%Y-%m-%d')
plt.figure(figsize=(12, 6))
sns.heatmap(performance_df.T, cmap='coolwarm', center=0, annot=True, fmt='.2%', annot_kws={"size": 5})
plt.title("Weekly Sector Stock Perform")
plt.xlabel("日期")
plt.ylabel("Sector")
plt.tight_layout()
plt.show()
