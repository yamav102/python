#! python3
# _12_11win32comでグラフを削除.py
from pathlib import Path
import openpyxl
xlpath = Path(__file__).parent / 'sampleChart.xlsx'
# グラフを削除したいなら、
# win32com を使った方が確実
from win32com.client import Dispatch
xlapp = Dispatch('excel.application')
wb = xlapp.Workbooks.Open(xlpath)
for ws in wb.Worksheets:
    print(ws.Name, 'charts=', ws.ChartObjects().Count)
    while ws.ChartObjects().Count > 0:
        ws.ChartObjects(1).Delete()        
# wb.Save()

# 別名で保存して可視
xlpath = Path(__file__).parent / 'sampleNoChart2.xlsx'
wb.SaveAs(str(xlpath))
xlapp.Visible = True

