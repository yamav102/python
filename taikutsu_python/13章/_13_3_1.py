#! python3
# P349
# 13.3 Word文書
# _13_3_1 Word文書を読み込む
import sys
# print(sys.path)
# for p in sys.path:
    # print(p)
import docx
def main()->None:
    doc = docx.Document('demo.docx')
    print(len(doc.paragraphs))
    print(doc.paragraphs[0].text)
    print(doc.paragraphs[1].text)
    paragraph_cnt = 0
    for prgrph in doc.paragraphs:
        paragraph_cnt += 1
        print(f'第{paragraph_cnt} パラグラフ')
        print(prgrph.text)

    print(len(doc.paragraphs[1].runs))
    print(doc.paragraphs[1].runs[0].text)
    print(doc.paragraphs[1].runs[1].text)
    print(doc.paragraphs[1].runs[2].text)
    print(doc.paragraphs[1].runs[3].text)
    for rns in doc.paragraphs[1].runs:
        print(rns.text)
# $ py _13_3_1.py 
# 7
# Document Title
# A plain paragraph with some bold and some italic
# 第1 パラグラフ
# Document Title
# 第2 パラグラフ
# A plain paragraph with some bold and some italic
# 第3 パラグラフ
# Heading, level 1
# 第4 パラグラフ
# Intense quote
# 第5 パラグラフ
# first item in unordered list
# 第6 パラグラフ
# first item in ordered list
# 第7 パラグラフ

# 4
# A plain paragraph with some 
# bold
#  and some 
# italic
# A plain paragraph with some 
# bold
#  and some 
# italic
     

if __name__ == '__main__':
    main()
