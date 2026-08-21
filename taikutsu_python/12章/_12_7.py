# python3
# P319 12.7
# _12_7.py
# セルのフォントスタイルを設定する
import openpyxl
from openpyxl.styles import Font # from module import class Fontオブジェクトを返すコンストラクタという理解で良い
import win32com.client
from typing import cast
from openpyxl.cell.cell import Cell
from pathlib import Path

wb = openpyxl.Workbook()
# sheet = wb['Sheet']
sheet = wb.worksheets[0] # 1番目のworksheet

# rng = sheet['A1']
# cell | mergedcell で、
# mergedcell に .value は無いので型チェッカーが警告を出すのを cast で防いでいる。
rng = cast(Cell, sheet.cell(1,1)) 

italic24_font = Font(size=24, italic=True)
rng.font = italic24_font
rng.value = 'Hello World!' 

tgtpath = Path(__file__).parent / '_12_7.xlsx'
wb.save(tgtpath) # 保存していないメモリ上だけにある wb を excel で開くことは出来ない。
wb.close()

# # COM経由でExcelを起動してファイルを開く
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
excel.Workbooks.Open(str(tgtpath))

# # Quit() は呼ばない（呼ばないとExcelは開いたまま残る）
# # print("Excelを開きました。スクリプト終了します。")
# input(f'{fpath.name} を閉じて、削除します。')
# excel.Quit()