#! python3
# _12_14_5.py
# ブックを開く。シートの１列毎の全行を、
# 一行ずつテキストファイルへ出力して保存。
import openpyxl
import argparse
import sys
from pathlib import Path
from typing import cast
from openpyxl.cell.cell import Cell
def mk_save_name(path:str | Path)->Path:
    if not type(path) == Path:
        p = Path(path).resolve()
    cand = p # cand:candidate>候補    
    i = 1
    while cand.exists():        
        # with_name は parent はそのままで、
        # ファイル名部分のみ差し替えるメソッド
        cand = p.with_name(f'{(p.stem).upper()}({i}){p.suffix}')
        i += 1
    return cand
def main(xlsxpath:Path)->None:
    wb = openpyxl.load_workbook(xlsxpath, data_only=True)
    ws = wb.worksheets[0]
    # ↓この書き方で min_column～max_columnの範囲をループしてくれる。
    for col in ws.columns:
        if all(cell.value is None for cell in col):# →(True, True, ...)
            continue
        letter = cast(Cell, col[0]).column_letter
        # with_name パスはそのままでファイル名部分だけ差し替える
        out = xlsxpath.with_name(f'{letter}.txt')
        out = mk_save_name(out)

        lines = [
            '' if cell.value is None else str(cell.value)
            for cell in col
        ]
        # 最後のセルが空白でなくなるまで lines を詰める
        while lines and lines[-1]=='': # 列タプルに要素があって、且つ、タプルの最後が空白
            lines.pop() # 引数なしで、最後の要素を詰める
        # with out.open('w', encoding='utf-8') as f:
        #     f.write('\n'.join(lines)+'\n')
        # out はPathオブジェクトなので、以下の書き方が出来る。
        out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    # for clm in ws.columns:

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='.xlsx シートの列の値を、.txt へ出力します。',
        epilog=f'py {Path(sys.argv[0]).name} hoge.xlsx'
    )
    parser.add_argument(
        'xlsxpath',
        type=Path,
        help='excelブックのパス'
    )
    args = parser.parse_args()
    main(args.xlsxpath)