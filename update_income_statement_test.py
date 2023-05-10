import os
import time
import pandas as pd
from yahooquery import Ticker

def get_income_statement_q_single(ticker_list):
    get_data_start_time = time.time()  # Record start time
    print("Start Getting Income Statement Quarterly")
    income_statement_q = Ticker(ticker_list).income_statement(frequency='q')
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = round(get_data_end_time - get_data_start_time, 2)  # Compute elapsed time
    print(f"Get Income Statement Quarterly Elapsed time: {get_data_elapsed_time} seconds")
    return income_statement_q

def update_income_statement(tickers_in):
    csv_file = 'income_statement.csv'
    if os.path.exists(csv_file):
        # Read the CSV file
        # income_statement_q_csv = pd.read_csv(csv_file, index_col=0)
        income_statement_q_csv = pd.read_csv(csv_file, index_col=0, parse_dates=['asOfDate'])

        print("CSV file has been read.")
        print(income_statement_q_csv)
    else:
        print("Can't find CSV file.")
        income_statement_q_csv = pd.DataFrame()

    income_statement_q = get_income_statement_q_single(tickers_in)
    print(income_statement_q)

    # Reset the index of both DataFrames, and apply the changes in-place
    income_statement_q_csv.reset_index(inplace=True)
    income_statement_q.reset_index(inplace=True)

    # 合併兩個 DataFrame
    income_statement_q_all = pd.concat([income_statement_q_csv, income_statement_q])

    # Remove duplicates based on all columns
    income_statement_q_all.drop_duplicates(inplace=True)

    # Set 'symbol' as the index again, and apply the changes in-place
    income_statement_q_all.set_index('symbol', inplace=True)

    print("income_statement_q_all")
    print(income_statement_q_all)

    # 在寫入 CSV 文件之前，刪除 'index' 列（如果存在）
    if 'index' in income_statement_q_all.columns:
        income_statement_q_all.drop(columns=['index'], inplace=True)

    # 寫入csv檔
    income_statement_q_all['asOfDate'] = income_statement_q_all['asOfDate'].dt.strftime('%Y-%m-%d')
    income_statement_q_all.to_csv('income_statement.csv', index=True)

    return income_statement_q_all

test_tickers = ['CCS', 'FLNG', 'ENLT', 'PCAR', 'TSLA']
income_statement_q = update_income_statement(test_tickers)