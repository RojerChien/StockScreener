import numpy as np
import pandas as pd
import yfinance as yf
import webbrowser
from yahooquery import Ticker


def backtest_strategy_old2(stock_data, stock_symbol):
    stock_data = stock_data.copy()
    stock_data['SMA21'] = stock_data['close'].rolling(window=21).mean()
    stock_data['SMA55'] = stock_data['close'].rolling(window=55).mean()
    stock_data['SMA155'] = stock_data['close'].rolling(window=155).mean()

    buy_signals = []
    sell_signals = []
    position = False

    for i in range(1, len(stock_data)):
        sma21_cross_sma55 = stock_data['SMA21'].iloc[i - 1] < stock_data['SMA55'].iloc[i - 1] and stock_data['SMA21'].iloc[i] > \
                            stock_data['SMA55'].iloc[i]
        sma_conditions = stock_data['close'].iloc[i] > stock_data['SMA21'].iloc[i] > stock_data['SMA55'].iloc[i] > \
                         stock_data['SMA155'].iloc[i]
        sma_increasing = stock_data['SMA21'].iloc[i] > stock_data['SMA21'].iloc[i - 1] and stock_data['SMA55'].iloc[i] > \
                         stock_data['SMA55'].iloc[i - 1] and stock_data['SMA155'].iloc[i] > stock_data['SMA155'].iloc[i - 1]

        if sma21_cross_sma55 and sma_conditions and sma_increasing and not position:
            buy_signals.append(stock_data.index[i])
            position = True
        elif stock_data['close'].iloc[i] < stock_data['SMA21'].iloc[i] and position:
            sell_signals.append(stock_data.index[i])
            position = False

    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    initial_balance = 200000
    balance = initial_balance
    shares = 0
    profit_count = 0
    total_trades = len(buy_signals)

    investment_ratios = [0.1, 0.50, 1]
    investment_thresholds = [0, 0.03, 0.06]

    trade_records = []

    for buy_date, sell_date in zip(buy_signals, sell_signals):
        buy_price = stock_data.loc[buy_date]['close']
        sell_price = stock_data.loc[sell_date]['close']

        total_investment = 0
        total_shares = 0
        investment_count = 0
        for idx, (ratio, threshold) in enumerate(zip(investment_ratios, investment_thresholds)):
            current_profit = (sell_price - buy_price) / buy_price
            if current_profit >= threshold:
                investment_amount = balance * ratio
                shares_to_buy = investment_amount // buy_price
                total_shares += shares_to_buy
                balance -= shares_to_buy * buy_price
                total_investment += shares_to_buy * buy_price
                investment_count += 1

        balance += total_shares * sell_price
        profit = total_shares * (sell_price - buy_price)
        if profit > 0:
            profit_count += 1
        total_shares = 0

        trade_record = {
            'buy_date': buy_date,
            'buy_price': buy_price,
            'sell_date': sell_date,
            'sell_price': sell_price,
            'exposure days': sell_date - buy_date,
            'investment_amount': total_investment,
            'investment percentage': total_investment / (balance - profit),
            'total_investments': investment_count,
            'profit': profit,
            'balance': balance,
            'cumulative_profit': balance - initial_balance
        }
        trade_records.append(trade_record)
        if total_trades > 0:
            winning_percentage = profit_count / total_trades * 100
        else:
            winning_percentage = 0

        final_balance = balance + shares * stock_data['close'][-1]
        total_return = (final_balance - initial_balance) / initial_balance * 100

        return {
            'ticker': stock_symbol,
            'winning_percentage': winning_percentage,
            'initial_balance': initial_balance,
            'final_balance': final_balance,
            'total_return': total_return,
            'trade_records': trade_records,
            'total_investments': investment_count
        }


def backtest_strategy_single(stock_data, stock_symbol):
    stock_data = stock_data.copy()
    stock_data['SMA21'] = stock_data['close'].rolling(window=21).mean()
    stock_data['SMA55'] = stock_data['close'].rolling(window=55).mean()
    stock_data['SMA155'] = stock_data['close'].rolling(window=155).mean()

    buy_signals = []
    sell_signals = []
    position = False

    for i in range(1, len(stock_data)):
        sma21_cross_sma55 = stock_data['SMA21'].iloc[i - 1] < stock_data['SMA55'].iloc[i - 1] and stock_data['SMA21'].iloc[i] > \
                            stock_data['SMA55'].iloc[i]
        sma_conditions = stock_data['close'].iloc[i] > stock_data['SMA21'].iloc[i] > stock_data['SMA55'].iloc[i] > \
                         stock_data['SMA155'].iloc[i]
        sma_increasing = stock_data['SMA21'].iloc[i] > stock_data['SMA21'].iloc[i - 1] and stock_data['SMA55'].iloc[i] > \
                         stock_data['SMA55'].iloc[i - 1] and stock_data['SMA155'].iloc[i] > stock_data['SMA155'].iloc[i - 1]

        if sma21_cross_sma55 and sma_conditions and sma_increasing and not position:
            buy_signals.append(stock_data.index[i])
            position = True
        elif stock_data['close'].iloc[i] < stock_data['SMA21'].iloc[i] and position:
            sell_signals.append(stock_data.index[i])
            position = False

    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    initial_balance = 200000
    balance = initial_balance
    shares = 0
    profit_count = 0
    total_trades = len(buy_signals)

    investment_ratios = [0.1, 0.50, 1]
    investment_thresholds = [0, 0.03, 0.06]

    trade_records = []

    for buy_date, sell_date in zip(buy_signals, sell_signals):
        buy_price = stock_data.loc[buy_date]['close']
        sell_price = stock_data.loc[sell_date]['close']

        total_investment = 0
        total_shares = 0
        second_investment_made = False
        investment_count = 0  # Reset investment_count at the beginning of each trade

        for idx, (ratio, threshold) in enumerate(zip(investment_ratios, investment_thresholds)):
            current_profit = (sell_price - buy_price) / buy_price
            if current_profit >= threshold:
                # If the third investment is made before the second investment, skip
                if idx == 2 and not second_investment_made:
                    continue

                investment_amount = balance * ratio
                shares_to_buy = investment_amount // buy_price
                total_shares += shares_to_buy
                balance -= shares_to_buy * buy_price
                total_investment += shares_to_buy * buy_price

                if idx == 1:
                    second_investment_made = True

                investment_count += 1  # Increment investment_count when buying shares

            if investment_count == 0:
                investment_amount = balance * investment_ratios[0]
                shares_to_buy = investment_amount // buy_price
                total_shares += shares_to_buy
                balance -= shares_to_buy * buy_price
                total_investment += shares_to_buy * buy_price
                investment_count = 1

            balance += total_shares * sell_price
            profit = total_shares * (sell_price - buy_price)
            if profit > 0:
                profit_count += 1
            total_shares = 0

            trade_record = {
                'buy_date': buy_date,
                'buy_price': buy_price,
                'sell_date': sell_date,
                'sell_price': sell_price,
                'exposure days': sell_date - buy_date,
                'investment_amount': total_investment,
                'investment percentage': total_investment / (balance - profit),
                'total_investments': investment_count,
                'profit': profit,
                'balance': balance,
                'cumulative_profit': balance - initial_balance
            }
            trade_records.append(trade_record)

        if total_trades > 0:
            winning_percentage = profit_count / total_trades * 100
        else:
            winning_percentage = 0

        final_balance = balance + shares * stock_data['close'][-1]
        total_return = (final_balance - initial_balance) / initial_balance * 100

        return {
            'ticker': stock_symbol,
            'winning_percentage': winning_percentage,
            'initial_balance': initial_balance,
            'final_balance': final_balance,
            'total_return': total_return,
            'trade_records': trade_records,
            'total_investments': investment_count
        }



def backtest_strategy(stock_data, stock_symbol):
    stock_data = stock_data.copy()
    stock_data['SMA21'] = stock_data['close'].rolling(window=21).mean()
    stock_data['SMA55'] = stock_data['close'].rolling(window=55).mean()
    stock_data['SMA155'] = stock_data['close'].rolling(window=155).mean()

    buy_signals = []
    sell_signals = []
    position = False

    for i in range(1, len(stock_data)):
        sma21_cross_sma55 = stock_data['SMA21'].iloc[i - 1] < stock_data['SMA55'].iloc[i - 1] and stock_data['SMA21'].iloc[i] > \
                            stock_data['SMA55'].iloc[i]
        sma_conditions = stock_data['close'].iloc[i] > stock_data['SMA21'].iloc[i] > stock_data['SMA55'].iloc[i] > \
                         stock_data['SMA155'].iloc[i]
        sma_increasing = stock_data['SMA21'].iloc[i] > stock_data['SMA21'].iloc[i - 1] and stock_data['SMA55'].iloc[i] > \
                         stock_data['SMA55'].iloc[i - 1] and stock_data['SMA155'].iloc[i] > stock_data['SMA155'].iloc[i - 1]

        if sma21_cross_sma55 and sma_conditions and sma_increasing and not position:
            buy_signals.append(stock_data.index[i])
            position = True
        elif stock_data['close'].iloc[i] < stock_data['SMA21'].iloc[i] and position:
            sell_signals.append(stock_data.index[i])
            position = False

    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    initial_balance = 200000
    balance = initial_balance
    shares = 0
    profit_count = 0
    total_trades = len(buy_signals)

    investment_ratios = [0.1, 0.50, 1]
    investment_thresholds = [0, 0.03, 0.06]

    trade_records = []

    for buy_date, sell_date in zip(buy_signals, sell_signals):
        buy_price = stock_data.loc[buy_date]['close']
        sell_price = stock_data.loc[sell_date]['close']

        total_investment = 0
        total_shares = 0
        second_investment_made = False
        investment_made = False
        investment_count = 0  # 在每次交易開始時重置 investment_count
        for idx, (ratio, threshold) in enumerate(zip(investment_ratios, investment_thresholds)):
            current_profit = (sell_price - buy_price) / buy_price
            if current_profit >= threshold:
                # 如果在第三筆資金注入之前沒有執行第二筆資金注入，則跳過
                if idx == 2 and not second_investment_made:
                    continue

                investment_amount = balance * ratio
                shares_to_buy = investment_amount // buy_price
                total_shares += shares_to_buy
                balance -= shares_to_buy * buy_price
                total_investment += shares_to_buy * buy_price

                if idx == 1:
                    second_investment_made = True

                investment_count += 1  # 在購買股票時遞增 investment_count

        if not investment_made:
            investment_amount = balance * investment_ratios[0]
            shares_to_buy = investment_amount // buy_price
            total_shares += shares_to_buy
            balance -= shares_to_buy * buy_price
            total_investment += shares_to_buy * buy_price

        balance += total_shares * sell_price
        profit = total_shares * (sell_price - buy_price)
        if profit > 0:
            profit_count += 1
        total_shares = 0

        trade_record = {
            'buy_date': buy_date,
            'buy_price': buy_price,
            'sell_date': sell_date,
            'sell_price': sell_price,
            'exposure days': sell_date - buy_date,
            'investment_amount': total_investment,
            'investment percentage': total_investment / (balance - profit),
            'total_investments': investment_count,
            'profit': profit,
            'balance': balance,
            'cumulative_profit': balance - initial_balance
        }
        trade_records.append(trade_record)

    if total_trades > 0:
        winning_percentage = profit_count / total_trades * 100
    else:
        winning_percentage = 0

    final_balance = balance + shares * stock_data['close'][-1]
    total_return = (final_balance - initial_balance) / initial_balance * 100

    return {
        'ticker': stock_symbol,
        'winning_percentage': winning_percentage,
        'initial_balance': initial_balance,
        'final_balance': final_balance,
        'total_return': total_return,
        'trade_records': trade_records,
        'total_investments': investment_count
    }


# 取得S&P 500股票清單
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)
sp500_table = tables[0]
sp500_symbols_tmp = sp500_table['Symbol'].tolist()
sp500_symbols = [symbol.replace(".", "-") for symbol in sp500_symbols_tmp]
sp500_symbols = ['AAPL', 'TSLA']

# 設定回測時間範圍
start_date = '2023-04-01'
end_date = '2023-04-25'

# 一次下載所有股票數據
# all_stock_data = {}
# for symbol in sp500_symbols:
#    all_stock_data[symbol] = yf.download(symbol, start=start_date, end=end_date)
# 一次下載所有股票數據
print("ready to download")
ticker = Ticker(sp500_symbols, asynchronous=True)
all_stock_data = ticker.history(period="max", interval="1d")
#all_stock_data = yf.download(sp500_symbols, start=start_date, end=end_date, group_by='ticker')
print("downloaded~~")
print(all_stock_data)

# 進行回測並保存結果
results = []
all_trade_records = []

for symbol in sp500_symbols:
    try:
        result = backtest_strategy(all_stock_data.loc[symbol], symbol)
        results.append(result)

        trade_records_df = pd.DataFrame(result['trade_records'])
        trade_records_df['symbol'] = symbol
        all_trade_records.append(trade_records_df)

    except Exception as e:
        print(f"Error processing symbol {symbol}: {e}")


results_df = pd.DataFrame(columns=['ticker', 'winning_percentage', 'initial_balance', 'final_balance', 'total_return'])

# 將結果添加到 DataFrame
for result in results:
    results_df = results_df.append({
        'ticker': result['ticker'],
        'winning_percentage': result['winning_percentage'],
        'initial_balance': result['initial_balance'],
        'final_balance': result['final_balance'],
        'total_return': result['total_return']
    }, ignore_index=True)

all_trade_records_indexed = []

for trade_records_df in all_trade_records:
    multiindex = pd.MultiIndex.from_arrays([trade_records_df['symbol'], trade_records_df.index],
                                           names=['symbol', 'trade_id'])
    trade_records_df = trade_records_df.set_index(multiindex)
    all_trade_records_indexed.append(trade_records_df)

all_trade_records_df = pd.concat(all_trade_records_indexed)

# all_trade_records_df = pd.concat(all_trade_records).set_index(['symbol', all_trade_records[0].index])


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

filename_trade_records = "trade_records_15_15.html"

trade_records_html = all_trade_records_df.to_html(index=True, classes="sortable", table_id="tradeRecordsTable")

final_trade_records_html = html_template.format(table=trade_records_html)

# 將交易記錄HTML保存到檔案
with open(filename_trade_records, "w") as f:
    f.write(final_trade_records_html)
webbrowser.open(filename_trade_records)

filename_results = "results_15_15.html"
results_html = results_df.to_html(index=True, classes="sortable", table_id="resultsTable")
final_results_html = html_template.format(table=results_html)

# 將結果HTML保存到檔案
with open(filename_results, "w") as f:
    f.write(final_results_html)
webbrowser.open(filename_results)
