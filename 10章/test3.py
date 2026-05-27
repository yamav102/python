#! python3

# import test2
# test2.hoge()
# from pathlib import Path
# pt = Path(__file__).parent
# print(pt)
import logging
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        force=True
    )

logger = logging.getLogger(__name__)
#logger.debug("これはsetup_logging前なので出ないはず")   # ← まだ出ない
logger.warning("これはsetup_logging前だが、"
               "defaultのlevelはwarningなので出る筈")   # ← 出る
print('ここは出るます')
if __name__ == "__main__":
    setup_logging()                                   # ← ここで設定
    logger.debug("ここからは出るようになる")           # ← 出る