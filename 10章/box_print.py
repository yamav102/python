#! python3
# box_print.py
# テキストを箱型にして表示する関数
def box_print(symbol: str, width: int, height: int) -> None:
    if len(symbol) != 1:
        raise ValueError('symbol は1文字でなければなりません。')
    if width < 2:
        raise ValueError('width は2以上でなければなりません。')
    if height < 2:
        raise ValueError('height は2以上でなければなりません。')
    
    print(symbol * width)
    for _ in range(height - 2):
        print(symbol + (' ' * (width - 2)) + symbol)    
    print(symbol * width)

for sym, w, h in (('*', 4, 4), ('O', 20, 5), ('x', 1, 3),('ZZ', 3, 3)):
    try:
        box_print(sym, w, h)
    except Exception as err:
        print(f'エラー: {err}')

if __name__ == '__main__':
    # コマンドライン引数の処理
    import argparse
    parser = argparse.ArgumentParser(
        description='四角形を描画する関数 box_print をテストします。',
        epilog='例: python box_print.py "*" 4 4')
    parser.add_argument('symbol', help='四角形を描画するための1文字のシンボル')
    parser.add_argument('width', type=int, help='四角形の幅 (2  以上)')
    parser.add_argument('height', type=int, help='四角形の高さ (2  以上)')
    
    args = parser.parse_args()
    box_print(args.symbol, args.width, args.height)
