#! python3
# x_minimum_post.py
import tweepy

client = tweepy.Client(
    consumer_key="sxsqW2rj2IGtcVFXRMorK1rmj",
    consumer_secret="txMlFV4jcKv5lMUzXzs5RP2gPBmSlXtY5BIxuQbWB4f97FnbBc",
    access_token="116830056-lu8VHAUCQ31L48clFdxJySlD842ghXvLbayG7HZm",
    access_token_secret="wsgb2gQaT8qXdf9nnBmKogzJEs63oEq3r8yinVakxT2lB",
)

# フリープランだと厳しい↓
# response = client.create_tweet(text="テスト投稿 from Python (2026/7/7)")
# print(response)

# ユーザー名からユーザー情報を取得
# user = client.get_user(username="yamav102")
# print("ユーザーID:", user.data.id) # type: ignore

# # 自分の最新ツイートを取得
# response = client.get_users_tweets(
#     id=me.data.id,      # 自分のユーザーID
#     max_results=10
# )

# if response.data: # type: ignore
#     # print('hoge')
#     for tweet in response.data: # type: ignore
#         print(f"{tweet.id} : {tweet.text[:100]}...")
# else:
#     print("ツイートが見つかりませんでした")


# 最も基本的な読み取り
me = client.get_me(user_fields=['public_metrics'])
print(me.data) # type: ignore
print("フォロワー数:", me.data.public_metrics['followers_count']) # type: ignore
# おぉ！出来た。！！
# yamav102
# フォロワー数: 1687

# 自分の詳細情報
me = client.get_me(user_fields=['public_metrics', 'description', 'created_at'])
print("ユーザー名:", me.data.username)
print("表示名:", me.data.name)
print("自己紹介:", me.data.description)
print("フォロワー数:", me.data.public_metrics['followers_count'])
print("フォロー数:", me.data.public_metrics['following_count'])

# yamav102
# フォロワー数: 1687
# ユーザー名: yamav102
# 表示名: yamaV1.02β
# 自己紹介: つげ義春と吾妻ひでおとＥＬＰを愛でるふうてん
# フォロワー数: 1687
# フォロー数: 2257