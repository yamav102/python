#! python3
# P236_9_7_3_2.py
import os
from pathlib import Path
import re
import shutil
import argparse

# 一つのフォルダで、指定した接頭辞を持つ連番ファイルを探し、
# 連番に空きが出来るよう rename する。
# 戻り値：リネイムしたファイルの数
# フォルダパス、接頭辞、、隙間を作る番号の範囲。例: 2-4、拡張子（省略可能）

def _zfill_width(fname:str, prefix:str, suffix:str) -> int:

    # ファイル名から、接頭辞と拡張子を除いた数値部分の桁数を返す。
    if suffix:
        stem = fname[:-len(suffix)]
    else:
        stem = Path(fname).stem
    return len(stem[len(prefix):])

# 連番抽出
def _get_findx(filename: str, prefix: str, suffix: str) -> int:
    if suffix:
        stem = filename[:-len(suffix)]
    else:
        stem = Path(filename).stem
    return int(stem[len(prefix):])

def _make_glob_pattern(prefix: str, num: int, zcnt: int, suffix: str) -> str:
    """occupied判定用のglobパターンを作成"""
    num_str = f"{num:0{zcnt}d}"
    if suffix:
        return f"{prefix}{num_str}{suffix}"
    else:
        return f"{prefix}{num_str}*"
    
def _get_next_free(
        tgt: str, 
        prefix:str, 
        suffix: str, 
        mx: int,
        zcnt: int) -> int:
    # 連番:mx の次に空いている位置を取得
    next_free = mx + 1
    while True:
        pattern = _make_glob_pattern(prefix, next_free, zcnt, suffix)
        if not any(tgt.glob(pattern)):
            break
        next_free += 1
    return next_free

def main(tgtfolderpath: str, 
         prefix: str,
         blankrng: str,
         suffix:str
         ) ->int:        

    tgt = Path(tgtfolderpath).resolve()
    # フォルダ引数チェック
    if not(tgt.is_dir()):
          raise NotADirectoryError(f'{tgt}はフォルダではありません。')
      
    # 隙間を作る番号の範囲の引数チェック
    # + は、直前の文字が一つ以上続くパターン。
    blankrng = blankrng.strip()
    pattern = re.compile(r'\d+')      
    mo1 = pattern.match(blankrng)      
    pattern = re.compile(r'\d+-\d+')      
    mo2 = pattern.match(blankrng)

    if mo1 == None and mo2 == None:
        raise ValueError(
            f'{blankrng} には、'
            '2 の位置に、1ファイル分空きを作る場合は、2 のように指定。'
            '2,3,4に空きを作りたい場合は、 2-4 のように指定します。'
            )
    else:
        # 数値の配列に変換
        # files = [f for f in candidates if pattern.match(f.name)]
        nums = [int(n) for n in blankrng.split('-')]          
        # 空きにする最小番号
        mn = min(nums)                                    
        # 空きにする最大番号
        mx = max(nums)
      
    range_str = f'[{mn}]' if mx == mn else f'[{mn}～{mx}]'
    print(
        f'検索フォルダ: {tgt}\n'
        f'接頭辞:{prefix}\n'
        f'拡張子:{suffix if suffix else "指定なし"}\n'
        f'連番{range_str}のファイル分、'
        '連番が空くように、ファイル名を付け直します。')
    
    # ユーザーに確認を求める
    while True:
        response = input(
            '続行してよろしいですか？ (y/n): ').strip().lower()
        if response == 'y':
            break
        elif response == 'n':
            print('処理は中止されました。')
            return 0
        else:
            print('無効な入力です。y または n を入力してください。')
            
    # 拡張子の指定があれば、ドット付を担保。
    suffix = suffix.strip()
    if suffix:
        suffix = '.' + suffix.lstrip('.')

    # 条件のファイルをリスト化
    # 階層探索しない。接頭辞だけの条件で候補を絞ったリストを取得する。
    candidates = list(tgt.glob(prefix + '*' + suffix)) 
    # または rglob('**/' + suffix + '*') で再帰も可
      
    # 正規表現で厳密にフィルタ（接頭辞の直後に1桁以上の数字が続き、任意の続き）
    # ^ = 文字列の先頭, \d+ = 数字1回以上
    pattern = re.compile(
        rf'{re.escape(prefix)}\d+{re.escape(suffix)}',
            re.IGNORECASE
    )      
      
    files = [f for f in candidates if pattern.match(f.name)]    
    if len(files)==0:
        print(f'検索フォルダ: {tgt}\n'
            f'接頭辞:{prefix}\n'
            f'拡張子:{suffix} のファイルはありません。')
        return 0
      
    # リスト降順ソート
    files.sort(reverse=True)
      
    # ファイル名の連番振り直し
    rename_count = 0
    # 0埋めの個数
    if files:
        # 既存ファイル名で連番の最大桁を取得する。
        indexs = [_zfill_width(f.name, prefix, suffix) for f in files]
        zcnt = max(indexs)
    else:
        zcnt = 2

    # 必要なシフト数を算出
    ## 連番:mx の次に空いている位置を取得
    next_free = _get_next_free(tgt, prefix, suffix, mx, zcnt)
    

    ### 空き番号にしたい番号が使われている件数を取得する。
    occupied_number = 0
    for i in range(mn, mx + 1): # mn から mx + 1 未満までループ
        pattern = _make_glob_pattern(prefix, i, zcnt, suffix)
        if any(tgt.glob(pattern)):
            occupied_number += 1

    # 空きを作りたい番号で、使用されている件数 > 0 ならば           
    if occupied_number > 0: 

        # 必要なシフト数 = 空きにしたい番号の最大値の次の空き番号 - 空きにしたい番号の最小値
        shift = next_free - mn
        for file in files:         
            oldname = file
            # ファイルの連番の数値を取得。
            f_indx = _get_findx(oldname.name, prefix, suffix)

            # 空き番号の最小値より、連番のインデックスが小さければループを抜ける
            if f_indx < mn:
                break
            # 空き番号の最小値以上の連番であれば、空き番号の指定数大きい連番でリネイムする。
            # [空き番号の指定数]とは、12-15 の指定の場合 12,13,14,15 の [4]つ。
            s_seq_num = str(f_indx + shift)
            newname = (
                tgt
                / f'{prefix}'
                    f'{s_seq_num.zfill(zcnt)}'
                    f'{file.suffix}'
                    )            
            msg = f'{oldname.name} ⇒ {newname.name} リネイム'
            try:
                if newname.exists():
                    raise FileExistsError(f'{newname} は既に存在します。')
                shutil.move(oldname, newname) 
                print(msg)
                rename_count += 1                  
            except PermissionError as e:
                print(f'権限エラー:{msg}\n{e}')
            except FileExistsError as e:
                print(f'ファイルは既に存在します。:{msg}\n{e}')                  
            except Exception as e:
                print(f'予期せぬエラー:{msg}\n{e}')

    # 処理したファイル数を return
    if occupied_number == 0:
        print(f'{mn if mn == mx else f"{mn}-{mx}"} の範囲は既に空いています。')
    else:
        print(f'{rename_count} ファイルをリネイムしました。')
    return rename_count

if __name__ == '__main__':
    # >python test.py -h とコマンドラインで指定すると、使い方が表示される。    
    parser = argparse.ArgumentParser(
        description='一つのフォルダで、指定した接頭辞を持つ連番ファイルを探し、\n'
        '連番の飛びがあれば、以降に続く連番を、連続番号になるようrename する。',
        epilog='例）>python test.py c:\\mydir Spam --suffix .txt'
    )
    parser.add_argument('tgtfolderpath',
                        help='同じ接頭辞を持つ連番ファイルの保存されているフォルダパス'
                        )
    parser.add_argument('prefix',
                        help='接頭辞部分を指定します（例: Spam001.txt の場合は "Spam"）。'
                        '大文字小文字は無視されますが、'
                        'リネーム後はここで指定した通りの大文字小文字で出力されます。')    
    parser.add_argument('blankrng',
                        help='空きを作る連番の指定します。'
                        '（例：Spam002.txtの位置に空きを作る場合は "2"、\n'
                        '2-5 と指定すると、範囲指定になります。）'
                        )     
    parser.add_argument('--suffix','-s',
                        default='',
                        help='拡張子（省略可能）。指定が無ければ拡張子を無視します。')     
    args = parser.parse_args()

    # 省略可能の引数は、コマンドラインでは -- を付けて書くが、
    # Pythonコード内では -- をすべて除いて、args.XXX の形でアクセスするpythonルール。
    # min-number と min_numberの混在は意識的にやっている。
    # コマンドライン引数ではハイフンの使用が一般的。一方、python変数名にハイフンは使えない。
    main(args.tgtfolderpath, args.prefix, args.blankrng, args.suffix)