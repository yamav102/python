#! python3
# 13章 P338
# _13_1_2.py
# encrypted された PDF を password:'rosebud' で復号して開く
# python -m pip install PyPDF2==2.12.1
# 3.0.0以降 バージョン3.0.0以降はメソッドの廃止や大規模な仕様変更
# （PdfFileReaderの完全削除など）が行われたため、
# 書籍のコードをそのまま試すには2.*.*の環境を選択します。
import PyPDF2
from pathlib import Path
import argparse

def main(pdf_path:Path, password:str)->str:        
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        if pdf_reader.is_encrypted:
            result = pdf_reader.decrypt(password)
            if result == 0:
                return f'{password}では復号できませんでした。'

        # page_obj = pdf_reader.getPage(0)        
        page_obj = pdf_reader.pages[0] # 2.12.1推奨
        return page_obj.extract_text()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description= 'pdfファイルパス と パスワードを渡して、pdf ファイルのテキストを取得します。',
        epilog= f'py {Path(__file__).name} hoge.pdf --password="<password>"'
    )
    parser.add_argument(
        'pdfpath',
        type=Path,
        help='pdfファイルパス'
    )
    parser.add_argument(
        '--password',
        type=str,
        default='',
        help='パスワード'
    )
    args = parser.parse_args()
    print(main(args.pdfpath, args.password))