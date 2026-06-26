#! python3
# buggyAddingProgram.py
# デバッグの練習
import logging
from pathlib import Path
def setup_logging():
    # Root logger を明示的に取得して設定
    root = logging.getLogger() # ここで root logger が見える形になる
    root.setLevel(logging.INFO)
    root.handlers.clear()      # 以前の設定のクリア（念為

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    # ファイルハンドラ
    file_handler = logging.FileHandler(
        Path(__file__).parent / 'app.log', encoding= 'utf-8'
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    # コンソールハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    print('足し合わせる第一の数を入力してください:')
    first = input()
    print('足し合わせる第二の数を入力してください:')
    second = input()
    print('足し合わせる第三の数を入力してください:')
    third = input()
    print('合計は ' + first + second + third)


if __name__  == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__) # 無ければ生成して取得。
    logger.info(__name__ + 'のlogger')
