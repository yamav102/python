#! python3
# lucky.py P278 11.5
# google検索結果をいくつか開く
# lucky.pyはうまく行かない
'''
現在のGoogle検索ページでは、requests + BeautifulSoupだけでは実用的に検索結果のリンクを安定して取るのが非常に難しい状況になっています。なぜUser-AgentだけではダメなのかGoogleはJavaScriptで検索結果を後から描画している部分が大きい。
requestsはJSを一切実行しないので、初回にサーバーから返ってくるHTML（ほぼ結果が入っていない）しか取得できない。
クラス名（.zReHsなど）はGoogleが頻繁に変更・難読化する（A/Bテストでも変わる）。2026年現在、.zReHsはすでに古くなっています。

User-Agentをブラウザ風にしても、JS実行 + 追加のボット検知で十分な結果が得られにくくなっています。
'''
import requests
# import sys
import argparse
import webbrowser
from bs4 import BeautifulSoup

def main(args: argparse.Namespace)->str:
    '''
    処理の概説
    '''    
    # Googleページを\ダウンロード中にテキスト表示
    print('Googling...') 
    search_words = args.search_words # 
    
    url = ('https://www.google.com/search?q=' + 
        ' ' .join(search_words) 
    )
    # res = requests.get(url) このまま取得してもjs実行まえのソースを取得するだけなので、スクレイピングが出来ない。
    # User-Agent にブラウザを指定して js実行後のソースを取得できるようにしている。
    # Googleは公式に検索API（Custom Search JSON APIなど）を提供しているので、本気で検索結果を扱うならスクレイピングではなくAPIを使うことを強くおすすめします。
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)    
    res.raise_for_status()
    restext = res.text
    #TODO: 上位の検索結果のリンクを取得する
    # soup はhtmlソースを返すのではなく、パースしたhtml構造を
    # 構築したオブジェクト。printするとhtmlを返すが、構築した内部ツリーから
    # もう一度テキストに戻した値を返している。
    # 単なる文字列ではなく、.find(), .select(), .prettify(), .text など
    # 便利なメソッドを持っている。
    # BeatifulSoupを使う最大のメリットは、解析済みである事。
    soup = BeautifulSoup(
        res.text, features='html.parser') 
    # class="zReHs" の aタグが、検索結果のリンクである事を
    # htmlソースを観察して突き止める。google検索ページの仕様が変われば
    # このスクリプトは動かなくなる。
    link_elems = soup.select('.zReHs a')
    if len(link_elems) == 0:
        raise Exception('検索結果を取得できません。')
    #TODO: リンクをブラウザの各タブで開く
    num_open = min(5, len(link_elems))
    for i in range(num_open):
        webbrowser.open('http://google.com' + link_elems[i].get('href'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='検索ワードをスペース区切りで列挙して引数を渡します。',
        epilog='c:>py lucky word1 word2 ...'
    )
    parser.add_argument(
        'search_words',
        # 指定引数の数が不定で、
        # 指定しなくても良い場合の書き方。
        # 一つ以上指定ならば ='+'
        # n は number の 'n'との事。リストで渡される。
        nargs='*', 
        help='検索ワードを、スペース区切りで指定します。'
        )
    args = parser.parse_args() 
    # print(f'type(args.search_words):{type(args.search_words)}') # <class 'list'>
    print(f'type(args):{type(args)}')
    # print(f'str(args):{str(args)}')
    # print(f'str(args): {args}')                    # デバッグ用
    # print(f'search_words: {args.search_words}')    # これが普通の使い方    
    # main(args.search_words) リストだけを渡す
    main(args) # python標準的な書き方はこっち