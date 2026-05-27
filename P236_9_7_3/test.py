

def 計測器(func):           # ← デコレータの定義
    def wrapper():
        print("処理を開始します")
        func()             # 元の関数を実行
        print("処理が終わりました")
    return wrapper
@計測器 # デコレータ―
def main():
    print('こんにちは')
main()