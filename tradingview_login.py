import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 使用這個函數保存cookies
def save_cookies(driver, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

# 使用這個函數讀取cookies
def load_cookies(driver, file_path):
    with open(file_path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

# 登入後的URL，您需要在登入後替換為實際的URL
logged_in_url = "https://www.tradingview.com/#signin"

# 將cookies保存到文件中
# driver = webdriver.Chrome(executable_path="./chromedriver")
# driver.get(logged_in_url)
# save_cookies(driver, "cookies.pkl")

# 從保存的cookies文件中讀取cookies
driver = webdriver.Chrome(executable_path="./chromedriver")
time.sleep(120)
driver.quit()