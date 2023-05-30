import logging
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser, XbrlInstance

logging.basicConfig(level=logging.INFO)
cache: HttpCache = HttpCache('./cache')
cache.set_headers({'From': 'YOUR@EMAIL.com', 'User-Agent': 'py-xbrl/2.1.0'})
parser = XbrlParser(cache)

schema_url = "https://www.sec.gov/Archives/edgar/data/885725/000088572523000026/bsx-20230331.htm"
inst: XbrlInstance = parser.parse_instance(schema_url)
print(inst.json(override_fact_ids=True))