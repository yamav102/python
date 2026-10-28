#! python3
# P356
# _13_3_6.py
# Word文書を書き込む

import docx
# Word新規作成
doc = docx.Document()
print(doc.add_paragraph('Hello world!'))
# <docx.text.paragraph.Paragraph object at 0x000001FFCC45B230>
doc.save('hellloworld.docx')
