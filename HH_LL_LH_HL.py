import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker

def zigzag(data, percent_change):
    zz_points = [data.index[0]]
    zz_values = [data["Close"][0]]
    up_trend = True
    last_pivot = data["Close"][0]

    for i in range(1, len(data)):
        current_price = data["Close"][i]

        if up_trend:
            change = (current_price - last_pivot) / last_pivot
            if change >= percent_change:
                zz_points.append(data.index[i])
                zz_values.append(current_price)
                last_pivot = current_price
                up_trend = False
            elif change <= -percent_change:
                up_trend = False
        else:
            change = (current_price - last_pivot) / last_pivot
            if change <= -percent_change:
                zz_points.append(data.index[i])
                zz_values.append(current_price)
                last_pivot = current_price
                up_trend = True
            elif change >= percent_change:
                up_trend = True

    return pd.DataFrame(zz_values, index=zz_points, columns=["Close"])

symbol = "TSLA"
start_date = "2020-01-01"
end_date = "2021-01-01"
data = yf.download(symbol, start=start_date, end=end_date)
data.index = pd.to_datetime(data.index)

zigzag_data = zigzag(data, 0.1)
filtered_zigzag = zigzag_data.reset_index()

ap = mpf.make_addplot(filtered_zigzag, type="scatter", markersize=100, marker="^", color="r")

fig, axlist = mpf.plot(data, type="candle", volume=True, title="Tesla (TSLA) K線圖 with Zigzag", style="yahoo", addplot=ap, returnfig=True)
mpf.show()
