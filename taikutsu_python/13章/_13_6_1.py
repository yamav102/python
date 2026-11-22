#! python3
# P362
# PDF をまとめて暗号化
# サブフォルダまで探索してpdf を探す。
# 見つけたpdf を暗号化し、ファイル名に _encrypted を繋げてリネイムする。
# 復号出来る事を確認するプロセスを含める事。
from pathlib import Path
import argparse
import PyPDF2
# from PyPDF2._encryption import PasswordType
from typing import Final
import sys
SUFFIX:Final[str] = '_encrypted'
def main(tgtfldr: Path, password: str)-> None:
    # case_sensitive は 省略すると osの標準ルールに従う。
    # linux だと大文字小文字が区別される。
    # list()で囲まないと generator 型
    # rglob は recursive な glob← ワイルドカードで一括取得（内部的にループ処理している）
    pdf_list = list(tgtfldr.rglob('*.pdf', case_sensitive=False)) 
    for p in pdf_list:
        with open(p, 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            pdf_writer = PyPDF2.PdfFileWriter()
            if pdf_reader.is_encrypted:
                print(f'{p} \nは、既に暗号化されています。')
            else:
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                pdf_writer.encrypt(password)
                # 編集不可の保護にする場合は、
                # pdf_writer.encrypt(
                #     user_password=password,
                #     owner_password=<強度のあるパスワード>)
                # と書く。空文字の指定は「パスワード無し」を意味する。
                # 特定の操作（印刷とか）だけに許可を設定する、第三引数もある。
                out_file = p.with_name(f'{p.stem}{SUFFIX}.pdf')
                with open(out_file, 'wb') as out:
                    pdf_writer.write(out)

                # 暗号化前のファイルを
                ## 閉じる
                f.close()
                               
                ## 削除。 missing_ok: ファイルが無くてもエラーで止まらせないオプション
                orgin_file = Path(p) 
                orgin_file.unlink(missing_ok=True) 

                # 正しく暗号化された事の確認ステップ
                check_reader = PyPDF2.PdfReader(out_file)
                if check_reader.is_encrypted:
                    print(f'OK: {out_file} \nは、暗号化されています。')
                    result = check_reader.decrypt(password=password)
                    if result > 0: 
                        # 1: は user_password(閲覧のみ), 2: は ornner_password(編集可)
                        print(f'OK: {out_file} \nは、パスワードでの復号復号に成功しました。(ステータス：{result})')                        
                        print(f'総ページ数：{len(check_reader.pages)}')
                    else:
                        print(
                            f'NG: {out_file} \n'
                            'は、設定したパスワードでは復号出来ませんでした。')
                else:
                    print(f'NG: {out_file} \nは、暗号化されていません。')


# なぜ「チェックステップ」が求められるのか

# PDFの暗号化は、個人情報や請求書などの機密情報を外部に送付する
# 直前のセキュリティ対策として使われることが多い処理です。
# もし暗号化に失敗していても例外（エラー）が出ずに処理が完了してしまうと、
# 「パスワードがかかっていない機密PDFをメールやサーバーにアップロードしてしまう
# （情報漏洩）」という重大なインシデントに直結します。
# そのため、今回のような課題では「処理が成功したか」だけでなく、
# 「万が一失敗していた場合に、後続の送信・公開処理を確実にストップさせる
# 安全装置（フェイルセーフ）を組めるか」という実務的な観点が評価されています。

# python の暗号化の信頼性が低いという事ではなく、ロジックの分岐漏れで
# 暗号化したつもりで、暗号化されないまま出力されてしまうケースが最も多い原因。

if __name__ == '__main__':
    # 結果検証のため、print出力先をターミナルではなく、外部.txt へ出力する設定
    out_file = open(
        Path(__file__).parent / 'result.txt', 
        'w', encoding='utf-8'
        )
    ## print の出力先をファイルに変更
    sys.stdout = out_file    

    parser = argparse.ArgumentParser(
        description='指定パス以下の pdf を階層探索してパスワード付きにします。',
        epilog=f'py {Path(__file__).name} tgtpath password',
    )
    parser.add_argument(
        'tgtpath',
        type=Path,
        help='pdfファイルを探索するフォルダパス'
    )
    parser.add_argument(
        'password',
        type=str,
        help='pdfファイルを暗号化するパスワード'
    )    
    args = parser.parse_args()
    main(args.tgtpath, args.password)

    out_file.close() # printの出力先のファイルを閉じる。
