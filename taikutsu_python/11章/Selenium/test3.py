#! python3
# test3.py
from playwright.sync_api import sync_playwright
import time
from pathlib import Path
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 検索実行
    page.goto("https://o-dan.net/ja/")
    page.fill("#q", "猫")                    # 検索ワード入力
    page.check("input[name='sCc']")          # 商用利用可チェック（必要なら）
    page.click("input[type='submit']")       # または page.press("#q", "Enter")
    
    # 結果がロードされるまで待つ
    page.wait_for_load_state("networkidle")
    time.sleep(3)  # 画像読み込み待ち（調整可能）
    
    # HTML全体を取得
    html = page.content()
    save_html = Path(__file__).parent / 'odan_full.html'
    with open(save_html, "w", encoding="utf-8") as f:
        f.write(html)
    
    # 画像URLをすべて抽出
    images = page.eval_on_selector_all("img", "imgs => imgs.map(img => img.src || img.dataset.src)")
    print(f"取得した画像URL数: {len(images)}")
    for img in images[:10]:  # 最初の10個だけ表示
        print(img)
    
    browser.close()