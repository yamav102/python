#! python3
# downloadXkcd.py
'''
Webコミック http://xkcd.com/ から画像をダウンロードして HDに保存する。
'''
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Final
from urllib.parse import urljoin
import time

def download_file(
        url: str,                   # dl元URL
        save_path: str,             # 保存先パス
        chunk_size: int = 8192)->None:
    '''
    url のファイルを save_path に保存する
    8192=8Kbyte 大き過ぎず小さ過ぎない「ちょうどいいサイズ」。
    公式ドキュメントでも良く使われる値。    
    '''        
    save_path = Path(save_path)    
    # 保存パス親ディレクトリが無い場合も自動作成
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # url の Responseを取得
    with requests.get(url, stream=True) as res: # Responseオブジェクトが戻る
        res.raise_for_status() 
        with open(save_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=chunk_size):
                if chunk: 
                    # if chunk の理由。
                    # iter_content は最後に空のchunkを返す可能性がある
                    # 空のchunkをwrite()すると無駄な処理になる（稀に問題を起こすことも）
                    f.write(chunk)

def main():
    ROOT_URL:Final[str] = 'https://xkcd.com' # 開始URL（Finalは定数である事を型チェッカーに伝えている）
    url = ROOT_URL
    # breakpoint() #test　vba の stopに相当する。
    url = ROOT_URL 
    save_folder = Path(__file__).parent / 'xkcd'
    Path.mkdir(save_folder, exist_ok=True)

    # Prevボタンで一つ前の画面に遷移する。最初のページは、https://xkcd.com/1/# で、
    # これ以上は、前の画面に戻れない。
    while not url.endswith('#'):
        # ページをダウンロードする
        print('ページをダウンロード中 {}...'.format(url))
        res =requests.get(url) # Responseオブジェクトが戻る
        res.raise_for_status()    

        # ページのソースからコミック画像のURLを見つける
        ## <div id="comic">内の<img>
        ### #comic 内の img 
        soup = BeautifulSoup(res.text, features='html.parser')    
        comic_elem = soup.select('#comic img') # bs4.element.ResultSetが戻る

        if comic_elem == []:
            print('コミック画像が見つかりませんでした。')
        else:
            comic_url = '' # 初期化
            image_count = len(comic_elem)
            print('{}画像をダウンロード中 {}...'.format(image_count, comic_url))
            for i in range(image_count):
                src = comic_elem[i].get('src')
                if not src:
                    continue
                comic_url = urljoin(url, src)
                # src のパス指定には、
                # プロトコル相対パス、ルート相対パス、./../ 等の相対パスがある。
                # プロトコル相対パス。例: <img src="//imgs.xkcd.com/comics/crystal_gazing.png" ←絶対パスからプロトコルを除いて記述する書式
                # ルート相対パス　例：<img src="/2067/asset/challengers_header.png" ←最上位パスより下のパスを記述する書式
                # 場合分けして手作業で絶対パスを取得するのは手間がかかる。
                # urljoinを使うと、安全に絶対パスを取得できる。

                # 画像をダウンロードする  
                filename = Path(comic_url).name
                save_path = save_folder / filename
                if save_path.exists():
                    print(f'スキップ（既存）{filename}')
                    continue
                download_file(comic_url, save_path)

        # PrevボタンのURLを取得する
        prev_link = soup.select('a[rel="prev"]')[0]
        url = ROOT_URL + prev_link.get('href')

    print('完了') 

if __name__ == '__main__':
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f'実行時間：{end - start}秒')