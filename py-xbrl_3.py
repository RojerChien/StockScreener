import requests
import re
import logging
import json
import csv
import pandas as pd
import time  # 导入 time 模块
from bs4 import BeautifulSoup
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser
from sec_edgar_py import EdgarWrapper
from collections import defaultdict


def remove_ptp_list(ptp_tickers, tickers):
    # 移除 PTP 列表
    us_non_ptp_tickers = [x for x in tickers if x not in ptp_tickers]
    us_ptp_tickers = [x for x in tickers if x in ptp_tickers]
    print("PTP US stocks:", us_ptp_tickers)
    us_ptp_tickers_length = len(us_ptp_tickers)
    print("Total Removed PTP Tickers:", us_ptp_tickers_length)
    # print("Non-PTP US stocks:", us_non_ptp_tickers)
    return us_non_ptp_tickers


def get_ptp_tickers(url1='https://help.zh-tw.firstrade.com/article/841-new-1446-f-regulations',
                    url2='https://www.itigerup.com/bulletin/ptp'):
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
    ptp_lists_len = len(ptp_lists)
    print("Total PTP Tickers:", ptp_lists_len)
    return ptp_lists


def get_tickers(category, start):
    print(f'############ Start Getting Ticker by {category} mode')
    if category == "FIN":
        tickers = get_finviz_screener_tickers()
        tickers_length = len(tickers)
    else:
        df = pd.read_excel("Tickers.xlsx", sheet_name=category, usecols=[0])
        tickers = df.iloc[:, 0].tolist()
        tickers_length = len(tickers)

    if start != 0:
        tickers = tickers[start:]
        tickers_length = len(tickers)
        print(f'Total {category} Tickers after Slicing:', tickers_length)

    if category == "US" or category == "ETF" or category == "FIN":
        print(f'Total {category} Tickers before remove PTP:', tickers_length)
        ptp_lists = get_ptp_tickers()
        # print(f'PTP Stock List: {ptp_lists}')
        remove_ptp_list(ptp_lists, tickers)
        print(f'Total {category} Tickers after remove PTP:', tickers_length)
    else:
        print(f'Total {category} Tickers:', tickers_length)

    print(f'############ Finish Getting Ticker by {category} mode')
    return tickers


def parse_instance_and_write_csv(ticker, schema_url: str, output_filename: str = 'output.csv'):
    logging.basicConfig(level=logging.INFO)

    cache: HttpCache = HttpCache('./cache')
    cache.set_headers({'From': 'YOUR@EMAIL.com', 'User-Agent': 'py-xbrl/2.1.0'})

    try:
        # 下载XML实例文件内容
        response = requests.get(schema_url)
        xml_content = response.text

        # 预处理XML内容
        xml_content = preprocess_xml_content(xml_content)

        parser = XbrlParser(cache)
        inst = parser.parse_instance(xml_content)

    except FileNotFoundError:
        print(f"File not found for ticker {ticker}. Skipping...")

    headers = {
        'User-Agent': 'Wantai Corp',
        'From': 'rojer.chien@gmail.com'
    }

    # 下载XML实例文件内容
    response = requests.get(schema_url)

    xml_content = response.text

    # 预处理XML内容
    xml_content = preprocess_xml_content(xml_content)

    parser = XbrlParser(cache)
    inst = parser.parse_instance(xml_content)

    inst.json('./test.json')
    print(inst.json)
    data = json.loads(inst.json())
    # print(data)
    target_concept = "TradingSymbol"
    found = False

    for key, value in data["facts"].items():
        if "dimensions" in value and "concept" in value["dimensions"] and value["dimensions"][
            "concept"] == target_concept:
            trading_symbol = value["value"]
            # print(f"找到符合的資料：{key} 的 TradingSymbol 值為 {trading_symbol}")
            found = True

    if not found:
        print(f"找不到符合的資料：Concept 為 {target_concept}")

    data_rows = {}

    for fact_id, fact in data["facts"].items():
        try:
            concept = fact["dimensions"]["concept"]
            if concept in ["NetIncomeLoss", "EarningsPerShareBasic", "EarningsPerShareDiluted"]:
                period = tuple(fact["dimensions"]["period"].split('/'))

                entity = fact["dimensions"]["entity"]
                row = data_rows.get(period, {
                    "TradingSymbol": ticker,
                    "StartDate": period[0],
                    "EndDate": period[1]
                })

                row[f"{concept}"] = fact["value"]
                row[f"{concept}_Decimals"] = fact["decimals"]

                data_rows[period] = row
        except TypeError:
            print(f"Unexpected data type for fact: {fact}")

    with open(output_filename, 'a', newline='') as csvfile:
        fieldnames = ["TradingSymbol", "StartDate", "EndDate",
                      "NetIncomeLoss", "NetIncomeLoss_Decimals",
                      "EarningsPerShareBasic", "EarningsPerShareBasic_Decimals",
                      "EarningsPerShareDiluted", "EarningsPerShareDiluted_Decimals"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        for row in data_rows.values():
            writer.writerow(row)

def get_filing_urls(symbol: str, form_types=['10-Q', '10-K'], amount=1):
    client = EdgarWrapper()
    filings = client.get_company_filings(symbol, form_types=form_types, amount=amount)

    url_list = []
    for filing in filings['filings']:
        url_list.append(filing['URL'])
    return url_list

def preprocess_xml_content(xml_content):
    # 替换或删除未定义的实体
    processed_xml_content = re.sub(r'&([^;]+);', '', xml_content)
    # 可以根据需要进行其他处理，例如删除特定的元素或属性

    return processed_xml_content


def remove_duplicates(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    seen = set()
    unique_rows = []

    for row in rows:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            unique_rows.append(row)
            seen.add(row_tuple)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(unique_rows)

us_tickers = get_tickers("US", 0)
# us_tickers = ['BBY']

run_number = 0
empty_number = 0
url_number = 0
err_number = 0
count = 0
# filter_tickers = ['TSM']

print(us_tickers)

for symbol in us_tickers:
    # symbol = 'aapl'
    print(symbol)
    run_number += 1
    print(f"Count:{count}")

    if count < 100:
        try:
            urls = get_filing_urls(symbol)
        except ValueError as e:
            print(f"Error for ticker {symbol}: {str(e)}")
            err_number += 1
            continue  # 跳过当前符号，继续下一个符号的循环

        if not urls:
            print("urls is empty")
            empty_number += 1
        else:
            csv_file_name = f"filing.csv"
            url_number += 1
            for url in urls:
                parse_instance_and_write_csv(symbol, url, csv_file_name)
            remove_duplicates(csv_file_name)
        count += 1
    else:
        count = 0

df = pd.read_csv('filing.csv')
# 选择需要的列
columns_to_check = ['EarningsPerShareBasic',
                    'EarningsPerShareBasic_Decimals',
                    'EarningsPerShareDiluted',
                    'EarningsPerShareDiluted_Decimals']

# 删除含有空值的行
df = df.dropna(subset=columns_to_check)

# 保存新的CSV文件
df.to_csv('filing.csv', index=False)


print(f"Total ticker number: {run_number}")
print(f"Wi URL number: {url_number}")
print(f"Wo URL number: {empty_number}")
print(f"Error URL number: {err_number}")








