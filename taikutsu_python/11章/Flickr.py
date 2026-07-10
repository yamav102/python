#! python3
# 退屈な事はpythonにやらせよう:11.10.2 画像サイトダウンローダー
# Flickr.py
# usage:py Flickr cat white
import sys
import requests
import bs4
import os
from pathlib import Path
from urllib.parse import urljoin
def download_file(url: str, save_path: Path, chunk_size: int = 8192) -> tuple[str, bool]:
    """画像をダウンロード。結果を文字列で返す"""
    try:
        # 同じ url のファイルはスキップ
        if save_path.exists():
            size_kb = save_path.stat().st_size / 1024
            return f"スキップ済み ({size_kb:.1f}KB)", False
        
        with requests.get(url, stream=True, timeout=20) as res:
            res.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            size_kb = save_path.stat().st_size / 1024
        return f"✅ 完了 ({size_kb:.1f}KB)", True
        
    except Exception as e:
        return f"❌ エラー: {type(e).__name__}", False

def main()->None:
    save_cnt = 0
    MAX_IMAGE = 3
    DIR = 'Flickr_img'
    os.makedirs(Path(__file__).parent / DIR, exist_ok=True)

    keyword = ' '.join(sys.argv[1:])

    # Flickr
    base_url = 'https://www.flickr.com/'
    res = requests.get(base_url + 'search/?text=' + keyword)
    res.raise_for_status()

    # tag検索
    soup = bs4.BeautifulSoup(res.text, 'lxml') # lxml:高速パーサー
    # links = soup.select('.photo-list-photo-view')
    imgs = soup.select('.photo-list-photo-container img')
    for i in range(min(MAX_IMAGE, len(imgs))):
        # SRC PickUp
        src = str(
            imgs[i].get('data-src') or 
            imgs[i].get('data-original') or 
            imgs[i].get('data-lazy') or 
            imgs[i].get('src')
            ).strip()

        if src:
            # パス記述の相異を吸収する
            img_url = urljoin(base_url, src)
            print(img_url)

            # img Save            
            save_path = img_url.split('/')[-1]
            save_path=Path(__file__).parent / DIR / save_path
            message, success = download_file(img_url, save_path=save_path)
            print(message)
            if success:
                save_cnt += 1
            
    print('--------------------------------------------------')
    print(f'{save_cnt} ファイルの画像をダウンロードしました。')

if __name__ == '__main__':
    main()

    
