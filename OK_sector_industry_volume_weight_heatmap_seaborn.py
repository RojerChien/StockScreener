import datetime
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from dateutil.relativedelta import relativedelta
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday

def calculate_industry_group_data(selected_sector, selected_week_index):
    selected_week_index = selected_week_index - 1
    industry_groups_in_sector = sp500_table[sp500_table['GICS Sector'] == selected_sector]['GICS Sub-Industry'].unique()

    industry_group_percentages = [weekly_percentage_by_industry_group[industry_group][selected_week_index] for
                                  industry_group in industry_groups_in_sector]

    return industry_groups_in_sector, industry_group_percentages


def display_industry_group_data(selected_sector, selected_duration_index, industry_groups_in_sector, industry_group_percentages):
    # 创建 DataFrame
    industry_group_df = pd.DataFrame(
        {"Industry Group": industry_groups_in_sector, "Percentage": industry_group_percentages})

    # 绘制条形图
    plt.figure(figsize=(20, 10))
    ax = sns.barplot(x="Industry Group", y="Percentage", data=industry_group_df, palette="viridis")
    plt.title(f"{selected_sector} Industry Group Percentage (Week {selected_duration_index + 1})")
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Percentage")

    # 添加百分比标签
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2%}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='baseline', fontsize=9, color='black', xytext=(0, 3),
                    textcoords='offset points')

    # plt.show()
    plt.savefig(f"R_{selected_sector}_Week_{selected_duration_index + 1}.png", bbox_inches='tight')



# display_industry_group_data("Information Technology", 3) # 顯示Information Technology第三週的heatmap

# 获取SP500公司列表
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_data = pd.read_html(sp500_url)
sp500_table = sp500_data[0]
# print(sp500_table)
# 获取每个sector的股票列表
sectors = sp500_table['GICS Sector'].unique()
# print(sectors)
stocks_by_sector = {sector: sp500_table[sp500_table['GICS Sector'] == sector]['Symbol'].tolist() for sector in sectors}
# print(stocks_by_sector)

# 获取每个industry group的股票列表
industry_groups = sp500_table['GICS Sub-Industry'].unique()
stocks_by_industry_group = {
    industry_group: sp500_table[sp500_table['GICS Sub-Industry'] == industry_group]['Symbol'].tolist() for
    industry_group in industry_groups}

# 将BRK.B替换为BRK-B
for sector in stocks_by_sector:
    stocks_by_sector[sector] = [stock.replace(".", "-") for stock in stocks_by_sector[sector]]
for industry_group in stocks_by_industry_group:
    stocks_by_industry_group[industry_group] = [stock.replace(".", "-") for stock in
                                                stocks_by_industry_group[industry_group]]

# 在此添加一个频率变量，可选值为'D'（日）、'W'（周）或'M'（月）
frequency = 'D'
time_value = 31

us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())




class CustomHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Year Holiday', month=1, day=2),
        Holiday('Martin Luther King Jr. Day', month=1, day=16),
        Holiday('Washington Day', month=2, day=20),
        Holiday('Good Friday', month=4, day=7),
        Holiday('Memorial Day', month=5, day=29),
        Holiday('Juneteenth', month=6, day=19),
        Holiday('Independence Day', month=7, day=4),
        Holiday('Labor Day', month=9, day=4),
        Holiday('Thanksgiving Day', month=11, day=23),
        Holiday('Christmas Day', month=12, day=25)
    ]

custom_bd = CustomBusinessDay(calendar=CustomHolidayCalendar())

# 计算每日/周/月的交易量
if frequency == 'D':
    # 获取今天的日期
    today = datetime.datetime.today()
    time_ago = today - relativedelta(days=time_value)
    start_date = time_ago
    end_date = today
    # date_range = pd.date_range(start_date, end_date, freq='D')
    date_range = pd.date_range(start_date, end_date, freq=custom_bd)

elif frequency == 'W':
    today = datetime.datetime.today()
    time_ago = today - relativedelta(weeks=time_value)
    start_date = time_ago
    end_date = today
    date_range = pd.date_range(start_date, end_date, freq='W')
elif frequency == 'M':
    today = datetime.datetime.today()
    time_ago = today - relativedelta(months=time_value)
    start_date = time_ago
    end_date = today
    date_range = pd.date_range(start_date, end_date, freq='M')
else:
    raise ValueError("Invalid frequency value, choose 'D', 'W', or 'M'")

# 下载所有股票的数据
all_stocks = sp500_table['Symbol'].str.replace('.', '-', regex=True).tolist()
# all_stock_data = yf.download(all_stocks, start=start_date, end=end_date)
all_stock_data = yf.download(all_stocks, start=start_date, end=end_date, group_by='ticker')

# 计算每周的总交易量
weekly_total_volume = []
# 计算每周的sector交易量
weekly_volume_by_sector = {sector: [] for sector in sectors}
# print(weekly_volume_by_sector)

for start, end in zip(date_range[:-1], date_range[1:]):
    week_total_volume = 0
    for stock in all_stocks:
        if stock in all_stock_data.columns.get_level_values(0):
            stock_volume = all_stock_data[stock]['Volume'].loc[start:end].sum()
            week_total_volume += stock_volume
    weekly_total_volume.append(week_total_volume)
# print(weekly_total_volume)
weekly_volume_by_industry_group = {industry_group: [] for industry_group in industry_groups}
# print(weekly_volume_by_industry_group)

for start, end in zip(date_range[:-1], date_range[1:]):
    for sector, stocks in stocks_by_sector.items():
        sector_volume = 0
        for stock in stocks:
            if stock in all_stock_data.columns.get_level_values(0):
                stock_volume = all_stock_data[stock]['Volume'].loc[start:end].sum()
                sector_volume += stock_volume
        weekly_volume_by_sector[sector].append(sector_volume)

    for industry_group, stocks in stocks_by_industry_group.items():
        industry_group_volume = 0
        for stock in stocks:
            if stock in all_stock_data.columns.get_level_values(0):
                stock_volume = all_stock_data[stock]['Volume'].loc[start:end].sum()
                industry_group_volume += stock_volume
        weekly_volume_by_industry_group[industry_group].append(industry_group_volume)

# 计算每周的sector和industry group比例
weekly_percentage_by_sector = {
    sector: [volume / total_volume if total_volume != 0 else 0 for volume, total_volume in zip(week_volumes, weekly_total_volume)]
    for sector, week_volumes in weekly_volume_by_sector.items()
}
weekly_percentage_by_industry_group = {
    industry_group: [volume / total_volume if total_volume != 0 else 0 for volume, total_volume in zip(week_volumes, weekly_total_volume)]
    for industry_group, week_volumes in weekly_volume_by_industry_group.items()
}

# print(weekly_percentage_by_sector)
# print(weekly_percentage_by_industry_group)

# 转换为 DataFrame
percentage_df = pd.DataFrame(weekly_percentage_by_sector).T
percentage_df.index = weekly_percentage_by_sector.keys()
# percentage_df.columns = date_range[:-1]
percentage_df.columns = [date.strftime('%Y-%m-%d') for date in date_range[:-1]]
# percentage_df.columns = [date.strftime('%Y-%m-%d') for date in date_range[:-1]]


# 绘制热力图
plt.figure(figsize=(20, 10))
# sns.heatmap(percentage_df, annot=True, fmt=".1%", cmap="viridis", linewidths=.5, annot_kws={"size": 6})
sns.heatmap(percentage_df, annot=True, fmt=".1%", cmap="plasma", linewidths=.5, annot_kws={"size": 8})
plt.title("Sector Weekly Volume Percentage")
plt.xticks(rotation=45)
plt.show()

for sector in sectors:
    industry_groups_in_sector, industry_group_percentages = calculate_industry_group_data(sector, 6)
    display_industry_group_data(sector, 6, industry_groups_in_sector, industry_group_percentages)

print("Start date:", all_stock_data.index.min())
print("End date:", all_stock_data.index.max())
print("Finished!")

