#! python3
# 退屈な事はPythonにやらせよう P297 11.10.3
# https://play2048.co/ のゲームをブラウザで開き上下左右キーを送信し続けてゲームを進める

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import random
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 上下左右キーをランダムで n回実行
def main(n: int)->None:
    # Webbrowser 起動
    service = Service(
        log_output="geckodriver.log",     # 同じフォルダに保存
        service_args=['--log', 'info']    # 必要に応じて debug / trace に変更
    )

    driver = webdriver.Firefox(service=service)

    # 2048のページへ移動
    url = 'https://play2048.co/'
    driver.get(url)    
    
    # ★★★ ゲームの読み込みを確実に待機する ★★★
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    # JavaScriptでページが完全に読み込まれたか確認
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(0.8)  # 少し余裕を持たせる    

    html_body = driver.find_element(By.TAG_NAME, 'html')
    arrows_base = [Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT]
    for i in range(n):
        print(f'{i+1}回目/{n}')
        # 基本 右→上→右→上 が 2048 は良い結果が出るらしい→そうでもない？？
        # GAME OVER になりがちなダメプログラム
        # html_body.send_keys(Keys.RIGHT) 
        # html_body.send_keys(Keys.UP) 
        arrows =  arrows_base[:] # shallow copy [:]スライスを獲る事で参照コピーになる事を回避している
        random.shuffle(arrows)                
        # html_body.send_keys(arrows[0])
        # if i % 2 == 0: # 剰余
        #     html_body.send_keys(Keys.UP) 
        #     html_body.send_keys(Keys.RIGHT)
        for key in arrows:
            html_body.send_keys(key)        
        time.sleep(.5) # .5秒待機
    input('Enterキーで終了')
    driver.quit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ValueError('方向キー実行回数を指定して下さい。')
    main(int(sys.argv[1]))