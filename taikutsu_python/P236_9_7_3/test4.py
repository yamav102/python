#! python3
# test3.py
def _get_shifted_descending_indexes(indexes: list[int], mn: int, mx: int)-> list:
  
    """
    指定範囲 [mn〜mx] を空けるために、後続の番号を適切に押し上げる
    
    特徴:
      - mnより小さい番号はそのまま保持
      - mn〜mxの範囲を空ける
      - それ以降の番号は「空けた分だけ」押し上げる（飛びは維持）
    """
    if not indexes:
        return []
        
    # 昇順並び替えたコピーを取る
    idx = sorted(indexes)
    result = []
    shift = 0
    for num in idx:
        if num < mn:
            result.append(num) # mnより小さい番号はそのまま保持
        else:
            result.append(num + shift) # それ以降の番号は「空けた分だけ」加算
            if mn <= num <= mx:
                shift += 1 # mn〜mxの範囲を空けるため、shiftを増加
                        
    # 降順並び替え
    indexes.sort(reverse = True)
    return indexes

def main():
    # indexes = [2,1,3,4,5,6,7,8,9]
    # indexes = [1,3,4,]
    indexes = [2,1,3,4,6,8,]
    mn = 5
    mx = 7
    print(_get_shifted_descending_indexes(indexes, mn, mx))

main()