#! python3
# P351
# _13_3_2.py
# .docxファイルから全テキストを取得する

import docx
from pathlib import Path
import argparse
import sys
def main(filename: Path)->str:
    doc = docx.Document(str(filename))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='docx の全テキストを取得します。',
        # '%(prog)s' は argparse の中だけで使えるプレースホルダ。
        # %s と言う書き方は c言語ライク
        # Path(sys.argv[0]).name と同じく、スクリプト名を返す
        usage='%(prog)s docpath', 
        epilog=f'py {Path(sys.argv[0]).name} docpath'
    )
    parser.add_argument(
        'docpath',
        type=Path,
        help='docx のパス'
    )
    args = parser.parse_args()    
    print(main(args.docpath))