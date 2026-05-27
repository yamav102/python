#!python3
# test5.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
def search_with_selenium(keyword="猫"):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")   # 最初はコメントアウト（動作確認用）
    
    # ユーザーエージェント
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("ページを開いています...")
        driver.get("https://o-dan.net/ja/")
        time.sleep(3)
        
        # 検索ワード入力
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "q"))
        )
        search_box.clear()
        search_box.send_keys(keyword)
        
        # 検索実行
        submit_btn = driver.find_element(By.ID, "qBtn")
        submit_btn.click()
        
        print("検索実行後、結果を待機中...")
        time.sleep(5)  # 画像読み込み待ち
        
        # 少しスクロールしてさらに画像をロードさせる
        driver.execute_script("window.scrollTo(0, 1500);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 3000);")
        time.sleep(3)
        
        # HTML保存
        html = driver.page_source
        save_html = Path(__file__).parent / 'odan_selenium_result.html'
        with open(save_html, "w", encoding="utf-8") as f:
            f.write(html)
        
        print("HTMLを odan_selenium_result.html に保存しました")
        
        # imgタグの数を確認
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"検出されたimgタグ数: {len(images)}")
        
        # 実際の画像URLをいくつか表示
        for img in images[:10]:
            src = img.get_attribute("src") or img.get_attribute("data-src") or img.get_attribute("data-original")
            if src and ("http" in src) and not src.startswith("data:"):
                print(src[:150])  # 長くなりすぎないように
        
    except Exception as e:
        print(f"エラー発生: {e}")
    finally:
        # driver.quit()   # 終了したくなければコメントアウト
        pass

# 実行
search_with_selenium("猫")