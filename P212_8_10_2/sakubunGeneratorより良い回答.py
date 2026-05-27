#! python3
# sakubunGeneratorより良い回答.py
# Usage: cmdで >sakubunGeneratorより良い回答.py を実行
def main():
    print('Enter an adjective')
    adjective = input().strip()

    print('Enter an noun')
    noun1 = input().strip()

    print('Enter an verb')
    verb = input().strip()

    print('Enter an noun')
    noun2 = input().strip()

    template = (
       'The {ADJECTIVE} panda walked to the {NOUN1} '
       'and then {VERB}. A nearby {NOUN2} was unaffected by these events.'
       )

    # 安全に置き換え
    text = template.format(
        ADJECTIVE = adjective,
        # 2つの {NOUN}が noun1 に置き換わる
        NOUN1 = noun1,
        VERB = verb,
        # Pythonでは 関数呼び出しやリスト・辞書・タプル・setなどの
        # 最後の要素の後にカンマを付けても構文エラーにならない
        # ようになっています。
        # コードを後から編集するときに便利（新しい行を追加してもgit差分が汚れない）
        NOUN2 = noun2,        
    )

    filename = 'sakubunOutput.txt'
    try:
        with open(filename, 'w', encoding = 'utf-8') as f:
            f.write(text + '\n')
        import os
        print(f"出力しました：{os.path.abspath(filename)}")
    except PermissionError as e:
        # print("書き込み権限がありません。別のフォルダで試してください。")
        print(f"PemissionError:{str(e)}")
    except Exception as e:
        print(f"エラー発生:{e}") # エラー発生:[Errno 13] Permission denied: 'sakubunOutput.txt'

if __name__ == '__main__':
    main()
