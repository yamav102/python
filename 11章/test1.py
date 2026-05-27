#! python3
# test1.py
import logging
import os
from pathlib import Path
os.chdir(Path(__file__).parent)
print('aaa:' + str(Path.cwd()))


if __name__ == '__main__':
    # logger
    logging.basicConfig(
        level= logging.DEBUG,
        format='%(asctime)s [%(levelname)s %(name)s - %(message)s ]',
        force= True,
                        )