import pandas as pd
import yfinance as yf

# 获取SP500公司列表
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_data = pd.read_html(sp500_url)
sp500_table = sp500_data[0]

# 获取每个sector的股票列表
sectors = sp500_table['GICS Sector'].unique()
stocks_by_sector = {sector: sp500_table[sp500_table['GICS Sector'] == sector]['Symbol'].tolist() for sector in sectors}

# 获取每个industry group的股票列表
industry_groups = sp500_table['GICS Sub-Industry'].unique()
stocks_by_industry_group = {industry_group: sp500_table[sp500_table['GICS Sub-Industry'] == industry_group]['Symbol'].tolist() for industry_group in industry_groups}

# 将BRK.B替换为BRK-B
for sector in stocks_by_sector:
    stocks_by_sector[sector] = [stock.replace(".", "-") for stock in stocks_by_sector[sector]]
for industry_group in stocks_by_industry_group:
    stocks_by_industry_group[industry_group] = [stock.replace(".", "-") for stock in stocks_by_industry_group[industry_group]]

# 计算每个sector及industry group的平均交易量
start_date = '2022-01-01'
end_date = '2022-12-31'
volume_by_sector = {}
volume_by_industry_group = {}
volume_by_sector_and_industry_group = {}

# 计算各sector及industry group在总交易量中的比例
total_volume = sum(volume_by_sector.values())
volume_percentage_by_sector = {sector: (volume / total_volume) for sector, volume in volume_by_sector.items()}
total_volume_industry_group = sum(volume_by_industry_group.values())
volume_percentage_by_industry_group = {industry_group: (volume / total_volume_industry_group) for industry_group, volume in volume_by_industry_group.items()}


for sector, stocks in stocks_by_sector.items():
    stock_data = yf.download(stocks, start=start_date, end=end_date, group_by='ticker')
    sector_volume = 0
    industry_groups_in_sector = sp500_table[sp500_table['GICS Sector'] == sector]['GICS Sub-Industry'].unique()
    industry_group_volumes = {}

    for industry_group in industry_groups_in_sector:
        industry_group_stocks = stocks_by_industry_group[industry_group]
        industry_group_volume = 0
        for stock in industry_group_stocks:
            if stock in stock_data:
                stock_volume = stock_data[stock]['Volume'].mean()
                sector_volume += stock_volume
                industry_group_volume += stock_volume
        industry_group_volumes[industry_group] = industry_group_volume / len(industry_group_stocks)

    volume_by_sector_and_industry_group[sector] = {
        'sector_volume': sector_volume / len(stocks),
        'industry_group_volumes': industry_group_volumes
    }

# 计算各sector及industry group在总交易量中的比例
total_volume = sum(volume_by_sector.values())
volume_percentage_by_sector = {sector: (volume / total_volume) for sector, volume in volume_by_sector.items()}
total_volume_industry_group = sum(volume_by_industry_group.values())
volume_percentage_by_industry_group = {industry_group: (volume / total_volume_industry_group) for industry_group, volume in volume_by_industry_group.items()}

# 输出各sector及industry group的交易量及在总交易量中的比例
print("Sectors:")
for sector, percentage in volume_percentage_by_sector.items():
    print(f"{sector}: {volume_by_sector[sector]:,.0f}, {percentage * 100:.2f}%")

print("\nIndustry Groups:")
for industry_group, percentage in volume_percentage_by_industry_group.items():
    print(f"{industry_group}: {volume_by_industry_group[industry_group]:,.0f}, {percentage * 100:.2f}%")

# 输出各sector及其包含的industry groups的交易量
print("Sectors and Industry Groups:")
for sector, data in volume_by_sector_and_industry_group.items():
    print(f"{sector}: {data['sector_volume']:.0f}")
    for industry_group, volume in data['industry_group_volumes'].items():
        print(f"  - {industry_group}: {volume:.0f}")

# 输出各sector及industry group的交易量及在总交易量中的比例
print("Sectors:")
for sector, percentage in volume_percentage_by_sector.items():
    print(f"{sector}: {volume_by_sector[sector]:,.0f}, {percentage * 100:.2f}%")

print("\nIndustry Groups:")
for industry_group, percentage in volume_percentage_by_industry_group.items():
    print(f"{industry_group}: {volume_by_industry_group[industry_group]:,.0f}, {percentage * 100:.2f}%")

# 计算sector及industry group百分比的总和
total_percentage_sectors = sum(volume_percentage_by_sector.values()) * 100
total_percentage_industry_groups = sum(volume_percentage_by_industry_group.values()) * 100

print("\nTotal Percentage:")
print(f"Sectors: {total_percentage_sectors:.2f}%")
print(f"Industry Groups: {total_percentage_industry_groups:.2f}%")