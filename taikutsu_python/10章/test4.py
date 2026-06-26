#! python3
# test4.py
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('test.log', encoding='utf-8') ,         
        logging.StreamHandler()
        ]
)
logger = logging.getLogger(__name__)
logger.info('infoのテスト')