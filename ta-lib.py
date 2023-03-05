#https://www.twblogs.net/a/5c546dc0bd9eee06ef364f99
import yfinance as yf
import talib
import matplotlib.pyplot as plt

# Download the data
ticker = yf.Ticker("AAPL")
data = ticker.history(period="1y")

# Calculate the MACD indicator
macd, macdsignal, macdhist = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

# Plot the MACD indicator
plt.plot(macd, label='MACD')
plt.plot(macdsignal, label='Signal')
plt.plot(macdhist, label='Histogram')
plt.legend(loc='upper left')
plt.show()
