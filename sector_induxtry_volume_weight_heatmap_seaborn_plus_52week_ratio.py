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
import pandas_datareader as pdr
import matplotlib.ticker as mticker


def get_market_cap(ticker):
    try:
        stock_info = yf.Ticker(ticker).info
        market_cap = stock_info.get('marketCap', None)
        print(market_cap)
        return market_cap
    except Exception as e:
        print(f"Error fetching market cap for {ticker}: {e}")
        return None


def get_market_cap_fred(ticker):
    try:
        stock_info = pdr.get_quote_yahoo(ticker)
        market_cap = stock_info.loc[ticker, 'marketCap']
        return market_cap
    except Exception as e:
        print(f"Error fetching market cap for {ticker} from FRED: {e}")
        return None



sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_data = pd.read_html(sp500_url)
sp500_table = sp500_data[0]

sectors = sp500_table['GICS Sector'].unique()
stocks_by_sector = {sector: sp500_table[sp500_table['GICS Sector'] == sector]['Symbol'].tolist() for sector in sectors}

for sector in stocks_by_sector:
    stocks_by_sector[sector] = [stock.replace(".", "-") for stock in stocks_by_sector[sector]]

all_stocks = sp500_table['Symbol'].str.replace('.', '-', regex=True).tolist()
start_date = datetime.datetime.today() - relativedelta(years=2)
end_date = datetime.datetime.today()
all_stock_data = yf.download(all_stocks, start=start_date, end=end_date, group_by='ticker')

latest_close_prices = {}
for stock in all_stocks:
    if stock in all_stock_data.columns.get_level_values(0):
        latest_close_prices[stock] = all_stock_data[stock]['Close'][-1]

sma233 = {}
for stock in all_stocks:
    if stock in all_stock_data.columns.get_level_values(0):
        sma233[stock] = all_stock_data[stock]['Close'].rolling(window=233).mean()[-1]

sector_percentage_above_sma233 = {}
sector_stock_counts = {}
sector_stock_counts_above_sma233 = {}
for sector, stocks in stocks_by_sector.items():
    count_above_sma233 = 0
    for stock in stocks:
        if stock in latest_close_prices and stock in sma233:
            if latest_close_prices[stock] > sma233[stock] * 0.95:
                count_above_sma233 += 1
    sector_percentage_above_sma233[sector] = count_above_sma233 / len(stocks)
    sector_stock_counts[sector] = len(stocks)
    sector_stock_counts_above_sma233[sector] = count_above_sma233

print("Percentage of stocks with latest close price > 95% of SMA233:")
for sector, percentage in sector_percentage_above_sma233.items():
    print(f"{sector}: {percentage:.2%} ({sector_stock_counts_above_sma233[sector]} out of {sector_stock_counts[sector]})")

sector_percentage_df = pd.DataFrame(
    {"Sector": list(sector_percentage_above_sma233.keys()), "Percentage": list(sector_percentage_above_sma233.values())}
)

plt.figure(figsize=(20, 10))
ax = sns.barplot(x="Sector", y="Percentage", data=sector_percentage_df, palette="viridis")
plt.title("Percentage of Stocks with Latest Close Price > 90% of SMA233")
plt.xticks(rotation=45)

sectors_list = list(sector_percentage_above_sma233.keys())

for i, p in enumerate(ax.patches):
    sector = sectors_list[i]
    ax.annotate(f"{p.get_height():.2%}\n({sector_stock_counts_above_sma233[sector]}/{sector_stock_counts[sector]})",
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline', fontsize=9, color='black', xytext=(0, 3),
                textcoords='offset points')

plt.show()

# 获取每个sector的股票列表和industry
sectors_and_industries = sp500_table.groupby(['GICS Sector', 'GICS Sub-Industry'])['Symbol'].apply(list).to_dict()

# 为每个sector生成条形图
for sector, industries in sectors_and_industries.items():
    industry_percentage_above_sma233 = {}
    industry_stock_counts = {}
    industry_stock_counts_above_sma233 = {}

    for industry, stocks in industries.items():
        count_above_sma233 = 0
        for stock in stocks:
            stock = stock.replace(".", "-")
            if stock in latest_close_prices and stock in sma233:
                if latest_close_prices[stock] > sma233[stock] * 0.95:
                    count_above_sma233 += 1
        industry_percentage_above_sma233[industry] = count_above_sma233 / len(stocks)
        industry_stock_counts[industry] = len(stocks)
        industry_stock_counts_above_sma233[industry] = count_above_sma233

    # 绘制sector条形图
    industry_percentage_df = pd.DataFrame(
        {"Industry": list(industry_percentage_above_sma233.keys()),
         "Percentage": list(industry_percentage_above_sma233.values())}
    )

    plt.figure(figsize=(20, 10))
    ax = sns.barplot(x="Industry", y="Percentage", data=industry_percentage_df, palette="viridis")
    plt.title(f"{sector}: Percentage of Stocks with Latest Close Price > 95% of SMA233")
    plt.xticks(rotation=45)

    industries_list = list(industry_percentage_above_sma233.keys())

    # 添加百分比标签
    for i, p in enumerate(ax.patches):
        industry = industries_list[i]
        ax.annotate(f"{p.get_height():.2%}\n({industry_stock_counts_above_sma233[industry]}/{industry_stock_counts[industry]})",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='baseline', fontsize=9, color='black', xytext=(0, 3),
                    textcoords='offset points')

    # 修改y轴百分比显示
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    plt.show()