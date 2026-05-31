#! python3
# downloadXkcd_bulk_parallel.py
'''
おめでとうございます！ 大幅高速化に成功しました！結果まとめ項目
以前の逐次版
以前の並列版
今回（一括並列版）
改善度
総実行時間
約109分
約112分
49.1 分
約2.2倍
総処理ファイル
3290前後
3290前後
3292
-

約60分近く短縮されました。非常に良い結果です。

By Grok
'''
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Final, List, Tuple
from urllib.parse import urljoin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm   # pip install tqdm がまだなら実行してください

def download_file(url: str, save_path: Path, chunk_size: int = 8192) -> str:
    """画像をダウンロード。結果を文字列で返す"""
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
    
    except Exception as e:
        return f"❌ エラー: {type(e).__name__}"


def main():
    ROOT_URL: Final[str] = 'https://xkcd.com'
    save_folder = Path(__file__).parent / 'xkcd高速版3'
    save_folder.mkdir(exist_ok=True)

    MAX_WORKERS = 12          # ← ここを調整（8〜20くらいが現実的）
    tasks: List[Tuple[str, Path]] = []   # (画像URL, 保存パス)
    page_count = 0
    start_time = time.perf_counter()

    print("=== Phase 1: 全コミックページを巡回して画像URLを収集中 ===\n")

    url = ROOT_URL
    while not url.endswith('#'):
        page_count += 1
        if page_count % 500 == 0:
            print(f"  {page_count} ページまで収集完了...")

        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print(f"ページ取得失敗: {url} - {e}")
            break

        soup = BeautifulSoup(res.text, 'html.parser')
        
        for img_tag in soup.select('#comic img'):
            src = img_tag.get('src')
            if not src:
                continue
            comic_url = urljoin(url, str(src))
            save_path = save_folder / Path(comic_url).name
            tasks.append((comic_url, save_path))

        # Prevリンク
        prev_links = soup.select('a[rel="prev"]')
        if not prev_links:
            break
        url = urljoin(ROOT_URL, str(prev_links[0].get('href')))

    print(f"\n=== Phase 1 完了 ===")
    print(f"総ページ数: {page_count}")
    print(f"収集した画像数: {len(tasks)} 個\n")

    # Phase 2: 一括並列ダウンロード
    print(f"=== Phase 2: 一括並列ダウンロード開始 (同時接続数: {MAX_WORKERS}) ===\n")

    downloaded = 0
    skipped = 0
    skips = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_task = {executor.submit(download_file, u, p): (u, p) 
                         for u, p in tasks}
        
        for future in tqdm(as_completed(future_to_task), total=len(tasks), desc="ダウンロード進捗"):
            result = future.result()
            comic_url, save_path = future_to_task[future]
            
            if "✅ 完了" in result:
                downloaded += 1
            elif "スキップ済み" in result:
                skipped += 1
                skips.append(f"{save_path.name}  →  {comic_url}")

    elapsed = time.perf_counter() - start_time

    print("\n=== すべての処理が完了しました ===")
    print(f"新規ダウンロード : {downloaded} ファイル")
    print(f"スキップ         : {skipped} ファイル")
    print(f"総処理           : {len(tasks)} ファイル")
    print(f"総実行時間       : {elapsed/60:.1f} 分 ({elapsed:.1f} 秒)")

    if skips:
        print(f"\n--- スキップされた画像 ({len(skips)} 件) ---")
        for item in skips[:20]:          # 多すぎる場合は先頭20件だけ表示
            print(item)
        if len(skips) > 20:
            print(f"... 他 {len(skips)-20} 件")


if __name__ == '__main__':    
    main()