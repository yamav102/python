#! python3
# P362
# _13_6_1_2.py
# PDF をまとめて復号化
# サブフォルダまで探索してpdf を探す。
# 見つけたpdf を復号化した複製をつくる。
# パスワードが間違っていたら、メッセージを表示して、処理は続ける。
from pathlib import Path
import argparse
import PyPDF2
import sys
from typing import Final
SUFFIX: Final[str] = '_decripted'
def main(tgtfldr_path: Path, password: str)->None:
    pdf_files = list(tgtfldr_path.rglob('*.pdf', case_sensitive=False))
    for p in pdf_files:
        with open(p, 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            if pdf_reader.is_encrypted:
                result = pdf_reader.decrypt(password)
                if result == 0:
                    print(f'{f} は復号に失敗しました。')
                elif result in (1, 2):
                    pdf_writer = PyPDF2.PdfFileWriter()
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                    # 書き出し
                    out_path = Path(p)
                    name = out_path.stem
                    
                    out_path = out_path.with_stem(name+SUFFIX)
                    with open(out_path, 'wb') as out_f:
                        pdf_writer.write(out_f)
                        print(f'{out_path} を作成しました。')

            else:
                print(f'{Path(p)} は暗号化されていません。')

if __name__ == '__main__':
    out_file = open(
        Path(__file__).parent / 'result.txt',
        'w',
        encoding='utf-8'
    )
    sys.stdout = out_file

    parser = argparse.ArgumentParser(
        description='指定フォルダ下の pdf のパスワード解除した複製を、'
        '*_decrypted.pdf として生成します。',
        epilog=f'py {Path(__file__).name} tgtpath password'
    )
    parser.add_argument(
        'tgtpath',
        type=Path,
        help='pdfファイルを探索するフォルダパス'
    )
    parser.add_argument(
        'password',
        type=str,
        help='pdfファイルを復号化するパスワード'
    )
    args = parser.parse_args()
    main(args.tgtpath, args.password)

    out_file.close()

