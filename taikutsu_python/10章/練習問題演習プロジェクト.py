#! python3
# 練習問題演習プロジェクト.py
# コイン投げゲームをデバッグする
import logging
import random
guess = ''
#while guess not in ('表', '裏'):
while guess not in ('1', '0'):
    # print('コインの表裏を当ててください。表か裏かを入力してください:')
    print('コインの表裏を当ててください。表:1 か、裏:0 かを入力してください:')
    guess = input()
assert guess in ('1', '0'),'guess は intger で、1 か 0 です。'
toss = random.randint(0, 1) # 0:裏、1:表

if toss == int(guess):
    print('当たり！')
else:
    print('はずれ！もう一回当てて！')
    guess = input()
    if toss == int(guess):
        print('当たり！')
    else:
        print('はずれ。このゲームは苦手ですね。')

if __name__ == '__main__':
    # ログ設定は mainガードの中に書くべき。
    # そうしないと、import された場合、勝手にログ設定が変わってしまうリスクがある。
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname) [%(name)%] - %(message)s",
        force= True # これまでのログ設定を上書きする。
        # __main__ で実行される箇所であれば、書いておく事が強く推奨される
        )

