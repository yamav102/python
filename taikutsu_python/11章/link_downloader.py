#! python3
# link_downloader.py
# 退屈な事は python にやらせよう P297 11章演習プロジェクト 11.10.4
# Webページの URL を指定すると、そのページからリンクされたすべてのページをダウンロードするプログラム
# ステータスコードが 404となるページには リンク切れ を表示する。
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm # tqdm:アラビア語で進捗を表す言葉から来ているらしい。

def download_file(url: str, save_path: Path, chunk_size: int = 8192) -> str:
    """リンクをダウンロード。結果を文字列で返す"""
    try:
        if save_path.exists():
            size_kb = save_path.stat().st_size / 1024
            return f"スキップ済み ({size_kb:.1f}KB)"
        
        with requests.get(url, stream=True, timeout=20) as res:
            res.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            size_kb = save_path.stat().st_size / 1024
        return f"✅ 完了 ({size_kb:.1f}KB)"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # print(f'404 Not Found:{url}') # tqdm と printを同時に使うと出力が乱れる場合があるので、 tqdm.writeを使う。
            tqdm.write(f'404 Not Found:{url}')
            return f"❌ 404 Not Found: {type(e).__name__}" # ZeroDivisionError であれば文字列 "ZeroDivisionError" が返ります。    
        else:            
            # print(f"❌ エラー: {type(e).__name__}-{url}")
            tqdm.write(f"❌ エラー: {type(e).__name__}-{url}")
            return f"❌ エラー: {type(e).__name__}"
            
    except Exception as e:
        # print(f"❌ エラー: {type(e).__name__}-{url}")
        tqdm.write(f"❌ エラー: {type(e).__name__}-{url}")
        return f"❌ エラー: {type(e).__name__}"

# import asyncio # ファイルDL のような時間が掛かる処理の場合の非同期処理
# async def main(url: str)->None:
def main(url: str)->None:    
    # async を付けたメソッドを コルーチンという。
    # 通常、関数は一度呼び出されると最後まで一気に実行されますが、
    # コルーチンは呼び出し元と処理を譲り合いながら効率的に並行処理を行います。
    # await asyncio.sleep(1)

    # DLファイル保存場所
    save_folder= Path(__file__).parent / 'link_downloadedfiles'
    save_folder.mkdir(exist_ok=True)
    
    # url hrefを取得
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f'ページ取得失敗:{url} - {e}')
        raise # 例外を上へ伝搬
    soup = BeautifulSoup(res.text, 'lxml')
    # リンクの src と 保存パスのリストを取得
    MAX_WORKERS = 10
    tasks: list[tuple[str, Path]] = []
    link_tags = soup.select('a')
    for i in range(len(link_tags)):
        href = str(
            link_tags[i].get('href') 
        )
        link_url = urljoin(url, str(href))
        save_path = save_folder / Path(link_url).name # name:末尾のフォルダ名/ファイル名を取得
        tasks.append((link_url, save_path))
    
    skips = []
    downloaded = 0
    skipped = 0
    err404 = 0
    anotherErr = 0
    # 一括並列ダウンロード
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 「辞書内包表記 (dictionary comprehension)」
        # Future は「まだ完了していない処理の結果を将来受け取るための入れ物」という意味です。
        future_to_task = {executor.submit(download_file, u, p):(u ,p) for u, p in tasks}
        # 👆を判りやすく書くと👇
        # future_to_task = {}　# {}は、辞書型
        # for u, p in tasks:
        #     future = executor.submit(download_file, u, p)
        #     future_to_task[future] = (u, p)
        
        # 進捗表示
        for future in tqdm(as_completed(future_to_task), total=len(tasks), desc='ダウンロード進捗'):
            result = future.result()
            link_url, save_path = future_to_task[future]

            if "✅ 完了" in result:
                downloaded += 1
            elif "404" in result:                
                err404 += 1
            elif "❌ エラー" in result:
                anotherErr += 1
            elif "スキップ済み" in result:
                skipped += 1
                # skips.append(f"{save_path.name}  →  {link_url}")

    print("\n=== すべての処理が完了しました ===")
    print(f"新規ダウンロード : {downloaded} ファイル")
    print(f"スキップ         : {skipped} ファイル")
    print(f"404Error         : {err404} ファイル")
    print(f"他エラー         : {anotherErr} ファイル")
    print(f"総処理           : {len(tasks)} ファイル")            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('targetUrl') # 引数名
    # parser.add_argument('targetUrl2') # 2つ目の引数→この書き方は「位置引数の指定」
    parser.add_argument(
        'url', 
        nargs=1, # 引数の数を定義できる
        help='ダウンロードするリンクのあるURLを渡します。',
        ) 
    args = parser.parse_args() # 受け取った引数
    # print(args.target)
    # asyncio.run(main(args.url))
    main(args.url[0]) # https://yamav102.github.io/HomePage/htm_file/keijibann.htm