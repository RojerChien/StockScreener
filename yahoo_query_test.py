from yahooquery import Ticker
from tabulate import tabulate
import time


def get_fund_ownership_number(ticker, fund_ownership_data):
    if 'symbol' not in fund_ownership_data.columns:
        fund_ownership_data.reset_index(inplace=True)
    # fund_ownership_data.reset_index(inplace=True)  # 重置索引，将 symbol 转换为列
    # 筛选 symbol 为 'ticker' 的行
    filtered_data = fund_ownership_data[fund_ownership_data['symbol'] == ticker]
    print(filtered_data)
    fund_ownership_no = len(filtered_data)
    return fund_ownership_no


def get_yq_financial_data_single(ticker_list):
    get_data_start_time = time.time()  # Record start time
    print("Start Getting Stock Financial Data")
    asset_profile = Ticker(ticker_list).asset_profile
    income_statement_q = Ticker(ticker_list).income_statement(frequency='q')
    fund_ownership = Ticker(ticker_list).fund_ownership
    summary_detail = Ticker(ticker_list).summary_detail
    summary_profile = Ticker(ticker_list).summary_profile
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = round(get_data_end_time - get_data_start_time, 2)  # Compute elapsed time
    print(f"Get Financial Data Elapsed time: {get_data_elapsed_time} seconds")
    return asset_profile, income_statement_q, fund_ownership, summary_detail, summary_profile


def get_income_statement_q_eps(ticker, income_statement_q_data):
    # 如果索引尚未被重置，則重置索引，将 symbol 转换为列
    if 'symbol' not in income_statement_q_data.columns:
        income_statement_q_data.reset_index(inplace=True)
    # 筛选 symbol 为 'ticker' 的行
    filtered_data = income_statement_q_data[income_statement_q_data['symbol'] == ticker]

    # 筛选 periodType = 3M 的行
    filtered_data = filtered_data[filtered_data['periodType'] == '3M']

    # 仅选择 asOfDate, BasicEPS 和 DilutedEPS 列
    selected_columns = filtered_data[['asOfDate', 'BasicEPS', 'DilutedEPS']]

    # 按 asOfDate 降序排列
    sorted_data = selected_columns.sort_values(by='asOfDate', ascending=False)

    # 重置索引
    sorted_data.reset_index(drop=True, inplace=True)

    basic_eps_0 = sorted_data.iloc[0]['BasicEPS']
    basic_eps_4 = sorted_data.iloc[4]['BasicEPS']
    return basic_eps_0, basic_eps_4


def get_income_statement_q_eps_old(ticker, income_statement_q_data):
    income_statement_q_data.reset_index(inplace=True)  # 重置索引，将 symbol 转换为列
    # 筛选 symbol 为 'ticker' 的行
    filtered_data = income_statement_q_data[income_statement_q_data['symbol'] == ticker]

    # 筛选 periodType = 3M 的行
    filtered_data = filtered_data[filtered_data['periodType'] == '3M']

    # 仅选择 asOfDate, BasicEPS 和 DilutedEPS 列
    selected_columns = filtered_data[['asOfDate', 'BasicEPS', 'DilutedEPS']]

    # 按 asOfDate 降序排列
    sorted_data = selected_columns.sort_values(by='asOfDate', ascending=False)

    # 重置索引
    sorted_data.reset_index(drop=True, inplace=True)

    basic_eps_0 = sorted_data.iloc[0]['BasicEPS']
    basic_eps_4 = sorted_data.iloc[4]['BasicEPS']
    return basic_eps_0, basic_eps_4


tickers = ['PCAR','GOOG', 'GOOGL', 'AMZN']

asset_profile, income_statement_q, fund_ownership, summary_detail_source, summary_profile = \
        get_yq_financial_data_single(tickers)


filter_tickers = []
for ticker in tickers:
        # 得到的資料格式，若是dict的話，可以用以下的方式去查詢
        sector = summary_profile[ticker]['sector']
        industry = summary_profile[ticker]['industry']
        website = summary_profile[ticker]['website']
        eps_0, eps_4 = get_income_statement_q_eps(ticker, income_statement_q)
        # fund_ownership = fund_ownership.loc[ticker]
        fund_ownership_number = get_fund_ownership_number(ticker, fund_ownership)
        print("")
        print(f'ticker:{ticker}')
        print(f'sector:{sector}')
        print(f'industry:{industry}')
        print(f'website:{website}')
        print(f'eps_0:{eps_0}')
        print(f'eps_4:{eps_4}')
        print(f'fund_ownership_number:{fund_ownership_number}')

# data = Ticker('goog, googl, amzn, pcar').income_statement(frequency='q')

# table = tabulate(income_statement_q, headers='keys', tablefmt='psql')
# print(income_statement_q)
# eps_0, eps_4 = get_income_statement_q_eps('PCAR', income_statement_q)
# print(eps_0)
# print(eps_4)
# print(income_statement_q)