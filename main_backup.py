import pandas as pd
import os
import time
import webbrowser
import requests
import datetime
import numpy as np
from highcharts import Highstock
from bs4 import BeautifulSoup
from yahooquery import Ticker

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


def add_vwap_to_chart(chart, dfin, window, color, line_width, yAxis=0, id=None):
    vwap = dfin[f'vwap{window}'].values.tolist()
    vwap = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(v, 2)]
        for i, v in enumerate(vwap)
    ]
    chart.add_data_set(vwap, 'line', f'vwap{window}', yAxis=yAxis, color=color, lineWidth=line_width, id=id,
                       dataGrouping={'units': [['day', [1]]]})


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


def get_us_tickers(category) -> dict:
    print(f'############ Start Getting Ticker by new {category} mode')
    df = pd.read_excel("Tickers.xlsx", sheet_name=category)

    # 把Symbol, Sector, Industry這三個欄位的值都存儲到列表中
    symbols = [str(sym).replace('/', '-') for sym in df["Symbol"] if '^' not in str(sym)]
    sectors = df["Sector"].tolist()
    industries = df["Industry"].tolist()

    # 使用Symbol作為鍵，建立一個字典來查找Sector和Industry的值
    us_tickers_dict = {}
    for symbol, sector, industry in zip(symbols, sectors, industries):
        symbol = str(symbol).replace('/', '-')
        us_tickers_dict[symbol] = {"Sector": sector, "Industry": industry}

    tickers_length_pre = len(symbols)
    print(f'Total {category} Tickers before remove PTP:', tickers_length_pre)
    ptp_lists = get_ptp_tickers()
    # print(f'PTP Stock List: {ptp_lists}')
    symbols_removed_ptp = remove_ptp_list(ptp_lists, symbols)
    tickers_length_post = len(symbols_removed_ptp)
    print(f'Total {category} Tickers after remove PTP:', tickers_length_post)

    return us_tickers_dict, symbols_removed_ptp


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
    # print(fin_data)
    return fin_data


def sel_yq_financial_data(data_all, ticker_in):
    # 初始化变量
    industry = 'N/A'
    sector = 'N/A'

    # 提取键值为 'AA' 的数据
    data_aa = data_all.get(ticker_in, {})
    # print(f"data_aa: {data_aa}")
    # 检查提取的数据是否是字典
    if isinstance(data_aa, dict):
        # 提取 'industry' 的值
        industry = data_aa.get('assetProfile', {}).get('industry', 'N/A')

        # 提取 'sector' 的值
        sector = data_aa.get('assetProfile', {}).get('sector', 'N/A')

        print(f"Industry: {industry}")
        print(f"Sector: {sector}")
    else:
        print(f"Data for {ticker_in} is not a dictionary.")

    return industry, sector



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


def vwap_strategy_screener_in_range(tickers_in, tickers_dict_in, scenario=144, days=233, percentage=2, ticker_type="US",
                                    run_number=1, update_historical_data=1):
    # line_notify_message("Start: " + str(today) + " " + str(ticker_type))
    data_all_tickers = get_yq_historical_data(tickers_in)
    data_all_tickers.to_csv('data_all_tickers.csv', index=True)
    data_all_financial = get_yq_financial_data(tickers_in)
    # 將字典轉換為 DataFrame
    # data_all_financial_df = pd.DataFrame(data_all_financial)
    # 保存 DataFrame 到 CSV 文件
    # data_all_financial_df.to_csv('data_all_financial.csv', index=True)

    # print(data_all_financial)
    df_sector = pd.DataFrame(columns=['Ticker', 'Industry', 'Sector'])
    for ticker in tickers_in:
        sector = tickers_dict_in[ticker]["Sector"]
        industry = tickers_dict_in[ticker]["Industry"]
        print(ticker_type, ticker, run_number)
        if update_historical_data:
            df = sel_yq_historical_data(data_all_tickers, ticker)
            df.to_csv('yq_historical.csv', index=False)
            industry, sector = sel_yq_financial_data(data_all_financial, ticker)
            df_sector = pd.concat(
                [df_sector, pd.DataFrame({'Ticker': [ticker], 'Industry': [industry], 'Sector': [sector]})],
                ignore_index=True)
            # 将 DataFrame 写入 Excel 文件
            df_sector.to_excel('industry_sector.xlsx', index=False)

        else:
            if os.path.exists('yq_historical.csv'):
                df = pd.read_csv('yq_historical.csv')
        if df.empty:
            continue

        run_number += 1
        # 計算過去 days 天的最高價
        highest_price = df['close'].rolling(window=days).max().iloc[-1]

        # 計算正負 percentage% 的範圍
        upper_range = highest_price * (1 + percentage / 100)
        lower_range = highest_price * (1 - percentage / 100)
        # print(upper_range)
        # print(lower_range)

        # 篩選出最近的收盤價在範圍內的股票
        last_close_price = round(df['close'].iloc[-1], 2)
        stocks_in_range = (last_close_price >= lower_range) & (last_close_price <= upper_range)

        # global scenario
        df['AvgVol'] = df['volume'].rolling(55).mean()  # 55為平均的天數
        last_avgvol55 = round(df['AvgVol'].iloc[-1], 2)
        last_vwap55 = round(df['vwap55'].iloc[-1], 2)
        avg_money_traded = (last_avgvol55 * last_vwap55) >= 2000000
        # avg_money_traded
        volatility_H = df['close'].max() / df['close'].mean()  # 把voltility改成用close來算max，避免一些小型股會有突然上漲後再拉回的情況
        volatility_L = df['close'].min() / df['close'].mean()  # 把voltility改成用close來算min，避免一些小型股會有突然上漲後再拉回的情況
        volatility = volatility_H - volatility_L
        # 計算最後的15天的波動率
        last_15_days = df['close'].tail(15)
        volatility_H_15 = last_15_days.max() / last_15_days.mean()  # 把voltility改成用close來算max，避免一些小型股會有突然上漲後再拉回的情況
        volatility_L_15 = last_15_days.min() / last_15_days.mean()  # 把voltility改成用close來算min，避免一些小型股會有突然上漲後再拉回的情況
        volatility_15 = volatility_H_15 - volatility_L_15
        # print (str(len(df.index)) + " " + str(volatility_H) + " " + str(volatility_L) + " " + str(volatility))

        if len(df.index) > 144 and volatility_15 > 0.01 and volatility > 0.15 and avg_money_traded:  # 過濾資料筆數少於144筆的股票，確保上市時間有半年並且判斷半年內的波動率，像死魚一樣不動的股票就不分析
            if ForcePLOT == 1:
                url = get_tradingview_url(ticker, ticker_type)
                # url = f'https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{tickers_in}'
                highchart_chart(df, tickers_in, url)
            df['VWAP21_Result'] = (df['vwap5'] > df['vwap21'])
            df['VWAP55_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55'])
            df['VWAP89_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55']) & (
                    df['vwap55'] > df['vwap89'])
            df['VWAP144_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55']) & (
                    df['vwap55'] > df['vwap89']) & (df['vwap89'] > df['vwap144'])
            df['VWAP233_Result'] = (df['vwap5'] > df['vwap21']) & (df['vwap21'] > df['vwap55']) & (
                    df['vwap55'] > df['vwap89']) & (df['vwap89'] > df['vwap144']) & (
                                           df['vwap144'] > df['vwap233'])

            # VWAP5_inc = (df['vwap5'].iloc[-1] > df['vwap5'].iloc[-2])
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
            last_vwap_value_233 = df['VWAP233_Result'][-1]
            pattern_233 = np.array([False] * 20 + [True])
            VWAP233_history = np.array_equal(vwap_values_233[-21:-1], pattern_233[:-1]) and vwap_values_233[-1] == \
                              pattern_233[-1]

            vwap_values_144 = df['VWAP144_Result'].values
            last_vwap_value_144 = df['VWAP144_Result'][-1]
            pattern_144 = np.array([False] * 20 + [True])
            VWAP144_history = np.array_equal(vwap_values_144[-21:-1], pattern_144[:-1]) and vwap_values_144[-1] == \
                              pattern_144[-1]

            vwap_values_89 = df['VWAP89_Result'].values
            pattern_89 = np.array([False] * 20 + [True])
            VWAP89_history = np.array_equal(vwap_values_89[-21:-1], pattern_89[:-1]) and vwap_values_89[-1] == \
                             pattern_89[
                                 -1]

            vwap_values_55 = df['VWAP55_Result'].values
            pattern_55 = np.array([False] * 20 + [True])
            VWAP55_history = np.array_equal(vwap_values_55[-21:-1], pattern_55[:-1]) and vwap_values_55[-1] == \
                             pattern_55[
                                 -1]
            vwap_values_21 = df['VWAP21_Result'].values
            pattern_21 = np.array([False] * 20 + [True])
            VWAP21_history = np.array_equal(vwap_values_21[-21:-1], pattern_21[:-1]) and vwap_values_21[-1] == \
                             pattern_21[
                                 -1]
            final_result = "FALSE"
            # scenario = 144
            VWAP55_history = "True"  # 只找出價格在範圍內的股票 VWAP144_Result
            if (scenario == 55) and (VWAP55_inc == True) and (last_vwap_value_144 == True):
                final_result = "TRUE"
            elif (scenario == 21) and (VWAP21_inc == True) and (last_vwap_value_144 == True):
                final_result = "TRUE"
            elif (scenario == 89) and (VWAP89_inc == True) and (last_vwap_value_144 == True):
                final_result = "TRUE"
            elif (scenario == 144) and (VWAP144_inc == True) and (last_vwap_value_144 == True):
                final_result = "TRUE"
            elif (scenario == 233) and (VWAP233_inc == True) and (last_vwap_value_144 == True):
                final_result = "TRUE"
            else:
                # print ("No Scenario")
                # print("No Scenario")
                # return 1
                continue
            # print(final_result)
            if (final_result == 'TRUE'):
                url = get_tradingview_url(ticker, ticker_type)
                # url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + ticker)
                print(ticker)
                print(today)
                print(url)
                highchart_chart(df, ticker, url)
                # plotly_chart(df, plot_title, 0)
        else:
            print("volume or volatility not meet, skip analysis!")
        # lineNotifyMessage(token, "Finished: " + today + " " + category + "\nScanned " + str(run_number) + " of " + str(
        #    start) + " Stocks in " + category + " Market\n" + str(true_number) + " Meet Criteria")


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
run_vwap_strategy_screener_in_range = 1  # VWAP均線的策略，均線呈多頭排序時買入，且限價在最高價正負2%的股票

# 要執行的ticker種類
TEST = 0
US = 1

# 將讀取到的資料轉換為 list，並存入 tickers 變數中
if US == 1:
    us_tickers_dict, us_tickers = get_us_tickers("US")
if TEST == 1:
    test_tickers = ['AAPL', 'MSFT', 'JPM']
    test_tickers_dict = {
        "AAPL": {"Sector": "Technology", "Industry": "Electronics"},
        "MSFT": {"Sector": "Technology", "Industry": "Software"},
        "JPM": {"Sector": "Finance", "Industry": "Banking"}
    }

start_time = time.time()  # 記錄開始時間

#############################################################################

# debug mode => 寫出較多的資料
# debugmode = 1
# 決定是否要執行screener
lets_party = 1

if lets_party == 1:
    if TEST == 1:
        category = "TEST"
        vwap_strategy_screener_in_range(test_tickers, test_tickers_dict)

    if US == 1:
        category = "US"
        vwap_strategy_screener_in_range(us_tickers, us_tickers_dict)

end_time = time.time()  # 記錄結束時間
elapsed_time = round(end_time - start_time, 2)  # 計算運行時間
print(f"Elapsed time: {elapsed_time} seconds")
