#! python3
# P292_2.py
'''
フォームを記入して送信する
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
browser = webdriver.Firefox()
# browser.get('https://yamav102.github.io/HomePage/htm_file/hyoushihidari.htm')
browser.get('https://yamav102.github.io/HomePage/index.htm')
'''
[掲示板集email]ボタンをクリック
'''
# login_elem = browser.find_element(By.ID, 'username')
# login_elem.send_keys('abcde')
# next_btn_elem = browser.find_element(
#     By.CSS_SELECTOR, 
#     'button[class="uds-button-brand uds-button-primary uds-button uds-ring uds-hit-target Y0daaae72"]'
#     )
# next_btn_elem.submit()
input('Enterキーで終了します')
browser.quit()

