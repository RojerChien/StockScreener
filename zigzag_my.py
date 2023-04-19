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

def filter(values, percentage):
    filtered_values = []
    filtered_values.append(values.iloc[0])
    for value in values.iloc[1:]:
        relative_difference = np.abs(value - filtered_values[-1]) / filtered_values[-1]
        if relative_difference > percentage:
            filtered_values.append(value)
    return pd.Series(filtered_values, index=values.index[values.isin(filtered_values)])


ticker = "TSLA"
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

data = yf.download(ticker, start=start_date, end=end_date)
data_low = data['Low']
data_high = data['High']

peak_indexes = signal.argrelextrema(data_high.values, np.greater)[0]
valley_indexes = signal.argrelextrema(data_low.values, np.less)[0]

df_peaks = pd.DataFrame({'date': data_high.index[peak_indexes], 'price': data_high.iloc[peak_indexes]})
df_valleys = pd.DataFrame({'date': data_low.index[valley_indexes], 'price': data_low.iloc[valley_indexes]})
df_peaks_valleys = pd.concat([df_peaks, df_valleys], axis=0, ignore_index=True, sort=True).sort_values(by=['date'])

p = 0.10
filtered_prices = filter(df_peaks_valleys.price, p)
zigzag = df_peaks_valleys[df_peaks_valleys.price.isin(filtered_prices)]

# 確保你的dataframe已經被正確設置為datetime index
data.index = pd.to_datetime(data.index)
zigzag = zigzag.set_index('date')
print(zigzag)


# 繪制K線圖
mpf.plot(data, type='candle', style='yahoo', title='Zigzag K', ylabel='Price', figratio=(12, 6))

# 繪製zigzag直線
fig, ax = plt.subplots(figsize=(12, 6))
for i in range(len(zigzag) - 1):
    start_date = zigzag.index[i]
    end_date = zigzag.index[i + 1]
    start_price = zigzag.loc[start_date, 'price']
    end_price = zigzag.loc[end_date, 'price']

    if start_date in data.index and end_date in data.index:
        ax.plot([start_date, end_date], [start_price, end_price], marker='o', linestyle='-',)

ax.set_title('Filter Data')
ax.set_ylabel('Price')
ax.set_xlabel('Data')
plt.xticks(rotation=45)
plt.show()
