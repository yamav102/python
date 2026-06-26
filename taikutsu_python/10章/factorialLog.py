#! python3
# factorialLog.py
# factorial:階乗
# logging の使い方を理解する事を目的とする。

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
script_dir = Path(__file__).parent.resolve()
log_file = script_dir / 'factorial.log'
handler = RotatingFileHandler(
    filename=log_file,
    maxBytes= 10 * 1024 ** 2, # 10MB
    backupCount= 30, # 30日分のこす
    encoding= 'utf-8'
)

# 最初に一回だけ設定（できれば main ガードの中で）
logging.basicConfig(
    # ↓こうしておくと、DEBUGをログに出さない。大文字なのは定数だから。
    # DEBUG < INFO < WARNING < ERROR < CRITICAL:10<20<30<40<50。
    # INFO, WARNING は本番でも残すべき.　ERROR, CRITICAL は消すべきではない。
    # level=logging.INFO, 
    # ----------------------------------
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        handler
        # logging.FileHandler(log_file, encoding='utf-8'),
        # logging.StreamHandler() # コンソールにも出力したい場合
    ]
)

logger = logging.getLogger(__name__) # これが現代的な書き方

def factorial(n: int) -> int:
    logger.debug('factorial(%s) 開始', n) # フォーマットは , で渡す（おすすめ）
    total = 1
    for i in range(1, n + 1):
        total *= i
        #logger.debug('i = %d, total = %d', i, total)
        logger.debug('i = %s, total = %s', i, total)
    logger.debug('factorial(%s) 終了', n)
    return total

if __name__ == "__main__":
    print(factorial(5)) # 結果だけは pirnt でOK
    logger.info('プログラム正常終了')