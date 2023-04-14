import pandas as pd
import yfinance as yf

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
end_date = '2023-04-12'
performance_by_sector = {}

for sector, stocks in stocks_by_sector.items():
    stock_data = yf.download(stocks, start=start_date, end=end_date, group_by='ticker')
    sector_performance = 0
    for stock in stocks:
        stock_close = stock_data[stock]['Close']
        stock_return = (stock_close[-1] - stock_close[0]) / stock_close[0]
        sector_performance += stock_return
    performance_by_sector[sector] = sector_performance / len(stocks)

# 输出每个sector的股票表现
for sector, performance in performance_by_sector.items():
    print(f"{sector}: {performance * 100:.2f}%")
