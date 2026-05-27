#!python3
# test6.py
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from pathlib import Path
def search_o_dan(keyword="猫"):
    options = uc.ChromeOptions()
    #options.headless = False  # 最初はFalseで確認
    options.add_argument("--start-maximized")
    
    # ← ここが重要：自分のChromeバージョンに合わせる
    driver = uc.Chrome(
        options=options,
        version_main=148          # ← あなたのChromeバージョンに変更
    )
    
    try:
        driver.get("https://o-dan.net/ja/")
        time.sleep(4)
        
        driver.find_element(By.ID, "q").send_keys(keyword)
        driver.find_element(By.ID, "qBtn").click()
        
        time.sleep(6)                    # 待機を長めに
        driver.execute_script("window.scrollTo(0, 2000)")
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, 4000)")
        time.sleep(4)
        
        # HTML保存
        save_path = Path(__file__).parent / 'odan_final.html'
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # 本物の画像URLを抽出
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"imgタグ総数: {len(images)}")
        
        urls = []
        for img in images:
            src = img.get_attribute("src") or img.get_attribute("data-src") or img.get_attribute("data-original")
            if src and ("unsplash.com" in src or "pixabay.com" in src or "images." in src):
                urls.append(src)
        
        print(f"有用な画像URL数: {len(urls)}")
        for url in urls[:8]:
            print(url)
            
    finally:
        # driver.quit()
        pass

search_o_dan("猫")