import numpy as np
import pandas as pd
import yfinance as yf

import numpy as np
import pandas as pd
import yfinance as yf

def backtest_strategy(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data['SMA21'] = stock_data['Close'].rolling(window=21).mean()
    stock_data['SMA55'] = stock_data['Close'].rolling(window=55).mean()
    stock_data['SMA155'] = stock_data['Close'].rolling(window=155).mean()

    # Calculate RSI
    delta = stock_data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    stock_data['RSI'] = 100 - (100 / (1 + rs))

    buy_signals = []
    sell_signals = []
    position = False
    stop_loss_price = None
    total_trades = 0
    winning_trades = 0
    balance = 10000
    shares = 0

    for i in range(1, len(stock_data)):
        sma21_cross_sma55 = stock_data['SMA21'][i - 1] < stock_data['SMA55'][i - 1] and stock_data['SMA21'][i] > stock_data['SMA55'][i]
        sma_conditions = stock_data['Close'][i] > stock_data['SMA21'][i] > stock_data['SMA55'][i] > stock_data['SMA155'][i]
        sma_increasing = stock_data['SMA21'][i] > stock_data['SMA21'][i - 1] and stock_data['SMA55'][i] > stock_data['SMA55'][i - 1] and stock_data['SMA155'][i] > stock_data['SMA155'][i - 1]
        rsi_condition = stock_data['RSI'][i] > 70

        if sma21_cross_sma55 and sma_conditions and sma_increasing and rsi_condition and not position:
            buy_signals.append(stock_data.index[i])
            stop_loss_price = stock_data['Close'][i] * 0.92
            shares = balance / stock_data['Close'][i]
            balance = 0
            position = True
        elif position and (stock_data['Close'][i] < stock_data['SMA21'][i] or (stop_loss_price and stock_data['Close'][i] < stop_loss_price)):
            sell_signals.append(stock_data.index[i])
            balance = shares * stock_data['Close'][i]
            shares = 0
            position = False
            stop_loss_price = None

            # Update the number of winning trades
            total_trades += 1
            if balance > 10000:
                winning_trades += 1

    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    initial_balance = 10000
    balance = initial_balance
    shares = 0
    profit_count = 0
    total_trades = len(buy_signals)

    # Calculate the number of exposure days
    exposure_days = sum([(sell_date - buy_date).days for buy_date, sell_date in zip(buy_signals, sell_signals)])

    final_balance = balance + shares * stock_data['Close'][-1]
    # total_return = (final_balance - initial_balance) / initial_balance * 100
    if balance == 0:
      total_return = 0
    else:
      total_return = (final_balance - balance) / balance * 100
    total_trades = len(buy_signals)
    winning_trades = sum([1 for buy_date, sell_date in zip(buy_signals, sell_signals) if stock_data['Close'][sell_date] > stock_data['Close'][buy_date]])
    winning_percentage = 100 * winning_trades / total_trades if total_trades > 0 else 0
    return {
        'ticker': stock_symbol,
        'winning_percentage': winning_percentage,
        'initial_balance': initial_balance,
        'final_balance': final_balance,
        'total_return': total_return,
        'total_trades': total_trades,
        'exposure_days': exposure_days
    }


def generate_html_table(backtest_results):
    html = '<table border="1">'
    html += "<tr><th>Ticker</th><th>Winning Percentage</th><th>Initial Balance</th><th>Final Balance</th><th>Total Return</th><th>Total Trades</th><th>Exposure Days</th></tr>"
    for results_html in backtest_results:
        html += f"<tr><td>{results_html['ticker']}</td><td>{results_html['winning_percentage']:.2f}%</td><td>${results_html['initial_balance']:,.2f}</td><td>${results_html['final_balance']:,.2f}</td><td>{results_html['total_return']:.2f}%</td><td>{results_html['total_trades']}</td><td>{results_html['exposure_days']}</td></tr>"
    html += "</table>"
    return html

# 取得S&P 500股票清單
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)
sp500_table = tables[0]
sp500_symbols_tmp = sp500_table['Symbol'].tolist()
sp500_symbols = [symbol.replace(".", "-") for symbol in sp500_symbols_tmp]
sp500_symbols = ['AAPL', 'TSLA']

start_date = '2007-01-01'
end_date = '2023-04-10'

# 回测所有股票并将结果存储在列表中
backtest_results = [backtest_strategy(stock_symbol, start_date, end_date) for stock_symbol in sp500_symbols]

# 按照某个指标（例如总收益）对结果进行排序
backtest_results.sort(key=lambda x: x['total_return'], reverse=True)

# 使用generate_html_table函数生成HTML表格
html_table = generate_html_table(backtest_results)

# 或者将HTML表格保存到文件
with open("backtest_results_wi_rsi_stoploss.html", "w") as f:
    f.write(html_table)
print("Finished!")