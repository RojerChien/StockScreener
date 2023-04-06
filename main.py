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

    # 返回 Ticker 列表
    return tickers


def get_yq_historical_data(ticker_list):
    # print(ticker_list)
    get_data_start_time = time.time()  # Record start time
    print("Start getting stock historical data")
    ticker = Ticker(ticker_list, asynchronous=True)
    data_all = ticker.history(period="3y", interval="1d")
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = get_data_end_time - get_data_start_time  # Compute elapsed time
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


def highchart_chart(dfin, ticker_in, date, url):
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


def get_yq_financial_data(ticker_list):
    # print(ticker_list)
    get_data_start_time = time.time()  # Record start time
    print("Start getting stock financial data")
    # fin_data = Ticker(ticker_list).get_modules(['summaryDetail'])
    fin_data = Ticker(ticker_list).all_modules

    # print(fin_data)
    # fin_data = Ticker(ticker_list).get_modules(['summaryDetail', 'balanceSheetHistory'])
    get_data_end_time = time.time()  # Record end time
    get_data_elapsed_time = get_data_end_time - get_data_start_time  # Compute elapsed time
    print(f"Get Data Elapsed time: {get_data_elapsed_time} seconds")
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


def filter_financial_ticker(tickers_in):
    start_time = time.time()  # 記錄開始時間
    fin_data = get_yq_financial_data(tickers_in)
    print(fin_data)
    end_time = time.time()  # 記錄結束時間
    elapsed_time = end_time - start_time  # 計算運行時間
    print(f"Elapsed time: {elapsed_time} seconds")
    filter_tickers = []
    for ticker in tickers_in:
        if 'Quote not found for ticker symbol:' in fin_data[ticker] or 'For input string' in fin_data[ticker]:
            print(f'Quote not found for ticker symbol:{ticker}')
            continue
        else:
            print(ticker)
            summary_detail = fin_data[ticker].get('summaryDetail')
            if summary_detail is not None:
                # ticker_previous_close = get_financial_data("summary_detail", "previousClose")
                ticker_previous_close = summary_detail.get('previousClose')
                if ticker_previous_close is not None:
                    ticker_previous_close = fin_data[ticker]['summaryDetail']['previousClose']
                    print(f'ticker_previous_close {ticker_previous_close}')

                ticker_forward_pe = summary_detail.get('forwardPE')
                if ticker_forward_pe is not None:
                    ticker_forward_pe = fin_data[ticker]['summaryDetail'].get('forwardPE', None)
                    print(f'ticker_forward_pe {ticker_forward_pe}')

                ticker_trailing_pe = summary_detail.get('trailingPE')
                if ticker_trailing_pe is not None:
                    ticker_trailing_pe = fin_data[ticker]['summaryDetail'].get('trailingPE', None)
                    print(f'ticker_forward_pe {ticker_trailing_pe}')

                ticker_average_daily_volume_10day = summary_detail.get('averageDailyVolume10Day')
                if ticker_average_daily_volume_10day is not None:
                    ticker_average_daily_volume_10day = fin_data[ticker]['summaryDetail'].get('averageDailyVolume10Day', None)
                    print(f'ticker_average_daily_volume_10day {ticker_average_daily_volume_10day}')

                ticker_52_week_low = summary_detail.get('fiftyTwoWeekLow')
                if ticker_52_week_low is not None:
                    ticker_52_week_low = fin_data[ticker]['summaryDetail'].get('fiftyTwoWeekLow', None)
                    print(f'ticker_52_week_low {ticker_52_week_low}')

                ticker_52_week_high = summary_detail.get('forwardPE')
                if ticker_52_week_high is not None:
                    ticker_52_week_high = fin_data[ticker]['summaryDetail'].get('fiftyTwoWeekHigh', None)
                    print(f'ticker_52_week_high {ticker_52_week_high}')

                ticker_50_day_average = summary_detail.get('fiftyDayAverage')
                if ticker_50_day_average is not None:
                    ticker_50_day_average = fin_data[ticker]['summaryDetail'].get('fiftyDayAverage', None)
                    print(f'ticker_50_day_average {ticker_50_day_average}')

                ticker_200_day_average = summary_detail.get('twoHundredDayAverage')
                if ticker_200_day_average is not None:
                    ticker_200_day_average = fin_data[ticker]['summaryDetail'].get('twoHundredDayAverage', None)
                    print(f'ticker_200_day_average {ticker_200_day_average}')

                if (ticker_forward_pe is not None and ticker_trailing_pe is not None and
                        ticker_forward_pe != "Infinity" and ticker_trailing_pe != "Infinity"):
                    print("PE is not valid, skip")
                    if ((ticker_previous_close / ticker_52_week_low > 1.3) and
                            (ticker_forward_pe > ticker_trailing_pe) and
                            (ticker_50_day_average > ticker_200_day_average)):
                        filter_tickers.append(ticker)

                else:
                    continue
            print(filter_tickers)


def refresh_financial_data(tickers_in):
    get_fin_start_time = time.time()  # 記錄開始時間
    fin_data = get_yq_financial_data(tickers_in)
    # print(fin_data)
    get_fin_end_time = time.time()  # 記錄結束時間
    get_fin_elapsed_time = get_fin_end_time - get_fin_start_time  # 計算運行時間
    print(f"Elapsed time: {get_fin_elapsed_time} seconds")
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


def calculate_vwap(df_in, duration):
    # data['Typical Price'] = (data['high'] + data['low'] + data['close']) / 3
    df_in['VWPrice'] = df_in['close'] * df_in['volume']
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
            highchart_chart(df, tickers_in, today, url)
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
            highchart_chart(df, tickers_in, today, url)
            # plotly_chart(df, plot_title, 0)
    else:
        print("volume or volatility not meet, skip analysis!")
    # lineNotifyMessage(token, "Finished: " + today + " " + category + "\nScanned " + str(run_number) + " of " + str(
    #    start) + " Stocks in " + category + " Market\n" + str(true_number) + " Meet Criteria")


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
                highchart_chart(df, tickers_in, today, url)
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
    volatility = volatility_h + volatility_l
    # print(f"Volativity: {n_days} days {volatility}")

    return volatility


def calculate_avg_volume(df, n_days):
    hist = df.tail(n_days)
    avg_volume = hist['volume'].mean()
    return avg_volume


def vcp_screener_strategy(ticker_in, data):
    print("Running VCP")
    volatility_5 = calculate_volatility(data, 5)
    volatility_13 = calculate_volatility(data, 13)
    volatility_21 = calculate_volatility(data, 21)
    volatility_34 = calculate_volatility(data, 34)
    avg_volume_5 = calculate_avg_volume(data, 5)
    avg_volume_13 = calculate_avg_volume(data, 13)
    avg_volume_21 = calculate_avg_volume(data, 21)
    avg_volume_34 = calculate_avg_volume(data, 34)
    if volatility_5 < 0.03 < volatility_13 < volatility_21 < volatility_34 and avg_volume_5 < avg_volume_13 < avg_volume_21 < avg_volume_34:
        url = f"https://www.tradingview.com/chart/sWFIrRUP/?symbol={ticker_in}"
        # webbrowser.open(url)
        highchart_chart(data, ticker_in, today, url)

        plot_title = "{} {} {} {}".format(ticker_in, today, last_close_price, scenario)
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
        if data_one_ticker.empty:
            continue
        # print(data)
        run_number += 1
        last_close_price = round(data_one_ticker["close"][-1], 2)
        plot_title = "{} {} {} {}".format(ticker, today, last_close_price, scenario)

        # print (ticker)
        if run_vwap_strategy_screener == 1:
            vwap_strategy_screener(ticker, data_one_ticker, run_number, ticker_type)
        if run_vcp_screener_strategy == 1:
            print("Running VCP")
            vcp_screener_strategy(ticker, data_one_ticker)
        if run_buy_signal_strategy_screener == 1:
            buy_signal_strategy_screener(ticker, data_one_ticker, run_number, ticker_type, screener_day, vol_factor)
        if run_find_stocks_in_range == 1:
            stocks_in_range = find_stocks_in_range(data_one_ticker)
            if stocks_in_range.any():
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + ticker)
                highchart_chart(data_one_ticker, ticker, today, url)
                # plotly_chart(data, plot_title, 0)


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
vol_factor = 15  # volume factor for VWAP_SCREENER

# screener要判斷的平均天數
screener_day = 8

# 強制寫出plotly，主要用來測試
ForcePLOT = 0
OnlyPLOT = False  # True / False

# 若程式執行至一半中斷，可以設定重新執行的位置
test_start = 0
us_start = 0
tw_start = 0
etf_start = 0
fin_start = 0

# 設定要執行的種類
# VCP_TEST = 0
run_vcp_screener_strategy = 0
run_buy_signal_strategy_screener = 1
run_vwap_strategy_screener = 0
run_find_stocks_in_range = 0

# 要執行的ticker種類
TEST = 1
US = 0
TW = 0
ETF = 0
FIN = 0  # Filter tickers from finviz screener

# 將讀取到的資料轉換為 list，並存入 tickers 變數中
if TW == 1:
    tw_tickers = get_tickers("TW", tw_start)
if US == 1:
    us_tickers = get_tickers("US", us_start)
if ETF == 1:
    etf_tickers = get_tickers("ETF", etf_start)
if FIN == 1:
    fin_tickers = get_tickers("FIN", fin_start)
if TEST == 1:
    test_tickers = ['RKT', 'ICHR', 'LPG', 'UFPT', 'IMOS', 'ASTL', 'HCCI', 'SXC', 'TGI']

start_time = time.time()  # 記錄開始時間

run_refersh_financial_data = 1
if run_refersh_financial_data == 1:
    filter_financial_ticker(test_tickers)

#############################################################################

# debug mode => 寫出較多的資料
# debugmode = 1
# 決定是否要執行screener
lets_party = 0

if lets_party == 1:
    if TEST == 1:
        party_on("TEST", test_tickers)
    if US == 1:
        party_on("US", us_tickers)
    if TW == 1:
        party_on("TW", tw_tickers)
    if ETF == 1:
        party_on("ETF", etf_tickers)
    if FIN == 1:
        # remove_list = ['BREZR','DAVEW','DWACW']
        # for item in remove_list:
        #    fin_tickers.remove(item)
        # print(fin_tickers)
        party_on("FIN", fin_tickers)

end_time = time.time()  # 記錄結束時間
elapsed_time = end_time - start_time  # 計算運行時間
print(f"Elapsed time: {elapsed_time} seconds")
