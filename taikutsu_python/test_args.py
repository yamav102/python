import sys

print("--- sys.argv ---")
print(sys.argv)

print("\n--- 引数の数 ---")
print(len(sys.argv))

print("\n--- 各引数 ---")
if len(sys.argv) > 1:
    for i, arg in enumerate(sys.argv):
        print(f"インデックス {i}: {arg}")
else:
    print("引数がありませんでした。")

print("\n--- スクリプト名を除いた引数 ---")
# スクリプト名を除いた引数のみを取り出す
args_only = sys.argv[1:]
print(args_only)