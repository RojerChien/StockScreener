from finvizfinance.screener.overview import Overview

# 設定篩選器
filters = ['ta_change_u5']

# 創建Overview對象，並獲取符合篩選條件的股票列表
stock_list = Overview(filters=filters, order='price')

# 輸出股票列表
for stock in stock_list:
    print(stock['Ticker'], stock['Price'], stock['Change'])