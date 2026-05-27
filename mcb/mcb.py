#! python3
# mcb Multi Clip Board の略
# .pyw は python 実行時ターミナルウィンドウを表示しない。

# 動作確認用
import datetime

log_file = open(r"E:\yamaPythonScripts\mcb\mcb_started.txt", mode="a", encoding='utf-8')
log_file.write(f"起動しました: {datetime.datetime.now():%Y/%m/%d %I:%M:%S}\n")
log_file.close()
# デバッグは拡張子を.py に変えて、cmdから実行すると print出力を確認できる。.pywではprintは何処にも表示されず捨てられる。
# 次のステップは、IDLEが起動されていればIDLE画面に表示される
# print('mcbTest ' + f'{datetime.datetime.now():%Y/%m/%d %I:%M:%S}\n')


# /動作確認用

# mcb.pyw - クリップボードのテキストを保持・復元
# Usage: ユーセージ/ユーザージ 使い方
# mcb.pyw は
   # a:P208MultiClipBoard.vbs, b:mcb.pyw
   # a または、b を ['save',<keyword>]の引数を指定して実行。⇒クリップボード内容が keywordに紐づけられて 'mcb'shelfに登録する
   # a または、b を <keyword>の引数を指定して実行。⇒ keywordに紐づいていう内容をクリップボードに paste する
   # a または、b を 'list' の引数を指定して実行。⇒ 'mcb'shelf に登録されている keyword 一覧をクリップボードに paste する
# py.exe mcb.pyw save <keyword> - クリップボードをキーワードに紐づけて保持➊ py.exeは、複数のpythonがインストールされていても最新バージョンを起動してくれる python lawncher。ランチャーとローンチは同じ言葉。起動する、という意味。
# py.exe mcb.pyw <keyword> キーワードに紐づけられたテキストをクリップボードにコピー
# py.exe mcb.pyw list - 全キーワードをクリップボードにコピー
# 拡張子 .py で動作確認できても、.pywにすると動作しない。.bat越しに実行しても結果は同じ。windows10以前ならコンソールウィンドウ非表示で動いたらしい。
# windows11 以降のosでは、「OSのセキュリティ強化で今はほぼ使い物にならなくなったのが現状です。(by grok)」との事。.py のまま使うのがとりあえず正解か。
# .bat経由で @python.exe "E:\yamaPythonScripts\mcb\mcb.pyw %*" として、「ファイル名を指定して実行」から実行しても、pythonw.exeで実行されてしまうのか、動作しなかった。


import shelve, pyperclip, sys #❷

mcb_shelf = shelve.open('mcb') #❸

# クリップボードの内容を保持
# Pythonのsys.argv[0]は、コマンドラインからスクリプトを実行した際に、実行されたスクリプト自身のファイル名（またはパス）
if len(sys.argv) > 3 or len(sys.argv) < 2:
   # 次のステップは、IDLEが起動されていればIDLE画面に表示される
   print('Err:引数は1つ、または、2つ指定します。 ' + f'{datetime.datetime.now():%Y/%m/%d %I:%M:%S}\n')
   raise Exception('Err:引数は1つ、または、2つ指定します。使い方は mcb.pyw の Usage参照 ')

try:
   if len(sys.argv) == 3 and sys.argv[1].lower() == 'save': # ➊
       mcb_shelf[sys.argv[2]] = pyperclip.paste() # ❷
       msg = 'keywordは{}'.format(sys.argv[2])    
   elif len(sys.argv) == 2:
       # キーワード一覧と、内容の読み込み # ❸
       if sys.argv[1].lower() == 'list': # ➊
           pyperclip.copy(str(list(mcb_shelf.keys()))) # ❷
       elif sys.argv[1] in mcb_shelf:
           pyperclip.copy(mcb_shelf[sys.argv[1]]) # ❸
       else:
          msg = f"キーワードが見つかりません: {sys.argv[1:]}"          
          print(msg)
   

except IndexError as e:
   msg = f"IndexError:{str(e)}"
   print(msg)
except Exception as e:
   # 「{e}」は、f"エラー発生: {str(e)}" と内部的にほぼ同じ書き方。eはエラーオブジェクトが代入された変数名。メッセージを返すプロパティは無い。
   # {e.args[0]} とも書ける筈。Pythonの設計思想として、例外の「メッセージ」は .args 属性（タプル）で管理されており、
   # 多くの場合それが1要素のタプル（('エラーメッセージ',)）になっています。
   msg = f"エラー発生:{e}"
   print(msg)
   
finally:
   mcb_shelf.close()
