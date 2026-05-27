#! Python3
# renameDates.py - 米国式日付MM-DD-YYYYのファイル名を欧州式DD-MM-YYYYに書き換える
import shutil, os, re
# 既に存在するファイル名なら、ファイル名にindexを付けて
# 一意なファイル名に加工して返す。
def safe_name(fullpath :str) -> str:
    if os.path.isdir(fullpath):
        raise ValueError('引数には、ファイルパスを渡します。')
    basename = os.path.basename(fullpath)
    parentdir = os.path.dirname(fullpath)
    prts = basename.split('.')
    i = 1
    if len(prts) > 1:
        extention = '.' + prts[len(prts)-1]
    else:
        extention = ''
    basename = basename[:len(basename) - len(extention)]
    
    while os.path.exists(fullpath):
        i += 1 
        fullpath = os.path.join(
            parentdir,basename + '(' + str(i) + ')' + extention
            )        
    return fullpath
    

# 米国式日付のファイル名にマッチする正規表現を作る
date_pattern = re.compile(
    r'^(.*?)'                  # 日付の前の全テキスト
    r'(0?[1-9]|1[0-2])-'       # 月を表す1, 2桁の数字
    r'(0?[1-9]|[12]\d|3[01])-' # 日を表す1, 2桁の数字
    r'((19|20)\d{2})'          # 年を表す4桁の数字
    r'(.*?)$'                  # 日付の後の全テキスト
    , re.VERBOSE)
#print(date_pattern.search('asdf01-12-2020xyz.pdf').group())
# TODO: カレントディレクトリの全ファイルをループする
tgtdir = r'E:\yamaPythonScripts\P226復習\tgtdir'
for amer_filename in os.listdir(tgtdir):
    mo = date_pattern.search(amer_filename)

    # 米国式日付パターンの無いファイルをスキップする
    if mo == None:
        continue
    
    # TODO: ファイル名を部分分割する
    # 正規表現に()が使われる度にグループの番号は1増える。cf (4(5))
    before_part = mo.group(1)
    month_part = mo.group(2)
    day_part = mo.group(3)
    year_part = mo.group(4)
    after_part = mo.group(6)
    
    # TODO: 欧州式の日付ファイル名を作る
    euro_filename = (
        before_part
        + day_part
        + '-'
        + month_part
        + '-'
        + year_part
        + after_part)
    #既に同名のファイルがあれば、ファイル名に(index)を付ける
    euro_filename = safe_name(euro_filename)
    # TODO: ファイル名を変更する。
    print('Renaming "{}" to "{}"...'.format(amer_filename, euro_filename))
    #shutil.move(amer_filename, euro_filename) # テスト後にコメントを外す
