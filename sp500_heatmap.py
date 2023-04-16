import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from dateutil.relativedelta import relativedelta

# 获取今天的日期
today = datetime.datetime.today()

# 计算前一年的日期
one_year_ago = today - relativedelta(years=1)

# 下载S&P 500数据
sp500 = yf.download("^GSPC", start=one_year_ago, end=today)

# 创建一个简单的价格图
sp500['Close'].plot(title='S&P 500 Price Chart')

# 创建一个热力图数据
heatmap_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}, index=["X", "Y", "Z"])

# 创建两个子图 - 一个价格图和一个热力图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={"height_ratios": [3, 1]})
fig.subplots_adjust(hspace=0.3)

# 在顶部子图中绘制价格图
ax1.plot(sp500['Close'])
ax1.set_title('S&P 500 Price Chart')

# 在底部子图中绘制热力图
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="viridis", linewidths=.5, annot_kws={"size": 10}, ax=ax2)
ax2.set_title("Heatmap")

# 显示图表
plt.show()
