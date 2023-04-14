import datetime
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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

# 计算每周的交易量
start_date = datetime.datetime(2022, 1, 1)
end_date = datetime.datetime(2022, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='W')

# 下载所有股票的数据
# all_stocks = sp500_table['Symbol'].str.replace('.', '-').tolist()
all_stocks = sp500_table['Symbol'].str.replace('.', '-', regex=True).tolist()

all_stock_data = yf.download(all_stocks, start=start_date, end=end_date, group_by='ticker')

# 计算每周的总交易量
weekly_total_volume = []
# 计算每周的sector交易量
weekly_volume_by_sector = {sector: [] for sector in sectors}

for start, end in zip(date_range[:-1], date_range[1:]):
    week_total_volume = 0
    for stock in all_stocks:
        if stock in all_stock_data:
            stock_volume = all_stock_data[stock]['Volume'].loc[start:end].sum()
            week_total_volume += stock_volume
    weekly_total_volume.append(week_total_volume)

weekly_volume_by_industry_group = {industry_group: [] for industry_group in industry_groups}

# 计算每周的sector和industry group比例
weekly_percentage_by_sector = {sector: [volume / total for volume, total in zip(week_volumes, weekly_total_volume)] for sector, week_volumes in weekly_volume_by_sector.items()}
weekly_percentage_by_industry_group = {industry_group: [volume / total for volume, total in zip(week_volumes, weekly_total_volume)] for industry_group, week_volumes in weekly_volume_by_industry_group.items()}


for start, end in zip(date_range[:-1], date_range[1:]):
    for sector, stocks in stocks_by_sector.items():
        sector_volume = 0
        for stock in stocks:
            if stock in all_stock_data:
                stock_volume = all_stock_data[stock]['Volume'].loc[start:end].sum()
                sector_volume += stock_volume
        weekly_volume_by_sector[sector].append(sector_volume)

    for industry_group, stocks in stocks_by_industry_group.items():
        industry_group_volume = 0
        for stock in stocks:
            if stock in all_stock_data:
                stock_volume = all_stock_data[stock]['Volume'].loc[start:end].sum()
                industry_group_volume += stock_volume
        weekly_volume_by_industry_group[industry_group].append(industry_group_volume)


# 计算每周的sector和industry group比例
weekly_percentage_by_sector = {sector: [volume / sum(week_volumes) for volume in week_volumes] for sector, week_volumes in weekly_volume_by_sector.items()}
weekly_percentage_by_industry_group = {industry_group: [volume / sum(week_volumes) for volume in week_volumes] for industry_group, week_volumes in weekly_volume_by_industry_group.items()}

# 创建交互式热力图
fig = make_subplots(rows=1, cols=1, subplot_titles=("Sector Weekly Volume Percentage",))

sector_heatmap = go.Heatmap(
    z=list(weekly_percentage_by_sector.values()),
    x=date_range[:-1],
    y=list(weekly_percentage_by_sector.keys()),
    hovertemplate="%{y}: %{z:.2%}<extra></extra>",
    colorscale="Viridis",
    name="sectors",
    showscale=False
)

fig.add_trace(sector_heatmap)

def display_industry_group_data(trace, points, selector):
    selected_sector = points.ys[0]
    selected_week_index = points.xs[0]

    industry_groups_in_sector = sp500_table[sp500_table['GICS Sector'] == selected_sector]['GICS Sub-Industry'].unique()

    industry_group_percentages = [weekly_percentage_by_industry_group[industry_group][selected_week_index] for industry_group in industry_groups_in_sector]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=industry_groups_in_sector, y=industry_group_percentages, text=[f"{p:.2%}" for p in industry_group_percentages], textposition='auto'))
    fig2.update_layout(title=f"{selected_sector} Industry Group Percentage (Week {selected_week_index + 1})", yaxis_title="Percentage", xaxis_tickangle=-45)
    fig2.show()


sector_heatmap.on_click(display_industry_group_data)

fig.update_layout(height=600, width=1000)
fig.show()
print("Finished!")

