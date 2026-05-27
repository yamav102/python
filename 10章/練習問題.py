#! python3
# 10章練習問題
import logging
from pathlib import Path
# ============== 定数・設定 =======================
log_file = Path(__file__).parent / 'renshumondai10.log'
# ========================~=======================
def setup_logging(logging_level: int = logging.DEBUG) -> None:
    """
    プロジェクト全体のログ設定（最初に一回だけ呼ぶ）
    """
    # ルートログ
    root = logging.getLogger() 
    root.setLevel(logging_level)
    # 既存のハンドラをクリア
    root.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    #コンソール出力
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    # ファイル出力
    file_handler = logging.FileHandler(
        log_file,
        encoding='utf-8'
        )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

# 10-1
def ren10_1()->None:
    ''' docstringはこの位置に書くのが python の作法。
      変数 spam が10未満の時に AssertionError となる assert文
    '''
    for spam in range(11,1,-1):
        # print(spam)
        assert spam >= 10,'spam は 10以上です' 
# 10-2
def ren10_2()->None:
    '''
    変数 eggs bacon が大文字、小文字 を区別せず同じ文字列である場合に、
    エラーになる assert文
    '''
    eggs = 'abC'
    bacon = 'Abc'
    assert \
        eggs.upper() != bacon.upper(), (
        "eggs bacon は大文字小文字を区別しない場合に異なる文字列になります。"
    )
# 10-3
def ren10_3()->None:
    '''
    常に assertError になる assert文
    '''
    assert False,"常にassertエラー"
# 10-4 ⇒ 10_7_4.py
# 10-5 ⇒ 10_7_5.py
# 10-6
# ５つのログレベルは何か？
def ren10_6()->dict:
    '''
    root logger の levelの既定値は WARNING
    子logger の level は root の level を継承するが、単独では NOTSET:0
    NOTSET < DEBUG < INFO < WARNING < ERROR  < CRITICAL
    WARN, FATAL は非推奨（廃止予定の古い書き方）
    '''
    return logging.getLevelNamesMapping()
# 10-7
def ren10_7():
    '''
    全てのログメッセージを無効にする
    '''
    logging.disable() 
    # 引数なしの書き方は python3.7以降
    # 、logging.disable(loggin.CRITICAL) と同等。
    
    logging.critical('disableの確認') # 表示されない。

# 10-8
# print() でログを出力すべきではない理由。
# loggingは制御が容易。print()は無効にしたい場合、全スクリプトの箇所を修正するのは大変。
# タイムスタンプ、どのスクリプトのログなのか、呼び出し先のスクリプトにもLevelの継承が出来る 
# など、ログ取得に特化した機能を使える。

# 10-9
# STEP実行、
# OVER:呼び出し先関数でのステップをスキップする
# OUT: ステップ中の関数のステップを抜ける

# 10-10
# Goボタンは、最後まで実行するか、ブレークポイントで止まるか。

# 10-11 設定した位置で一時停止させｒ機能が「ブレークポイント」

# 10-12
# IDLEでコードの行にブレークポイントを置く手順は？
# 行を右クリックして、[Set Breakpoint]を選択する。

# ren10_1()
# ren10_2()
# ren10_3()
# print(ren10_6()) # {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40, 'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
# ren10_7()

# mainガードはスクリプトの最後に実行する
# 関数の外側：平場での logging.debug はデフォルトlevelが warningなので
# 無視されるが、平場に log 出力を記述して良い事はないらしい。
if __name__ == '__main__':
    setup_logging(logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('logging設定完了')

