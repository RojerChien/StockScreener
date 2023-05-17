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
import logging
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
    if "value" in value and value["value"] == TradingSymbol:
        print(f"找到符合的資料：{key} 的 TradingSymbol 值為 {target_value}")
        found = True

if not found:
    print(f"找不到符合的資料：TradingSymbol 值為 {target_value}")

