#! python3
# mapIt.py
# webbrowserモジュールを用いる
# コマンドラインやクリップボードに指定した住所の地図を開く
import argparse
import logging
from pathlib import Path
import webbrowser
import sys
import pyperclip
def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    # force = True は basicConfigの引数で、個別に指定する場合は使えない。
    # handlers.clear する事で、出力先もformatter も初期化される。
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s %(message)s'
    )
    file_handler = logging.FileHandler(
        Path(__file__).parent / 'mapIt.log',
        encoding='utf-8'
    )
    
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)
    
if len(sys.argv) > 1:
    # コマンドラインから住所を取得する
    address = ' '.join(sys.argv[1:]) # argv[0]:ファイル名を除外して繋いでいる

# todo: クリップボードから住所を取得する    
else:
    address = pyperclip.paste()
    
webbrowser.open('https://www.google.com/maps/place/' + address)    


    
if __name__ == '__main__':
    setup_logging()
    parser = argparse.ArgumentParser(
        description='ここに何をするスクリプトなのかの説明を書く',
        epilog='例）>python test.py c:\\mydir Spam --suffix .txt --min-number 5'
    )
    parser.add_argument(
        '引数名',
        help='引数の説明を書く'
        )
    # ...