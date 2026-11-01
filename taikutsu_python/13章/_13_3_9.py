#! python3
# _13_3_9.py
# P360
# 図を追加する

import docx
from docx.shared import Inches, Cm
doc = docx.Document()
# インチ指定、Cm指定が出来る
pic = doc.add_picture('zophie.png', 
                width=Inches(2.5),
                height=Cm(8.5))
# width heightは int なのだが、
# python-docx の場合：
# 8.5 cm → 3060000 EMU   （単位を細かくして整数化）
# EMUという単位に再計算された結果が整数として扱われるので、少数点以下の指定も出来る。
print(type(pic))
# <class 'docx.shape.InlineShape'>
# docx で挿入する画像は inline のみ。
# AIに訊くと、とりあえずの対処コードは書いてくれるが、word のバージョンUPでの動作保証はない。

doc.save('zophie.docx')