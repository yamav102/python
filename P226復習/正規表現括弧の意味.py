import re

texts = ["19月", "12月", "2月", "20月", "09月"]

for t in texts:
    no_group = re.search(r'0?[1-9]|1[0-2]月', t)
    with_group = re.search(r'(?:0?[1-9]|1[0-2])月', t) # (?:⇒グループ化はしたけれど、非キャプチャにしている。
    
    print(f"文字列: {t:6}")
    print(f"  括弧なし → {no_group.group() if no_group else '×'}")
    print(f"  括弧あり → {with_group.group() if with_group else '×'}")
    print()
