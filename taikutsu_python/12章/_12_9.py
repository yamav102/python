#! python3
# _12_9.py
# P321

# 数式
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet 
from pathlib import Path
import jaconv
import time
# import win32com 
# # win32com は　module だが、下位の .client まで 
# import しないと Dispatch 関数を使う事は出来ない
import win32com.client

wb = openpyxl.Workbook()
sheet = wb.active
print(type(Worksheet))
assert isinstance(sheet, Worksheet)
sheet['a1'] = 200 
sheet['a2'] = 300
sheet['a3'] = '=sum(a1:a2)'
xlPath = Path(__file__).parent / 'writeFormula.xlsx'
if (
    not xlPath.exists()
    or 
    jaconv.zen2han(input(f'上書きしますか？\n{xlPath.name}(y/n)').strip().lower(), ascii=True) == 'y'
    ):
    wb.save(xlPath)
    wb.close
    time.sleep(.5)
    xlapp = win32com.client.Dispatch('Excel.Application')
    xlapp.visible = True
    xlapp.Workbooks.Open(xlPath)
else:
    print('保存はキャンセルされました。')    

