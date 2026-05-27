#! python3
# 練習問題 10-4
# logging させるための最小限のコード

# import logging
# logging.basicConfig(level=logging.DEBUG) # 既定の level は warning
# logger = logging.getLogger(__name__)


# logger.debug('ログです') # ⇒ DEBUG:__main__:ログです

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s- %(message)s')

logging.debug('本書の回答はこれだった')
# ⇒ 2026-04-23 16:30:44,163 - DEBUG- 本書の回答はこれだった