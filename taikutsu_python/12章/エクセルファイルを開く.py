# python 3
# P315
# 12.5.3
import openpyxl
from pathlib import Path
import win32com.client
from openpyxl.worksheet.worksheet import Worksheet
# import ファイル（モジュール）とは、書けるが、
# import クラス とは書けない。
# from モジュール import クラス と書くことはできる。
import time

# openpyxlでファイルを作成・保存
# メモリ上にwbがあるだけで、xlが起動しているわけではない。
wb = openpyxl.Workbook()
sheet = wb.active
# assert(isinstance(sheet, openpyxl.worksheet.worksheet.Worksheet)) #動くが、型チェッカーが面倒みてくれないので、よろしくない
assert(isinstance(sheet, Worksheet))

print(type(sheet))
sheet['A1'] = 'Hello world'
print(sheet['A1'].value)

fpath = (Path(__file__).parent / 'output.xlsx').resolve()
wb.save(fpath)
wb.close()

# COM経由でExcelを起動してファイルを開く
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
excel.Workbooks.Open(str(fpath))

# Quit() は呼ばない（呼ばないとExcelは開いたまま残る）
# print("Excelを開きました。スクリプト終了します。")
input(f'{fpath.name} を閉じて、削除します。')
excel.Quit()
time.sleep(1)
fpath.unlink() # 保存した output.xlsx を削除