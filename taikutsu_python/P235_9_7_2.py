#! python3
# P235_9_7_2.py
# 巨大ファイルを探す
import os
from pathlib import Path
import argparse

# '100MB' を渡し、バイト数に変換した数値を返す
def _parse_size(size_str:str)->int:
    size_str = size_str.strip().upper()
    if size_str.endswith('MB'):
        num = size_str[:-2]
    elif size_str.endswith('M'):
        num = size_str[:-1]
    else:
        num = size_str
    try:
        return int(num) * 1024 ** 2
    except ValueError:
        raise ValueError(
            f'サイズの指定が不正です: {size_str} '
            '（例: 100MB または 100）'
        )
'''
windows10以降 ファイルパス文字数260文字制限対応：
powershell(管理者権限)
--------
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
--------
最大32,767文字 まで扱えるようになります
'''    
def main(fileMBsize:str,dirpath: str)->None:
    root = Path(dirpath).resolve()
    filesize = _parse_size(fileMBsize)
    print('巨大ファイルを検索します。\n'
          f'{fileMBsize} より大きい。\n'
          f'検索場所: {root}'
          )
    cnt = 0
    errors = []
     
    # 本処理でサブディレクトリは使われないため _ で表記
    for curdir, _, files in os.walk(root):
        for file in files:
            try:   
                filepth = Path(curdir) / file
                if filepth.stat().st_size > filesize:
                    print(filepth.resolve())
                    cnt += 1
            except Exception as e:
                errors.append(f'予期しないエラー{e}')                              
    print(f'{cnt} ファイルを抽出しました。エラー{len(errors)} 件')
    if len(errors):
        print('err ---------------')
        for err in errors:            
            print(err)
        print('/err ---------------')
# import された場合に、実行されないようにする if文
if __name__ == '__main__':
    # e:\GitHub\yamaPythonScripts>python test.py -h とコマンドラインで指定すると、使い方が表示される。
    parser = argparse.ArgumentParser(
        description='指定フォルダパス以下にある、指定サイズを超えるファイルパスを抽出します。',
        epilog='例：python test.py 100MB C:\\Users'
    )
    parser.add_argument('fileMBsize',
                        help='100MB または、100 のように指定します。'
                        )
    parser.add_argument('dirpath',
                        help='調査するフォルダパスを指定します。'
                        )
    args = parser.parse_args()

    main(args.fileMBsize, args.dirpath)
    