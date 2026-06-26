#! python3
# test4.py
from playwright.sync_api import sync_playwright
import time
from pathlib import Path
def search_o_dan(keyword: str):
    with sync_playwright() as p:
        # ブラウザ起動オプション（重要）
        browser = p.chromium.launch(
            #headless=False,           # 最初はFalseで動作確認（後でTrueに）
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-infobars',
                '--disable-extensions',
            ]
        )
        
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            locale="ja-JP",
        )
        
        # Stealth対策（自動化痕跡を隠す）
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['ja-JP', 'ja']});
        """)
        
        page = context.new_page()
        
        try:
            print("ページにアクセス中...")
            page.goto("https://o-dan.net/ja/", wait_until="domcontentloaded")
            time.sleep(2)
            
            print("検索ワード入力中...")
            page.fill("#q", keyword)
            
            # 商用利用可チェック（必要なら）
            # page.check("input[name='sCc']")
            
            print("検索実行...")
            page.click("#qBtn")          # submitボタン
            # または page.press("#q", "Enter")
            
            # 結果読み込み待ち（重要）
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(4)   # 画像が遅れてロードされるため余裕を持たせる
            
            print("HTML取得中...")
            html = page.content()
            
            save_html = Path(__file__).parent / 'odan_result2.html'
            with open(save_html, "w", encoding="utf-8") as f:
                f.write(html)
            
            # 画像URL抽出
            images = page.eval_on_selector_all("img", """
                imgs => imgs.map(img => ({
                    src: img.src,
                    data_src: img.dataset.src || img.getAttribute('data-src'),
                    alt: img.alt
                }))
            """)
            
            print(f"検出された画像数: {len(images)}")
            for img in images[:15]:
                src = img['src'] or img['data_src']
                if src and 'http' in src:
                    print(src)
                    
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            browser.close()

# 使用例
search_o_dan("猫")