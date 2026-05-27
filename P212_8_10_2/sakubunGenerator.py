#! python3
# sakubunGenerator.py
# Usage: cmdで
out_file = None
try:
    
    print('Enter an adjective')
    adjective = input()

    print('Enter an noun')
    noun1 = input()

    print('Enter an verb')
    verb = input()    

    print('Enter an noun')
    noun2 = input()
    
    sakubun = (
       'The ADJECTIVE panda walked to the NOUN '
       'and then VERB. A nearby NOUN was unaffected by these events.'
       )
    # 置き換え
    sakubun = sakubun.replace('ADJECTIVE', adjective)
    # replace の３つめの引数は、置き換える数(count.ただし名前付きでの指定は出来ない)。
    # 文字列左から１つ目まで置き換える指定。
    sakubun = sakubun.replace('NOUN', noun1, 1)
    sakubun = sakubun.replace('VERB', verb)
    sakubun = sakubun.replace('NOUN', noun2)

    # テキストファイル出力
    out_file = open('sakubunOutput.txt', 'w')    
    out_file.write(sakubun)
    import os
    print(os.path.abspath(out_file.name) + " を出力しました。")
    
except Exception as e:
    msg = f'エラー発生:{e}'
    print(msg)
finally:    
    if out_file is not None :
        try:
            out_file.close()
        except Exception as close_err:
            print(f"close 失敗: {close_err}")
