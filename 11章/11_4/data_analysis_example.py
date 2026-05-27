# %% [markdown]
# # データ分析の典型的な流れ（インタラクティブ用サンプル）

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'sans-serif'  # または 'Yu Gothic', 'Meiryo' など環境に合ったフォント
plt.rcParams['font.sans-serif'] = ['Yu Gothic', 'Meiryo', 'MS Gothic', 'Hiragino Sans']
import seaborn as sns

# %%
# --- 1. データの読み込み ---
# 注意: 実際のデータファイルに置き換えてください
# df = pd.read_csv('your_data.csv')   # ← ここを自分のデータに変更

# サンプルデータで試したい場合はこちらを使う（おすすめ）
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 40, 28],
    'salary': [70000, 80000, 95000, 120000, 65000],
    'department': ['Sales', 'Engineering', 'Engineering', 'Management', 'Sales']
}
df = pd.DataFrame(data)

print("データ形状:", df.shape)
df.head()

# %%
# --- 2. 簡単な前処理 ---
print("基本統計量:")
print(df.describe())

# 部門ごとの平均年収
print("\n部門ごとの平均年収:")
print(df.groupby('department')['salary'].mean())

# %%
# --- 3. 可視化 ---
plt.figure(figsize=(8, 5))
sns.barplot(x='department', y='salary', data=df, estimator=np.mean)
# plt.title('部門ごとの平均年収')
plt.title('部門別 平均年収(万円)')
plt.xlabel('部署')
plt.ylabel('年収 (円)')
# plt.ylabel('Salary')
plt.show()

# %%
# --- 4. さらに分析を追加したいときの例 ---
# 年齢と年収の散布図
plt.figure(figsize=(8, 5))
sns.scatterplot(x='age', y='salary', hue='department', data=df, s=100)
plt.title('年齢と年収の関係')
plt.show()
# %%
