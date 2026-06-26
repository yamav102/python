#! python3
# test2.py
# requests.get の正常終了 ↓
# res.status_code = requests.codes.ok ← 200
# 以外の時、raise Exception するには、
# res.raise_for_status() を使う
# requests.get は、res.rase_for_status() を使うようにしましょう。
import requests
res = requests.get('https://inventwithpython.com/page_that_does_not_exist')

try:
    res.raise_for_status()
except Exception as exc:
    print('問題あり:{}'.format(exc)) # ← 404:Not Found 