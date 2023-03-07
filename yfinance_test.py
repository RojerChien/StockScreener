import yfinance as yf
import pandas as pd
import numpy as np

# 下載 S&P 500 的 15 分鐘線數據
symbol = "^GSPC"
start_date = "2022-01-01"
end_date = "2022-12-31"
interval = "15m"
data = yf.download(symbol, period="60d", interval=interval)
print(data)
# 計算每個15分鐘時間間隔的一年累計成交量
# 計算每個時間區間的15分鐘線數據
data["15min_interval"] = pd.to_datetime(data.index).strftime("%H:%M")
data["15min_interval"] = data["15min_interval"].apply(lambda x: pd.to_datetime(x).strftime("%M")).astype(int) // 15
data["year"] = pd.to_datetime(data.index).year

# 定義副程式
def calc_cumulative_volume(data, start_time, end_time):
    """
    計算一段時間內每15分鐘的一年累計成交量
    """
    data_period = data.between_time(start_time, end_time)
    data_period_15min = data_period.groupby(["year", "15min_interval"]).first()
    data_period_15min["cumulative_volume_15min"] = data_period_15min["Volume"].cumsum()
    return data_period_15min

# 計算每個時間區間的一年累計成交量
cumulative_volume_15min_list = []
for i in range(0, 17):
    start_time = "{:02d}:{}".format(9 + i // 4, str((i % 4) * 15).zfill(2))
    end_time = "{:02d}:{}".format(9 + (i+1) // 4, str(((i+1) % 4) * 15).zfill(2))
    cumulative_volume_15min_list.append(calc_cumulative_volume(data, start_time, end_time))

# 將每個時間區間的一年累計成交量合併為一個 DataFrame
cumulative_volume_15min = pd.concat(cumulative_volume_15min_list)

# 顯示結果
print(cumulative_volume_15min)
