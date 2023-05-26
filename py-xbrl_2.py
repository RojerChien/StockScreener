import logging
import json
import csv
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser
from sec_edgar_py import EdgarWrapper
from collections import defaultdict

def parse_instance_and_write_csv(schema_url: str, output_filename: str = 'output.csv'):
    logging.basicConfig(level=logging.INFO)

    cache: HttpCache = HttpCache('./cache')
    cache.set_headers({'From': 'YOUR@EMAIL.com', 'User-Agent': 'py-xbrl/2.1.0'})
    parser = XbrlParser(cache)
    inst = parser.parse_instance(schema_url)

    inst.json('./test.json')
    print(inst.json)
    data = json.loads(inst.json())
    # print(data)
    target_concept = "TradingSymbol"
    found = False

    for key, value in data["facts"].items():
        if "dimensions" in value and "concept" in value["dimensions"] and value["dimensions"]["concept"] == target_concept:
            trading_symbol = value["value"]
            print(f"找到符合的資料：{key} 的 TradingSymbol 值為 {trading_symbol}")
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
                    "TradingSymbol": trading_symbol,
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

# def get_filing_urls(symbol: str, form_types=['10-Q', '10-K', '6-K', '20-F'], amount=1):

def get_filing_urls(symbol: str, form_types=['10-Q', '10-K'], amount=1):
    client = EdgarWrapper()
    filings = client.get_company_filings(symbol, form_types=form_types, amount=amount)

    url_list = []
    for filing in filings['filings']:
        url_list.append(filing['URL'])
    print (url_list)
    return url_list


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

filter_tickers = ['NVDA', 'TME', 'GOOG', 'GOOGL', 'AMZN', 'PCAR', 'BRK-B', 'TSLA', 'NVDA', 'UNH', 'JPM']
# filter_tickers = ['TSM']
for symbol in filter_tickers:
    # symbol = 'aapl'
    urls = get_filing_urls(symbol)
    print('URL List:', urls)
    csv_file_name = f"filing.csv"
    for url in urls:
        parse_instance_and_write_csv(url, csv_file_name)
    remove_duplicates(csv_file_name)