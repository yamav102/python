#!/usr/bin/env python3
# lucky_playwright_debug.py

# Googleは明確にスクレイピングを禁止する方針を取っています。
# Googleの利用規約（Terms of Service）では、自動化された手段（ロボット、スクリプト、スクレイパーなど）でアクセスすることを禁じています。違反するとIPブロック、CAPTCHA、永久BANなどの対策を取られます。これがPlaywrightやSeleniumで苦戦する最大の理由です。特に個人で頻繁に実行すると、すぐに検知されます。

# SERP APIとは？SERP API（Search Engine Results Page API）は、Google検索結果を合法的かつ安定して取得するための有料APIサービスです。自分ではスクレイピングせず、専門業者がGoogleに対して大量のプロキシ・CAPTCHA回避・ブラウザ偽装などを駆使してデータを取得し、きれいなJSON形式で返してくれます。
# https://weel.co.jp/media/tech/serper-custom-search-json/
'''
 サードパーティ製にAPIを使わないと、検索エンジンのスクレイピングは
 「ロボット避け」と張り合うぐらいの知見が無いと、「難しい」という事。

'''




import argparse
import asyncio
import urllib.parse
import random
from pathlib import Path
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    parser = argparse.ArgumentParser(description='Google検索デバッグ版')
    parser.add_argument('search_words', nargs='*', help='検索ワード')
    args = parser.parse_args()

    if not args.search_words:
        parser.print_help()
        return

    query = ' '.join(args.search_words)
    print(f'Googling... "{query}"')

    encoded_query = urllib.parse.quote_plus(query)
    # url = f'https://www.google.com/search?q={encoded_query}&hl=ja&gl=jp'
    # google はロボット避けが厳しいので、amazon で試してみる。
    url = f'https://www.amazon.co.jp/s?k={encoded_query}&hl=ja&gl=jp'

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            locale="ja-JP",
            timezone_id="Asia/Tokyo",
        )

        page = await context.new_page()

        print("Googleにアクセス中...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        await page.wait_for_timeout(4000)

        # === デバッグ情報取得 ===
        title = await page.title()
        print(f"ページタイトル: {title}")

        # ページに表示されているテキストを一部取得
        body_text = await page.evaluate("document.body.innerText")
        print(f"\nページに含まれるテキスト（先頭300文字）:\n{body_text[:300]}...")

        # CAPTCHA検出
        captcha = await page.get_by_text("私はロボットではありません").count()
        if captcha > 0:
            print("✅ CAPTCHAページを検出しました")

        # スクリーンショット保存
        debug_dir = Path("debug_google")
        debug_dir.mkdir(exist_ok=True)
        await page.screenshot(path=debug_dir / "google_page.png")
        with open(debug_dir / "google_page.html", "w", encoding="utf-8") as f:
            f.write(await page.content())

        print(f"\nデバッグファイル保存完了 → {debug_dir} フォルダを確認してください")

        # 手動でCAPTCHAを解決したい場合
        if captcha > 0:
            print("\n手動でCAPTCHAを解決してください（ブラウザが開いています）")
            input("解決し終わったらEnterキーを押してください...")

        # h3を待機（無理に待たない）
        try:
            await page.wait_for_selector("h3", timeout=8000)
            titles = await page.locator("h3").all()
            print(f"見つかったh3要素: {len(titles)}個")
        except Exception as e:
            print(f"h3待機タイムアウト: {e}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())