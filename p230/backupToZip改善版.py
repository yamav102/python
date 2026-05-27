#! python3
# -*- coding: utf-8 -*-
"""
フォルダ全体を連番付きZIPファイルにバックアップする（自分自身は除外）
"""
import zipfile
import os
from pathlib import Path
from typing import Union

def backup_to_zip(folderpath: Union[str, Path]) -> None:
    folder = Path(folderpath).resolve() #絶対パスに正規化

    if not folder.is_dir():
        print(f'エラー：{folder} はフォルダではありません')
        return
    # 連番ファイル名を決める（カレントディレクトリに作成）
    number = 1
    while True:
        zip_filename = f"{folder.stem}_{number:03d}.zip"
        zip_path = Path(zip_filename)
        if not zip_path.exists():
            break
        number += 1

    print(f"作成開始: {zip_path}")

    try:
        with zipfile.ZipFile(
            zip_path,
            'w',
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=6, # 6はバランスが良い(9は遅い)
            ) as zf:

            # バックアップするフォルダパスを「基底フォルダ」という別名の変数で再定義して、
            # スクリプトを読みやすくしている
            base_dir = folder

            # os.walk
            for dirpath, dirnames, filenames in os.walk(folder, topdown=True):
                # ZIP内の早退パスを計算
                rel_dir = os.path.relpath(dirpath, base_dir)

                # 最上位フォルダの時のみ rel_dir == '.' になる。
                # この if 文がないと'.'と言う名前のフォルダを作ろうとしてエラーになる（筈）
                if rel_dir != '.':
                    # アーカイブパスはパスもファイル名も任意に指定できる。
                    # 関数呼び出し時、引数にフォルダフルパスを指定された場合
                    # ドライブ直下フォルダからのパス構造がZIP内に作られてしまう事を回避
                    zf.write(dirpath, arcname=rel_dir)

                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)

                    # 今回作成中のZIPファイル自身ならスキップ
                    # c:\a\.\z.txt は c:\a\z.txt を指すが、両Pathオブジェクトを比較しても同じにはならない。
                    # resolve() で絶対パスにして比較する事で、確実に動作する堅牢なコーディングとなる。
                    if Path(full_path).resolve() == zip_path.resolve():
                        print(f' スキップ（自身）:{filename}')
                        continue

                    rel_path = os.path.relpath(full_path, base_dir)
                    print(f' 追加: {rel_path}')
                    zf.write(full_path, arcname=rel_path)
            # :, カンマ区切り指定
        print(f'完了: {zip_path} ({zip_path.stat().st_size:,} bytes)')

    except PermissionError as e:          
        print(f'権限エラー: {e}')
    except OSError as e:
        print(f'入出力エラー: {e}')
    except Exception as e:
        print(f'予期しないエラー: {e}')
            
# コマンドプロンプトから実効した場合、ココを通る。            
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使い方：python backup_zip.py 対象フォルダ")
        sys.exit(1) # 1は異常終了、0は正常終了 実行後に echo %errorlevel%で確認できる

    backup_to_zip(sys.argv[1])
