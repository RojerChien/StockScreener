from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://tw.tradingview.com/chart/sWFIrRUP/?symbol=NASDAQ%3AINTC"

# 初始化WebDriver
driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get(url)

# 等待網頁加載完成
time.sleep(5)

# 模擬按下Ctrl + W組合鍵
body = driver.find_element_by_tag_name("body")
body.send_keys(Keys.CONTROL + "w")

# 等待一段時間，然後關閉WebDriver
time.sleep(5)
driver.quit()