#! python3
# _12_8.py
# Fontオブジェクト
import openpyxl
from openpyxl.styles import Font
from pathlib import Path
import win32com.client # module
import time
wb = openpyxl.Workbook()
sheet = wb['Sheet']
font_obj1 = Font(name= 'Times New Romoan', bold=True)
rngA1 = sheet['a1']
rngA1.font = font_obj1
rngA1.value = 'Bold Times new Roman'
font_obj2 = Font(size=24, italic=True)
rngB3 = sheet['b3']
rngB3.font = font_obj2
rngB3.value = '24 pt Italic'
savepath = Path(__file__).parent / 'styles.xlsx'
wb.save(savepath)
wb.close()
time.sleep(1)

xlapp = win32com.client.Dispatch('Excel.Application')
xlapp.Visible = True
xlapp.Workbooks.Open(str(savepath))