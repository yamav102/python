#! python3
# test7.py
import requests
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
import argparse
from typing import Final, List, Tuple
def main(search_word: str)->None:
    # 対象のページURL
    base_url = 'https://www.flickr.com/'
    # 検索ワードのページを取得    
    url = f'{base_url}/search/?text={search_word}'
    res = requests.get(url, timeout=10)
    res.raise_for_status
    soup = BeautifulSoup(res.text, features='html.parser')
    # print(res.status_code)
    # save_html = Path(__file__).parent / 'test7.html'
    # with open(save_html, "w", encoding="utf-8") as f:
    #     f.write(res.text)
    # imgURL回収
    MAX_WORKERS = 12
    # 型ヒント付き変数宣言
    tasks: List = [Tuple[str, Path]] # (保存パス, 画像URL)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='画像検索キーワード',
        epilog='c:>py image_site_download cat'
    )
    parser.add_argument(
        'search_word',
        help='画像検索のキーワード'
    )
    args = parser.parse_args()
    main(args.search_word)


