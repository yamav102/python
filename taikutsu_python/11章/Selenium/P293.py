#! python3
# P293.py
'''
特殊なキーを送信する
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
browser = webdriver.Firefox()
browser.get('http://nostarch.com') # 米国の技術書で有名なサイトらしい
html_elem = browser.find_element(By.TAG_NAME, 'html')
# 末尾にスクロール
#html_elem.send_keys(Keys.END)
for i in range(2):
    html_elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5) # 0.01秒も待てるらしい。精度はないらしい。
time.sleep(3) # 3秒

# 先頭にスクロール
#html_elem.send_keys(Keys.HOME)
for i in range(2):
    html_elem.send_keys(Keys.PAGE_UP)
    time.sleep(0.5)
input('Enterキーで終了します。')
browser.quit()
