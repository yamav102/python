#! python3
# _12_11.py 
# P327
# グラフ
import openpyxl
from openpyxl.chart import Reference
from openpyxl.chart import BarChart
from openpyxl.worksheet.worksheet import Worksheet
from pathlib import Path
from win32com.client import Dispatch
def openxl(xlpath:Path)->None:
    xlApp = Dispatch('Excel.Application')
    xlApp.Visible = True
    xlApp.Workbooks.Open(str(xlpath))
def main():
    wb = openpyxl.Workbook() # 新規 wb 作成
    sheet: Worksheet = wb.active # type: ignore[assingment]
    assert isinstance(sheet, Worksheet)
    for i in range(1, 11): 
        # 列A に適当にデータを作成
        sheet['a' + str(i)].value = i
    # セルの矩形領域から Referenceオブジェクトを作成する
    ref_obj = Reference(
        sheet, min_col=1, min_row=1, max_col=1, max_row=10)
    # Chartオブジェクトを作成(棒グラフ)
    chart_obj = BarChart()
    chart_obj.add_data(ref_obj)
    chart_obj.title = 'First Graph'
    chart_obj.title

    # サイズ(cm)
    chart_obj.width = 15
    chart_obj.height = 7.5

    # 位置をセルで指定
    sheet.add_chart(chart_obj, "C5") 

    xlpath = Path(__file__).parent / 'sampleChart.xlsx'
    wb.save(xlpath)
    openxl(xlpath)

if __name__ == '__main__':
    main()