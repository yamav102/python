import requests
from pathlib import Path
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
})

url = 'https://o-dan.net/ja/'

# まずGETでCookieなどを取得
session.get(url)

# その後POST
payload = {
    "q": "猫",
    "sCc": "only",
    "oAdWrn": "0",
}

response = session.post(url, data=payload)

print("Status:", response.status_code)
print("Length:", len(response.text))
save_html = Path(__file__).parent / "result.html"
with open(save_html, "w", encoding="utf-8") as f:
    f.write(response.text)