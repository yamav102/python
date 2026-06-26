#! python3
# downloadXkcd_parallel_improved.py
'''
逐次版：約88分（5300秒）
並列版 (MAX_WORKERS=8)：113.5分（6807秒）

逆に遅くなっています。これはよくある現象です。特にxkcdのような小規模運営のサイトでは、同時接続数を増やしすぎると以下の問題が発生します：サーバー側で接続を遅延させられる（throttling）
TCP接続のオーバーヘッドが増える
一時的にエラーが増えて再試行が発生する
'''
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Final
from urllib.parse import urljoin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_file(url: str, save_path: Path, chunk_size: int = 8192) -> str:
    """ダウンロード実行。結果を文字列で返す"""
    try:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        if save_path.exists():
            size_mb = save_path.stat().st_size / (1024*1024)
            return f"スキップ済み ({size_mb:.1f}MB)"
        
        with requests.get(url, stream=True, timeout=20) as res:
            res.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
        
        size_mb = save_path.stat().st_size / (1024*1024)
        return f"✅ 完了 ({size_mb:.1f}MB)"
    
    except Exception as e:
        return f"❌ エラー: {e}"


def main():
    ROOT_URL: Final[str] = 'https://xkcd.com'
    url = ROOT_URL
    save_folder = Path(__file__).parent / 'xkcd高速版'
    save_folder.mkdir(exist_ok=True)

    MAX_WORKERS = 8          # 6〜10の間で調整してください
    downloaded = 0
    skipped = 0

    print("=== xkcd 並列ダウンロード開始 ===\n")

    start_time = time.perf_counter()

    page_count = 0
    while not url.endswith('#'):
        page_count += 1
        print(f'[{page_count:4d}] ページ取得中 → {url}')
        
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print(f"   ページ取得失敗: {e}")
            break

        soup = BeautifulSoup(res.text, 'html.parser')
        comic_elems = soup.select('#comic img')

        tasks = []
        for img_tag in comic_elems:
            src = img_tag.get('src')
            if not src:
                continue
            comic_url = urljoin(url, src)
            save_path = save_folder / Path(comic_url).name
            tasks.append((comic_url, save_path))

        # 並列実行
        if tasks:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                future_to_path = {
                    executor.submit(download_file, u, p): p 
                    for u, p in tasks
                }
                
                for future in as_completed(future_to_path):
                    result = future.result()
                    print(f"   {result}")
                    
                    if "✅ 完了" in result:
                        downloaded += 1
                    elif "スキップ済み" in result:
                        skipped += 1

        # Prev
        prev_links = soup.select('a[rel="prev"]')
        if not prev_links:
            break
        url = urljoin(ROOT_URL, prev_links[0].get('href'))

    elapsed = time.perf_counter() - start_time

    print("\n=== 完了 ===")
    print(f"新規ダウンロード : {downloaded} ファイル")
    print(f"スキップ         : {skipped} ファイル")
    print(f"総処理ファイル   : {downloaded + skipped} ファイル")
    print(f"処理ページ数     : {page_count} ページ")
    print(f"総実行時間       : {elapsed/60:.1f} 分 ({elapsed:.1f} 秒)")
    print(f"保存先           : {save_folder}")


if __name__ == '__main__':
    main()