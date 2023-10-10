import pandas as pd
import pytz
import time
import webbrowser
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import os
import datetime
import numpy as np
import csv
import plotly.graph_objects as go
from finvizfinance.screener.overview import Overview
from pickle import TRUE
from highcharts import Highstock
from IPython.display import HTML, display
from csv import reader
from ta.trend import MACD
from ta.momentum import StochasticOscillator
from plotly.subplots import make_subplots
from bs4 import BeautifulSoup
from finviz.screener import Screener
from yahooquery import Ticker
from datetime import datetime as dt

pd.options.mode.chained_assignment = None  # 將警告訊息關閉

# start = 0
true_number = 0
# run_number = 0
today = str(datetime.datetime.now().date())


def get_ptp_tickers(url1='https://help.zh-tw.firstrade.com/article/841-new-1446-f-regulations',
                    url2='https://www.itigerup.com/bulletin/ptp'):
    # 爬取第一個網站的 PTP 股票代號列表
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.content, "html.parser")

    table1 = soup1.find("table", {"width": "100%"})
    tbody1 = table1.find("tbody")
    rows1 = tbody1.find_all("tr")
    ptp_lists = []

    for row in rows1:
        cols = row.find_all("td")
        if len(cols) == 3:
            symbol = cols[2].get_text().strip()
            ptp_lists.append(symbol)

    # 爬取第二個網站的 PTP 股票代號列表
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    table2 = soup2.find('table', {'class': 'table'})
    rows2 = table2.find_all('tr')
    ptp_tickers = []

    for row in rows2:
        code = row.find('td')
        if code:
            ptp_tickers.append(code.text.strip())

    # 合併兩個列表，並取得不重覆的值，最終返回 PTP 股票代號列表
    ptp_lists.extend(ptp_tickers)
    ptp_lists = list(set(ptp_lists))
    ptp_lists_len = len(ptp_lists)
    print("Total PTP Tickers:", ptp_lists_len)
    return ptp_lists
    print(ptp_lists)


def remove_ptp_list(ptp_tickers, tickers):
    us_non_ptp_tickers = [x for x in tickers if x not in ptp_tickers]
    us_ptp_tickers = [x for x in tickers if x in ptp_tickers]
    print("PTP US stocks:", us_ptp_tickers)
    us_ptp_tickers_length = len(us_ptp_tickers)
    print("Total Removed PTP Tickers:", us_ptp_tickers_length)
    # print("Non-PTP US stocks:", us_non_ptp_tickers)
    return us_non_ptp_tickers


def get_finviz_screener_tickers():
    print("Start getting finviz tickers")
    # 創建 Overview 物件
    foverview = Overview()

    # 定義 Finviz Screener 的篩選條件
    filters_dict = {
        '20-Day Simple Moving Average': 'SMA20 above SMA50',
        '50-Day Simple Moving Average': 'SMA50 above SMA200',
        'Average Volume': 'Over 100K',
        'Price': 'Over $3',
        'EPS growthpast 5 years': 'Positive (>0%)',
        'Change': 'Up 2%'
    }

    # 設置篩選條件
    foverview.set_filter(filters_dict=filters_dict)

    # 獲取篩選後的數據，轉換為 Ticker 列表
    df = foverview.screener_view()
    tickers = df['Ticker'].tolist()
    print(tickers)

    # 返回 Ticker 列表
    return tickers


def get_yq_historical_data(ticker_list):
    # print(ticker_list)
    get_data_start_time = time.time()  # Record start time
    print("Start getting stock historical data")
    ticker = Ticker(ticker_list, asynchronous=True)
    data_all = ticker.history(period="3y", interval="1d")
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = round(get_data_end_time - get_data_start_time, 2)  # Compute elapsed time
    print(f"Get Data Elapsed time: {get_data_elapsed_time} seconds")
    # Save DataFrame as CSV
    # data_all.to_csv('data_all.csv', index=True)
    # Save DataFrame as Parquet
    # data_all.to_parquet('data_all.parquet', index=True)
    return data_all


def add_vwap_to_chart(chart, dfin, window, color, line_width, yAxis=0, id=None):
    vwap = dfin[f'vwap{window}'].values.tolist()
    vwap = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(v, 2)]
        for i, v in enumerate(vwap)
    ]
    chart.add_data_set(vwap, 'line', f'vwap{window}', yAxis=yAxis, color=color, lineWidth=line_width, id=id,
                       dataGrouping={'units': [['day', [1]]]})


def highchart_chart_v2(tickers_in, category_in="US"):
    df = get_yq_historical_data(tickers_in)
    for ticker in tickers_in:
        df_one = sel_yq_historical_data(df, ticker)
        vcp_result = vcp_screener_strategy(ticker, df_one)
        if vcp_result == 1:
            url = get_tradingview_url(ticker, category_in)
            highchart_chart(df_one, ticker, url)


def highchart_chart(dfin, ticker_in, url, date=today):
    # 初始化highstock对象
    chart = Highstock(renderTo='container', width=None, height=930)  # 添加宽度和高度
    # chart = highstock(renderTo='container', width=1800, height=900)  # 添加宽度和高度

    # 加入RSI data
    rsi_data = dfin['RSI'].values.tolist()
    rsi_data = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(r, 2)]
        for i, r in enumerate(rsi_data)
    ]

    # 將RSI加到數據中
    chart.add_data_set(rsi_data, 'line', 'RSI', yAxis=2, dataGrouping={'units': [['day', [1]]]})

    # 添加10日成交量移動平均線
    dfin['volume_10ma'] = dfin['volume'].rolling(window=10).mean()
    volume_10ma = dfin['volume_10ma'].values.tolist()
    volume_10ma = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), v]
        for i, v in enumerate(volume_10ma)
    ]
    chart.add_data_set(volume_10ma, 'line', '10日成交量移動平均', yAxis=1, dataGrouping={'units': [['day', [1]]]})

    # 添加蜡烛图序列
    ohlc = dfin[['open', 'high', 'low', 'close']].values.tolist()
    ohlc = [[int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(o, 2), round(h, 2), round(l, 2), round(c, 2)] for
            i, (o, h, l, c) in enumerate(ohlc)]

    chart.add_data_set(ohlc, 'candlestick', ticker_in, dataGrouping={'units': [['day', [1]]]})
    add_vwap_to_chart(chart, dfin, 144, 'purple', 3, id='vwap144')
    add_vwap_to_chart(chart, dfin, 55, 'red', 3, id='vwap55')
    add_vwap_to_chart(chart, dfin, 21, 'orange', 3, id='vwap21')
    add_vwap_to_chart(chart, dfin, 5, 'blue', 3, id='vwap5')

    # 添加成交量序列
    volume = dfin[['open', 'close', 'volume']].values.tolist()
    volume = [{'x': int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), 'y': v, 'color': 'red' if o > c else 'green'} for
              i, (o, c, v) in enumerate(volume)]

    # chart.add_data_set(volume, 'column', '成交量', yAxis=1, dataGrouping={'units': [['day', [1]]]})
    # 禁用datagroup，讓volume在顯示時是正常的，但也可能影響效能
    chart.add_data_set(volume, 'column', '成交量', yAxis=1, dataGrouping={'enabled': False})

    # 设置图表选项
    options = {
        'chart': {
            'events': {
                'load': """
                    function () {
                        var chart = this;

                        // Create the toggleVwapLines function
                        var toggleVwapLines = function () {
                            var vwap144 = chart.get('vwap144'),
                                vwap55 = chart.get('vwap55'),
                                vwap21 = chart.get('vwap21');
                                vwap5 = chart.get('vwap5');
                            if (vwap144.visible) {
                                vwap144.hide();
                                vwap55.hide();
                                vwap21.hide();
                                vwap5.hide();
                            } else {
                                vwap144.show();
                                vwap55.show();
                                vwap21.show();
                                vwap5.show();
                            }
                        };

                        // Add a custom button
                        chart.renderer.button('Toggle VWAP Lines', null, null, toggleVwapLines)
                            .attr({
                                zIndex: 3
                            })
                            .add();
                    }
                """
            }
        },
        'navigation': {
            'buttonOptions': {
                'align': 'right',
                'verticalAlign': 'top',
                'y': 0
            }
        },
        'rangeSelector': {'selected': 4},
        'title': {'text': f'{ticker_in} ({date})'},
        'yAxis': [
            {'labels': {'align': 'right', 'x': -3},
             'title': {'text': 'OHLC'},
             'height': '70%',
             'lineWidth': 2},
            {'labels': {'align': 'right', 'x': -3},
             'title': {'text': '成交量'},
             'top': '72%',
             'height': '13%',
             'offset': 0,
             'lineWidth': 2},
            {'labels': {'align': 'right', 'x': -3},
             'title': {'text': 'RSI'},
             'top': '87%',  # 調整此值以設置RSI圖表的位置
             'height': '13%',  # 調整此值以設置RSI圖表的高度
             'offset': 0,
             'lineWidth': 2,
             'plotLines': [
                 {'value': 30,
                  'color': '#FF4500',
                  'width': 1},
                 {'value': 70,
                  'color': '#FF4500',
                  'width': 1}
             ]}
        ],
        'tooltip': {
            'formatter': f"""
                function () {{
                    var dataIndex = this.points[0].point.index;
                    var s = '<b>' + Highcharts.dateFormat('%A, %b %e, %Y', this.x) + '</b>';
                    s += '<br/>';

                    this.points.forEach(function (point) {{
                        if (point.series.name === '{ticker_in}') {{
                            s += '<br/>' + point.series.name + ': ';
                            s += 'Open: ' + point.point.open.toFixed(2);
                            s += ', High: ' + point.point.high.toFixed(2);
                            s += ', Low: ' + point.point.low.toFixed(2);
                            s += ', Close: ' + point.point.close.toFixed(2);

                            // 計算漲跌幅
                            var change = 0;
                            if (dataIndex > 0) {{
                                var previousClose = point.series.options.data[dataIndex - 1][4];
                                change = ((point.point.close - previousClose) / previousClose) * 100;
                            }}
                            s += '<br/>漲跌幅: ' + change.toFixed(2) + '%';
                        }} else {{
                            s += '<br/>' + point.series.name + ': ' + point.y;
                        }}
                    }});

                    return s;
                }}
            """
        },
        'plotOptions': {
            'line': {
                'showInLegend': True
            },
            'candlestick': {
                'color': 'red',
                'upColor': 'green'
            },
            'column': {
                'borderColor': 'none'
            }
        },
        'subtitle': {
            'text': f'<a href="{url}" target="_blank" style="color: #003399; text-decoration: underline; cursor: pointer;">TradingView</a>',
            'useHTML': True,
            'align': 'center',
            'y': 35
        },
    }

    chart.set_dict_options(options)

    # 显示图表
    # chart.save_file('candlestick_volume')
    # with open('candlestick_volume.html', 'w', encoding='utf-8') as f:
    # filename = f'./HTML/{date}/{ticker_in}_{date}.html'
    filename = f'{ticker_in}_{date}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(chart.htmlcontent)
    webbrowser.open(filename)


def calculate_rsi(data, period):
    delta = data['close'].diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def get_yq_financial_data_single(ticker_list):
    get_data_start_time = time.time()  # Record start time
    print("Start Getting Stock Financial Data by Single Mode")
    print("Getting asset_profile")
    asset_profile = Ticker(ticker_list).asset_profile
    income_statement_q = Ticker(ticker_list).income_statement(frequency='q')
    fund_ownership = Ticker(ticker_list).fund_ownership
    summary_detail = Ticker(ticker_list).summary_detail
    summary_profile = Ticker(ticker_list).summary_profile
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = round(get_data_end_time - get_data_start_time, 2)  # Compute elapsed time
    print(f"Get Financial Data Elapsed time: {get_data_elapsed_time} seconds")
    return asset_profile, income_statement_q, fund_ownership, summary_detail, summary_profile


def get_income_statement_q_single(ticker_list):
    get_data_start_time = time.time()  # Record start time
    print("Start Getting Income Statement Quarterly")
    income_statement_q = Ticker(ticker_list).income_statement(frequency='q')
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = round(get_data_end_time - get_data_start_time, 2)  # Compute elapsed time
    print(f"Get Income Statement Quarterly Elapsed time: {get_data_elapsed_time} seconds")
    return income_statement_q


def get_yq_financial_data(ticker_list):
    # print(ticker_list)
    get_data_start_time = time.time()  # Record start time
    print("Start Getting Stock Financial Data")
    # fin_data = Ticker(ticker_list).get_modules(['summaryDetail'])
    fin_data = Ticker(ticker_list, validate=True, progress=True).all_modules
    # fin_data = Ticker(ticker_list).get_modules(['incomeStatementHistoryQuarterly',
    # 'fundOwnership', 'summaryDetail', 'summaryProfile'])

    # print(fin_data)
    # fin_data = Ticker(ticker_list).get_modules(['summaryDetail', 'balanceSheetHistory'])
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = round(get_data_end_time - get_data_start_time, 2)  # Compute elapsed time
    print(f"Get Financial Data Elapsed time: {get_data_elapsed_time} seconds")
    # Save DataFrame as CSV
    # data_all.to_csv('data_all.csv', index=True)
    # Save DataFrame as Parquet
    # data_all.to_parquet('data_all.parquet', index=True)
    return fin_data


def get_yq_financial_data_all(ticker_list):
    # print(ticker_list)
    get_data_start_time = time.time()  # Record start time
    print("Start Getting Stock Financial Data")
    # fin_data = Ticker(ticker_list).get_modules(['summaryDetail'])
    fin_data = Ticker(ticker_list, validate=True, progress=True).all_modules

    # print(fin_data)
    # fin_data = Ticker(ticker_list).get_modules(['summaryDetail', 'balanceSheetHistory'])
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = round(get_data_end_time - get_data_start_time, 2)  # Compute elapsed time
    print(f"Get Financial Data Elapsed time: {get_data_elapsed_time} seconds")
    # Save DataFrame as CSV
    # data_all.to_csv('data_all.csv', index=True)
    # Save DataFrame as Parquet
    # data_all.to_parquet('data_all.parquet', index=True)
    return fin_data


def get_financial_data(dictname1, dictname2):
    varname = dictname1.get(dictname2)
    if varname is not None:
        varname = dictname1.get(dictname2, None)
    return varname


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
    if len(sorted_data) >= 5:
        basic_eps_now = sorted_data.iloc[0]['BasicEPS']
        basic_eps_old = sorted_data.iloc[4]['BasicEPS']
        eps_compare_method = "yearly"

    elif len(sorted_data) == 4 or len(sorted_data) == 3:
        basic_eps_now = sorted_data.iloc[0]['BasicEPS']
        basic_eps_old = sorted_data.iloc[1]['BasicEPS']
        eps_compare_method = "quarterly"

    else:
        basic_eps_now = 0
        basic_eps_old = 0
        eps_compare_method = "NA"
    return basic_eps_now, basic_eps_old, eps_compare_method


def get_fund_ownership_number(ticker, fund_ownership_data):
    # if 'symbol' not in fund_ownership_data.columns:
    #     fund_ownership_data.reset_index(inplace=True)
    # fund_ownership_data.reset_index(inplace=True)  # 重置索引，将 symbol 转换为列
    # 筛选 symbol 为 'ticker' 的行
    # filtered_data = fund_ownership_data[fund_ownership_data['symbol'] == ticker]
    # print(filtered_data)
    # print(fund_ownership_data)
    fund_ownership_no = len(fund_ownership_data)
    return fund_ownership_no


def get_financial_info(fin_data, ticker, level1, level2):
    get_level1 = fin_data[ticker].get(level1)
    get_level2 = get_level1.get(level2)
    return get_level2


def update_income_statement(tickers_in, reload='1'):
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

    if reload == "1":
        income_statement_q = get_income_statement_q_single(tickers_in)
        # print(income_statement_q)

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
    else:
        income_statement_q_all = income_statement_q_csv

    return income_statement_q_all


def filter_financial_ticker(tickers_in, category_in):
    # start_time = time.time()  # 記錄開始時間
    fin_data = get_yq_financial_data(tickers_in)

    # asset_profile, income_statement_q, fund_ownership, summary_detail_source, summary_profile = \
    # get_yq_financial_data_single(tickers_in)
    income_statement_q = update_income_statement(tickers_in, 0)

    # df.to_csv('example.csv', index=False)
    # print(income_statement_q)
    # print(fin_data)
    # end_time = time.time()  # 記錄結束時間
    # elapsed_time = round(end_time - start_time, 2)  # 計算運行時間
    # print(f"Elapsed time: {elapsed_time} seconds")

    # 建立一個新的list，用來放符合條件的ticker
    filter_tickers = []
    ticker_wi_eps = 0
    ticker_wo_eps = 0
    ticker_no = 0
    method_yearly = 0
    method_quarterly = 0
    method_na = 0
    for ticker in tickers_in:
        if ticker not in fin_data:
            print(f'Quote not found for ticker symbol: {ticker}')
            continue
        elif 'Quote not found for ticker symbol:' in fin_data[ticker] or 'For input string' in fin_data[ticker]:
            print(f'Quote not found for ticker symbol:{ticker}')
            continue
        else:
            # print(ticker)
            # 得到的資料格式，若是dict的話，可以用以下的方式去查詢
            if ticker in fin_data and isinstance(fin_data[ticker], dict):
                summary_detail = fin_data[ticker].get('summaryDetail')
            else:
                print(f"Unexpected data format for ticker: {ticker}")
                continue
            # summary_detail = fin_data[ticker].get('summaryDetail')
            # print(f'summary_detail:{summary_detail}')
            # sector = fin_data[ticker]['summaryProfile']['sector']
            # industry = fin_data[ticker]['summaryProfile']['industry']
            # website = fin_data[ticker]['summaryProfile']['website']
            ticker_no += 1
            eps_new, eps_old, method = get_income_statement_q_eps(ticker, income_statement_q)

            if eps_new != 0 and eps_old != 0:
                eps_growth = round(eps_new / eps_old, 2)
                ticker_wi_eps += 1
                if method == "yearly":
                    method_yearly += 1
                elif method == "quarterly":
                    method_quarterly += 1
                elif method == "NA":
                    method_na += 1
            else:
                eps_growth = 0
                ticker_wo_eps += 1

            # fund_ownership = fin_data[ticker].get('fundOwnership')
            fund_ownership = fin_data[ticker].get('fundOwnership', {'ownershipList': []})['ownershipList']
            # fund_ownership = fin_data[ticker]['fundOwnership']['ownershipList']
            if fund_ownership:
                fund_ownership_number = get_fund_ownership_number(ticker, fund_ownership)
            else:
                fund_ownership_number = 0  # 或設置為其他適當的預設值
            print("============================================================================")
            print(f'ticker:{ticker}')
            # print(f'sector:{sector}')
            # print(f'industry:{industry}')
            # print(f'website:{website}')
            print(f'eps_new:{eps_new}')
            print(f'eps_old:{eps_old}')
            print(f'eps_growth:{eps_growth}')
            print(f'fund_ownership_number:{fund_ownership_number}')

            summary_detail = fin_data[ticker].get('summaryDetail')
            # summary_detail = summary_detail_source[ticker]
            # if summary_detail is not None:
            if summary_detail is not None:
                # ticker_previous_close = get_financial_data("summary_detail", "previousClose")
                ticker_previous_close = summary_detail.get('previousClose')
                if ticker_previous_close is not None:  # 上次收盤價
                    ticker_previous_close = fin_data[ticker]['summaryDetail']['previousClose']
                    # print(f'ticker_previous_close {ticker_previous_close}')

                ticker_forward_pe = summary_detail.get('forwardPE')  # Forward PE是下一個會計年度的每股盈餘來計算
                if ticker_forward_pe is not None:
                    ticker_forward_pe = fin_data[ticker]['summaryDetail'].get('forwardPE', None)
                    # print(f'ticker_forward_pe {ticker_forward_pe}')

                ticker_trailing_pe = summary_detail.get('trailingPE')  # Trailing PE是指最近四季的每股盈餘來計算
                if ticker_trailing_pe is not None:
                    ticker_trailing_pe = fin_data[ticker]['summaryDetail'].get('trailingPE', None)
                    # print(f'ticker_trailing_pe {ticker_trailing_pe}')

                ticker_average_daily_volume_10day = summary_detail.get('averageDailyVolume10Day')  # 10天的平均成交量
                if ticker_average_daily_volume_10day is not None:
                    ticker_average_daily_volume_10day = fin_data[ticker]['summaryDetail'].get('averageDailyVolume10Day',
                                                                                              None)
                    # print(f'ticker_average_daily_volume_10day {ticker_average_daily_volume_10day}')

                ticker_52_week_low = summary_detail.get('fiftyTwoWeekLow')  # 52週的低點
                if ticker_52_week_low is not None:
                    ticker_52_week_low = fin_data[ticker]['summaryDetail'].get('fiftyTwoWeekLow', None)
                    # print(f'ticker_52_week_low {ticker_52_week_low}')

                ticker_52_week_high = summary_detail.get('fiftyTwoWeekLow')  # 52週的高點
                if ticker_52_week_high is not None:
                    ticker_52_week_high = fin_data[ticker]['summaryDetail'].get('fiftyTwoWeekHigh', None)
                    # print(f'ticker_52_week_high {ticker_52_week_high}')

                ticker_50_day_average = summary_detail.get('fiftyDayAverage')  # 50天的平均成交價(sma50)
                if ticker_50_day_average is not None:
                    ticker_50_day_average = fin_data[ticker]['summaryDetail'].get('fiftyDayAverage', None)
                    # print(f'ticker_50_day_average {ticker_50_day_average}')

                ticker_200_day_average = summary_detail.get('twoHundredDayAverage')  # 200天的平均成交價(sma200)
                if ticker_200_day_average is not None:
                    ticker_200_day_average = fin_data[ticker]['summaryDetail'].get('twoHundredDayAverage', None)
                    # print(f'ticker_200_day_average {ticker_200_day_average}')
                if (ticker_forward_pe is not None and ticker_trailing_pe is not None and
                        ticker_forward_pe != "Infinity" and ticker_trailing_pe != "Infinity"):

                    # print("PE is not valid, skip")
                    # if (ticker_trailing_pe > ticker_forward_pe) and \
                    if eps_growth >= 1.1 and \
                            fund_ownership_number >= 1 and \
                            (ticker_previous_close / ticker_52_week_low > 1.3) and \
                            (ticker_previous_close / ticker_52_week_high < 1.25) and \
                            (ticker_previous_close / ticker_52_week_high > 0.75) and \
                            (ticker_50_day_average > ticker_200_day_average):
                        filter_tickers.append(ticker)


                        url = f"https://www.tradingview.com/chart/sWFIrRUP/?symbol={ticker}"
                        filter_tickers_df = pd.DataFrame({
                            'Ticker': [ticker],
                            'URL': [url]
                        })
                        if os.path.exists('filter_ticker.csv'):
                            filter_tickers_df.to_csv('filter_ticker.csv', mode='a', index=False, header=False)
                        else:
                            filter_tickers_df.to_csv('filter_ticker.csv', mode='a', index=False)
                        # webbrowser.open(url)
                else:
                    continue
    # 將DataFrame寫入.csv檔案，如果檔案已存在，則在原檔案的基礎上新增行
    # filter_tickers_df.to_csv('filter_ticker.csv', mode='a', index=False)
    print("============================================================================")
    print(f'total_ticker_no:{ticker_no}')
    print(f'ticker_wi_eps:{ticker_wi_eps}')
    print(f'ticker_wo_eps:{ticker_wo_eps}')
    print(f'Method yearly:{method_yearly}')
    print(f'Method quarterly:{method_quarterly}')
    print(f'Method quarterly:{method_na}')

    print("============================================================================")
    # 顯示過濾後的所有ticker，並計算數量
    print(filter_tickers)
    tickers_length = len(filter_tickers)
    print(f'Total Filtered Tickers:', tickers_length)

    # 將過濾過的ticker，寫入YF_US這個csv中
    df_filter_ticker = pd.DataFrame(filter_tickers)
    # 將 DataFrame 寫入名為 'YF' 的工作表
    df_filter_ticker.to_csv('YF_US.csv', index=False, header=None)

    hist_df = get_yq_historical_data(filter_tickers)

    for ticker in filter_tickers:
        print(f"Checking VCP Ticker: {ticker}")
        df_one = sel_yq_historical_data(hist_df, ticker)
        vcp_screener_strategy(ticker, df_one)

    # highchart_chart_v2(filter_tickers, "US")


def filter_financial_ticker_backup(tickers_in, category_in):
    # start_time = time.time()  # 記錄開始時間
    fin_data = get_yq_financial_data(tickers_in)
    # print(fin_data)
    # end_time = time.time()  # 記錄結束時間
    # elapsed_time = round(end_time - start_time, 2)  # 計算運行時間
    # print(f"Elapsed time: {elapsed_time} seconds")
    filter_tickers = []
    for ticker in tickers_in:
        if ticker not in fin_data:
            print(f'Quote not found for ticker symbol: {ticker}')
            continue
        elif 'Quote not found for ticker symbol:' in fin_data[ticker] or 'For input string' in fin_data[ticker]:
            print(f'Quote not found for ticker symbol:{ticker}')
            continue
        else:
            # print(ticker)
            summary_detail = fin_data[ticker].get('summaryDetail')
            if summary_detail is not None:
                # ticker_previous_close = get_financial_data("summary_detail", "previousClose")
                ticker_previous_close = summary_detail.get('previousClose')
                if ticker_previous_close is not None:  # 上次收盤價
                    ticker_previous_close = fin_data[ticker]['summaryDetail']['previousClose']
                    # print(f'ticker_previous_close {ticker_previous_close}')

                ticker_forward_pe = summary_detail.get('forwardPE')  # Forward PE是下一個會計年度的每股盈餘來計算
                if ticker_forward_pe is not None:
                    ticker_forward_pe = fin_data[ticker]['summaryDetail'].get('forwardPE', None)
                    # print(f'ticker_forward_pe {ticker_forward_pe}')

                ticker_trailing_pe = summary_detail.get('trailingPE')  # Trailing PE是指最近四季的每股盈餘來計算
                if ticker_trailing_pe is not None:
                    ticker_trailing_pe = fin_data[ticker]['summaryDetail'].get('trailingPE', None)
                    # print(f'ticker_trailing_pe {ticker_trailing_pe}')

                ticker_average_daily_volume_10day = summary_detail.get('averageDailyVolume10Day')  # 10天的平均成交量
                if ticker_average_daily_volume_10day is not None:
                    ticker_average_daily_volume_10day = fin_data[ticker]['summaryDetail'].get('averageDailyVolume10Day',
                                                                                              None)
                    # print(f'ticker_average_daily_volume_10day {ticker_average_daily_volume_10day}')

                ticker_52_week_low = summary_detail.get('fiftyTwoWeekLow')  # 52週的低點
                if ticker_52_week_low is not None:
                    ticker_52_week_low = fin_data[ticker]['summaryDetail'].get('fiftyTwoWeekLow', None)
                    # print(f'ticker_52_week_low {ticker_52_week_low}')

                ticker_52_week_high = summary_detail.get('fiftyTwoWeekLow')  # 52週的高點
                if ticker_52_week_high is not None:
                    ticker_52_week_high = fin_data[ticker]['summaryDetail'].get('fiftyTwoWeekHigh', None)
                    # print(f'ticker_52_week_high {ticker_52_week_high}')

                ticker_50_day_average = summary_detail.get('fiftyDayAverage')  # 50天的平均成交價(sma50)
                if ticker_50_day_average is not None:
                    ticker_50_day_average = fin_data[ticker]['summaryDetail'].get('fiftyDayAverage', None)
                    # print(f'ticker_50_day_average {ticker_50_day_average}')

                ticker_200_day_average = summary_detail.get('twoHundredDayAverage')  # 200天的平均成交價(sma200)
                if ticker_200_day_average is not None:
                    ticker_200_day_average = fin_data[ticker]['summaryDetail'].get('twoHundredDayAverage', None)
                    # print(f'ticker_200_day_average {ticker_200_day_average}')
                if (ticker_forward_pe is not None and ticker_trailing_pe is not None and
                        ticker_forward_pe != "Infinity" and ticker_trailing_pe != "Infinity"):

                    # print("PE is not valid, skip")
                    if (ticker_trailing_pe > ticker_forward_pe) and \
                            (ticker_previous_close / ticker_52_week_low > 1.3) and \
                            (ticker_previous_close / ticker_52_week_high < 1.25) and \
                            (ticker_previous_close / ticker_52_week_high > 0.75) and \
                            (ticker_50_day_average > ticker_200_day_average):
                        filter_tickers.append(ticker)

                else:
                    continue
    # 顯示過濾後的所有ticker，並計算數量
    print(filter_tickers)
    tickers_length = len(filter_tickers)
    print(f'Total Filtered Tickers:', tickers_length)

    # 將過濾過的ticker，寫入YF_US這個csv中
    df_filter_ticker = pd.DataFrame(filter_tickers)
    # 將 DataFrame 寫入名為 'YF' 的工作表
    df_filter_ticker.to_csv('YF_US.csv', index=False, header=None)

    hist_df = get_yq_historical_data(filter_tickers)
    ## filter_tickers = ['GOOG', 'GOOGL', 'AMZN', 'PCAR', 'BRK-B', 'TSLA', 'NVDA', 'V', 'TSM', 'XOM', 'META', 'UNH', 'JPM', 'JNJ', 'WMT', 'MA', 'PG', 'NVO', 'CVX', 'LLY', 'HD', 'ABBV', 'MRK', 'BAC', 'KO', 'AVGO', 'ASML', 'PEP', 'BABA', 'ORCL', 'PFE', 'SHEL', 'COST', 'TMO', 'AZN', 'CSCO', 'MCD', 'CRM', 'TM', 'NKE', 'DHR', 'NVS', 'DIS', 'ABT', 'WFC', 'LIN', 'TMUS', 'ACN', 'BHP', 'VZ', 'MS', 'UPS', 'TXN', 'CMCSA', 'TTE', 'PM', 'ADBE', 'HSBC', 'BMY', 'RTX', 'NEE', 'SCHW', 'NFLX', 'RY', 'QCOM', 'SAP', 'T', 'COP', 'HON', 'AXP', 'CAT', 'UNP', 'UL', 'AMD', 'DE', 'AMGN', 'HDB', 'BA', 'LMT', 'BP', 'PDD', 'BUD', 'RIO', 'TD', 'SNY', 'LOW', 'SBUX', 'GS', 'IBM', 'PLD', 'INTU', 'ELV', 'SPGI', 'MDT', 'INTC', 'CVS', 'SONY', 'BLK', 'GILD', 'BKNG', 'DEO', 'C', 'SYK', 'AMAT', 'EQNR', 'GE', 'ADI', 'ADP', 'AMT', 'MDLZ', 'TJX', 'EL', 'NOW', 'CB', 'CI', 'BTI', 'MUFG', 'REGN', 'PGR', 'PYPL', 'MO', 'MMC', 'ISRG', 'VALE', 'CNI', 'ENB', 'ZTS', 'SLB', 'TGT', 'VRTX', 'INFY', 'CHTR', 'FISV', 'JD', 'ABNB', 'IBN', 'CP', 'DUK', 'ITW', 'NOC', 'USB', 'PBR', 'EOG', 'GSK', 'ETN', 'SO', 'HCA', 'BSX', 'AMOV', 'BN', 'UBS', 'BMO', 'AMX', 'CME', 'BX', 'BDX', 'CNQ', 'UBER', 'LRCX', 'SAN', 'APD', 'CSX', 'GD', 'EQIX', 'ABB', 'HUM', 'AON', 'WM', 'CL', 'PNC', 'FCX', 'MELI', 'MU', 'TFC', 'ATVI', 'MMM', 'BNS', 'MPC', 'SMFG', 'STLA', 'RELX', 'TRI', 'SCCO', 'SHW', 'PANW', 'ICE', 'NTES', 'CCI', 'SNPS', 'OXY', 'MET', 'GM', 'VLO', 'MNST', 'MRNA', 'MCO', 'CDNS', 'ORLY', 'MAR', 'AIG', 'PSA', 'KLAC', 'FDX', 'NSC', 'BIDU', 'SHOP', 'ING', 'F', 'PSX', 'PXD', 'KDP', 'HSY', 'EW', 'RACE', 'MCK', 'TAK', 'DG', 'EMR', 'KHC', 'KKR', 'WDS', 'E', 'WDAY', 'VMW', 'GIS', 'AZO', 'FTNT', 'SRE', 'APH', 'BBVA', 'ITUB', 'SU', 'NXPI', 'SQ', 'D', 'PH', 'NGG', 'ECL', 'DXCM', 'LVS', 'ROP', 'CTVA', 'AEP', 'ADM', 'MSI', 'CTAS', 'HMC', 'MCHP', 'NUE', 'ADSK', 'JCI', 'SNOW', 'HES', 'KMB', 'TRV', 'TT', 'STM', 'O', 'TEAM', 'ANET', 'PUK', 'AFL', 'A', 'TDG', 'CM', 'LYG', 'DOW', 'COF', 'CMG', 'MSCI', 'APO', 'STZ', 'RSG', 'NTR', 'TEL', 'BK', 'TRP', 'LHX', 'BCE', 'LNG', 'PAYX', 'ABEV', 'SPG', 'EXC', 'MFG', 'LULU', 'BSBR', 'AJG', 'IQV', 'IDXX', 'BIIB', 'KMI', 'HLT', 'MRVL', 'SYY', 'ODFL', 'ROST', 'CARR', 'CRH', 'CNC', 'FIS', 'MFC', 'WBD', 'WMB', 'WELL', 'CVE', 'DVN', 'PRU', 'AMP', 'YUM', 'OTIS', 'CMI', 'SE', 'GFS', 'XEL', 'HLN', 'VICI', 'NEM', 'WCN', 'NWG', 'GWW', 'GEHC', 'HAL', 'DD', 'ROK', 'FMX', 'PCG', 'CPRT', 'ALL', 'ALC', 'SGEN', 'BCS', 'AME', 'KR', 'VOD', 'URI', 'DLTR', 'ON', 'MTD', 'ILMN', 'BKR', 'CTSH', 'LYB', 'ABC', 'PPG', 'RMD', 'MBLY', 'ED', 'APTV', 'DHI', 'BNTX', 'EA', 'ORAN', 'STT', 'WBA', 'DFS', 'FERG', 'FAST', 'IMO', 'PEG', 'CHT', 'OKE', 'ALB', 'DLR', 'GPN', 'GLW', 'CSGP', 'SLF', 'TU', 'ENPH', 'GOLD', 'DELL', 'CRWD', 'HPQ', 'KEYS', 'VRSK', 'SBAC', 'WEC', 'NDAQ', 'LEN', 'VEEV', 'TTD', 'CDW', 'ANSS', 'BBD', 'ULTA', 'CBRE', 'ACGL', 'FANG', 'NOK', 'IT', 'WIT', 'FNV', 'ZBH', 'ES', 'MTB', 'YUMC', 'TLK', 'AWK', 'CCEP', 'HZNP', 'MT', 'TSCO', 'CPNG', 'WTW', 'BGNE', 'EBAY', 'ARE', 'TROW', 'DB', 'CEG', 'EIX', 'EFX', 'DAL', 'FITB', 'HIG', 'LI', 'GMAB', 'TCOM', 'BEKE', 'GPC', 'BBDO', 'SQM', 'VMC', 'RCI', 'ALNY', 'TEF', 'ALGN', 'FTV', 'WST', 'DDOG', 'HEI', 'AVB', 'EC', 'IR', 'IFF', 'EQR', 'WY', 'HRL', 'PWR', 'STLD', 'RJF', 'MPWR', 'SPOT', 'K', 'NU', 'RBLX', 'MLM', 'CNHI', 'FE', 'EXR', 'FRC', 'CAJ', 'ETR', 'HBAN', 'GIB', 'RF', 'RYAAY', 'AEM', 'AEE', 'TECK', 'DOV', 'DASH', 'LH', 'TSN', 'DTE', 'FSLR', 'ZM', 'CHD', 'IX', 'VRSN', 'UMC', 'PFG', 'LPLA', 'TS', 'TDY', 'HPE', 'CTRA', 'LUV', 'PPL', 'BAX', 'PODD', 'CFG', 'QSR', 'NET', 'HOLX', 'MKC', 'PKX', 'CLX', 'NTRS', 'CAH', 'VTR', 'ARGX', 'ZTO', 'WAB', 'MOS', 'FTS', 'JBHT', 'ZS', 'TTWO', 'HUBS', 'WPM', 'CINF', 'FOXA', 'GRMN', 'PBA', 'BMRN', 'WAT', 'STE', 'INVH', 'ICLR', 'OMC', 'BBY', 'ERIC', 'MAA', 'XYL', 'RCL', 'ELP', 'MKL', 'WRB', 'HWM', 'SEDG', 'EPAM', 'SWKS', 'DRI', 'CNP', 'SUI', 'TRGP', 'INCY', 'PAYC', 'FOX', 'ROL', 'FICO', 'CAG', 'BALL', 'WPC', 'PINS', 'EXPD', 'CMS', 'UAL', 'CHWY', 'MGM', 'IEX', 'CF', 'NVR', 'KEY', 'BR', 'SPLK', 'AMCR', 'AVTR', 'SIRI', 'AES', 'LYV', 'MRO', 'PARAA', 'SIVB', 'EXPE', 'FWONK', 'WMG', 'PLTR', 'HTHT', 'FMC', 'UI', 'MGA', 'MOH', 'COO', 'ATO', 'FDS', 'AER', 'SJM', 'SNAP', 'BRO', 'RPRX', 'PKI', 'ASX', 'FLT', 'TER', 'CPB', 'CHKP', 'ZBRA', 'COIN', 'RTO', 'WLK', 'SYF', 'DGX', 'LKQ', 'KOF', 'AXON', 'LCID', 'IRM', 'J', 'RE', 'TXT', 'ETSY', 'RS', 'KB', 'TW', 'EBR', 'AGR', 'SSNC', 'PTC', 'LW', 'RIVN', 'AVY', 'BG', 'NIO', 'FWONA', 'SHG', 'BEN', 'SJR', 'ESS', 'L', 'ARES', 'PHG', 'BURL', 'PARA', 'BIO', 'CBOE', 'AZPN', 'MDB', 'GLPI', 'TPL', 'BAM', 'NTAP', 'UDR', 'IPG', 'POOL', 'TME', 'CCL', 'VTRS', 'EVRG', 'HUBB', 'LDOS', 'TYL', 'CE', 'STX', 'CSL', 'MKTX', 'WPP', 'CRBG', 'SNA', 'NICE', 'IP', 'SRPT', 'PEAK', 'PKG', 'APA', 'TRMB', 'WYNN', 'LNT', 'BAH', 'OKTA', 'BLDR', 'KIM', 'CTLT', 'H', 'TWLO', 'NDSN', 'SNN', 'TRU', 'LBRDA', 'UHAL', 'CG', 'LBRDK', 'ELS', 'ENTG', 'SWK', 'GEN', 'VIV', 'CUK', 'ACM', 'CPT', 'ERIE', 'DT', 'DOCU', 'PHM', 'NMR', 'HST', 'WDC', 'JKHY', 'CCJ', 'FHN', 'EQT', 'IHG', 'TECH']

    for ticker in filter_tickers:
        print(f"Checking VCP Ticker: {ticker}")
        df_one = sel_yq_historical_data(hist_df, ticker)
        vcp_screener_strategy(ticker, df_one)

    # highchart_chart_v2(filter_tickers, "US")


def refresh_financial_data(tickers_in):
    get_fin_start_time = time.time()  # 記錄開始時間
    fin_data = get_yq_financial_data(tickers_in)
    # print(fin_data)
    # get_fin_end_time = time.time()  # 記錄結束時間
    # get_fin_elapsed_time = round(get_fin_end_time - get_fin_start_time, 2)  # 計算運行時間
    # print(f"Elapsed time: {get_fin_elapsed_time} seconds")
    # print(data)
    ticker_previous_close = fin_data['AAPL']['summaryDetail']['previousClose']
    print(ticker_previous_close)
    """# 初始化一個空的 DataFrame 來儲存所有公司的數據
    combined_df = pd.DataFrame()

    # 遍歷 fin_data 中的每個股票代碼及其相應的數據
    for ticker, data in fin_data.items():
        # 提取 summaryDetail 中的數據
        summary_data = data['summaryDetail']

        # 提取 balanceSheetHistory 中的數據
        balance_sheet_data = data['balanceSheetHistory']['balanceSheetStatements'][0]

        # 結合兩個字典
        merged_data = {**summary_data, **balance_sheet_data}

        # 將字典轉換為 DataFrame
        df = pd.DataFrame(merged_data, index=[ticker])

        # 將 df 添加到 combined_df 中
        combined_df = pd.concat([combined_df, df])

    # 重置索引
    combined_df.reset_index(inplace=True)
    combined_df.rename(columns={'index': 'Ticker'}, inplace=True)

    # 查看整合後的 DataFrame
    print(combined_df)
    # 將 DataFrame 轉換為 HTML 字符串
    html_data = combined_df.to_html()

    # 將 HTML 字符串寫入文件
    with open("combined_df.html", "w", encoding="utf-8") as f:
        f.write(html_data)

    print("HTML file saved as 'combined_df.html'")
    """

    """
    # 開啟文件並將字典寫入CSV
    with open("output.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入列名（header）
        writer.writeheader()

        # 寫入字典中的資料
        for row in data_list:
            writer.writerow(row)
   # 開啟文件並將字典寫入CSV
    with open("output.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入列名（header）
        writer.writeheader()

        # 寫入字典中的資料
        for row in data:
            writer.writerow(row)

    # print(financial_all_tickers)
    """


def get_tickers(category, start):
    print(f'############ Start Getting Ticker by {category} mode')
    if category == "FIN":
        tickers = get_finviz_screener_tickers()
        tickers_length = len(tickers)
    else:
        df = pd.read_excel("Tickers.xlsx", sheet_name=category, usecols=[0])
        tickers = df.iloc[:, 0].tolist()
        tickers_length = len(tickers)

    if start != 0:
        tickers = tickers[start:]
        tickers_length = len(tickers)
        print(f'Total {category} Tickers after Slicing:', tickers_length)

    if category == "US" or category == "ETF" or category == "FIN":
        print(f'Total {category} Tickers before remove PTP:', tickers_length)
        ptp_lists = get_ptp_tickers()
        # print(f'PTP Stock List: {ptp_lists}')
        remove_ptp_list(ptp_lists, tickers)
        print(f'Total {category} Tickers after remove PTP:', tickers_length)
    else:
        print(f'Total {category} Tickers:', tickers_length)

    print(f'############ Finish Getting Ticker by {category} mode')
    return tickers


def calculate_sma(data, window):
    return data['close'].rolling(window=window).mean()


def check_continuous_increase(sma, days):
    continuous_increase = 0
    for i in range(len(sma) - 1, 0, -1):
        if sma[i] > sma[i - 1]:
            continuous_increase += 1
        else:
            break

    return continuous_increase >= days


def calculate_vwap(df_in, duration, ochl='close'):
    # data['Typical Price'] = (data['high'] + data['low'] + data['close']) / 3
    df_in['VWPrice'] = df_in[ochl] * df_in['volume']
    df_in[f'vwap{duration}'] = df_in['VWPrice'].rolling(window=duration).sum() / df_in['volume'].rolling(
        window=duration).sum()
    return df_in


def sel_yq_historical_data(data_all, ticker_in):
    # Select data from get_yq_financial_data by tickers
    # print(data_all)
    # print(ticker_in)
    # data_org = data_all.reset_index()

    # 確定資料裡面有ticker這個index的資料
    if ticker_in in data_all.index.get_level_values('symbol'):
        data_org = data_all.loc[ticker_in]
        data_org = calculate_vwap(data_org, 5)
        data_org = calculate_vwap(data_org, 8)
        data_org = calculate_vwap(data_org, 13)
        data_org = calculate_vwap(data_org, 21)
        data_org = calculate_vwap(data_org, 34)
        data_org = calculate_vwap(data_org, 55)
        data_org = calculate_vwap(data_org, 89)
        data_org = calculate_vwap(data_org, 144)
        data_org = calculate_vwap(data_org, 233)
        data_org = calculate_vwap(data_org, 377)
        data_org = calculate_vwap(data_org, 610)
        data_org['AvgVol'] = data_org['volume'].rolling(55).mean()  # 55為平均的天數
        data_org['RSI'] = calculate_rsi(data_org, rsi_period)
    else:
        print(f'Index not found:{ticker_in}')
        empty_df = pd.DataFrame()
        return empty_df
    # data_org = data_all.loc[ticker_in]
    # Check if the DataFrame has at least two rows
    # if data_org.shape[0] < 2:
    #     print("DataFrame must have at least two rows.")
    #     return 0
    # else:

    return data_org
    print("DataFrame has at least two rows.")


def line_notify_message(msg, token='YuvfgED98JDWMvATPEAnDu3u9Ge0R2B9BkrOvCwHZId'):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


def get_tradingview_url(ticker_in, category):
    #  不是台灣的ticker
    if (category != "TW"):
        url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + ticker_in)
    # 若是台灣的ticker，則會需要分上市及上櫃
    else:
        if (ticker_in[-1] == "W"):
            row2 = ticker_in[:4]
            url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
        else:
            row2 = ticker_in[:4]

            url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
    return url


def vwap_strategy_screener(tickers_in, df, true_number, category):
    global scenario
    df['AvgVol'] = df['volume'].rolling(55).mean()  # 55為平均的天數
    last_close_price = round(df["close"][-1], 2)

    plot_title = "{} {} {} {}".format(tickers_in, today, last_close_price, scenario)
    # plot_tile = (row + today + last_close_price)
    volatility_H = df['high'].max() / df['close'].mean()
    volatility_L = df['low'].min() / df['close'].mean()
    volatility = volatility_H - volatility_L
    # print (str(len(df.index)) + " " + str(volatility_H) + " " + str(volatility_L) + " " + str(volatility))
    if (len(df.index) > 144 and volatility > 0.1):  # 過濾資料筆數少於144筆的股票，確保上市時間有半年並且判斷半年內的波動率，像死魚一樣不動的股票就不分析
        if (ForcePLOT == 1):
            # year = df[-200:]
            url = f'https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{tickers_in}'
            linemessage = (
                f"{true_number} - url - ")
            # f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - {info_sector}")
            # lineNotifyImage(token, linemessage, str(true_number) + ".jpg")
            highchart_chart(df, tickers_in, url)
            # plotly_chart(df, plot_title, 0)
            # if not OnlyPLOT:
            #    webbrowser.open(url)
        df['VWAP21_Result'] = (df['vwap5'] > df['vwap21'])
        df['VWAP55_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55'])
        df['VWAP89_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55']) & (
                df['vwap55'] > df['vwap89'])
        df['VWAP144_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55']) & (
                df['vwap55'] > df['vwap89']) & (df['vwap89'] > df['vwap144'])
        df['VWAP233_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55']) & (
                df['vwap55'] > df['vwap89']) & (df['vwap89'] > df['vwap144']) & (
                                       df['vwap144'] > df['vwap233'])

        VWAP5_inc = (df['vwap5'].iloc[-1] > df['vwap5'].iloc[-2])
        VWAP21_inc = (df['vwap5'].iloc[-1] > df['vwap5'].iloc[-2]) and (
                df['vwap21'].iloc[-1] > df['vwap21'].iloc[-2])
        VWAP55_inc = (df['vwap5'].iloc[-1] > df['vwap5'].iloc[-2]) and (
                df['vwap21'].iloc[-1] > df['vwap21'].iloc[-2]) and (
                             df['vwap55'].iloc[-1] > df['vwap55'].iloc[-2])
        VWAP89_inc = (df['vwap5'].iloc[-1] > df['vwap5'].iloc[-2]) and (
                df['vwap21'].iloc[-1] > df['vwap21'].iloc[-2]) and (
                             df['vwap55'].iloc[-1] > df['vwap55'].iloc[-2]) and (
                             df['vwap89'].iloc[-1] > df['vwap89'].iloc[-2])
        VWAP144_inc = (df['vwap5'].iloc[-1] > df['vwap5'].iloc[-2]) and (
                df['vwap21'].iloc[-1] > df['vwap21'].iloc[-2]) and (
                              df['vwap55'].iloc[-1] > df['vwap55'].iloc[-2]) and (
                              df['vwap89'].iloc[-1] > df['vwap89'].iloc[-2]) and (
                              df['vwap144'].iloc[-1] > df['vwap144'].iloc[-2])
        VWAP233_inc = (df['vwap5'].iloc[-1] > df['vwap5'].iloc[-2]) and (
                df['vwap21'].iloc[-1] > df['vwap21'].iloc[-2]) and (
                              df['vwap55'].iloc[-1] > df['vwap55'].iloc[-2]) and (
                              df['vwap89'].iloc[-1] > df['vwap89'].iloc[-2]) and (
                              df['vwap144'].iloc[-1] > df['vwap144'].iloc[-2]) and (
                              df['vwap233'].iloc[-1] > df['vwap233'].iloc[-2])

        vwap_values_233 = df['VWAP233_Result'].values
        pattern_233 = np.array([False] * 20 + [True])
        VWAP233_history = np.array_equal(vwap_values_233[-21:-1], pattern_233[:-1]) and vwap_values_233[-1] == \
                          pattern_233[-1]

        vwap_values_144 = df['VWAP144_Result'].values
        pattern_144 = np.array([False] * 20 + [True])
        VWAP144_history = np.array_equal(vwap_values_144[-21:-1], pattern_144[:-1]) and vwap_values_144[-1] == \
                          pattern_144[-1]

        vwap_values_89 = df['VWAP89_Result'].values
        pattern_89 = np.array([False] * 20 + [True])
        VWAP89_history = np.array_equal(vwap_values_89[-21:-1], pattern_89[:-1]) and vwap_values_89[-1] == pattern_89[
            -1]

        vwap_values_55 = df['VWAP55_Result'].values
        pattern_55 = np.array([False] * 20 + [True])
        VWAP55_history = np.array_equal(vwap_values_55[-21:-1], pattern_55[:-1]) and vwap_values_55[-1] == pattern_55[
            -1]
        vwap_values_21 = df['VWAP21_Result'].values
        pattern_21 = np.array([False] * 20 + [True])
        VWAP21_history = np.array_equal(vwap_values_21[-21:-1], pattern_21[:-1]) and vwap_values_21[-1] == pattern_21[
            -1]
        final_result = "FALSE"
        scenario = 55

        if (scenario == 55) and (VWAP55_history == True) and (VWAP55_inc == True):
            final_result = "TRUE"
        elif (scenario == 21) and (VWAP21_history == True) and (VWAP21_inc == True):
            final_result = "TRUE"
        elif (scenario == 89) and (VWAP89_history == True) and (VWAP89_inc == True):
            final_result = "TRUE"
        elif (scenario == 144) and (VWAP144_history == True) and (VWAP144_inc == True):
            final_result = "TRUE"
        elif (scenario == 233) and (VWAP233_history == True) and (VWAP233_inc == True):
            final_result = "TRUE"
        else:
            # print ("No Scenario")
            return 1
        # print(final_result)
        if (final_result == 'TRUE'):
            if (category != "TW"):
                linemessage = (
                    f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={tickers_in}")
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + tickers_in)
                # if not OnlyPLOT:
                #    webbrowser.open(url)

            else:
                if (tickers_in[-1] == "W"):
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2}")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
                    # if not OnlyPLOT:
                    #    webbrowser.open(url)

                else:
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2}")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
                    # if not OnlyPLOT:
                    #    webbrowser.open(url)
            print(tickers_in)
            print(today)
            print(url)
            highchart_chart(df, tickers_in, url)
            # plotly_chart(df, plot_title, 0)
    else:
        print("volume or volatility not meet, skip analysis!")
    # lineNotifyMessage(token, "Finished: " + today + " " + category + "\nScanned " + str(run_number) + " of " + str(
    #    start) + " Stocks in " + category + " Market\n" + str(true_number) + " Meet Criteria")

    # 連續2季EPS成長20%


def buy_signal_strategy_screener(tickers_in, df, true_number, category, day, volume_factor):
    # Check if the dataframe is empty
    if df.empty:
        return

    # Calculate rolling averages and other computations
    df['AvgVol'] = df['volume'].rolling(day).mean()
    df['VWPrice'] = df['close'] * df['volume']
    df['VWPrice_day'] = df['VWPrice'].rolling(day).mean()

    # Calculate vwap and use NaN to avoid divide by zero error
    # df['vwap144'] = df['VWPrice'].rolling(window=144).sum() / df['volume'].replace(0, np.nan).rolling(
    #    window=144).sum()

    if len(df) < 2:
        print("Error: The DataFrame must have at least two rows.")
    else:
        # Get the last data points
        last_turnover_data = df['VWPrice_day'].tail(1).iloc[0] * volume_factor
        last_vwap144_data = df['vwap144'].tail(1).iloc[0]
        last_close_price = df["close"].iloc[-1]
        last2_close_price = df["close"].iloc[-2]
        change_percentage = ((last_close_price / last2_close_price) - 1) * 100
        change_percentage = round(change_percentage, 2)
        # print(df["close"])
        # print(f'last_close_price:{last_close_price}')
        # rint(f'last2_close_price:{last2_close_price}')
        # Calculate change percentage
        # change_percentage = ((last_close_price / last2_close_price) - 1) * 100
        # print(f'change_percentage:{change_percentage}')

        # Check if the conditions are met for analysis
        if last_turnover_data > 100000 and last_close_price > last_vwap144_data:
            # Calculate vwap
            df[f'vwap{day}'] = df['VWPrice'].rolling(window=day).sum() / df['volume'].rolling(window=day).sum()

            # Get the last data points
            # last_vwap = df[f'vwap{day}'].iloc[-1]
            # second_last_vwap = df[f'vwap{day}'].iloc[-2]
            last_volume = df['volume'].iloc[-1] * volume_factor
            second_last_avg_volume = df['AvgVol'].iloc[-1]

            # Check if price and volume conditions are met based on the category
            if (category != "TW"):
                is_meet_price_and_volume = last2_close_price * 1.06 > last_close_price > last2_close_price * 1.02 and last_volume > second_last_avg_volume * 1.5
            else:
                is_meet_price_and_volume = last2_close_price * 1.09 > last_close_price > last2_close_price * 1.02 and last_volume > second_last_avg_volume * 1.5

            # 如果最後一天的vwap大於最後第二天的vwap的1.03倍，並且最後一天的成交量大於5天平均成交量的最後一天的2倍，則畫圖並傳送Line通知
            if is_meet_price_and_volume:
                plot_title = f"{tickers_in} {today} {day} {change_percentage}% screener"
                if category != "TW":
                    line_message = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={tickers_in} - screener")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + tickers_in)
                    # if not OnlyPLOT:
                    #   webbrowser.open(url)

                else:
                    if (tickers_in[-1] == "W"):
                        row2 = tickers_in[:4]
                        line_message = (
                            f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - screener")
                        url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
                        # if not OnlyPLOT:
                        # webbrowser.open(url)

                    else:
                        row2 = tickers_in[:4]
                        line_message = (
                            f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2} - screener")
                        url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
                        # if not OnlyPLOT:
                        # webbrowser.open(url)
                highchart_chart(df, tickers_in, url)
                # plotly_chart(df, plot_title, 0)
                # lineNotifyImage(token, line_message, str(true_number) + ".jpg")


def calculate_volatility(df, n_days):
    # 選擇最後n_days天的數據
    hist = df.tail(n_days)

    # 計算最高價格/平均價格和最低價格/平均價格
    avg_close_price = hist['close'].mean()
    max_close_price = hist['close'].max()
    min_close_price = hist['close'].min()
    volatility_h = max_close_price / avg_close_price - 1
    volatility_l = avg_close_price / min_close_price - 1
    # print(f"Volativity high: {n_days} days {volatility_h}")
    # print(f"Volativity low:  {n_days} days {volatility_l}")
    volatility = round(volatility_h + volatility_l, 2)
    # print(f"Volativity: {n_days} days {volatility}")

    return volatility


def calculate_volatility_duration(df, end_day, start_day='0'):
    # 選擇從start_day到end_day之間的數據
    hist = df.iloc[start_day:end_day + 1]

    # 計算最高價格/平均價格和最低價格/平均價格
    avg_close_price = hist['close'].mean()
    max_close_price = hist['close'].max()
    min_close_price = hist['close'].min()
    volatility_h = max_close_price / avg_close_price - 1
    volatility_l = avg_close_price / min_close_price - 1
    # print(f"Volativity high: {start_day} to {end_day} {volatility_h}")
    # print(f"Volativity low:  {start_day} to {end_day} {volatility_l}")
    volatility = round(volatility_h + volatility_l, 2)
    # print(f"Volativity: {start_day} to {end_day} {volatility}")

    return volatility


def calculate_avg_volume_duration(df, end_day, start_day=0):
    # 選擇從start_day到end_day之間的數據
    hist = df.iloc[start_day:end_day + 1]
    avg_volume = hist['volume'].mean()
    return avg_volume


def calculate_avg_volume(df, n_days):
    hist = df.tail(n_days)
    avg_volume = hist['volume'].mean()
    return avg_volume


def vcp_screener_strategy(ticker_in, data):
    # print("Running VCP")
    # print(data)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #    print(data)
    volatility_8 = calculate_volatility_duration(data, 8, 0)
    if isinstance(volatility_8, pd.Series):
        volatility_8 = volatility_8.iloc[-1]
    volatility_21 = calculate_volatility_duration(data, 21, 13)
    if isinstance(volatility_21, pd.Series):
        volatility_21 = volatility_21.iloc[-1]
    volatility_55 = calculate_volatility_duration(data, 55, 21)
    if isinstance(volatility_55, pd.Series):
        volatility_55 = volatility_55.iloc[-1]

    avg_volume_8 = calculate_avg_volume_duration(data, 8, 0)
    # avg_volume_21 = calculate_avg_volume_duration(data, 13, 21)
    avg_volume_55 = calculate_avg_volume_duration(data, 55, 21)
    # print(f"volatility_8: {volatility_8}")
    # print(f"volatility_21: {volatility_21}")
    # print(f"volatility_55: {volatility_55}")
    # print("volatility_8 is of type:", type(volatility_8))
    # print("volatility_21 is of type:", type(volatility_21))
    # print("volatility_55 is of type:", type(volatility_55))
    # print(f"avg_volume_8: {avg_volume_8}")
    # print(f"avg_volume_55: {avg_volume_55}")
    sma55 = calculate_sma(data, 55)
    # print(data)
    vcma55 = calculate_vwap(data, 55)
    # print(vcma55)
    last_vcma55 = round(vcma55.iloc[-1], 2)
    vcma144 = calculate_vwap(data, 144)
    last_vcma144 = round(vcma144.iloc[-1], 2)
    vcma233 = calculate_vwap(data, 233)
    last_vcma233 = round(vcma233.iloc[-1], 2)
    # print(f"last_vcma55: {last_vcma55}")
    # print(f"last_vcma144: {last_vcma144}")
    # print(f"last_vcma233: {last_vcma233}")
    # print("last_vcma55 is of type:", type(last_vcma55))
    # print("last_vcma144 is of type:", type(last_vcma144))
    # print("last_vcma233 is of type:", type(last_vcma233))
    # print(f"sma55: {sma55}")
    last_sma55 = round(sma55[-1], 2)
    # print(f"last_sma55: {last_sma55}")
    sma144 = calculate_sma(data, 144)
    last_sma144 = round(sma144[-1], 2)
    # print(f"last_sma144: {last_sma144}")
    sma233 = calculate_sma(data, 233)
    last_sma233 = round(sma233[-1], 2)
    # print(f"last_sma233: {last_sma233}")
    # print("last_sma233 is of type:", type(last_sma233))
    is_continuous_increase_sma233 = check_continuous_increase(sma233.dropna(), days=21)
    # is_continuous_increase_vcma233 = check_continuous_increase(vcma233.dropna(), days=21)
    # print(f"sma233_rising_21: {is_continuous_increase}")
    # print(f"is_continuous_increase_sma233: {is_continuous_increase_sma233}")
    # print("is_continuous_increase_sma233:", type(is_continuous_increase_sma233))
    # print("last_sma55 is of type:", type(last_sma55))
    # print("last_sma144 is of type:", type(last_sma144))
    # print("last_sma233 is of type:", type(last_sma233))
    # if (volatility_8 < volatility_21) and (volatility_21 < volatility_55) \
    # print("Start if statement...")
    print(f"volatility_8: {volatility_8}")
    print(f"volatility_21: {volatility_21}")
    print(f"volatility_55: {volatility_55}")

    if volatility_8 != "0" and volatility_21 != "0" and volatility_55 != "0":
        if (volatility_8 < volatility_21) & (volatility_21 < volatility_55) \
                and (avg_volume_8 < avg_volume_55) \
                and ((avg_volume_8 / avg_volume_55) < 0.7) \
                and ((volatility_55 / volatility_21) > 1.5) \
                and ((volatility_21 / volatility_8) > 1.5) \
                and (volatility_8 < 0.1) \
                and (last_sma55 > last_sma144) and (last_sma144 > last_sma233) \
                and (is_continuous_increase_sma233 is True):
            # and (last_vcma55 > last_vcma144) & (last_vcma144 > last_vcma233):
            # and is_continuous_increase_vcma233 is True:
            # print("End if statement...")
            url = f"https://www.tradingview.com/chart/sWFIrRUP/?symbol={ticker_in}"
            webbrowser.open(url)
            highchart_chart(data, ticker_in, url)
            print("MATCH VCP!!!")

        # return 1

        # plot_title = "{} {} {} {}".format(ticker_in, today, last_close_price, scenario)
        # plotly_chart(data, plot_title, 0)


def vcp_screener_strategy_bak(ticker_in, data):
    # print("Running VCP")
    # print(data)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #    print(data)
    volatility_8 = calculate_volatility_duration(data, 8, 0)
    if isinstance(volatility_8, pd.Series):
        volatility_8 = volatility_8.iloc[-1]
    volatility_21 = calculate_volatility_duration(data, 21, 13)
    if isinstance(volatility_21, pd.Series):
        volatility_21 = volatility_21.iloc[-1]
    volatility_55 = calculate_volatility_duration(data, 55, 21)
    if isinstance(volatility_55, pd.Series):
        volatility_55 = volatility_55.iloc[-1]

    avg_volume_8 = calculate_avg_volume_duration(data, 8, 0)
    # avg_volume_21 = calculate_avg_volume_duration(data, 13, 21)
    avg_volume_55 = calculate_avg_volume_duration(data, 55, 21)
    print(f"volatility_8: {volatility_8}")
    print(f"volatility_21: {volatility_21}")
    print(f"volatility_55: {volatility_55}")
    print("volatility_8 is of type:", type(volatility_8))
    print("volatility_21 is of type:", type(volatility_21))
    print("volatility_55 is of type:", type(volatility_55))
    # print(f"avg_volume_8: {avg_volume_8}")
    # print(f"avg_volume_55: {avg_volume_55}")
    sma55 = calculate_sma(data, 55)
    # print(data)
    vcma55 = calculate_vwap(data, 55)
    # print(vcma55)
    last_vcma55 = round(vcma55.iloc[-1], 2)

    vcma144 = calculate_vwap(data, 144)
    last_vcma144 = round(vcma144.iloc[-1], 2)
    vcma233 = calculate_vwap(data, 233)
    last_vcma233 = round(vcma233.iloc[-1], 2)
    # print(f"sma55: {sma55}")
    last_sma55 = round(sma55[-1], 2)
    # print(f"last_sma55: {last_sma55}")
    sma144 = calculate_sma(data, 144)
    last_sma144 = round(sma144[-1], 2)
    # print(f"last_sma144: {last_sma144}")
    sma233 = calculate_sma(data, 233)
    last_sma233 = round(sma233[-1], 2)
    # print(f"last_sma233: {last_sma233}")
    is_continuous_increase_sma233 = check_continuous_increase(sma233.dropna(), days=21)
    # is_continuous_increase_vcma233 = check_continuous_increase(vcma233.dropna(), days=21)
    # print(f"sma233_rising_21: {is_continuous_increase}")
    print(f"is_continuous_increase_sma233: {is_continuous_increase_sma233}")
    print("is_continuous_increase_sma233:", type(is_continuous_increase_sma233))
    print("last_sma55 is of type:", type(last_sma55))
    print("last_sma144 is of type:", type(last_sma144))
    print("last_sma233 is of type:", type(last_sma233))
    # if (volatility_8 < volatility_21) and (volatility_21 < volatility_55) \
    print("Start if statement...")

    if (volatility_8 < volatility_21) & (volatility_21 < volatility_55) \
            and (avg_volume_8 < avg_volume_55) \
            and ((avg_volume_8 / avg_volume_55) < 0.7) \
            and ((volatility_55 / volatility_21) > 1.5) \
            and ((volatility_21 / volatility_8) > 1.5) \
            and (volatility_8 < 0.1) \
            and (last_sma55 > last_sma144) and (last_sma144 > last_sma233) \
            and (is_continuous_increase_sma233 is True) \
            and (last_vcma55 > last_vcma144) & (last_vcma144 > last_vcma233):
        # and is_continuous_increase_vcma233 is True:
        print("End if statement...")
        url = f"https://www.tradingview.com/chart/sWFIrRUP/?symbol={ticker_in}"

        # webbrowser.open(url)
        highchart_chart(data, ticker_in, url)
        print("MATCH VCP!!!")

        # return 1

        # plot_title = "{} {} {} {}".format(ticker_in, today, last_close_price, scenario)
        # plotly_chart(data, plot_title, 0)


def find_stocks_in_range(data, days=233, percentage=2):
    # 計算過去 days 天的最高價
    highest_price = data['close'].rolling(window=days).max().iloc[-1]

    # 計算正負 percentage% 的範圍
    upper_range = highest_price * (1 + percentage / 100)
    lower_range = highest_price * (1 - percentage / 100)
    # print(upper_range)
    # print(lower_range)

    # 篩選出最近的收盤價在範圍內的股票
    recent_close = data['close'].iloc[-1]
    # print(recent_close)
    stocks_in_range = (recent_close >= lower_range) & (recent_close <= upper_range)

    return stocks_in_range


def party_on(ticker_type, tickers_in, run_number=1):
    # run_number = start + 1
    line_notify_message("Start: " + str(today) + " " + str(ticker_type))
    # Select the first tickers
    # tickers_in = tickers_in[:100]
    # Select the last tickers
    # new_tickers = new_tickers[-1000:]
    # data_all_tickers = get_yq_financial_data(tickers_in)
    data_all_tickers = get_yq_historical_data(tickers_in)

    # print(data_all_tickers)
    # data_all = pd.read_csv('data_all.csv', index_col=[0, 1])
    # for ticker in tickers_in[start:]:
    for ticker in tickers_in:
        print(ticker_type, run_number, ticker)
        # print(data)
        # print (data)
        # print(ticker)
        data_one_ticker = sel_yq_historical_data(data_all_tickers, ticker)
        # print(data_one_ticker)
        if data_one_ticker.empty:
            continue
        run_number += 1
        # last_close_price = round(data_one_ticker["close"][-1], 2)
        # print(last_close_price)
        # plot_title = "{} {} {} {}".format(ticker, today, last_close_price, scenario)

        # print (ticker)
        if run_vwap_strategy_screener == 1:
            vwap_strategy_screener(ticker, data_one_ticker, run_number, ticker_type)
        if run_vcp_screener_strategy == 1:
            # print("Running VCP")
            vcp_screener_strategy(ticker, data_one_ticker)
        if run_buy_signal_strategy_screener == 1:
            buy_signal_strategy_screener(ticker, data_one_ticker, run_number, ticker_type, screener_day, vol_factor)
        if run_find_stocks_in_range == 1:
            stocks_in_range = find_stocks_in_range(data_one_ticker)
            if stocks_in_range.any():
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + ticker)
                highchart_chart(data_one_ticker, ticker, url)
                # plotly_chart(data, plot_title, 0)


# stockscreener.condition1_enabled = False
# stockscreener.condition2_enabled = False
# stockscreener.condition3_enabled = False

# VWAP Scenario
scenario = 144  # 21, 55, 89, 144, 233共5種

# RSI的日期範圍
rsi_period = 14

# plotly的圖檔大小
plotly_resolution = "high"

if plotly_resolution == "high":
    jpg_resolution = 1080
else:
    jpg_resolution = 800

# volume Factor
vol_factor = 1  # volume factor for VWAP_SCREENER

# screener要判斷的平均天數
screener_day = 8

# 強制寫出plotly，主要用來測試
ForcePLOT = 0
OnlyPLOT = False  # True / False

# 若程式執行至一半中斷，可以設定重新執行的位置
test_start = 0
us_start = 0
tw_start = 0
yf_start = 0
etf_start = 0
fin_start = 0

# 設定要執行的種類
# VCP_TEST = 0
run_vcp_screener_strategy = 0  # 找VCP型態的股票
run_buy_signal_strategy_screener = 1  # 找帶量突破的股票
run_vwap_strategy_screener = 0  # VWAP均線的策略，均線呈多頭排序時買入
run_find_stocks_in_range = 0  #

# 要執行的ticker種類
TEST = 0
US = 0
TW = 0
ETF = 0
FIN = 0  # Filter tickers from finviz screener
YF = 0

# 將讀取到的資料轉換為 list，並存入 tickers 變數中
if TW == 1:
    tw_tickers = get_tickers("TW", tw_start)
if YF == 1:
    yf_tickers = get_tickers("YF", yf_start)
if US == 1:
    us_tickers = get_tickers("US", us_start)
if ETF == 1:
    etf_tickers = get_tickers("ETF", etf_start)
if FIN == 1:
    fin_tickers = get_tickers("FIN", fin_start)
if TEST == 1:
    # test_tickers = ['AMD', 'AMOV', 'V', 'ROJER']
    test_tickers = ['CCS', 'FLNG', 'ENLT', 'PCAR']
    # test_tickers = ['NVDA', 'MET']
start_time = time.time()  # 記錄開始時間

update_financial_tickers = 1
if update_financial_tickers == 1:

    # yf_tickers = get_tickers("YF", yf_start)
    # test_tickers = ['CCS', 'FLNG', 'ENLT', 'PCAR', 'TSLA', 'MSFT']
    # filter_financial_ticker(test_tickers, "US")
    # tw_tickers = get_tickers("TW", tw_start)
    us_tickers = get_tickers("US", us_start)
    filter_financial_ticker(us_tickers, "US")

run_refersh_financial_data = 0
if run_refersh_financial_data == 1:
    # us_tickers = get_tickers("US", us_start)
    tw_tickers = get_tickers("TW", tw_start)
    df = filter_financial_ticker(tw_tickers)

### TEST ###
# filter_tickers = ['GOOG', 'GOOGL', 'AMZN', 'PCAR', 'BRK-B', 'TSLA', 'NVDA', 'V', 'TSM', 'XOM', 'META', 'UNH', 'JPM', 'JNJ', 'WMT', 'MA', 'PG', 'NVO', 'CVX', 'LLY', 'HD', 'ABBV', 'MRK', 'BAC', 'KO', 'AVGO', 'ASML', 'PEP', 'BABA', 'ORCL', 'PFE', 'SHEL', 'COST', 'TMO', 'AZN', 'CSCO', 'MCD', 'CRM', 'TM', 'NKE', 'DHR', 'NVS', 'DIS', 'ABT', 'WFC', 'LIN', 'TMUS', 'ACN', 'BHP', 'VZ', 'MS', 'UPS', 'TXN', 'CMCSA', 'TTE', 'PM', 'ADBE', 'HSBC', 'BMY', 'RTX', 'NEE', 'SCHW', 'NFLX', 'RY', 'QCOM', 'SAP', 'T', 'COP', 'HON', 'AXP', 'CAT', 'UNP', 'UL', 'AMD', 'DE', 'AMGN', 'HDB', 'BA', 'LMT', 'BP', 'PDD', 'BUD', 'RIO', 'TD', 'SNY', 'LOW', 'SBUX', 'GS', 'IBM', 'PLD', 'INTU', 'ELV', 'SPGI', 'MDT', 'INTC', 'CVS', 'SONY', 'BLK', 'GILD', 'BKNG', 'DEO', 'C', 'SYK', 'AMAT', 'EQNR', 'GE', 'ADI', 'ADP', 'AMT', 'MDLZ', 'TJX', 'EL', 'NOW', 'CB', 'CI', 'BTI', 'MUFG', 'REGN', 'PGR', 'PYPL', 'MO', 'MMC', 'ISRG', 'VALE', 'CNI', 'ENB', 'ZTS', 'SLB', 'TGT', 'VRTX', 'INFY', 'CHTR', 'FISV', 'JD', 'ABNB', 'IBN', 'CP', 'DUK', 'ITW', 'NOC', 'USB', 'PBR', 'EOG', 'GSK', 'ETN', 'SO', 'HCA', 'BSX', 'AMOV', 'BN', 'UBS', 'BMO', 'AMX', 'CME', 'BX', 'BDX', 'CNQ', 'UBER', 'LRCX', 'SAN', 'APD', 'CSX', 'GD', 'EQIX', 'ABB', 'HUM', 'AON', 'WM', 'CL', 'PNC', 'FCX', 'MELI', 'MU', 'TFC', 'ATVI', 'MMM', 'BNS', 'MPC', 'SMFG', 'STLA', 'RELX', 'TRI', 'SCCO', 'SHW', 'PANW', 'ICE', 'NTES', 'CCI', 'SNPS', 'OXY', 'MET', 'GM', 'VLO', 'MNST', 'MRNA', 'MCO', 'CDNS', 'ORLY', 'MAR', 'AIG', 'PSA', 'KLAC', 'FDX', 'NSC', 'BIDU', 'SHOP', 'ING', 'F', 'PSX', 'PXD', 'KDP', 'HSY', 'EW', 'RACE', 'MCK', 'TAK', 'DG', 'EMR', 'KHC', 'KKR', 'WDS', 'E', 'WDAY', 'VMW', 'GIS', 'AZO', 'FTNT', 'SRE', 'APH', 'BBVA', 'ITUB', 'SU', 'NXPI', 'SQ', 'D', 'PH', 'NGG', 'ECL', 'DXCM', 'LVS', 'ROP', 'CTVA', 'AEP', 'ADM', 'MSI', 'CTAS', 'HMC', 'MCHP', 'NUE', 'ADSK', 'JCI', 'SNOW', 'HES', 'KMB', 'TRV', 'TT', 'STM', 'O', 'TEAM', 'ANET', 'PUK', 'AFL', 'A', 'TDG', 'CM', 'LYG', 'DOW', 'COF', 'CMG', 'MSCI', 'APO', 'STZ', 'RSG', 'NTR', 'TEL', 'BK', 'TRP', 'LHX', 'BCE', 'LNG', 'PAYX', 'ABEV', 'SPG', 'EXC', 'MFG', 'LULU', 'BSBR', 'AJG', 'IQV', 'IDXX', 'BIIB', 'KMI', 'HLT', 'MRVL', 'SYY', 'ODFL', 'ROST', 'CARR', 'CRH', 'CNC', 'FIS', 'MFC', 'WBD', 'WMB', 'WELL', 'CVE', 'DVN', 'PRU', 'AMP', 'YUM', 'OTIS', 'CMI', 'SE', 'GFS', 'XEL', 'HLN', 'VICI', 'NEM', 'WCN', 'NWG', 'GWW', 'GEHC', 'HAL', 'DD', 'ROK', 'FMX', 'PCG', 'CPRT', 'ALL', 'ALC', 'SGEN', 'BCS', 'AME', 'KR', 'VOD', 'URI', 'DLTR', 'ON', 'MTD', 'ILMN', 'BKR', 'CTSH', 'LYB', 'ABC', 'PPG', 'RMD', 'MBLY', 'ED', 'APTV', 'DHI', 'BNTX', 'EA', 'ORAN', 'STT', 'WBA', 'DFS', 'FERG', 'FAST', 'IMO', 'PEG', 'CHT', 'OKE', 'ALB', 'DLR', 'GPN', 'GLW', 'CSGP', 'SLF', 'TU', 'ENPH', 'GOLD', 'DELL', 'CRWD', 'HPQ', 'KEYS', 'VRSK', 'SBAC', 'WEC', 'NDAQ', 'LEN', 'VEEV', 'TTD', 'CDW', 'ANSS', 'BBD', 'ULTA', 'CBRE', 'ACGL', 'FANG', 'NOK', 'IT', 'WIT', 'FNV', 'ZBH', 'ES', 'MTB', 'YUMC', 'TLK', 'AWK', 'CCEP', 'HZNP', 'MT', 'TSCO', 'CPNG', 'WTW', 'BGNE', 'EBAY', 'ARE', 'TROW', 'DB', 'CEG', 'EIX', 'EFX', 'DAL', 'FITB', 'HIG', 'LI', 'GMAB', 'TCOM', 'BEKE', 'GPC', 'BBDO', 'SQM', 'VMC', 'RCI', 'ALNY', 'TEF', 'ALGN', 'FTV', 'WST', 'DDOG', 'HEI', 'AVB', 'EC', 'IR', 'IFF', 'EQR', 'WY', 'HRL', 'PWR', 'STLD', 'RJF', 'MPWR', 'SPOT', 'K', 'NU', 'RBLX', 'MLM', 'CNHI', 'FE', 'EXR', 'FRC', 'CAJ', 'ETR', 'HBAN', 'GIB', 'RF', 'RYAAY', 'AEM', 'AEE', 'TECK', 'DOV', 'DASH', 'LH', 'TSN', 'DTE', 'FSLR', 'ZM', 'CHD', 'IX', 'VRSN', 'UMC', 'PFG', 'LPLA', 'TS', 'TDY', 'HPE', 'CTRA', 'LUV', 'PPL', 'BAX', 'PODD', 'CFG', 'QSR', 'NET', 'HOLX', 'MKC', 'PKX', 'CLX', 'NTRS', 'CAH', 'VTR', 'ARGX', 'ZTO', 'WAB', 'MOS', 'FTS', 'JBHT', 'ZS', 'TTWO', 'HUBS', 'WPM', 'CINF', 'FOXA', 'GRMN', 'PBA', 'BMRN', 'WAT', 'STE', 'INVH', 'ICLR', 'OMC', 'BBY', 'ERIC', 'MAA', 'XYL', 'RCL', 'ELP', 'MKL', 'WRB', 'HWM', 'SEDG', 'EPAM', 'SWKS', 'DRI', 'CNP', 'SUI', 'TRGP', 'INCY', 'PAYC', 'FOX', 'ROL', 'FICO', 'CAG', 'BALL', 'WPC', 'PINS', 'EXPD', 'CMS', 'UAL', 'CHWY', 'MGM', 'IEX', 'CF', 'NVR', 'KEY', 'BR', 'SPLK', 'AMCR', 'AVTR', 'SIRI', 'AES', 'LYV', 'MRO', 'PARAA', 'SIVB', 'EXPE', 'FWONK', 'WMG', 'PLTR', 'HTHT', 'FMC', 'UI', 'MGA', 'MOH', 'COO', 'ATO', 'FDS', 'AER', 'SJM', 'SNAP', 'BRO', 'RPRX', 'PKI', 'ASX', 'FLT', 'TER', 'CPB', 'CHKP', 'ZBRA', 'COIN', 'RTO', 'WLK', 'SYF', 'DGX', 'LKQ', 'KOF', 'AXON', 'LCID', 'IRM', 'J', 'RE', 'TXT', 'ETSY', 'RS', 'KB', 'TW', 'EBR', 'AGR', 'SSNC', 'PTC', 'LW', 'RIVN', 'AVY', 'BG', 'NIO', 'FWONA', 'SHG', 'BEN', 'SJR', 'ESS', 'L', 'ARES', 'PHG', 'BURL', 'PARA', 'BIO', 'CBOE', 'AZPN', 'MDB', 'GLPI', 'TPL', 'BAM', 'NTAP', 'UDR', 'IPG', 'POOL', 'TME', 'CCL', 'VTRS', 'EVRG', 'HUBB', 'LDOS', 'TYL', 'CE', 'STX', 'CSL', 'MKTX', 'WPP', 'CRBG', 'SNA', 'NICE', 'IP', 'SRPT', 'PEAK', 'PKG', 'APA', 'TRMB', 'WYNN', 'LNT', 'BAH', 'OKTA', 'BLDR', 'KIM', 'CTLT', 'H', 'TWLO', 'NDSN', 'SNN', 'TRU', 'LBRDA', 'UHAL', 'CG', 'LBRDK', 'ELS', 'ENTG', 'SWK', 'GEN', 'VIV', 'CUK', 'ACM', 'CPT', 'ERIE', 'DT', 'DOCU', 'PHM', 'NMR', 'HST', 'WDC', 'JKHY', 'CCJ', 'FHN', 'EQT', 'IHG', 'TECH']
"""
filter_tickers = ['NVDA', 'TME', 'GOOG', 'GOOGL', 'AMZN', 'PCAR', 'BRK-B', 'TSLA', 'NVDA', 'V', 'TSM', 'XOM', 'META',
                  'UNH', 'JPM']
hist_df = get_yq_historical_data(filter_tickers)
for ticker in filter_tickers:
    print(f"Checking VCP Ticker: {ticker}")
    df_one = sel_yq_historical_data(hist_df, ticker)
    vcp_screener_strategy(ticker, df_one)
"""
### END TEST ###

#############################################################################

# debug mode => 寫出較多的資料
# debugmode = 1
# 決定是否要執行screener
lets_party = 0

if lets_party == 1:
    if TEST == 1:
        party_on("TEST", test_tickers)
        category = "TEST"
    if US == 1:
        party_on("US", us_tickers)
        category = "US"
    if TW == 1:
        party_on("TW", tw_tickers)
        category = "TW"
    if ETF == 1:
        party_on("ETF", etf_tickers)
        category = "ETF"
    if YF == 1:
        party_on("YF", yf_tickers)
        category = "YF"
    if FIN == 1:
        category = "FIN"
        # remove_list = ['BREZR','DAVEW','DWACW']
        # for item in remove_list:
        #    fin_tickers.remove(item)
        # print(fin_tickers)
        party_on("FIN", fin_tickers)

end_time = time.time()  # 記錄結束時間
elapsed_time = round(end_time - start_time, 2)  # 計算運行時間
print(f"Elapsed time: {elapsed_time} seconds")