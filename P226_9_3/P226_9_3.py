#! python3
# P226_9_8.py

# 準備: tgtFolder内に、MM-DD-YYYYを名前の部分に持つ2999ファイル を作成する。
from pathlib import Path
import os
os.chdir(r'E:\yamaPythonScripts\P226_9_3')

'''
# 削除
for filename in os.listdir():
    os.remove(filename)
'''

# 作りたいファイル数
n = 1500
for i in range(1, n + 1):
    filename = f'abcd_{i:04d}_01-02-2026 efghi.txt'    
    filename = os.path.join(r'.\tgtFolder', filename)
    Path(filename).touch()
for i in range(1, n + 1):
    filename = f'abcd_{i:04d}_1-2-1999 efghi.txt'    
    filename = os.path.join(r'.\tgtFolder', filename)
    Path(filename).touch()
for i in range(1, n + 1):
    filename = f'abcd_{i:04d}_11-22-2099 efghi.txt'    
    filename = os.path.join(r'.\tgtFolder', filename)
    Path(filename).touch()    
print('done')    
    

'''
# 米国式日付（MM-DD-YYYY）用の正規表現を作る
import shutil, os, re
date_pattern = re.compile(
                     r'^(.*?'           # 日付の前の全テキスト
                     r'((0|1)?\d)-'     # 月を表す1,2桁の数字
                     r'((0|1|2|3)?\d)-' # 日を表す1,2桁の数字
                     r'((19|20)\d\d)'   # 年を表す4桁の数字
                     r'(.*?)$'          # 日付の後のテキスト
                          
'''
