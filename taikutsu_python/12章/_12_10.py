#! python3
# P323
# _12_10.py
# 行と列を調整する
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from pathlib import Path
def main():
    wb = openpyxl.Workbook()
    sheet = wb.active
    assert isinstance(sheet, Worksheet)
    sheet['a1'] = 'Tall row'
    sheet['b2'] = 'Wide column'
    sheet.row_dimensions[1].height = 70 # 行1 の dimention:寸法 vbaのrows(1).rowheight = 70
    # 単位は ポイント（pt） です。1ポイントは 1/72 インチ（約0.35mm）です。

    sheet.column_dimensions['b'].width = 20 # 列Bの寸法 vbaのcolumns("b").columnwidth=20
    # 単位は 標準フォント（標準スタイル）での「半角文字の数」です. ポイントではない。
    # 列幅のポイントを python で取得する事が出来ないため、ポイント数を見ながら width を微調整して
    # ポイントで列幅を指定する、という方法をとる事もできない。

    xlpath = Path(__file__).parent / 'dimentions.xlsx'
    wb.save(xlpath)

if __name__ == '__main__':
    main()


