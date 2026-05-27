#! python3

def aa(arg1):
    print(str(arg1))

import argparse
parser = argparse.ArgumentParser('関数の説明？',
                                description='ここに関数の説明を書く？',
                                epilog='エピローグな説明')
parser.add_argument('arg1',
                    help='引数の説明をここに書く？'
                    )
args = parser.parse_args()
aa(args.arg1)   