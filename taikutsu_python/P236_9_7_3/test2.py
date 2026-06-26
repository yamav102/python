def asdf():
    asdf()
if True:
    import re
    from pathlib import Path

    def rename_files(tgt, prefix, suffix):
        # 対象フォルダをPathオブジェクト化
        tgt = Path(tgt)
        # 対象フォルダ内のファイルから、接頭辞と拡張子を除いた部分が数字のみのものを抽出
        nums = []
        for file in tgt.iterdir():
            if file.is_file() and file.name.startswith(prefix) and file.name.endswith(suffix):
                num_part = file.name[len(prefix):-len(suffix)]
                if num_part.isdigit():
                    nums.append(int(num_part))    
# python は　同一シグネチャの関数が複数ある場合、最後に定義された関数が有効になる。（まじかー
    def rename_files(tgt, prefix, suffix):
        # 対象フォルダをPathオブジェクト化
        tgt = Path(tgt)
        # 対象フォルダ内のファイルから、接頭辞と拡張子を除いた部分が数字のみのものを抽出
        nums = []
        for file in tgt.iterdir():
            if file.is_file() and file.name.startswith(prefix) and file.name.endswith(suffix):
                num_part = file.name[len(prefix):-len(suffix)]
                if num_part.isdigit():
                    nums.append(int(num_part))                      

