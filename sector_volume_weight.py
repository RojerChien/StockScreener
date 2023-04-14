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

# 计算每个sector的平均交易量
start_date = '2023-03-11'
end_date = '2023-04-11'
volume_by_sector = {}

for sector, stocks in stocks_by_sector.items():
    stock_data = yf.download(stocks, start=start_date, end=end_date, group_by='ticker')
    sector_volume = 0
    for stock in stocks:
        stock_volume = stock_data[stock]['Volume'].mean()
        sector_volume += stock_volume
    volume_by_sector[sector] = sector_volume / len(stocks)

# 计算各sector在总交易量中的比例
total_volume = sum(volume_by_sector.values())
volume_percentage_by_sector = {sector: (volume / total_volume) for sector, volume in volume_by_sector.items()}

# 输出各sector的交易量及在总交易量中的比例
for sector, percentage in volume_percentage_by_sector.items():
    print(f"{sector}: {volume_by_sector[sector]:,.0f}, {percentage * 100:.2f}%")
