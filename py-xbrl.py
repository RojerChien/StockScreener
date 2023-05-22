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
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser

# just to see which files are downloaded
logging.basicConfig(level=logging.INFO)

cache: HttpCache = HttpCache('./cache')
cache.set_headers({'From': 'YOUR@EMAIL.com', 'User-Agent': 'py-xbrl/2.1.0'})
parser = XbrlParser(cache)

# schema_url = "https://www.sec.gov/Archives/edgar/data/0000320193/000032019321000105/aapl-20210925.htm"
schema_url = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000064/aapl-20230401.htm"
# schema_url = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000064/aapl-20230401.htm"
inst = parser.parse_instance(schema_url)
# print json to console
print(inst.json())

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




for key, value in data["facts"].items():
    concept = value["dimensions"]["concept"]
    if concept in target_concepts:
        period = value["dimensions"]["period"]
        decimals = value["decimals"]
        value = value["value"]
        print(f"Concept: {concept}")
        print(f"Period: {period}")
        print(f"Decimals: {decimals}")
        print(f"Value: {value}")
        print("-----------")

data = [
    {
        "Concept": "EarningsPerShareBasic",
        "Period": "2023-01-01/2023-04-01",
        "Decimals": 2,
        "Value": 1.53
    },
    {
        "Concept": "EarningsPerShareBasic",
        "Period": "2021-12-26/2022-03-26",
        "Decimals": 2,
        "Value": 1.54
    },
    {
        "Concept": "EarningsPerShareBasic",
        "Period": "2022-09-25/2023-04-01",
        "Decimals": 2,
        "Value": 3.42
    },
    {
        "Concept": "EarningsPerShareBasic",
        "Period": "2021-09-26/2022-03-26",
        "Decimals": 2,
        "Value": 3.65
    }
]

quarters = {}

for item in data:
    concept = item["Concept"]
    period = item["Period"]
    value = item["Value"]

    start_date, end_date = period.split("/")
    quarter = f"{start_date[:4]}Q{int(start_date[5:7]) // 3 + 1}"

    if quarter not in quarters:
        quarters[quarter] = []

    quarters[quarter].append({
        "Concept": concept,
        "Period": period,
        "Value": value
    })

for quarter, items in quarters.items():
    print(f"季度 {quarter}:")
    for item in items:
        concept = item["Concept"]
        period = item["Period"]
        value = item["Value"]
        print(f"Concept: {concept}")
        print(f"Period: {period}")
        print(f"Value: {value}")
        print("-----------")