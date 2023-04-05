from yahooquery import Ticker
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_ptp_tickers(url1, url2):
    # 爬取第一個網站的 PTP 股票代號列表
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.content, "html.parser")

    table1 = soup1.find("table", {"width": "100%"})
    tbody1 = table1.find("tbody")
    rows1 = tbody1.find_all("tr")
    ptp_lists = []

    for row in rows1:
        cols = row.find_all("td")
        if len(cols) == 3:
            symbol = cols[2].get_text().strip()
            ptp_lists.append(symbol)

    # 爬取第二個網站的 PTP 股票代號列表
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    table2 = soup2.find('table', {'class': 'table'})
    rows2 = table2.find_all('tr')
    ptp_tickers = []

    for row in rows2:
        code = row.find('td')
        if code:
            ptp_tickers.append(code.text.strip())
    # 合併兩個列表，並取得不重覆的值，最終返回 PTP 股票代號列表
    ptp_lists.extend(ptp_tickers)
    ptp_lists = list(set(ptp_lists))
    return ptp_lists
    print(ptp_lists)


def remove_ptp_list(ptp_tickers, tickers):
    us_non_ptp_tickers = [x for x in tickers if x not in ptp_tickers]
    us_ptp_tickers = [x for x in tickers if x in ptp_tickers]
    print("PTP US stocks:", us_ptp_tickers)
    print("Non-PTP US stocks:", us_non_ptp_tickers)
    return us_non_ptp_tickers


def get_data_all(ticker_list):
    try:
        # data_org = yf.download(ticker_in, period="3y", progress=False)
        ticker = Ticker(ticker_list)
        data_all = ticker.history(period="3y", interval='1d')
    except Exception as e:
        data_all = pd.DataFrame()  # 返回一個空的數據帧
        print("Get Data Fail")
    return data_all


tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sp500 = tables[0]['Symbol'].tolist()
sp500 = [symbol.replace(".", "-") for symbol in sp500]


df_ticker = pd.read_excel("Tickers.xlsx", sheet_name="US", usecols=[0])
us_tickers = df_ticker.iloc[:, 0].tolist()
us_tickers = us_tickers[:500]
us_tickers_length = len(us_tickers)
print("Total US Tickers:", us_tickers_length)
start_time = time.time()  # 记录开始时间

pd_all = get_data_all(sp500)
# pd_all = get_data_all(us_tickers)
print(pd_all)
end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算运行时间
print(f"Elapsed time: {elapsed_time} seconds")

tsla_data = pd_all.loc['GOOG']
print(tsla_data)