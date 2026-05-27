#! python3
# sendmail.py
'''
mailaddress 本文テキストを受け取り、宛先へ送信する
ログインの動作はロボット避けや２段階認証仕様で自動化困難なので、
Google API:Google Cloud Console にログインして、
credentials.json を作成して、本スクリプトのフォルダに保存して実行。
結論：Selenium で安定してe-mailを自動送信させる事は現実的ではない。
send_gmail.py でGooGle API バージョンを実現している。
'''
import argparse
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

def loginpageopen()->webdriver:
    '''
    ログイン済みのGmailを開く
    '''
    options = Options()
    # ポートを合わせる
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  

    # EdgeDriverのパス（最新のものをselenium-managerか手動で用意）
    driver = webdriver.Edge(options=options)

    driver.get("https://mail.google.com/mail/u/0/#inbox")
    print("既存セッションに接続しました")
    time.sleep(5)  # 必要に応じて待機   
    return driver

def main(args: argparse.Namespace)->None:
    address = args.mailaddress
    subject = args.subject
    body = args.body
    # print(f'address:{address}')
    # print(f'subject:{subject}')
    # print(f'body:{body}')
    '''
    gmailページを開く
    ログインする
    新規メールを作成する
    宛先を設定、件名を設定、本文を設定
    送信する
    '''
    browser = loginpageopen()
    input('Enterキーで終了します。')
    browser.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='arg1:メールアドレス arg2:件名 arg3:本文',
        epilog='c:>py sendmail aaa@gmail.com test送信 こんにちは'
    )
    parser.add_argument(
        'mailaddress',
        help='メールアドレス'
        )
    parser.add_argument(
        'subject',
        help='件名'
    )
    parser.add_argument(
        'body',
        help='メール本文'
    )    
    args = parser.parse_args() 
    
    main(args) 