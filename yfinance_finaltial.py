import yfinance as yf

msft = yf.Ticker("MSFT")


print("\nIncome Statement:")
## print(msft.financials)
print("\nQuarterly Income Statement:")
## print(msft.quarterly_financials)

print("\nBalance Sheet:")
print(msft.balance_sheet)
print("\nQuarterly Balance Sheet:")
print(msft.quarterly_balance_sheet)

print("\nCash Flow Statement:")
print(msft.cashflow)
print("\nQuarterly Cash Flow Statement:")
print(msft.quarterly_cashflow)

print("\nMajor Holders:")
print(msft.major_holders)
print("\nInstitutional Holders:")
print(msft.institutional_holders)
print("\nMutual Fund Holders:")
print(msft.mutualfund_holders)

print("\nEarnings:")
print(msft.earnings)
print("\nQuarterly Earnings:")
print(msft.quarterly_earnings)

print("\nSustainability:")
print(msft.sustainability)

print("\nAnalysts Recommendations:")
print(msft.recommendations)
print("\nAnalysts Recommendations Summary:")


# 下載 Tesla 的資料
"""sft = yf.Ticker("MSFT")
# 獲取股票信息
msft_info = msft.info

print(msft_info)

# 獲取股息、拆股、資本利得等操作
msft_actions = msft.actions
msft_dividends = msft.dividends
msft_splits = msft.splits

print(msft_actions)
print(msft_dividends)
print(msft_splits)"""

""" "# 獲取財務報表
income_statement = tsla.financials
balance_sheet = tsla.balance_sheet
cashflow_statement = tsla.cashflow

# 顯示財務報表
print("Income Statement:")
print(income_statement)
print("\nBalance Sheet:")
print(balance_sheet)
print("\nCashflow Statement:")
print(cashflow_statement)"""