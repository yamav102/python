#! python3
# P326
# ウィンドウ枠の固定
import openpyxl
from pathlib import Path
from openpyxl.worksheet.worksheet import Worksheet
import win32com.client
def openxl(xlpath: str)->None:
    xlApp = win32com.client.Dispatch('Excel.Application')
    xlApp.Visible = True
    xlApp.Workbooks.open(xlpath)
def main():
    xlPath = Path(__file__).parent / 'produceSales.xlsx'
    wb = openpyxl.load_workbook(xlPath)
    sheet = wb.active
    assert isinstance(sheet, Worksheet)
    # visiblerange(2, 1)で設定されるので、a1をtopleft にしておく必要がある
    sheet.sheet_view.topLeftCell = 'a1'
    sheet.freeze_panes = 'a2' 
    wb.save(xlPath)
    openxl(xlpath=str(xlPath))
    
if __name__ == '__main__':
    main()