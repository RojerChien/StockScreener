import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from scipy import signal
import mplfinance as mpf

def filter(values, percentage):
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

ticker = "TSLA"
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

data = yf.download(ticker, start=start_date, end=end_date)
data_low = data['Low']
data_high = data['High']

peak_indexes = signal.argrelextrema(data_high.values, np.greater)[0]
valley_indexes = signal.argrelextrema(data_low.values, np.less)[0]

df_peaks = pd.DataFrame({'date': data_high.index[peak_indexes], 'zigzag_y': data_high.iloc[peak_indexes]})
df_valleys = pd.DataFrame({'date': data_low.index[valley_indexes], 'zigzag_y': data_low.iloc[valley_indexes]})
df_peaks_valleys = pd.concat([df_peaks, df_valleys], axis=0, ignore_index=True, sort=True).sort_values(by=['date'])

p = 0.20
filter_mask = filter(df_peaks_valleys.zigzag_y, p)
filtered = df_peaks_valleys[filter_mask]

# Create an empty series with the same index as the data dataframe
zigzag_series = pd.Series(index=data.index, dtype=float)

# Set the values of the zigzag series based on the filtered dataframe
for idx, row in filtered.iterrows():
    zigzag_series.at[row.date] = row.zigzag_y

# Fill the gaps with NaN values
zigzag_series = zigzag_series.interpolate(method='index', limit_area='inside')

apdict = mpf.make_addplot(zigzag_series, panel=0, secondary_y=True, color='blue', linestyle='-', marker='o', markersize=5)
mpf.plot(data, type='candle', style='yahoo', figsize=(10, 10), title='TSLA K線圖與ZigZag趨勢線', ylabel='價格', addplot=apdict)
