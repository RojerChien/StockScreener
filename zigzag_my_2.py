from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta

def filter(values, percentage):
    # the first value is always valid
    previous = values[0]
    mask = [True]
    # evaluate all points from the second to (n-1)th
    for value in values[1:-1]:
        relative_difference = np.abs(value - previous)/previous
        if relative_difference > percentage:
            previous = value
            mask.append(True)
        else:
            mask.append(False)
    # the last value is always valid
    mask.append(True)
    return mask

ticker = "TSLA"
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

data = yf.download(ticker, start=start_date, end=end_date)
data_low = data['Low']
data_high = data['High']

# Find peaks(max).
peak_indexes = signal.argrelextrema(data_high.values, np.greater)
peak_indexes = peak_indexes[0]
# Find valleys(min).
valley_indexes = signal.argrelextrema(data_low.values, np.less)
valley_indexes = valley_indexes[0]
# Merge peaks and valleys data points using pandas.
df_peaks = pd.DataFrame({'date': data_high.index[peak_indexes], 'zigzag_y': data_high[peak_indexes]})
df_valleys = pd.DataFrame({'date': data_low.index[valley_indexes], 'zigzag_y': data_low[valley_indexes]})
df_peaks_valleys = pd.concat([df_peaks, df_valleys], axis=0, ignore_index=True, sort=True)
# Sort peak and valley datapoints by date.
df_peaks_valleys = df_peaks_valleys.sort_values(by=['date'])

p = 0.20 # 20%
filter_mask = filter(df_peaks_valleys.zigzag_y, p)
filtered = df_peaks_valleys[filter_mask]
print(filtered)

 # Instantiate axes.
(fig, ax) = plt.subplots(figsize=(10,10))
# Plot zigzag trendline.
# ax.plot(df_peaks_valleys['date'].values, df_peaks_valleys['zigzag_y'].values,
                                                        # color='red', label="Extrema")
# Plot zigzag trendline.
ax.plot(filtered['date'].values, filtered['zigzag_y'].values,
                                                        color='blue', label="ZigZag")

# Plot original line.
# ax.plot(data_low.index, data_low, linestyle='dashed', color='black', label="Org. line", linewidth=1)
# ax.plot(data_high.index, data_high, linestyle='dashed', color='black', label="Org. line", linewidth=1)

# Format time.
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

plt.gcf().autofmt_xdate()   # Beautify the x-labels
plt.autoscale(tight=True)

plt.legend(loc='best')
plt.grid(True, linestyle='dashed')
plt.show()