#! python3
# 12.14.4
# P333
# テキストファイル（複数可）を読み込む。
# 1ファイルで1列使う。ファイルの行はシートの行に対応して格納する。
import openpyxl
import argparse
import sys
from pathlib import Path
import os
from typing import cast
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
# from typing import Union
def chkfile_existing(path:str)->str:
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f'ファイルがありません:{path}')
    return path
# 上書きしないファイルパスを返す
def mk_save_name(xlpath:str)->str:
    p = Path(xlpath)
    cand = p # cand:candidate>候補    
    i = 1
    while cand.exists():        
        # with_name は parent はそのままで、
        # ファイル名部分のみ差し替えるメソッド
        cand = p.with_name(f'{p.stem}({i}){p.suffix}')
        i += 1
    return str(cand)
# 可変長引数の場合、要素の型（str や Path）を直接指定します
# def main(*txtpath:tuple)->None:
# def main(*txtpath:Union[str, Path])->None:
# *仮引数名 で　受け取った値をタプルとして処理する
def main(*txtpath:str | Path)->None: # | は python 3.10以降でサポートされている
    savename = txtpath[0]
    savename = Path(savename).stem
    wb = openpyxl.Workbook()
    ws = cast(Worksheet, wb.active)
    clm = 0
    for path in txtpath:
        clm += 1
        with open(file=path, mode="r", encoding="utf-8") as f:
            # TODO ファイル一つづつA,B,C…列へ、一行を一セルへ転写していく
            rw = 0
            for line in f:
                rw += 1
                cast(Cell, ws.cell(rw, clm)).value = line.rstrip('\n')
    wb.save(mk_save_name(savename + '.xlsx'))
    

if __name__ == '__main__':    
    parser = argparse.ArgumentParser(
        description='1つ以上の txtファイルの中身を列に格納したエクセルファイルを生成します。',
        epilog=(
            f'py {Path(sys.argv[0]).name} a.txt \n'
            f'py {Path(sys.argv[0]).name} a.txt b.txt c.txt'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter, # 改行を保持する
    )
    parser.add_argument(
        'textfiles',
        nargs='+', # 引数の数 1つ以上の指定
        type=chkfile_existing, 
        # type= は「型名」専用ではなく、文字列を1つ受け取って値を返す callable を渡す。
        # 例: type=int なら内部で int('42') のように変換する。
        # chkfile_existing も同じ枠で、存在チェックしてパス文字列を返す自作関数を渡している。
        help='読み込む txt ファイルのパス（1つ以上）',        
    )
    args = parser.parse_args()
    # args は narg='+' の指定で listになる。
    # iterable に * を付けると、バラの引数として渡せる
    main(*args.textfiles)