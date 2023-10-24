import pandas as pd

# 從第二行開始讀取Excel文件
# df = pd.read_excel("Tickers.xlsx", skiprows=1)
df = pd.read_excel("Tickers.xlsx", sheet_name="US")
# print(df.columns)
# 把Symbol, Sector, Industry這三個欄位的值都存儲到列表中
#symbols = [sym for sym in df["Symbol"] if '^' not in str(sym)]
# symbols = df["Symbol"].tolist()

# 把Symbol, Sector, Industry這三個欄位的值都存儲到列表中
# 將 / 字符替換為 - 並確保不包含 ^
symbols = [str(sym).replace('/', '-') for sym in df["Symbol"] if '^' not in str(sym)]
sectors = df["Sector"].tolist()
industries = df["Industry"].tolist()

# 使用Symbol作為鍵，建立一個字典來查找Sector和Industry的值
symbol_sector_industry_dict = {}
for symbol, sector, industry in zip(symbols, sectors, industries):
    # 確保symbol是字串型態
    # symbol_str = str(symbol)
    # 略過包含^符號的symbol
    # if '^' not in symbol_str:
    symbol = str(symbol).replace('/', '-')
    symbol_sector_industry_dict[symbol] = {"Sector": sector, "Industry": industry}


def get_sector_and_industry_by_symbol(symbol):
    # 從字典中獲取值，如果找不到，則返回 {'Sector': 'NA', 'Industry': 'NA'}
    result = symbol_sector_industry_dict.get(symbol, {"Sector": 'NA', "Industry": 'NA'})

    # 如果 Sector 或 Industry 為 NaN，則將其替換為 'NA'
    if pd.isnull(result['Sector']):
        result['Sector'] = 'NA'
    if pd.isnull(result['Industry']):
        result['Industry'] = 'NA'

    return result


def unique_values_in_columns(file_name: str, sheet_name: str) -> (list, list):
    df = pd.read_excel(file_name, sheet_name=sheet_name)

    unique_sectors = df['Sector'].unique().tolist()
    unique_industries = df['Industry'].unique().tolist()

    return unique_sectors, unique_industries


# 使用函數獲取唯一值
unique_sectors, unique_industries = unique_values_in_columns("Tickers.xlsx", "US")

# 打印結果
print(f"Unique Sectors: {unique_sectors}")
print(f"Number of Unique Sectors: {len(unique_sectors)}")
print("--------------------------")
print(f"Unique Industries: {unique_industries}")
print(f"Number of Unique Industries: {len(unique_industries)}")

for symbol in symbols:
    # 確保symbol是字串型態且不包含^符號
    symbol_str = str(symbol)
    if '^' in symbol_str:
        continue
    result = get_sector_and_industry_by_symbol(symbol)
    print(f"Symbol: {symbol}")
    print(f"Sector: {result['Sector']}")
    print(f"Industry: {result['Industry']}")
    print("--------------------------")

print(f"總共有 {len(symbols)} 個symbol。")
print(f"Symbols with NaN: {pd.isnull(df['Symbol']).sum()}")
print(f"Sectors with NaN: {pd.isnull(df['Sector']).sum()}")
print(f"Industries with NaN: {pd.isnull(df['Industry']).sum()}")
