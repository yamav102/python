#! python3
# coinFlip.py
from pathlib import Path
import logging
import random
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s ] %(name)s %(message)s',
    handlers=[
        logging.FileHandler(
            Path(__file__).parent / 'coinFlip.log',
            encoding = 'utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

heads = 0
for i in range(1, 1001):
    if random.randint(0, 1) == 1:
        heads = heads + 1
    if i == 500:
        print('半分完了！')
print(f'表は{heads}回出ました。')

if __name__ == '__main__':
    logger.info('正常終了')