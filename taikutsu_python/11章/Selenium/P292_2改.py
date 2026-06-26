#! python3
# P292.2改.py
'''
フォームに記入して送信する
送信処理を確認は出来るが、ロボット避け画面になるので、最後まで実行できない。
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
browser = webdriver.Firefox()
browser.get('https://inventwithpython.com/')
# google検索txtbox
input_search = browser.find_element(
    By.CSS_SELECTOR, 'input[class="form-control me-2"]'
    )
input_search.send_keys('Automate the Boring Stuff with Python')
# submitボタン
button_submit = browser.find_element(
    By.CSS_SELECTOR, 'button[class="btn btn-outline-success"]'
)
button_submit.submit()

input('Enterキーで終了します。')
browser.quit()
