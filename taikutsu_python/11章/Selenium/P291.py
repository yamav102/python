#! python 3
# P291.py
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()
browser.get('http://inventwithpython.com')
try:
    # find_element_by_* は Selenium4.3以降で廃止されてエラーになる。
    # elem = browser.find_element_by_class_name('bookcover')
    # By.CLASS_NAME でクラス名にスペースが使われているとエラーになる。
    # elem = browser.find_element(By.CLASS_NAME,'img-float-left img-thumb')
    elem = browser.find_element(
        By.CSS_SELECTOR, 
        value = "[class='img-float-left img-thumb']"
        )
    classname = elem.get_attribute('class')
    print(f'クラス名 {classname} を持つ要素<{elem.tag_name}>を見つけた！')
except Exception as e:
    print(f'クラス名 {classname} を持つ要素はみつからなかった。{e}')