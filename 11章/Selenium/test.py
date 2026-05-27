#! python3
# test.py
import requests

# 対象のページURL（例）
base_url = 'https://o-dan.net/ja/'   # ← 実際のページURLに変更

payload = {
    "q": "猫",                    # 検索ワード
    "sCc": "only",                      # チェックON
    "oAdWrn": "0",                      # hidden
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

response = requests.post(base_url, data=payload, headers=headers)

print(response.status_code)
print(response.text)   # 必要なら