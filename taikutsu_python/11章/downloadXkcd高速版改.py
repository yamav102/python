#! python3
# downloadXkcd_parallel_optimal.py
'''
最新の実測結果まとめ
逐次版（元のスクリプト）: 6558.9秒 ≈ 109.3分
並列版（MAX_WORKERS=4）: 約112.5分

→ 並列化したのに逆に少し遅くなった状況です。
これはxkcdのサーバーが同時接続に弱い典型的なパターンです。
'''

import requests
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Final
from urllib.parse import urljoin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_file(url: str, save_path: Path, chunk_size: int = 8192) -> str:
    try:
        if save_path.exists():
            size = save_path.stat().st_size / (1024)
            return f"スキップ済み ({size:.1f}KB) - {save_path.name}"
        
        with requests.get(url, stream=True, timeout=15) as res:
            res.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
        
        size = save_path.stat().st_size / (1024)
        return f"✅ 完了 ({size:.1f}KB) - {save_path.name}"
    
    except Exception as e:
        return f"❌ エラー: {type(e).__name__}"


def main():
    ROOT_URL: Final[str] = 'https://xkcd.com'
    url = ROOT_URL
    save_folder = Path(__file__).parent / 'xkcd高速版2'
    save_folder.mkdir(exist_ok=True)

    # ★★★ ここを変更して試してください ★★★
    MAX_WORKERS = 4        # ← 3, 4, 5, 6 で試すのがおすすめ
    
    downloaded = 0
    skipped = 0
    skips = []  
    page_count = 0


    start_time = time.perf_counter()

    print(f"=== xkcd 並列ダウンロード開始 (同時接続数: {MAX_WORKERS}) ===\n")

    while not url.endswith('#'):
        page_count += 1
        if page_count % 50 == 0:
            print(f'[{page_count}] 現在 {url}')

        res = requests.get(url, timeout=10)
        res.raise_for_status()

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

        # 並列ダウンロード                          
        if tasks:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {
                    executor.submit(download_file, u, p): (u, p) 
                    for u, p in tasks
                }
                
                for future in as_completed(futures):
                    result = future.result()
                    print(f"   {result}")
                    comic_url, save_path = futures[future]

                    if "✅ 完了" in result:
                        downloaded += 1
                    elif "スキップ" in result:          # 「スキップ」という文字を含むかで判定
                        skipped += 1
                        comic_url, save_path = futures[future]
                        skips.append(f"{save_path.name}  →  {comic_url}")
 
        # Prev
        prev_links = soup.select('a[rel="prev"]')
        if not prev_links:
            break
        url = urljoin(ROOT_URL, prev_links[0].get('href'))

    elapsed = time.perf_counter() - start_time

    print("\n=== 完了 ===")
    print(f"同時接続数       : {MAX_WORKERS}")
    print(f"新規ダウンロード : {downloaded} ファイル")
    print(f"スキップ         : {skipped} ファイル")
    print(f"総処理ファイル   : {downloaded + skipped} ファイル")
    print(f"処理ページ数     : {page_count} ページ")
    print(f"総実行時間       : {elapsed/60:.1f} 分 ({elapsed:.1f} 秒)")

    # スキップされた画像一覧
    if skips:
        print(f'\n--- スキップされた画像 ({len(skips)} 件) ---')
        for item in skips:
            print(item)
    else:
        print("\nスキップされた画像はありませんでした。")

if __name__ == '__main__':
    main()