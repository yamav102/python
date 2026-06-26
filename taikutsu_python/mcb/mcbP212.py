#! python3
# mcb Multi Clip Board の略
# mcbP212.py pywをwindows11以降で使っても動かないので、.pyで作る。
# mcb.py の拡張版
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
# mcb.py は
   # a:mcbP212.py
   # a を ['save',<keyword>]の引数を指定して実行。⇒クリップボード内容が keywordに紐づけられて 'mcb'shelfに登録する
   # a を <keyword>の引数を指定して実行。⇒ keywordに紐づいていう内容をクリップボードに paste する
   # a を 'list' の引数を指定して実行。⇒ 'mcb'shelf に登録されている keyword 一覧をクリップボードに paste する
# py.exe mcbP212.py save <keyword> - クリップボードをキーワードに紐づけて保持➊ py.exeは、複数のpythonがインストールされていても最新バージョンを起動してくれる python lawncher。ランチャーとローンチは同じ言葉。起動する、という意味。
# py.exe mcbP212.py <keyword> キーワードに紐づけられたテキストをクリップボードにコピー
# py.exe mcbP212.py list - 全キーワードをクリップボードにコピー
# 拡張子 .py で動作確認できても、.pywにすると動作しない。.bat越しに実行しても結果は同じ。windows10以前ならコンソールウィンドウ非表示で動いたらしい。
# windows11 以降のosでは、「OSのセキュリティ強化で今はほぼ使い物にならなくなったのが現状です。(by grok)」との事。.py のまま使うのがとりあえず正解か。
# E:\yamaPythonScripts\mcb>python.exe mcb.pyw save key1　としてCMD上で実行すれば動作する。
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
   if len(sys.argv) == 3:
      if sys.argv[1].lower() == 'save': 
         mcb_shelf[sys.argv[2]] = pyperclip.paste() 
      # 演習8.10.1_1
      # 引数 delete <keyword> 2つ渡すと、シェルフから指定キーワードを削除する
      elif sys.argv[1].lower() == 'delete':
         #print('type(sys.argv[2])⇒' + str(type(sys.argv[2])))
         # deleteブロックの中にはさむ
         # key = sys.argv[2]
         # key_byte = key.encode('utf-8')
         # print('type(sys.argv[2])⇒' + str(type(key)))
         del mcb_shelf[sys.argv[2]]
   elif len(sys.argv) == 2:
       # キーワード一覧と、内容の読み込み # ❸
       if sys.argv[1].lower() == 'list': # ➊
           pyperclip.copy(str(list(mcb_shelf.keys()))) # ❷
       elif sys.argv[1].lower() == 'deleteall': # ➊

          # 演習8.10.1_2
          # 引数 deleteall 一つ渡すと、シェルフからキーワードを全削除する
   
           print('deleteallを通った')
           for k in mcb_shelf.keys():
              del mcb_shelf[k]
       elif sys.argv[1] in mcb_shelf:
          pyperclip.copy(mcb_shelf[sys.argv[1]])
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
   # msg = f"エラー発生:{e}"
   msg = f"エラー発生:{str(e)}"
   print(msg)
   
finally:
   mcb_shelf.close()
