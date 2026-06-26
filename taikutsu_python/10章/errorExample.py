#! python3
# errorExample.py
def spam():
    bacon()

def bacon():
    raise Exception('This is the error message.')

spam()

if __name__ == '__main__':
    # コマンドライン引数の処理
    import argparse
    parser = argparse.ArgumentParser(
        description='エラー例を示すスクリプトです。')
    