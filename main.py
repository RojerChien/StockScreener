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
from IPython.display import HTML,display
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

def highchart_chart(dfin, plot_title):
    # 初始化Highstock对象
    chart = Highstock(renderTo='container', width=1600, height=600)  # 添加宽度和高度

    # 添加蜡烛图序列
    ohlc = dfin[['Open', 'High', 'Low', 'Close']].values.tolist()
    ohlc = [[int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), round(o, 2), round(h, 2), round(l, 2), round(c, 2)] for
            i, (o, h, l, c) in enumerate(ohlc)]

    chart.add_data_set(ohlc, 'candlestick', 'TSLA', dataGrouping={'units': [['day', [1]]]})

    # 添加成交量序列
    volume = dfin[['Open', 'Close', 'Volume']].values.tolist()
    volume = [{'x': int(pd.Timestamp(dfin.index[i]).value // 10 ** 6), 'y': v, 'color': 'green' if o > c else 'red'} for
              i, (o, c, v) in enumerate(volume)]

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
    chart.save_file('candlestick_volume')
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

    # add VCMA to df
    df['total_price'] = df['Close'] * df['Volume']
    # df.loc[df['total_price']] = df['Close'] * df['Volume']

    windows = [233, 144, 55, 21, 5]
    for w in windows:
        rolling_total_price = df['total_price'].rolling(window=w).sum()
        rolling_volume = df['Volume'].rolling(window=w).sum()
        df[f'vcma{w}'] = rolling_total_price / rolling_volume
    # df['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
    # df['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
    # df['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
    # df['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
    # df['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

    # add moving average traces
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma5'],
                             opacity=0.7,
                             line=dict(color='blue', width=2),
                             name='VCMA 5'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma21'],
                             opacity=0.7,
                             line=dict(color='green', width=2),
                             name='VCMA 21'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma55'],
                             opacity=0.7,
                             line=dict(color='red', width=2),
                             name='VCMA 55'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma144'],
                             opacity=0.7,
                             line=dict(color='magenta', width=2),
                             name='VCMA 144'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma233'],
                             opacity=0.7,
                             line=dict(color='goldenrod', width=2),
                             name='VCMA 233'))

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


def VCMA_history(vcma_values):
    pattern = np.array([False] * 20 + [True])
    return np.array_equal(vcma_values[-21:-1], pattern[:-1]) and vcma_values[-1] == pattern[-1]


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
        df['total_price'] = df['Close'] * df['Volume']
        vcma = pd.DataFrame()

        vcma['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
        vcma['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
        vcma['vcma89'] = df['total_price'].rolling(window=89).sum() / df['Volume'].rolling(window=89).sum()
        vcma['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
        vcma['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
        vcma['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

        if (ForcePLOT == 1):
            # year = df[-200:]
            plotly_chart(df, plot_title, true_number, jpg_resolution)
            # plotly_chart(df, row, true_number)
            url = f'https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{tickers_in}'
            linemessage = (
                f"{true_number} - url - ")
            # f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - {info_sector}")
            lineNotifyImage(token, linemessage, str(true_number) + ".jpg")
            if not OnlyPLOT:
                webbrowser.open(url)
        vcma['VCMA21_Result'] = (vcma['vcma5'] > vcma['vcma21'])
        vcma['VCMA55_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55'])
        vcma['VCMA89_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
                vcma['vcma55'] > vcma['vcma89'])
        vcma['VCMA144_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
                vcma['vcma55'] > vcma['vcma89']) & (vcma['vcma89'] > vcma['vcma144'])
        vcma['VCMA233_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
                vcma['vcma55'] > vcma['vcma89']) & (vcma['vcma89'] > vcma['vcma144']) & (
                                         vcma['vcma144'] > vcma['vcma233'])

        VCMA5_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2])
        VCMA21_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2])
        VCMA55_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                             vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2])
        VCMA89_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                             vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2]) and (
                             vcma['vcma89'].iloc[-1] > vcma['vcma89'].iloc[-2])
        VCMA144_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                              vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2]) and (
                              vcma['vcma89'].iloc[-1] > vcma['vcma89'].iloc[-2]) and (
                              vcma['vcma144'].iloc[-1] > vcma['vcma144'].iloc[-2])
        VCMA233_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                              vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2]) and (
                              vcma['vcma89'].iloc[-1] > vcma['vcma89'].iloc[-2]) and (
                              vcma['vcma144'].iloc[-1] > vcma['vcma144'].iloc[-2]) and (
                              vcma['vcma233'].iloc[-1] > vcma['vcma233'].iloc[-2])

        vcma_values_233 = vcma['VCMA233_Result'].values
        pattern_233 = np.array([False] * 20 + [True])
        VCMA233_history = np.array_equal(vcma_values_233[-21:-1], pattern_233[:-1]) and vcma_values_233[-1] == \
                          pattern_233[-1]

        vcma_values_144 = vcma['VCMA144_Result'].values
        pattern_144 = np.array([False] * 20 + [True])
        VCMA144_history = np.array_equal(vcma_values_144[-21:-1], pattern_144[:-1]) and vcma_values_144[-1] == \
                          pattern_144[-1]

        vcma_values_89 = vcma['VCMA89_Result'].values
        pattern_89 = np.array([False] * 20 + [True])
        VCMA89_history = np.array_equal(vcma_values_89[-21:-1], pattern_89[:-1]) and vcma_values_89[-1] == pattern_89[
            -1]

        vcma_values_55 = vcma['VCMA55_Result'].values
        pattern_55 = np.array([False] * 20 + [True])
        VCMA55_history = np.array_equal(vcma_values_55[-21:-1], pattern_55[:-1]) and vcma_values_55[-1] == pattern_55[
            -1]
        vcma_values_21 = vcma['VCMA21_Result'].values
        pattern_21 = np.array([False] * 20 + [True])
        VCMA21_history = np.array_equal(vcma_values_21[-21:-1], pattern_21[:-1]) and vcma_values_21[-1] == pattern_21[
            -1]
        FinalResult = "FALSE"
        scenario = 55

        if (scenario == 55) and (VCMA55_history == True) and (VCMA55_inc == True):
            FinalResult = "TRUE"
        elif (scenario == 21) and (VCMA21_history == True) and (VCMA21_inc == True):
            FinalResult = "TRUE"
        elif (scenario == 89) and (VCMA89_history == True) and (VCMA89_inc == True):
            FinalResult = "TRUE"
        elif (scenario == 144) and (VCMA144_history == True) and (VCMA144_inc == True):
            FinalResult = "TRUE"
        elif (scenario == 233) and (VCMA233_history == True) and (VCMA233_inc == True):
            FinalResult = "TRUE"
        else:
            # print ("No Scenario")
            return 1
        # print(FinalResult)
        if (FinalResult == 'TRUE'):

            info_sector = ""

            # plotly_chart(df, tickers_in, true_number)
            plotly_chart(df, plot_title, true_number, jpg_resolution)
            if (category != "TW"):
                linemessage = (
                    f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={tickers_in}")
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + tickers_in)
                if not OnlyPLOT:
                    webbrowser.open(url)

            else:
                if (tickers_in[-1] == "W"):
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2}")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
                    if not OnlyPLOT:
                        webbrowser.open(url)

                else:
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2}")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
                    if not OnlyPLOT:
                        webbrowser.open(url)

            # open_web(url)
            # lineNotifyImage(token,str(start) + " - " + row+" - " + info_sector,str(true_number)+".jpg")
            if not OnlyPLOT:
                lineNotifyImage(token, linemessage, str(true_number) + ".jpg")

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
        data_org = yf.download(ticker_in, period="2y", progress=False)
    except Exception as e:
        lineNotifyMessage(token, f"{ticker_in} download failed: {str(e)}")
        data_org = pd.DataFrame()  # 返回一個空的數據帧
        print("Get Data Fail")
    return data_org


def vcma_and_volume_screener(tickers_in, df, true_number, category, day, volume_factor):
    # Check if the dataframe is empty
    if df.empty:
        return

    # Calculate rolling averages and other computations
    df['AvgVol'] = df['Volume'].rolling(day).mean()
    df['total_price'] = df['Close'] * df['Volume']
    df['total_price_day'] = df['total_price'].rolling(day).mean()

    # Calculate vcma and use NaN to avoid divide by zero error
    df['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].replace(0, np.nan).rolling(
        window=144).sum()


    if len(df) < 2:
        print("Error: The DataFrame must have at least two rows.")
    else:
        # Get the last data points
        last_turnover_data = df['total_price_day'].tail(1).iloc[0] * volume_factor
        last_vcma144_data = df['vcma144'].tail(1).iloc[0]
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
        if last_turnover_data > 100000 and last_close_price > last_vcma144_data:
            # Calculate vcma
            df[f'vcma{day}'] = df['total_price'].rolling(window=day).sum() / df['Volume'].rolling(window=day).sum()

            # Get the last data points
            # last_vcma = df[f'vcma{day}'].iloc[-1]
            # second_last_vcma = df[f'vcma{day}'].iloc[-2]
            last_volume = df['Volume'].iloc[-1] * volume_factor
            second_last_avg_volume = df['AvgVol'].iloc[-1]

            # Check if price and volume conditions are met based on the category
            if (category != "TW"):
                is_meet_price_and_volume = last2_close_price * 1.06 > last_close_price > last2_close_price * 1.02 and last_volume > second_last_avg_volume * 1.5
            else:
                is_meet_price_and_volume = last2_close_price * 1.09 > last_close_price > last2_close_price * 1.02 and last_volume > second_last_avg_volume * 1.5

            # 如果最後一天的vcma大於最後第二天的vcma的1.03倍，並且最後一天的成交量大於5天平均成交量的最後一天的2倍，則畫圖並傳送Line通知
            if is_meet_price_and_volume:
                plot_title = f"{tickers_in} {today} {day} {change_percentage}% screener"
                if category != "TW":
                    line_message = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={tickers_in} - screener")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + tickers_in)
                    if not OnlyPLOT:
                        webbrowser.open(url)

                else:
                    if (tickers_in[-1] == "W"):
                        row2 = tickers_in[:4]
                        line_message = (
                            f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - screener")
                        url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
                        if not OnlyPLOT:
                            webbrowser.open(url)

                    else:
                        row2 = tickers_in[:4]
                        line_message = (
                            f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2} - screener")
                        url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
                        if not OnlyPLOT:
                            webbrowser.open(url)

                # plotly_chart(df, plot_title, true_number, jpg_resolution)
                highchart_chart(df, plot_title)
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
        webbrowser.open(url)
        #print(ticker_in, url)

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
    print(f"Volativity High: {n_days} days {volatility_h}")
    print(f"Volativity Low:  {n_days} days {volatility_l}")
    volatility = volatility_h + volatility_l
    print(f"Volativity: {n_days} days {volatility}")

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
        if (VCMA_SCREENER == 1):
            vcma_and_volume_screener(ticker, data, run_number, ticker_type, screener_day, vol_factor)


# VCMA Scenario
scenario = 55  # 21, 55, 89, 144, 233共5種

# Volume Factor
vol_factor = 10  # voluume factor for VCMA_SCREENER

# 設定要執行的種類
VCP = 0
VCP_TEST = 0
VCMA_SCREENER = 1
gogogo_run = 0

# 強制寫出plotly，主要用來測試
ForcePLOT = 0
OnlyPLOT = False  # True / False

# Test Tickers
test_tickers = ['1456.TW', '1432.TW']

# 要執行的ticker種類
TEST = 0
US = 0
TW = 0
ETF = 0
FIN = 1  # Filter tickers from finviz screener

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
us_start = 0
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
