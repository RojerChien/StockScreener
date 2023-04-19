import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from scipy import signal
import matplotlib.pyplot as plt
import mplfinance as mpf


def filter_org(values, percentage):
    previous = values.iloc[0]
    mask = [True]
    for value in values.iloc[1:-1]:
        relative_difference = np.abs(value - previous) / previous
        if relative_difference > percentage:
            previous = value
            mask.append(True)
        else:
            mask.append(False)
    mask.append(True)
    return mask

def calculate_atr(data, atr_period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())

    true_range = pd.DataFrame({'hl': high_low, 'hc': high_close, 'lc': low_close}).max(axis=1)
    atr = true_range.rolling(window=atr_period).mean()

    return atr


def filter(values, percentage):
    filtered_values = []
    filtered_values.append(values.iloc[0])
    for value in values.iloc[1:]:
        relative_difference = np.abs(value - filtered_values[-1]) / filtered_values[-1]
        if relative_difference > percentage:
            filtered_values.append(value)
    return pd.Series(filtered_values, index=values.index[values.isin(filtered_values)])


ticker = "AAPL"
end_date = datetime.today()
start_date = end_date - timedelta(days=700)

data = yf.download(ticker, start=start_date, end=end_date)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(data)
data_low = data['Low']
data_high = data['High']

atr = calculate_atr(data)

atr_multiplier = 2.5  # 調整這個常數因子以獲得所需的波峰和波谷精度
window_size = int(np.ceil(atr.mean() * atr_multiplier))
print(f"window_size: {window_size}")

# window_size = 15  # 調整窗口大小以獲得所需的波峰和波谷精度
p = 0.08
# 找到波峰
data_high_rolling_max = data['High'].rolling(window=window_size, center=True).max()
peak_indexes = (data_high == data_high_rolling_max)

# 找到波谷
data_low_rolling_min = data['Low'].rolling(window=window_size, center=True).min()
valley_indexes = (data_low == data_low_rolling_min)

df_peaks = pd.DataFrame({'date': data_high.index[peak_indexes], 'price': data_high[peak_indexes]})
df_valleys = pd.DataFrame({'date': data_low.index[valley_indexes], 'price': data_low[valley_indexes]})
df_peaks_valleys = pd.concat([df_peaks, df_valleys], axis=0, ignore_index=True, sort=True).sort_values(by=['date'])




def filter_and_order(values, percentage):
    filtered_values = [values.iloc[0]]
    for i in range(1, len(values)):
        relative_difference = np.abs(values.iloc[i].price - filtered_values[-1].price) / filtered_values[-1].price
        if relative_difference > percentage:
            # 確保波峰接著波谷，或波谷接著波峰
            if len(filtered_values) >= 2 and (values.iloc[i].price > filtered_values[-1].price) == (
                    filtered_values[-1].price > filtered_values[-2].price):
                del filtered_values[-1]
            filtered_values.append(values.iloc[i])
    return filtered_values


df_peaks_valleys_ordered = filter_and_order(df_peaks_valleys, p)
filtered_prices = pd.Series([x.price for x in df_peaks_valleys_ordered],
                            index=[x.date for x in df_peaks_valleys_ordered])
zigzag = pd.DataFrame(filtered_prices, columns=['price'])

# 確保你的dataframe已經被正確設置為datetime index
data.index = pd.to_datetime(data.index)
zigzag.index = pd.to_datetime(zigzag.index)
print(zigzag)

zigzag_line = []
line = []
direction = None

for i in range(1, len(zigzag)):
    if not line:
        line.append((zigzag.index[0].strftime('%Y-%m-%d'), zigzag.iloc[0]['price']))
    if ((zigzag.iloc[i]['price'] > zigzag.iloc[i - 1]['price'] and not direction) or
            (zigzag.iloc[i]['price'] < zigzag.iloc[i - 1]['price'] and direction)):
        line.append((zigzag.index[i - 1].strftime('%Y-%m-%d'), zigzag.iloc[i - 1]['price']))
        zigzag_line.append(line)
        line = [(zigzag.index[i - 1].strftime('%Y-%m-%d'), zigzag.iloc[i - 1]['price']),
                (zigzag.index[i].strftime('%Y-%m-%d'), zigzag.iloc[i]['price'])]
        direction = not direction
if line:
    line.append((zigzag.index[-1].strftime('%Y-%m-%d'), zigzag.iloc[-1]['price']))
    zigzag_line.append(line)

# 印出 zigzag_line 列表
print(zigzag_line)

# 設定 zigzag 線的顏色
colors = ['r' if i % 2 == 0 else 'g' for i in range(sum(len(seg) for seg in zigzag_line))]

# 繪製 K 線圖並加入 zigzag 線
mpf.plot(data, type='candle', alines=dict(alines=zigzag_line, colors=colors))
