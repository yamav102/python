def get_shifted_descending_indexes(indexes: list[int], mn: int, mx: int) -> list[int]:
    """
    [mn〜mx] の範囲を空けるために、後続の番号を押し上げる
    
    ルール:
      - mn より小さい番号 → そのまま保持
      - mn〜mx の範囲に当たる番号が見つかったら、その位置から後ろ全部を +1 する
      - これを mn から mx まで順番に実行（これにより範囲全体が空く）
      - 元々あった「飛び」は維持される
    """
    if not indexes:
        return []
    
    # 昇順で処理
    result = sorted(indexes)
    
    # mn から mx まで順番に「その番号がまだ存在したら押し出す」
    for blanknum in range(mn, mx + 1):
        # blanknum と一致する位置を探す
        for i in range(len(result)):
            if result[i] == blanknum:
                # 見つかった位置から最後まで全部 +1
                for j in range(i, len(result)):
                    result[j] += 1
                break  # 1つ見つかったら次の blanknum へ
    
    # 降順にして返す
    result.sort(reverse=True)
    return result

# indexes = [2,1,3,4,6,8] 
# indexes = []
# # indexes = [4,6,8,]
# print(get_shifted_descending_indexes(indexes, 5, 7))
def test_get_shifted_descending_indexes():
    tests = [
        # 1. 範囲内に全くない → 後続はシフトされない（あなたのコードの仕様）
        ([1, 3, 4], 2, 2, [4, 3, 1]),           # 2がない → そのまま
        ([1, 3, 5], 2, 4, [7, 5, 1]),           # 3 → 4, 4 → 5 +2シフト
        
        # 2. 範囲内に一部ある（あなたの最初の例）
        ([2, 1, 3, 4, 6, 8], 5, 7, [10, 8, 4, 3, 2, 1]),   # 6だけ該当 → 6→7, 8→10
        
        # 3. 範囲内に複数ある
        ([1, 2, 3, 4, 5, 6, 7, 8], 5, 7, [11, 10, 9, 8, 4, 3, 2, 1]),  # 5,6,7全部該当 → +3シフト
        ([1, 5, 6, 10], 5, 7, [13, 9, 8, 1]),                      # 5,6該当 → +2シフト, 7は6のシフトで生成されるので、さらに +1シフト（合計 +3）
        
        # 4. 範囲の端だけ該当
        ([1, 5, 8], 5, 7, [11, 8, 1]),      # mn=5だけ該当
        ([1, 7, 8], 5, 7, [9, 8, 1]),       # mx=7だけ該当
        ([1, 4, 5], 5, 7, [8, 4, 1]),       # mn=5だけ
        
        # 5. 範囲より小さい番号だけ
        ([1, 2, 3, 4], 5, 7, [4, 3, 2, 1]), # 既に空き番号になっているので、何もシフトされない
        
        # 6. 範囲より大きい番号だけ
        ([10, 12, 15], 5, 7, [15, 12, 10]), # 既に空き番号になっているので、何もシフトされない
        
        # 7. 特殊ケース
        ([], 5, 7, []),                     # 空リスト
        ([5], 5, 5, [6]),                   # 範囲内1つだけ → それを空けるために +1 → 結果は6
        ([1, 5, 5], 5, 5, [6, 6, 1]),       # 重複がある場合
        ([10, 9, 8], 1, 1, [10, 9, 8]),    # 小さい範囲 → 既に空き番号になっているので、何もシフトされない
    ]
    errcnt = 0
    for indexes, mn, mx, expected in tests:
        result = get_shifted_descending_indexes(indexes, mn, mx)
        # assert result == expected, f"Failed: {indexes}, {mn}-{mx} → {result} != {expected}"
        if result != expected:
            print(f"Failed: {indexes}, {mn}-{mx} → 結果:{result} , 期待値: {expected}")
            errcnt += 1
    if errcnt == 0:
        print("✅ すべてのテスト通過！")
    else:
        print(f"❌ {errcnt}件のテスト失敗")
    

test_get_shifted_descending_indexes()