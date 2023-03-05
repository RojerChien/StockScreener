import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
from backtrader import Strategy, Order, Indicator
#from backtrader import Strategy, Order, Indicator, OrderExecType, OrderValid
import backtrader as bt
import backtrader.indicators as btind

symbol = "AAPL"
stock_data = yf.download(symbol, start='2020-01-01')
# 下載股票數據
#stock_data = pdr.get_data_yahoo("AAPL", start="2020-01-01", end="2020-12-31")

# 計算移動平均線
stock_data["20d"] = stock_data["Close"].rolling(window=20).mean()
stock_data["50d"] = stock_data["Close"].rolling(window=50).mean()

# 建立技術指標
stock_data["RSI"] = pd.DataFrame.ewm(stock_data["Close"], span=21).mean()

# 建立策略
class MyStrategy(Strategy):
    def next(self):
        # 如果當前持有股票，且 RSI 大於 70，則賣出
        if self.position and self.datas[0].rsi > 70:
            self.order = Order(size=-1, exectype=OrderExecType.Close)
        # 如果當前沒有持有股票，且 RSI 小於 30，則買進
        elif not self.position and self.datas[0].rsi < 30:
            self.order = Order(size=1, exectype=OrderExecType.Market)
# 執行回測
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
cerebro.adddata()