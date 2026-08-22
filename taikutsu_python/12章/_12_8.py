#! python3
# _12_8.py
# Fontオブジェクト
import openpyxl
from openpyxl.styles import Font
from pathlib import Path
import win32com.client # module
import time
import jaconv

wb = openpyxl.Workbook()
sheet = wb['Sheet']
font_obj1 = Font(name= 'Times New Romoan', bold=True)
rngA1 = sheet['a1']
rngA1.font = font_obj1
# sheet['a1'] = 'Bold Times new Roman' ←とは、書ける。
# cellオブジェクトの変数を使った場合 .value を使わないと、
# 文字列オブジェクトで cell オブジェクトを上書きしてしまうだけ。
rngA1.value = 'Bold Times new Roman'
font_obj2 = Font(size=24, italic=True)
rngB3 = sheet['b3']
rngB3.font = font_obj2
rngB3.value = '24 pt Italic'
rngC4 = sheet['c4']
# sheet['c4'] = '=sum(1,2)' とは書ける。
rngC4.value = '=sum(1,2)'
savepath = Path(__file__).parent / 'styles.xlsx'

if (not savepath.exists()
    or 
    jaconv.zen2han(
        input('上書きしますか？(y/n)').strip().lower(), 
        ascii=True) == 'y'
    ):
    wb.save(savepath)
    wb.close()
    time.sleep(1)

    # wb を開いて確認
    xlapp = win32com.client.Dispatch('Excel.Application')
    xlapp.Visible = True
    xlapp.Workbooks.Open(str(savepath))       
else:
    print('保存はキャンセルされました。')
