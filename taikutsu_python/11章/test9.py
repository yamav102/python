import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
}
url = 'https://www.google.com/search?q=abc'
res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, 'html.parser')

# 現在比較的効きやすいパターン
link_elems = soup.select('div.g a h3')   # h3を含むaタグ
print(f'len(link_elems):{len(link_elems)}') # grok提案スクリプトでも取得できない。
for elem in link_elems[:5]:
    a_tag = elem.find_parent('a')
    if a_tag and a_tag.get('href'):
        link = a_tag['href']
        if link.startswith('/url?q='):
            link = link.split('/url?q=')[1].split('&')[0]
        print(link)
        # webbrowser.open(link)