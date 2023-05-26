"""import logging
import json
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser, XbrlInstance
# just to see which files are downloaded
logging.basicConfig(level=logging.INFO)

cache: HttpCache = HttpCache('./cache')
cache.set_headers({'From': 'YOUR@EMAIL.com', 'User-Agent': 'py-xbrl/2.1.0'})
parser = XbrlParser(cache)

schema_url = "https://www.sec.gov/Archives/edgar/data/0000320193/000032019321000105/aapl-20210925.htm"
inst: XbrlInstance = parser.parse_instance(schema_url)


# pretty_json = json.dumps(inst, indent=4, sort_keys=True)

# print json to console
# print(inst.json(override_fact_ids=True))

######
data = json.loads(inst.json)

# 使用迴圈查詢符合條件的鍵值對
target_value = "AAPL"
found = False

for key, value in data["facts"].items():
    if "value" in value and value["value"] == target_value:
        print(f"找到符合的資料：{key} 的 TradingSymbol 值為 {target_value}")
        found = True

for key, value in inst.json["facts"].items():
    if "value" in value and value["value"] == target_value:
        print(f"找到符合的資料：{key} 的 TradingSymbol 值為 {target_value}")
        found = True

if not found:
    print(f"找不到符合的資料：TradingSymbol 值為 {target_value}")
#####

# save to file
inst.json('./test.json')"""



"""import logging
import json
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser, XbrlInstance

# just to see which files are downloaded
logging.basicConfig(level=logging.INFO)

cache: HttpCache = HttpCache('./cache')
cache.set_headers({'From': 'YOUR@EMAIL.com', 'User-Agent': 'py-xbrl/2.1.0'})
parser = XbrlParser(cache)

schema_url = "https://www.sec.gov/Archives/edgar/data/0000320193/000032019321000105/aapl-20210925.htm"
inst: XbrlInstance = parser.parse_instance(schema_url)

# pretty_json = json.dumps(inst, indent=4, sort_keys=True)

# print json to console
print(inst.json())

# save to file
inst.json('./test.json')

data = json.loads(inst.json())

# 使用迴圈查詢符合條件的鍵值對
target_value = "AAPL"
found = False

for key, value in data["facts"].items():
    if "value" in value and value["value"] == "TradingSymbol":
        print(f"找到符合的資料：{key} 的 TradingSymbol 值為 {target_value}")
        found = True

if not found:
    print(f"找不到符合的資料：TradingSymbol 值為 {target_value}")"""
import logging
import json
import csv
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser
from collections import defaultdict


# just to see which files are downloaded
logging.basicConfig(level=logging.INFO)

cache: HttpCache = HttpCache('./cache')
cache.set_headers({'From': 'YOUR@EMAIL.com', 'User-Agent': 'py-xbrl/2.1.0'})
parser = XbrlParser(cache)
schema_url = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000064/aapl-20230401.htm"
inst = parser.parse_instance(schema_url)
# print json to console
# print(inst.json())

# save to file
inst.json('./test.json')

data = json.loads(inst.json())

# 使用迴圈查詢符合條件的鍵值對
# target_concepts = ["EarningsPerShareBasic"]
# NetIncomeLoss
target_concepts = ["EarningsPerShareBasic", "EarningsPerShareDiluted", "NetIncomeLoss"]

target_concept = "TradingSymbol"
found = False



for key, value in data["facts"].items():
    if "dimensions" in value and "concept" in value["dimensions"] and value["dimensions"]["concept"] == target_concept:
        trading_symbol = value["value"]
        print(f"找到符合的資料：{key} 的 TradingSymbol 值為 {trading_symbol}")
        found = True

if not found:
    print(f"找不到符合的資料：Concept 為 {target_concept}")
processed = set()

for key, value in data["facts"].items():
    concept = value["dimensions"]["concept"]
    period = value["dimensions"]["period"]

    # Check if 'decimals' exists in the 'value' dictionary
    if 'decimals' in value:
        decimals = value["decimals"]
    else:
        decimals = None  # Default value if 'decimals' does not exist

    value_content = value["value"]

    # Use a tuple for the set to avoid duplicates
    data_item = (concept, period, decimals, value_content)

    if data_item not in processed:
        if concept in target_concepts:
            print(f"Concept: {concept}")
            print(f"Period: {period}")
            print(f"Decimals: {decimals}")
            print(f"Value: {value_content}")
            print("-----------")
        # Add data item to set, marking it as processed
        processed.add(data_item)




data_rows = {}
print(data)

# Loop through all the facts
for fact_id, fact in data["facts"].items():
    print(type(fact))  # print the type of fact
    print(fact)  # print the content of fact
    try:
        concept = fact["dimensions"]["concept"]
        if concept in ["NetIncomeLoss", "EarningsPerShareBasic", "EarningsPerShareDiluted"]:
            # Extract period and convert to tuple
            period = tuple(fact["dimensions"]["period"].split('/'))

            # Get or create row
            entity = fact["dimensions"]["entity"]
            row = data_rows.get(period, {
                "TradingSymbol": trading_symbol,
                "StartDate": period[0],
                "EndDate": period[1]
            })

            # Add fact data to row
            row[f"{concept}"] = fact["value"]
            row[f"{concept}_Decimals"] = fact["decimals"]

            # Save row
            data_rows[period] = row
    except TypeError:
        print(f"Unexpected data type for fact: {fact}")

# Write data to CSV
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ["TradingSymbol", "StartDate", "EndDate",
                  "NetIncomeLoss", "NetIncomeLoss_Decimals",
                  "EarningsPerShareBasic", "EarningsPerShareBasic_Decimals",
                  "EarningsPerShareDiluted", "EarningsPerShareDiluted_Decimals"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data_rows.values():
        writer.writerow(row)