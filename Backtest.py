import numpy as np
import pandas as pd
import yfinance as yf
import webbrowser
# from pandas_datareader import get_sp500_symbols

def backtest_strategy(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data['SMA21'] = stock_data['Close'].rolling(window=21).mean()
    stock_data['SMA55'] = stock_data['Close'].rolling(window=55).mean()
    stock_data['SMA155'] = stock_data['Close'].rolling(window=155).mean()

    buy_signals = []
    sell_signals = []
    position = False

    for i in range(1, len(stock_data)):
        sma21_cross_sma55 = stock_data['SMA21'][i - 1] < stock_data['SMA55'][i - 1] and stock_data['SMA21'][i] > stock_data['SMA55'][i]
        sma_conditions = stock_data['Close'][i] > stock_data['SMA21'][i] > stock_data['SMA55'][i] > stock_data['SMA155'][i]
        sma_increasing = stock_data['SMA21'][i] > stock_data['SMA21'][i - 1] and stock_data['SMA55'][i] > stock_data['SMA55'][i - 1] and stock_data['SMA155'][i] > stock_data['SMA155'][i - 1]

        if sma21_cross_sma55 and sma_conditions and sma_increasing and not position:
            buy_signals.append(stock_data.index[i])
            position = True
        elif stock_data['Close'][i] < stock_data['SMA21'][i] and position:
            sell_signals.append(stock_data.index[i])
            position = False

    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    initial_balance = 10000
    balance = initial_balance
    shares = 0
    profit_count = 0
    total_trades = len(buy_signals)

    for buy_date, sell_date in zip(buy_signals, sell_signals):
        buy_price = stock_data.loc[buy_date]['Close']
        sell_price = stock_data.loc[sell_date]['Close']
        shares_to_buy = balance // buy_price
        shares += shares_to_buy
        balance -= shares_to_buy * buy_price
        balance += shares * sell_price
        profit = shares * (sell_price - buy_price)
        if profit > 0:
            profit_count += 1
        shares = 0

    if total_trades > 0:
        winning_percentage = profit_count / total_trades * 100
    else:
        winning_percentage = 0

    final_balance = balance + shares * stock_data['Close'][-1]
    total_return = (final_balance - initial_balance) / initial_balance * 100

    return {
        'ticker': stock_symbol,
        'winning_percentage': winning_percentage,
        'initial_balance': initial_balance,
        'final_balance': final_balance,
        'total_return': total_return,
    }

# 取得S&P 500股票清單
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)
sp500_table = tables[0]
sp500_symbols_tmp = sp500_table['Symbol'].tolist()
sp500_symbols = [symbol.replace(".", "-") for symbol in sp500_symbols_tmp]
# sp500_symbols = ['AAPL', 'TSLA']

# 設定回測時間範圍
start_date = '2007-01-01'
end_date = '2024-04-10'

# 進行回測並保存結果
results = []
for symbol in sp500_symbols:
    try:
        result = backtest_strategy(symbol, start_date, end_date)
        results.append(result)
    except Exception as e:
        print(f"Error processing symbol {symbol}: {e}")

results_df = pd.DataFrame(results)

# 將結果轉換為HTML
#results_html = results_df.to_html(index=False)

results_html = results_df.to_html(index=False, classes="sortable", table_id="resultsTable")

# 加入排序功能的HTML和JavaScript
html_template = '''
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
  <script>
    $(document).ready(function() {{
      $('#resultsTable').DataTable({{
        "pageLength": -1,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
      }});
    }});
  </script>
</head>
<body>
{table}
</body>
</html>
'''

final_html = html_template.format(table=results_html)

filename = "backtest_results.html"

# 將HTML保存到檔案
with open(filename, "w") as f:
    f.write(final_html)
webbrowser.open(filename)
print("Finished!")
