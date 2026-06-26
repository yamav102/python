#! python3
# image_site_downloader.py
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from pathlib import Path
import argparse
from typing import Final, List, Tuple

import time
'''
画像共有サイトから、カテゴリを検索し画像をダウンロードする
無料写真素材が日本語で検索できる「O-DAN(オーダン)」
https://o-dan.net/ja/
'''
def download_image(img_url:str, save_path:str)->str:
    '''
    画像をダウンロード。結果を文字列で返す。
    '''
    chunk_size = 8192 # 8Kb
    return '結果：'
def main(search_word: str)->None:
    URL :Final[str] = 'https://o-dan.net/ja/'
    # 画像の保存フォルダ
    save_folder = (
        Path(__file__).resolve().parent
                   / ('o-dan_' + search_word)
                   )
    save_folder.mkdir(exist_ok=True)
    MAX_WORKERS:Final[int] = 12
    # 型ヒント付きの変数宣言
    tasks: List[Tuple[str, Path]] = [] # (画像URL, 保存パス)
    
    start_time = time.perf_counter()
    # ページ取得
    res = requests.get(URL, timeout=10) # timeoutで無限待機を防ぐ
    # 検索
    payload = {
        "q": 
    }
    res.raise_for_status
    # 画像URL取得
    soup = BeautifulSoup(res.text, features='html.parser')
    for img_tag in soup.select(''):
        pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='画像検索のキーワード',
        epilog='c:>py image_site_download 青空'
    )
    parser.add_argument(
        'search_word',
        help='画像検索のキーワード'
        )
    args = parser.parse_args()    
    main(args.search_word)
