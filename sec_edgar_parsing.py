import requests
from bs4 import BeautifulSoup

url = 'https://www.sec.gov/Archives/edgar/data/789019/000095017023014423/msft-20230331.htm'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
}

session = requests.Session()
response = session.get(url, headers=headers)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    basic_tag = soup.find('ix:nonfraction', {'name': 'us-gaap:EarningsPerShareBasic', 'unitref': 'U_UnitedStatesOfAmericaDollarsShare'})
    diluted_tag = soup.find('ix:nonfraction', {'name': 'us-gaap:EarningsPerShareDiluted', 'unitref': 'U_UnitedStatesOfAmericaDollarsShare'})

    if basic_tag:
        basic_number = float(basic_tag.text)
        print(f"Basic Earnings Per Share: {basic_number}")
    else:
        print("找不到相應的Basic Earnings Per Share標籤。")

    if diluted_tag:
        diluted_number = float(diluted_tag.text)
        print(f"Diluted Earnings Per Share: {diluted_number}")
    else:
        print("找不到相應的Diluted Earnings Per Share標籤。")
else:
    print(f"獲取網頁內容時出錯，狀態碼：{response.status_code}")


from sec_edgar_py import EdgarWrapper
client = EdgarWrapper()
edgar = client.get_company_filings('MSFT', form_types=['10-Q'], amount=5)
print(edgar)