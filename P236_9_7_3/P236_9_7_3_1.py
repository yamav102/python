#! python3
# P236_9_7_3_1.py
# 一つのフォルダで、指定した接頭辞を持つ連番ファイルを探し、
# 連番の飛びがあれば、以降に続く連番を、連続番号になるようrename する。
# 戻り値：リネイムしたファイルの数
# フォルダパス、接頭辞、拡張子（省略可能）、連番の最小値（省略可能）

import os
from pathlib import Path
import re
import shutil
import argparse
import zipfile
from datetime import datetime

def _get_current_timestamp() -> str:
    """現在の日時を yyyymmddhhmmss 形式で返す"""
    return datetime.now().strftime('%Y%m%d%H%M%S')

def _safe_foldername(base_path: Path) -> Path:
    """既存のフォルダと被らないよう、必要に応じて (2), (3), ... を付けたパスを返す"""
    counter = 1
    candidate = base_path

    while candidate.exists():
        counter += 1
        candidate = base_path.with_name(f"{base_path.name}({counter})")

    return candidate

def main(tgtfolderpath: str, 
         prefix: str,
         suffix:str,
         min_number:int) ->int:        

      tgt = Path(tgtfolderpath).resolve()
      # フォルダ引数チェック
      if not(tgt.is_dir()):
            raise ValueError(f'{tgt}はフォルダではありません。')        

      # 拡張子の指定があれば、ドット付を担保。
      suffix = suffix.strip()
      if suffix:
            suffix = '.' + suffix.lstrip('.')

      # 何をするのかを表示
      print('ファイルの連番の飛びを埋めるため、連番の振り直しを行います。\n'
            f'検索フォルダ: {tgt}\n'
            f'接頭辞:{prefix}\n'
            f'拡張子:{suffix if suffix else "指定なし"}\n'            
      )
      # ユーザーに確認を求める
      while True:
            response = input(
                 f'{tgt}内にバックアップ.zipを作成します。'
                 '続行してよろしいですか？ (y/n): ').strip().lower()
            if response == 'y':
                  break
            elif response == 'n':
                  print('処理は中止されました。')
                  return 0
            else:
                  print('無効な入力です。y または n を入力してください。')
      #　input('続行するにはEnterキーを押してください。')


      # 現状ファイル名構成状態のバックアップを作成
      backup_zip = tgt / (_get_current_timestamp() + 'backup.zip')
      with zipfile.ZipFile(backup_zip, 'w') as zipf:
          # iterdir(): 対象フォルダ内直下のファイルとフォルダをすべて列挙する。
          for file in tgt.iterdir():
              if file.is_file():
                  # *backupzipはアーカイブしない
                  if file.name.endswith('backup.zip'):
                      continue
                  zipf.write(file, arcname=file.name)

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
      
      # リスト昇順ソート
      files.sort()
      # 連番      
      idx = min_number
      
      # 0埋め数:ファイル数の桁数
      max_number = min_number + len(files) -1
      zcnt = len(str(max_number))
      zcnt += 1 # 一桁余裕を作る

      '上書きリスク排除のため、リネイムと同時に一時フォルダの中に移動'
      tmp = tgt / 'tmp'
      tmp_path = _safe_foldername(tmp.resolve())
      tmp_path.mkdir()
      
      # ファイル名の連番振り直し
      rename_count = 0
      for file in files:            
            oldname = file.resolve()
            newname = tmp_path / f"{prefix}{str(idx).zfill(zcnt)}{file.suffix}"
            
            msg = f'{oldname.name} ⇒ {newname.name} リネイム'
            try:  
                shutil.move(oldname, newname) 
                if oldname.name != newname.name:
                    print(msg)
                    rename_count += 1                  
            except PermissionError as e:
                  print(f'権限エラー:{msg}\n{e}')
            except Exception as e:
                  print(f'予期せぬエラー:{msg}\n{e}')
            idx += 1  

      # 一時フォルダから tgt にファイルを戻す
      for f in tmp_path.glob('*'):
           newname = tgt / f.name
           if newname.exists():
                raise FileExistsError(f'{f.name} は既に存在します。')
           shutil.move(f.resolve(),tgt / f.name)
      # 一時フォルダを削除
      tmp_path.rmdir()

      # 処理したファイル数を return
      print(f'{rename_count} ファイルをリネイムしました。')            
      return rename_count

if __name__ == '__main__':
    # >python test.py -h とコマンドラインで指定すると、使い方が表示される。    
    parser = argparse.ArgumentParser(
        description='一つのフォルダで、指定した接頭辞を持つ連番ファイルを探し、\n'
        '連番の飛びがあれば、以降に続く連番を、連続番号になるようrename する。',
        epilog='例）>python test.py c:\\mydir Spam --suffix .txt --min-number 5'
    )
    parser.add_argument('tgtfolderpath',
                        help='同じ接頭辞を持つ連番ファイルの保存されているフォルダパス'
                        )
    parser.add_argument('prefix',
                        help='接頭辞部分を指定します（例: Spam001.txt の場合は "Spam"）。'
                        '大文字小文字は無視されますが、'
                        'リネーム後はここで指定した通りの大文字小文字で出力されます。')    
    parser.add_argument('--suffix','-s',
                        default='',
                        help='拡張子（省略可能）。指定が無ければ拡張子を無視します。') 
    parser.add_argument('--min-number','-m',
                        type=int,
                        default= 1,
                        help='連番の最小値（省略可能）。指定が無ければ 1 から開始します。')     
    args = parser.parse_args()

    # 省略可能の引数は、コマンドラインでは -- を付けて書くが、
    # Pythonコード内では -- をすべて除いて、args.XXX の形でアクセスするpythonルール。
    # min-number と min_numberの混在は意識的にやっている。
    # コマンドライン引数ではハイフンの使用が一般的。一方、python変数名にハイフンは使えない。
    main(args.tgtfolderpath, args.prefix, args.suffix, args.min_number)