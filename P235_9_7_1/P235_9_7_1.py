#! python3
# P235_9_7_1.py ディレクトリツリーを渡り歩いて、.pdfや .jpg などの特定の拡張子を持つファイルを見つけ、新しいフォルダにコピーする
import os
from pathlib import Path
import ast
import sys
import shutil
def _safe_foldername(base_path: Path) -> Path:
    """既存のフォルダと被らないよう、必要に応じて (2), (3), ... を付けたパスを返す"""
    counter = 1
    candidate = base_path

    while candidate.exists():
        counter += 1
        candidate = base_path.with_name(f"{base_path.name}({counter})")

    return candidate
# フォルダ構造が存在しなければ作成してファイルをコピーする
# 既にフォルダが存在していたら何もしない。
# preserve_metadata:作成日時、修正日時、パーミッション（権限）などを保持
# 既にファイルが存在していたらエラー
# 使い方
# _safe_copy("c:/a/b/c.txt", "e:/a/b/c.txt")
def _safe_copy(src_path, dst_path, preserve_metadata=True)->Path:
    src = Path(src_path)
    dst = Path(dst_path)
    
    # parents=True で、親フォルダを一気に作成
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise FileExistsError(f'{dst} は既に存在します。')
    else:
        # python 3.14以降限定。3.14より前は copy()メソッド未実装
        # return src.copy(dst, preserve_metadata=preserve_metadata)
        if preserve_metadata:
            shutil.copy2(src, dst) # メタデータ保持
        else:
            shutil.copy(src, dst)
        return dst

# arg2>拡張子:list、arg3>作成するフォルダ名:str_省略可能
# main という関数名自体にC言語のような意味はない。
# コマンドラインから実行する場合、モジュール内部の関数名を意識しないので、
# 主要関数の関数名は 'main' が良い、というのが共通認識らしい。
# suffixs は list で渡したいが、コマンドリストでは文字列としてしか渡せないので、
# literal_eval でリストに型変換している。
def main(
        tgtdir: str,
        str_suffixs: str, 
        dstfolderpath: str | None = None
        )->None:    
    tgtfolder = Path(tgtdir).resolve()
    suffixs = ast.literal_eval(str_suffixs)

    # 移動先フォルダパスが未指定の場合、検索拡張子からフォルダ名を作成
    if dstfolderpath is None:
        dstfolderpath ="_".join(suffixs)
        dstfolderpath = dstfolderpath.replace('.','')
        dstfolderpath = tgtfolder.name + '_' + dstfolderpath
        pt = tgtfolder.parent / dstfolderpath

        # 絶対パスにして _safe_foldername に渡す。
        dstfolderpath = _safe_foldername(pt.resolve())    
    else:
        dstfolderpath = Path(dstfolderpath).resolve()
    # os.walk
    errors = [] # エラーの記録
    success = [] # 成功の記録
    print(f"対象フォルダ: {tgtfolder}")
    print(f"検索拡張子: {suffixs}")
    print(f"保存先フォルダ: {dstfolderpath}\n")

    # サブディレクトリは本処理では使わないので _ で表記しています。
    for curdir, _, files in os.walk(tgtfolder):        
        for file in files:
            # splt = file.split('.')
            # extnd = splt[-1]
            file_path = Path(curdir) / file
            if file_path.suffix.upper() in [s.upper() for s in suffixs]:                
                print(curdir + ' からコピー処理中...')
                try:
                    # 保存先フォルダ内は検索対象から除外する
                    #if not(str(Path(curdir).resolve()).startswith(str(dstfolderpath))): 
                    # ↑だと、c:\dst と c:\dst2 を区別できない。
                    if dstfolderpath in Path(curdir).resolve().parents:
                        continue
                    # 自分自身の .py ファイルをコピー対象から外す場合の条件
                    # script_file = Path(sys.argv[0]).resolve()
                    # if Path(curdir) / file != script_file:
                    print(file_path)
                    # 移動先にファイルコピー
                    # 同名ファイルの存在を考慮して、フォルダ構造ごと作成してコピーする        
                    relativepath = file_path.relative_to(tgtfolder) # tgtfolder以降の相対パスを取得
                    dst = dstfolderpath / relativepath
                    _safe_copy(file_path, dst)
                    success.append(file_path)
                except FileNotFoundError as e:
                    errors.append(file_path, f"コピー元が見つかりません: {e}")
                except FileExistsError as e:
                    errors.append(file_path, f"同名のファイルが既に存在します: {e}")
                except PermissionError as e:
                    errors.append(file_path, f'権限エラー: {e}')
                except OSError as e:
                    errors.append(file_path, f'入出力エラー: {e}')
                except Exception as e:
                    errors.append(file_path, f'予期しないエラー: {e}')

    # 処理のレポート                
    print(f'{len(success)} ファイル移動しました。エラー件数:{len(errors)} 件')
    if len(success):
        print(f'移動先: {dstfolderpath}')
    if len(errors):
        print('err-------------')
        for err in errors:
            print(err)
        print('//err-------------')

if __name__ ==  '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2],sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print('使い方: \n' \
        'python P235_9_7_1.py 対象フォルダパス 拡張子のリスト [保存先フォルダ名]\n' \
        'python P235_9_7_1.py c:\\fld1 [".bat"],c:\\fld2\n' \
        '[保存先フォルダ名]は省略可。指定した場合、フォルダが無ければ作成される。' 
        )
        sys.exit(1)
