#! python3
# _12_11ワークシートのグラフを削除1.py
from pathlib import Path
import openpyxl
xlpath = Path(__file__).parent / 'sampleChart.xlsx'
print(openpyxl.__version__) # 3.1.5
# 開いて保存して、グラフが消失している事を確認する ⇒　ver3.1.5 ではグラフを読み込めてしまった。
# 単純なグラフなら読見込める事が多い、というだけで、必ず読み込めることが保証されているわけでは
# ないらしい。
# グラフを削除する公式な手段は用意されていない。
# 非公式な方法 ws._charts = [] で、グラフを削除する事は出来る。
# 将来かわってしまう可能性はある。
wb = openpyxl.load_workbook(xlpath)
for ws in wb.worksheets:
    ws._charts = [] # 一つだけなら、del ws._charts[0]

xlpath = Path(__file__).parent / 'sampleNoChart.xlsx'
wb.save(xlpath) 

from win32com.client import Dispatch
xlapp = Dispatch('excel.application')
xlapp.workbooks.open(str(xlpath))
xlapp.Visible = True

