#! python3
# P345
# combinePdfs.py
# カレントディレクトリにあるすべてのPDFファイルを
# ファイル名でソートして、表紙以外を結合した allminutes.pdf を出力する
# パスワード保護された PDFファイルはスキップされます。

import PyPDF2 # py -m pip install PyPDF2==2.12.1
from pathlib import Path
from typing import Final
OUT_FILE_NAME: Final = 'allminutes.pdf'
# カレントディレクトリ
cur_dir = Path('.')
def main()->None:

    pdf_files = []
    # 最後に閉じるための、開いたままのPDFのリスト
    open_files = []

    for p in cur_dir.iterdir(): # iterdir> ディレクトリの中身をイテレタブルにして返す
        if p.name.lower().endswith('.pdf'):
            # Pathオブジェクトを lower 出来ないので str で cast
            pdf_files.append(str(p))
    pdf_files.sort(key=str.lower)    # 引数に関数を渡すと結果で並び替えてくれる。key=lenとか。
    pdf_writer = PyPDF2.PdfFileWriter()    
    # 総ページ数
    page_count = 0
    # ページが未追加であるか
    is_initial: bool = True
    try:
        # すべてのPDFファイルをループする
        for filename in pdf_files:            
            pdf_file_obj = open(filename, 'rb')
            open_files.append(pdf_file_obj)
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

            # 暗号化PDFは、スキップ
            if pdf_reader.is_encrypted:
                print(f'{filename} はパスワード保護されています。スキップされました。')
                continue
            # 1ページのみのPDFは統合の対象外
            if len(pdf_reader.pages) == 1:
                print(f'{filename} は1ページのみのPDFです。スキップされました。')
                continue

            # 表紙ページを含めるか、
            start_page = 0 if is_initial else 1
            page_each_count = 0
            for page_num in range(start_page, len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page_num]
                pdf_writer.add_page(page_obj)
                page_count += 1
                page_each_count += 1
            is_initial = False
            print(f'{filename} は、統合されました。[{page_each_count}]ページ')

        if is_initial:
            print('統合対象のページがありませんでした。')
            return
        
        # 結合したPDFをファイルに保存する
        with open(OUT_FILE_NAME, 'wb') as pdf_output:        
            pdf_writer.write(pdf_output)            
        print(f'done:総ページ数 {page_count}')

    finally:
        for f in open_files:
            f.close()
if __name__ == '__main__':
    if (cur_dir / OUT_FILE_NAME).exists():
        print(f'{OUT_FILE_NAME} は、既に存在します。')
    else:
        main()