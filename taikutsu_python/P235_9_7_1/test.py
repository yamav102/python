from pathlib import Path

def _safe_copy(src_path, dst_path, preserve_metadata=True)->Path:
    src = Path(src_path)
    dst = Path(dst_path)
    
    # parents=True で、親フォルダを一気に作成
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise FileExistsError(f'{dst} は既に存在します。')
    else:
        return src.copy(dst, preserve_metadata=preserve_metadata)

# 使い方
_safe_copy("c:/a/b/c.txt", "e:/a/b/c.txt")