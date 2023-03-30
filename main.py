from pickle import TRUE
# https://medium.com/geekculture/top-4-python-libraries-for-technical-analysis-db4f1ea87e09

import pandas as pd
from finvizfinance.screener.overview import Overview

pd.options.mode.chained_assignment = None  # 將警告訊息關閉
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
# import kaleido
import numpy as np
from highcharts import Highstock
from IPython.display import HTML, display
import os
# from datetime import datetime
from csv import reader

# import bs4 as bs
# import csv
import plotly.graph_objects as go
from ta.trend import MACD
from ta.momentum import StochasticOscillator
from plotly.subplots import make_subplots
import webbrowser

########################## 從Firstrade以及老處取得ptp stock tickers #####################
import requests
from bs4 import BeautifulSoup
from finviz.screener import Screener

"""def get_finviz_screener_tickers():
    print("Start getting finviz tickers")
    filters_dict = {'20-Day Simple Moving Average': 'SMA20 above SMA50',
                    '50-Day Simple Moving Average': 'SMA50 above SMA200',
                    'Average Volume': 'Over 100K',
                    'Price': 'Over $3',
                    'EPS growthpast 5 years' : 'Positive (>0%)',
                    'Change': 'Up 2%'}
    tickers = []
    for stock in Screener(filters=filters_dict, order='ticker'):
        tickers.append(stock['Ticker'])
    print("Finished getting finviz tickers")
    return tickers"""

"""def get_finviz_screener_tickers():
    print("Start getting finviz tickers")
    foverview = Overview()
    filters_dict = {'20-Day Simple Moving Average': 'SMA20 above SMA50',
                     '50-Day Simple Moving Average': 'SMA50 above SMA200',
                     'Average Volume': 'Over 100K',
                     'Price': 'Over $3',
                     'EPS growthpast 5 years' : 'Positive (>0%)',
                     'Change': 'Up 2%'}
    #filters_dict = {'Change': 'Up 3%'}
    foverview.set_filter(filters_dict=filters_dict)
    df = foverview.screener_view()
    tickers = df['Ticker'].tolist()
    print("Finished getting finviz tickers")
    return tickers"""


def calculate_vwap(df_in, duration):
    # data['Typical Price'] = (data['High'] + data['Low'] + data['Close']) / 3
    df_in['VWPrice'] = df_in['Close'] * df_in['Volume']
    df_in[f'vwap{duration}'] = df_in['VWPrice'].rolling(window=duration).sum() / df_in['Volume'].rolling(
        window=duration).sum()
    return df_in


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


def get_ptp_tickers(url1, url2):
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

    return ptp_lists
    print(ptp_lists)


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


def lineNotifyImage(token, message, image):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': message}
    image = open(image, 'rb')
    imageFile = {'imageFile': image}
    r = requests.post(url, headers=headers, data=data, files=imageFile)
    if r.status_code == requests.codes.ok:
        return '圖片發送成功！'
    else:
        return f'圖片發送失敗: {r.status_code}'
    image.close()


token = 'YuvfgED98JDWMvATPEAnDu3u9Ge0R2B9BkrOvCwHZId'

"""def add_vwap_tochart(chart, dfin, window, color, line_width, yAxis=0):
    vwap = dfin[f'vwap{window}'].values.tolist()
    vwap = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(v, 2)]
        for i, v in enumerate(vwap)
    ]
    chart.add_data_set(vwap, 'line', f'vwap{window}', yAxis=yAxis, color=color, lineWidth=line_width, dataGrouping={'units': [['day', [1]]]})
"""


def add_vwap_to_chart(chart, dfin, window, color, line_width, yAxis=0, id=None):
    vwap = dfin[f'vwap{window}'].values.tolist()
    vwap = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(v, 2)]
        for i, v in enumerate(vwap)
    ]
    chart.add_data_set(vwap, 'line', f'vwap{window}', yAxis=yAxis, color=color, lineWidth=line_width, id=id,
                       dataGrouping={'units': [['day', [1]]]})


def highchart_chart(dfin, ticker_in, date, url):
    # 初始化Highstock对象
    chart = Highstock(renderTo='container', width=None, height=930)  # 添加宽度和高度
    # chart = Highstock(renderTo='container', width=1800, height=900)  # 添加宽度和高度
    # 添加10日成交量移動平均線
    dfin['volume_10ma'] = dfin['Volume'].rolling(window=10).mean()
    volume_10ma = dfin['volume_10ma'].values.tolist()
    volume_10ma = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), v]
        for i, v in enumerate(volume_10ma)
    ]
    chart.add_data_set(volume_10ma, 'line', '10日成交量移動平均', yAxis=1, dataGrouping={'units': [['day', [1]]]})

    # 添加蜡烛图序列
    ohlc = dfin[['Open', 'High', 'Low', 'Close']].values.tolist()
    ohlc = [[int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(o, 2), round(h, 2), round(l, 2), round(c, 2)] for
            i, (o, h, l, c) in enumerate(ohlc)]

    chart.add_data_set(ohlc, 'candlestick', ticker_in, dataGrouping={'units': [['day', [1]]]})
    add_vwap_to_chart(chart, dfin, 144, 'purple', 3, id='vwap144')
    add_vwap_to_chart(chart, dfin, 55, 'red', 3, id='vwap55')
    add_vwap_to_chart(chart, dfin, 21, 'orange', 3, id='vwap21')
    add_vwap_to_chart(chart, dfin, 5, 'blue', 3, id='vwap5')

    # 添加成交量序列
    volume = dfin[['Open', 'Close', 'Volume']].values.tolist()
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
             'top': '75%',
             'height': '25%',
             'offset': 0,
             'lineWidth': 2}
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


def highchart_chart3(dfin, ticker_in, date):
    # 初始化Highstock对象
    chart = Highstock(renderTo='container', width=1600, height=600)  # 添加宽度和高度

    # 添加10日成交量移動平均線
    dfin['volume_10ma'] = dfin['Volume'].rolling(window=10).mean()
    volume_10ma = dfin['volume_10ma'].values.tolist()
    volume_10ma = [
        [int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), v]
        for i, v in enumerate(volume_10ma)
    ]
    chart.add_data_set(volume_10ma, 'line', '10日成交量移動平均', yAxis=1, dataGrouping={'units': [['day', [1]]]})

    # 添加蜡烛图序列
    ohlc = dfin[['Open', 'High', 'Low', 'Close']].values.tolist()
    ohlc = [[int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(o, 2), round(h, 2), round(l, 2), round(c, 2)] for
            i, (o, h, l, c) in enumerate(ohlc)]

    chart.add_data_set(ohlc, 'candlestick', ticker_in, dataGrouping={'units': [['day', [1]]]})

    # 添加成交量序列
    volume = dfin[['Open', 'Close', 'Volume']].values.tolist()
    volume = [{'x': int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), 'y': v, 'color': 'red' if o > c else 'green'} for
              i, (o, c, v) in enumerate(volume)]

    chart.add_data_set(volume, 'column', '成交量', yAxis=1, dataGrouping={'units': [['day', [1]]]})

    # 设置图表选项
    options = {
        'rangeSelector': {'selected': 4},
        'title': {'text': f'{ticker_in} ({date})'},
        'yAxis': [
            {'labels': {'align': 'right', 'x': -3},
             'title': {'text': 'OHLC'},
             'height': '60%',
             'lineWidth': 2},
            {'labels': {'align': 'right', 'x': -3},
             'title': {'text': '成交量'},
             'top': '65%',
             'height': '35%',
             'offset': 0,
             'lineWidth': 2}
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
            'candlestick': {
                'color': 'red',
                'upColor': 'green'
            },
            'column': {
                'borderColor': 'none'
            }
        }
    }

    chart.set_dict_options(options)

    # 显示图表
    # chart.save_file('candlestick_volume')
    with open('candlestick_volume.html', 'w', encoding='utf-8') as f:
        f.write(chart.htmlcontent)
    webbrowser.open('candlestick_volume.html')


def highchart_chart_2(dfin, plot_title):
    # 初始化Highstock对象
    chart = Highstock()

    # 添加蜡烛图序列
    ohlc = dfin[['Open', 'High', 'Low', 'Close']].values.tolist()
    ohlc = [[int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), o, h, l, c] for i, (o, h, l, c) in enumerate(ohlc)]

    chart.add_data_set(ohlc, 'candlestick', 'TSLA', dataGrouping={'units': [['day', [1]]]})

    # 添加成交量序列
    volume = dfin['Volume'].values.tolist()
    volume = [[int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), v] for i, v in enumerate(volume)]

    chart.add_data_set(volume, 'column', '成交量', yAxis=1, dataGrouping={'units': [['day', [1]]]})

    # 设置图表选项
    options = {
        'rangeSelector': {'selected': 1},
        'title': {'text': 'Tesla Inc.'},
        'yAxis': [
            {'labels': {'align': 'right', 'x': -3},
             'title': {'text': 'OHLC'},
             'height': '60%',
             'lineWidth': 2},
            {'labels': {'align': 'right', 'x': -3},
             'title': {'text': '成交量'},
             'top': '65%',
             'height': '35%',
             'offset': 0,
             'lineWidth': 2}
        ],
        'tooltip': {
            'shared': True
        }
    }

    chart.set_dict_options(options)

    # 显示图表
    chart.save_file('candlestick_volume')
    webbrowser.open('candlestick_volume.html')
    """"# 客制化調整參數
    color = '#4285f4'  # 線的顏色 (red/green/blue/purple)
    linewidth = 2  # 線的粗細
    title = plot_title  # 標題名稱
    width = 800  # 圖的寬度
    height = 500  # 圖的高度

    # 繪圖設定
    chart = Highchart(width=width, height=height)

    x = dfin.index
    y = round(dfin.Close, 2)

    # 設置圖表基本屬性
    chart.set_options('chart', {'type': 'line'})
    chart.set_options('title', {'text': 'Stock Price'})
    chart.set_options('xAxis', {'categories': df['date'].tolist()})
    chart.set_options('yAxis', {'title': {'text': 'Price'}})

    data = [[index, s] for index, s in zip(x, y)]
    chart.add_data_set(data, 'line', 'data', color=color)

    chart.set_options('xAxis', {'type': 'datetime'})
    chart.set_options('title', {'text': title, 'style': {'color': 'black'}})  # 設定title
    chart.set_options('plotOptions', {'line': {'lineWidth': linewidth, 'dataLabels': {'enabled': False}}})  # 設定線的粗度
    chart.set_options('tooltip', {'shared': True, 'crosshairs': True})  # 設定為可互動式
    chart.save_file('chart')
    display(HTML('chart.html'))
    chart.htmlcontent
    webbrowser.open('chart.html')
    # os.remove('chart.html')
    """


def plotly_chart(dfin, plot_title, number, width):
    # Reference: https://python.plainenglish.io/a-simple-guide-to-plotly-for-plotting-financial-chart-54986c996682
    my_width = width
    my_height = int(my_width * 0.56)
    plot_period = -155  # 只保留特定天數的資料
    df = dfin[plot_period:]

    # first declare an empty figure
    fig = go.Figure()
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01,
                        row_heights=[0.5, 0.1, 0.1])

    # removing all empty dates
    # build complete timeline from start date to end date
    dt_all = pd.date_range(start=df.index[0], end=df.index[-1])
    # retrieve the dates that ARE in the original datset
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
    # define dates with missing values
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    # MACD
    macd = MACD(close=df['Close'],
                window_slow=26,
                window_fast=12,
                window_sign=9)
    # stochastic
    stoch = StochasticOscillator(high=df['High'],
                                 close=df['Close'],
                                 low=df['Low'],
                                 window=14,
                                 smooth_window=3)
    # add OHLC
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 showlegend=False)
                  )

    # add moving averages to df
    # df['MA20'] = df['Close'].rolling(window=20).mean()
    # df['MA5'] = df['Close'].rolling(window=5).mean()

    # add VWAP to df
    df['VWPrice'] = df['Close'] * df['Volume']
    # df.loc[df['VWPrice']] = df['Close'] * df['Volume']

    windows = [233, 144, 55, 21, 5]
    for w in windows:
        rolling_VWPrice = df['VWPrice'].rolling(window=w).sum()
        rolling_volume = df['Volume'].rolling(window=w).sum()
        df[f'vwap{w}'] = rolling_VWPrice / rolling_volume
    # df['vwap233'] = df['VWPrice'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
    # df['vwap144'] = df['VWPrice'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
    # df['vwap55'] = df['VWPrice'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
    # df['vwap21'] = df['VWPrice'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
    # df['vwap5'] = df['VWPrice'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

    # add moving average traces
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vwap5'],
                             opacity=0.7,
                             line=dict(color='blue', width=2),
                             name='VWAP 5'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vwap21'],
                             opacity=0.7,
                             line=dict(color='green', width=2),
                             name='VWAP 21'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vwap55'],
                             opacity=0.7,
                             line=dict(color='red', width=2),
                             name='VWAP 55'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vwap144'],
                             opacity=0.7,
                             line=dict(color='magenta', width=2),
                             name='VWAP 144'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vwap233'],
                             opacity=0.7,
                             line=dict(color='goldenrod', width=2),
                             name='VWAP 233'))

    # hide dates with no values
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    # remove rangeslider
    fig.update_layout(xaxis_rangeslider_visible=False)
    # add chart title
    fig.update_layout(title=plot_title)
    fig.update_layout(width=my_width, height=my_height,
                      xaxis_title='Date',
                      yaxis_title='Price',
                      font=dict(family='Arial', size=24),
                      title_font=dict(family='Arial', size=36))

    # Set MACD color
    colors = ['green' if val >= 0
              else 'red' for val in macd.macd_diff()]
    # MACD_name = ['Positive MACD' if val >= 0
    #  else 'Negative MACD' for val in macd.macd_diff()]

    # Add MACD trace
    fig.add_trace(go.Bar(x=df.index,
                         y=macd.macd_diff(),
                         marker_color=colors, name="MACD"
                         ), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd(),
                             line=dict(color='blue', width=2),
                             name='MACD Fast'
                             ), row=3, col=1)

    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd_signal(),
                             line=dict(color='red', width=2),
                             name='MACD Signal'
                             ), row=3, col=1)
    fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)

    # Set Volume color
    colors = ['red' if row['Open'] - row['Close'] >= 0
              else 'green' for index, row in df.iterrows()]
    # Add volume trace
    fig.add_trace(go.Bar(x=df.index,
                         y=df['Volume'],
                         marker_color=colors, name="Volume"
                         ), row=2, col=1)
    # 添加 AvgVol 軌跡
    fig.add_trace(
        go.Scatter(x=df.index, y=df['AvgVol'], name="Average Volume"),
        row=2, col=1
    )
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    # removing white space
    fig.update_layout(margin=go.layout.Margin(
        l=60,  # left margin
        r=60,  # right margin
        b=60,  # bottom margin
        t=100  # top margin
    ))
    if not OnlyPLOT:
        fig.to_image()
        fig.show()
    fig.write_image(str(number) + ".jpg")
    # filename = first_word = plot_title.split()[0] + '_' + plot_title.split()[1] + '.jpg'
    filename = f"{plot_title.split()[0]}_{plot_title.split()[1]}.jpg"
    fig.write_image(filename)
    # plt.savefig(str(true_number) +
    # fig.to_image(format="png", engine="kaleido")


def plot_chart(stock_data, true_number):
    plt.rc('figure', figsize=(15, 10))
    fig, axes = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.tight_layout(pad=3)
    print(stock_data)
    close = stock_data.Close
    vol = stock_data.Volume
    date = stock_data.index
    plot_price = axes[0]
    plot_price.plot(date, close, color='blue',
                    linewidth=2, label='Price')
    ohlc = stock_data.loc[:, [stock_data.index, stock_data.Open, stock_data.High, stock_data.Low, stock_data.Close]]
    ohlc.date = pd.to_datetime(ohlc.index)
    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    fig.suptitle('Daily Candlestick Chart of NIFTY50')
    ohlc.date = ohlc.index.apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig(str(true_number) + ".jpg")  # 將圖存成 JPEG 檔


def VWAP_history(vwap_values):
    pattern = np.array([False] * 20 + [True])
    return np.array_equal(vwap_values[-21:-1], pattern[:-1]) and vwap_values[-1] == pattern[-1]


def detect_vcp(tickers, start, ptp_list):
    true_number = 0
    run_number = 0
    today = str(datetime.datetime.now().date())
    lineNotifyMessage(token, "Start VCP: " + today + " ")
    for row in tickers[start:]:
        ptp_no = 0
        ptp = "False"
        for row2 in ptp_list:  # for row2 in ptp_list[start:]:
            # print (row,row2)
            if (row == row2):
                ptp = "True"
                ptp_no += 1
                lineNotifyMessage(token, row + " is PTP stock!")
                print(row, " is PTP stock, skip analysis!")

        if (ptp != "True"):
            # print ("Start　analysis!")
            start += 1
            print(" " + str(start), str(row))
            # print(row)
            # df = yf.download(row, start=start, end=end)
            try:
                data = yf.download(row, period="2y", progress=False)
                data['AvgVol'] = data['Volume'].rolling(55).mean()  # 55為平均的天數
                last_close_price = round(data["Close"][-1], 2)

            except:
                lineNotifyMessage(token, row + " is not exist!")
                # pass
            # print(df)

            plot_title = "{} {} {} {}".format(row, today, last_close_price, scenario)

    data['Pct Change'] = data['Close'].pct_change()
    data['Trend'] = 0
    Trend = 0
    for i in range(1, len(data)):
        if data['Close'][i] > data['Close'][i - 1]:
            if Trend == -1:
                data['Trend'][i - 1] = -1
                Trend = 0
            else:
                Trend = 1
        elif data['Close'][i] < data['Close'][i - 1]:
            if Trend == 1:
                data['Trend'][i - 1] = 1
                Trend = 0
            else:
                Trend = -1

    data['Consolidation'] = 0
    Consolidation = 0
    for i in range(1, len(data)):
        if data['Trend'][i] == 0:
            Consolidation += 1
            if Consolidation >= 5:
                data['Consolidation'][i] = 1
        else:
            Consolidation = 0

    cons_data = data[data['Consolidation'] == 1]
    cons_data = cons_data[cons_data['Volume'] < cons_data['Volume'].shift()]

    for i in range(1, len(cons_data)):
        if data['Close'][cons_data.index[i]] > data['Close'][cons_data.index[i - 1]]:
            if data['Volume'][cons_data.index[i]] > data['Volume'][cons_data.index[i - 1]]:
                print("VCP pattern found!")
                plotly_chart(data, plot_title, 0, jpg_resolution)
                lineNotifyImage(token, "Meet VCP Criteria", str(true_number) + ".jpg")


start = 0
true_number = 0
run_number = 0
today = str(datetime.datetime.now().date())


# start += 1


# unique_tickers = list(set(un_unique_tickers))
# for ticker in unique_tickers[start:]:
#    process_data(ticker)
#    run_number += 1
def detect_vcp_20230304(ticker_in, data):
    lineNotifyMessage(token, "Start VCP: " + today + " ")
    data['AvgVol'] = data['Volume'].rolling(55).mean()  # 55為平均的天數
    last_close_price = round(data["Close"][-1], 2)

    plot_title = "{} {} {} {}".format(ticker_in, today, last_close_price, scenario)

    data['Pct Change'] = data['Close'].pct_change()
    data['Trend'] = 0
    Trend = 0
    for i in range(1, len(data)):
        if data['Close'][i] > data['Close'][i - 1]:
            if Trend == -1:
                data['Trend'][i - 1] = -1
                Trend = 0
            else:
                Trend = 1
        elif data['Close'][i] < data['Close'][i - 1]:
            if Trend == 1:
                data['Trend'][i - 1] = 1
                Trend = 0
            else:
                Trend = -1

    data['Consolidation'] = 0
    Consolidation = 0
    for i in range(1, len(data)):
        if data['Trend'][i] == 0:
            Consolidation += 1
            if Consolidation >= 5:
                data['Consolidation'][i] = 1
        else:
            Consolidation = 0

    cons_data = data[data['Consolidation'] == 1]
    cons_data = cons_data[cons_data['Volume'] < cons_data['Volume'].shift()]

    for i in range(1, len(cons_data)):
        if data['Close'][cons_data.index[i]] > data['Close'][cons_data.index[i - 1]]:
            if data['Volume'][cons_data.index[i]] > data['Volume'][cons_data.index[i - 1]]:
                print("VCP pattern found!")
                plotly_chart(data, plot_title, 0, jpg_resolution)
                lineNotifyImage(token, "Meet VCP Criteria", str(true_number) + ".jpg")


def gogogo_20230304(tickers_in, df, true_number, category):
    global scenario
    df['AvgVol'] = df['Volume'].rolling(55).mean()  # 55為平均的天數
    last_close_price = round(df["Close"][-1], 2)

    plot_title = "{} {} {} {}".format(tickers_in, today, last_close_price, scenario)
    # plot_tile = (row + today + last_close_price)
    volatility_H = df['High'].max() / df['Close'].mean()
    volatility_L = df['Low'].min() / df['Close'].mean()
    volatility = volatility_H - volatility_L
    # print (str(len(df.index)) + " " + str(volatility_H) + " " + str(volatility_L) + " " + str(volatility))
    if (len(df.index) > 144 and volatility > 0.1):  # 過濾資料筆數少於144筆的股票，確保上市時間有半年並且判斷半年內的波動率，像死魚一樣不動的股票就不分析
        # print ("meet volume or volatility, start analysis!")
        # run_number += 1
        # print (df.head())
        # print (df.tail())
        # period = "ytd"
        # print (df.shape[0])
        # df['VWPrice'] = df['Close'] * df['Volume']
        # vwap = pd.DataFrame()

        # vwap['vwap233'] = df['VWPrice'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
        # vwap['vwap144'] = df['VWPrice'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
        # vwap['vwap89'] = df['VWPrice'].rolling(window=89).sum() / df['Volume'].rolling(window=89).sum()
        # vwap['vwap55'] = df['VWPrice'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
        # vwap['vwap21'] = df['VWPrice'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
        # vwap['vwap5'] = df['VWPrice'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

        if (ForcePLOT == 1):
            # year = df[-200:]

            # plotly_chart(df, row, true_number)
            url = f'https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{tickers_in}'
            linemessage = (
                f"{true_number} - url - ")
            # f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - {info_sector}")
            # lineNotifyImage(token, linemessage, str(true_number) + ".jpg")
            highchart_chart(df, tickers_in, today, url)
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

            info_sector = ""

            # plotly_chart(df, tickers_in, true_number)
            # plotly_chart(df, plot_title, true_number, jpg_resolution)
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
            # open_web(url)
            # lineNotifyImage(token,str(start) + " - " + row+" - " + info_sector,str(true_number)+".jpg")
            # if not OnlyPLOT:
            #    lineNotifyImage(token, linemessage, str(true_number) + ".jpg")

        print("gogogo Finished")
    else:
        print("Volume or volatility not meet, skip analysis!")
    # lineNotifyMessage(token, "Finished: " + today + " " + category + "\nScanned " + str(run_number) + " of " + str(
    #    start) + " Stocks in " + category + " Market\n" + str(true_number) + " Meet Criteria")


def remove_ptp_list(ptp_tickers, tickers):
    us_non_ptp_tickers = [x for x in tickers if x not in ptp_tickers]
    us_ptp_tickers = [x for x in tickers if x in ptp_tickers]
    print("PTP US stocks:", us_ptp_tickers)
    print("Non-PTP US stocks:", us_non_ptp_tickers)
    return us_non_ptp_tickers


def get_data(ticker_in):
    try:
        data_org = yf.download(ticker_in, period="3y", progress=False)
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
        # print(data_org)
    except Exception as e:
        lineNotifyMessage(token, f"{ticker_in} download failed: {str(e)}")
        data_org = pd.DataFrame()  # 返回一個空的數據帧
        print("Get Data Fail")
    return data_org


def vwap_and_volume_screener(tickers_in, df, true_number, category, day, volume_factor):
    # Check if the dataframe is empty
    if df.empty:
        return

    # Calculate rolling averages and other computations
    df['AvgVol'] = df['Volume'].rolling(day).mean()
    df['VWPrice'] = df['Close'] * df['Volume']
    df['VWPrice_day'] = df['VWPrice'].rolling(day).mean()

    # Calculate vwap and use NaN to avoid divide by zero error
    # df['vwap144'] = df['VWPrice'].rolling(window=144).sum() / df['Volume'].replace(0, np.nan).rolling(
    #    window=144).sum()

    if len(df) < 2:
        print("Error: The DataFrame must have at least two rows.")
    else:
        # Get the last data points
        last_turnover_data = df['VWPrice_day'].tail(1).iloc[0] * volume_factor
        last_vwap144_data = df['vwap144'].tail(1).iloc[0]
        last_close_price = df["Close"].iloc[-1]
        last2_close_price = df["Close"].iloc[-2]
        change_percentage = ((last_close_price / last2_close_price) - 1) * 100
        change_percentage = round(change_percentage, 2)
        # print(df["Close"])
        # print(f'last_close_price:{last_close_price}')
        # rint(f'last2_close_price:{last2_close_price}')
        # Calculate change percentage
        # change_percentage = ((last_close_price / last2_close_price) - 1) * 100
        # print(f'change_percentage:{change_percentage}')

        # Check if the conditions are met for analysis
        if last_turnover_data > 100000 and last_close_price > last_vwap144_data:
            # Calculate vwap
            df[f'vwap{day}'] = df['VWPrice'].rolling(window=day).sum() / df['Volume'].rolling(window=day).sum()

            # Get the last data points
            # last_vwap = df[f'vwap{day}'].iloc[-1]
            # second_last_vwap = df[f'vwap{day}'].iloc[-2]
            last_volume = df['Volume'].iloc[-1] * volume_factor
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

                # plotly_chart(df, plot_title, true_number, jpg_resolution)
                highchart_chart(df, tickers_in, today, url)
                # lineNotifyImage(token, line_message, str(true_number) + ".jpg")


def my_vcp_screener(ticker_in, data):
    volatility_5 = calculate_volatility(data, 5)
    volatility_13 = calculate_volatility(data, 13)
    volatility_21 = calculate_volatility(data, 21)
    volatility_34 = calculate_volatility(data, 34)
    avg_volume_5 = calculate_avg_volume(data, 5)
    avg_volume_13 = calculate_avg_volume(data, 13)
    avg_volume_21 = calculate_avg_volume(data, 21)
    avg_volume_34 = calculate_avg_volume(data, 34)
    if volatility_5 < 0.03 < volatility_13 < volatility_21 < volatility_34 and avg_volume_5 < avg_volume_13 < avg_volume_21 < avg_volume_34:
        url = (f"https://www.tradingview.com/chart/sWFIrRUP/?symbol={ticker_in}")
        #webbrowser.open(url)
        highchart_chart(data, ticker_in, today, url)
        # print(ticker_in, url)


"""def my_vcp_screener(ticker_in, data):
    volatility_5 = calculate_volatility(data, 5)
    volatility_13 = calculate_volatility(data, 13)
    volatility_21 = calculate_volatility(data, 21)
    volatility_55 = calculate_volatility(data, 55)
    if volatility_5 < volatility_13 < volatility_21 < volatility_55:
        url = (f"https://www.tradingview.com/chart/sWFIrRUP/?symbol={ticker_in}")
        print(ticker_in, url)
"""


def calculate_avg_volume(df, n_days):
    hist = df.tail(n_days)
    avg_volume = hist['Volume'].mean()
    return avg_volume


def calculate_volatility(df, n_days):
    # 選擇最後n_days天的數據
    hist = df.tail(n_days)

    # 計算最高價格/平均價格和最低價格/平均價格
    avg_close_price = hist['Close'].mean()
    max_close_price = hist['Close'].max()
    min_close_price = hist['Close'].min()
    volatility_h = max_close_price / avg_close_price - 1
    volatility_l = avg_close_price / min_close_price - 1
    # print(f"Volativity High: {n_days} days {volatility_h}")
    # print(f"Volativity Low:  {n_days} days {volatility_l}")
    volatility = volatility_h + volatility_l
    # print(f"Volativity: {n_days} days {volatility}")

    return volatility


def party(ticker_type, tickers_in, start):
    run_number = start
    lineNotifyMessage(token, "Start: " + str(today) + " " + str(ticker_type))
    # print ("US LOOP")
    new_tickers = remove_ptp_list(ptp_lists, tickers_in)
    # new_tickers = remove_ptp_list(ptp_lists, test_tickers)
    # print (new_tickers)
    for ticker in new_tickers[start:]:
        print(ticker_type, run_number, " ", ticker)
        data = get_data(ticker)
        # print (data)
        run_number += 1
        # print ("before gogogo")
        # print (ticker)
        if (gogogo_run == 1):
            gogogo_20230304(ticker, data, run_number, ticker_type)
        if (VCP == 1):
            # detect_vcp_20230304(ticker, data)
            print("Running VCP")
            my_vcp_screener(ticker, data)
        if (VWAP_SCREENER == 1):
            vwap_and_volume_screener(ticker, data, run_number, ticker_type, screener_day, vol_factor)


# VWAP Scenario
scenario = 55  # 21, 55, 89, 144, 233共5種

# Volume Factor
vol_factor = 1  # voluume factor for VWAP_SCREENER

# 設定要執行的種類
VCP = 0
VCP_TEST = 0
VWAP_SCREENER = 0
gogogo_run = 1

# 強制寫出plotly，主要用來測試
ForcePLOT = 0
OnlyPLOT = False  # True / False

# Test Tickers
test_tickers = ['1456.TW', '1432.TW']

# 要執行的ticker種類
TEST = 0
US = 1
TW = 0
ETF = 0
FIN = 0  # Filter tickers from finviz screener

# plotly的圖檔大小
plotly_resolution = "high"

if plotly_resolution == "high":
    jpg_resolution = 1080
else:
    jpg_resolution = 800

# screener要判斷的平均天數
screener_day = 8

# 若程式執行至一半中斷，可以設定重新執行的位置
vcp_start = 0
test_start = 0
us_start = 4394
tw_start = 0
etf_start = 0
fin_start = 0

ptp = 0

url1 = "https://help.zh-tw.firstrade.com/article/841-new-1446-f-regulations"
url2 = 'https://www.itigerup.com/bulletin/ptp'
ptp_lists = get_ptp_tickers(url1, url2)

vcp_test_tickers = ['AAPL', 'ICPT']
test_tickers = ['UFPT', 'IPVF', 'SCU', 'ICD']

# 將讀取到的資料轉換為 list，並存入 tw_tickers 變數中
if TW == 1:
    df_tw = pd.read_excel("Tickers.xlsx", sheet_name="TW", usecols=[0])
    tw_tickers = df_tw.iloc[:, 0].tolist()
    tw_tickers_length = len(tw_tickers)
    print("Total TW Tickers:", tw_tickers_length)
if US == 1:
    df_us = pd.read_excel("Tickers.xlsx", sheet_name="US", usecols=[0])
    us_tickers = df_us.iloc[:, 0].tolist()
    us_tickers_length = len(us_tickers)
    print("Total US Tickers:", us_tickers_length)
if ETF == 1:
    df_etf = pd.read_excel("Tickers.xlsx", sheet_name="ETF", usecols=[0])
    etf_tickers = df_etf.iloc[:, 0].tolist()
    etf_tickers_length = len(etf_tickers)
    print("Total ETF Tickers:", etf_tickers_length)
if FIN == 1:
    fin_tickers = get_finviz_screener_tickers()
    fin_tickers_length = len(fin_tickers)
    print("Total FIN Tickers:", fin_tickers_length)
    print(fin_tickers)

#############################################################################


if TEST == 1:
    party("TEST", test_tickers, test_start)
if US == 1:
    party("US", us_tickers, us_start)
if TW == 1:
    party("TW", tw_tickers, tw_start)
if ETF == 1:
    party("ETF", etf_tickers, etf_start)
if FIN == 1:
    # remove_list = ['BREZR','DAVEW','DWACW']
    # for item in remove_list:
    #    fin_tickers.remove(item)
    # print(fin_tickers)
    party("FIN", fin_tickers, fin_start)