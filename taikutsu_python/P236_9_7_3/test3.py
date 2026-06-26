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
    
    # 昇順並び替えたコピーを取る
    result = sorted(indexes)
    # i: mn～mx を順番に見ていく
    # pos: result の中を順番に見ていくための位置
    # shift: mn～mx の範囲を空けるために、resultでの位置を後方へずらすため加算する値    
    for i in range(mn,mx+1):
        flg = True # 内側の forループを抜けるためのフラグ
        for pos in range(0,len(result)):
            # if flg == False:
            #     break
            if result[pos] == i:                            
                shift = 0 # 空けたい番号毎に、後続の番号に加算する値をリセット
                while True:
                    result[pos + shift] += 1
                    shift += 1 # 次の配列要素（result の最終要素までループして、+1 加算する）
                    if (pos + shift) >= len(result):                        
                        # # resultの最後まで来たら、内側のループを抜けるためのフラグを立てて、break
                        # flg = False
                        break              
                break # 1つ見つかったら、次の i へ（同じ番号が複数あっても、1回押し上げれば十分だから）            
    # 降順並び替え
    result.sort(reverse = True)
    return result

def main():
    # indexes = [2,1,3,4,5,6,7,8,9]
    # indexes = [1,3,4,]
    indexes = [4,6,8,]
    mn = 5
    mx = 7
    print(_get_shifted_descending_indexes(indexes, mn, mx))

main()