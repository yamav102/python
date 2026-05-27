#! python3
# Grepmodoki.py
# Usage:
# cmdで >cd <Grepmodoki.pyのあるディレクトリ>
# cmdで >Grepmodoki.py を実行
# 実行ディレクトリに tgtFolder がある事が動作条件
def main():
    tgtFolder = 'tgtFolder'
    import os, re
    if not os.path.isdir(tgtFolder):
        print(tgtFolder + ' フォルダが必要です。')
        return 1

    while True:
        try:        
            print(tgtFolder + '下のtxtファイルから、指定正規表現のパターンにマッチする行を検索します。')
            print("例：")
            print("  abc             → abc を含む行")
            print("  error|警告      → error または 警告 を含む行")
            print("  ^\\s*$          → 空行のみ")
            print("  (?i)todo        → 大文字小文字区別なく 'todo' を含む行")
            print("**** 検索終了は Ctrl + C ******")
            print("")    
            pattern = input('正規表現を入力してください。').strip()
            print() # 出力結果とユーザー入力値の間に空行挿入。どこからが出力なのかの区切りになって、操作感良くなる。
    

            flist = [
                f for f in os.listdir(tgtFolder)
                if f.lower().endswith('.txt') and os.path.isfile(os.path.join(tgtFolder, f))
                ]
                        
            regex = re.compile(pattern) # 正規表現が正しくない場合クラッシュせずに？エラーにできる
            found_any = False
            for f in flist:
                row = 0
                last_file = None
                with open(os.path.join(tgtFolder,f) ,'r', encoding = 'utf-8') as txt:                    
                    for line in txt:
                        row += 1
                        if regex.search(line):
                            #print('ファイル名: 'f, '行: ' + str(rw) + line.rstrip('\n') ,)
                            # ANSIカラー（Windows 10以降なら有効）
                            #print(f"ファイル名: {f} 行:{rw}\033[1;33m{line.rstrip('\r\n')}\033[0m")←f文字列（f"..."）の中の {...} 式（式部分）にはバックスラッシュ \ を直接書けない
                            if last_file != f:
                                print(f"\n=== {f} ===")
                                last_file = f
                            # print(f"ファイル名: {f} 行:{row}   \033[1;33m{line.rstrip()}\033[0m") ←問題なく動く
                            print(
                                "ファイル名: {} "
                                "行:{} "
                                "\033[1;33m{}\033[0m".format(f, row, line.rstrip('\r\n'))
                                )

                            found_any = True
            if not found_any:
                print("該当する行は見つかりませんでした。")

            print()
        
        
        except re.error as e:
            print(f'正規表現エラー:{e}')
            continue # もう一度入力してもらう
        # Ctrl+C
        except KeyboardInterrupt:
            print("\n終了します")
            return 0
        except Exception as e:
            print(f"エラー発生: {e}")
            return 1
        
if __name__ == '__main__':    
    main()
