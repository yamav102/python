#! python3
# P292.py
'''
Selenium でリンクをクリック
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
browser = webdriver.Firefox()
browser.get('http://inventwithpython.com')
link_elem = browser.find_element(By.LINK_TEXT, 'Read Online for Free')
print(f'type(link_elem):{type(link_elem)}')
link_elem.click()
# try:
#     while True:
#         time.sleep(1) # 1秒 sleep
# except KeyboardInterrupt:← ctrl+c でこのエラーがレイズされる環境である場合が多いらしい。windows + firefox では利かない
#     print('終了します。')
# finally:
#     browser.quit()
input('Enterキーで終了します') # ブラウザが直ぐ閉じてしまわないように、入力待ち状態にしている。
browser.quit()