# pip install sec-edgar-py
# import sec_edgar_py
from sec_edgar_py import EdgarWrapper
client = EdgarWrapper()
filings = client.get_company_filings('aapl', form_types=['10-Q','10-K','6-K','20-F'], amount=2)
print(filings)


form_list = []
filing_date_list = []
url_list = []

for filing in filings['filings']:
    form_list.append(filing['form'])
    filing_date_list.append(filing['filingDate'])
    url_list.append(filing['URL'])

print('Form List:', form_list)
print('Filing Date List:', filing_date_list)
print('URL List:', url_list)