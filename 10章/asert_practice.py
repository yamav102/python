#! python3
# assert_practice
# assertの練習: 信号シミュレーションにアサートを用いる

import logging
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s') # 効果不明？

# マーケット通りと２番通りの交差点
market_2nd = {'ns': 'green', 'ew': 'red'}
# ミッション通りと１６番通りの交差点
mission_16th = {'ns': 'red', 'ew': 'green'}

def switch_lights(stoplight:dict) -> None:
    for key in stoplight.keys():
        if stoplight[key] == 'green':
            stoplight[key] = 'yellow'
        elif stoplight[key] == 'yellow':
            stoplight[key] = 'red'
        elif stoplight[key] == 'red':
            stoplight[key] = 'green'
        assert 'red' in stoplight.values(), '赤信号がない！' + str(stoplight)

switch_lights(market_2nd)
print("done")

