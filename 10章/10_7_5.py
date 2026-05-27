#! python3
# 10_7_5.py
# 練習問題 10-5
# ファイルにlogging させるための最小限のコードを２行で書け
from pathlib import Path
import logging
log_file = Path(__file__).parent / 'programlog.txt'
logging.basicConfig(
    filename=log_file,
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s- %(levelname)s - %(message)s',
    ) 

logging.debug('10章練習問題　10-5')

