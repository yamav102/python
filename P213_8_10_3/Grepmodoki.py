#! python3
# Grepmodoki.py
# Usage:
# cmdで >cd <Grepmodoki.pyのあるディレクトリ>
# cmdで >Grepmodoki.py を実行
# 実行ディレクトリに tgtFolder がある事が動作条件
def main():
    tgtFolder = 'tgtFolder'
    print(tgtFolder + '下のtxtファイルから、指定正規表現のパターンにマッチする行を検索します。')
    pattern = input().strip()

    try:
        # フォルダ内ファイルをリストで取得
        import os
        # print('p1:' + str(os.listdir(tgtFolder))) # os.listdir：直下のファイル名やフォルダ名をリストで返す
        # f for f... は「リスト内包表記」という便利な書き方。
        # 普通の for 文で書くと
        '''
        result = []
            for f in files:
                if 条件(f):
                    result.append( ここに何かを入れる )
        '''
        flist = [
            f for f in os.listdir(tgtFolder)
            if f.lower().endswith('.txt') and os.path.isfile(os.path.join(tgtFolder, f))
            ]
        
        # print('p2:' + str(flist))
        import re
        for f in flist:
            rw = 0
            with open(os.path.join(tgtFolder,f) ,'r', encoding = 'utf-8') as txt:
                for line in txt:
                    rw = rw + 1
                    result = re.search(pattern, line)
                    if result:
                        print(line.rstrip('\n') ,f, '行: ' + str(rw))
    except Exception as e:
        print(f"エラー発生: {e}")
        
if __name__ == '__main__':    
    main()
