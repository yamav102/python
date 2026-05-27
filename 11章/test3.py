#!python3
# test3.py
# ダウンロードしたファイルをハードドライブに保存する
# textファイルを保存するには、書き込みバイナリモード(wb)を指定する。
# w、wt を指定すると、実行 os に沿った改行コードに置き換えられるので、
# バイト列を変えずにファイルに書き込みたい場合は 'wb' である必要がある。
import requests
import sys
from pathlib import Path
# 保存パス
savefile = Path(__file__).parent / 'RomeoAndJuliet.txt'
try:
    res = requests.get(
        'https://automatetheboringstuff.com/files/rj.txts'
        )
    # requests.getで問題が起きたか検知する
    res.raise_for_status()
except Exception as e:
    print(f'エラー:{e}',file=sys.stderr)
    sys.exit(1) # 0 以外でエラー終了を表す慣習
    
with open(savefile, 'wb') as play_file:
    # 100キロバイトのchunk(塊)
    for chunk in res.iter_content(100000): 
        # print(len(chunk))
        # 100000
        
        # 74126
        # write は、書き込んだバイト数を返す
        chnk_len= play_file.write(chunk) 
        print(chnk_len)
        print(str(type(chunk))) # <class 'bytes'>
