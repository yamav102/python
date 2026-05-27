#! python3
# send_gmail.py
# 要：pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path
import argparse
# 必要に応じてスコープを変更（送信だけならこれで十分）
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main(to_email, subject, body):
    # カレントディレクトリ を 実行スクリプトの親フォルダにする
    os.chdir(Path(__file__).resolve().parent)
    print(os.getcwd())

    creds = None
    # token.json があれば読み込む（2回目以降は認証不要）
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 認証が必要な場合
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # ブラウザで認証画面が開く

        # 次回以降のために保存
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()
        message.set_content(body)
        message['To'] = to_email
        message['Subject'] = subject
        # Fromは自動であなたのGmailアドレスになる

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {'raw': encoded_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        
        print(f"✅ 送信成功！ Message ID: {send_message['id']}")
        
    except HttpError as error:
        print(f"❌ エラー発生: {error}")

# ==================== 使い方 ====================
if __name__ == "__main__":
    # send_email(
    #     to_email="yamav102@gmail.com",
    #     subject="テストメール",
    #     body="これはPython + Gmail APIで送信したテストメールです。\n\n改行もできます。"
    # )
    parser = argparse.ArgumentParser(
        description='arg1:メールアドレス arg2:件名 arg3:本文',
        epilog='c:>py sendmail test@hoge.com test件名 test本文'
    )
    parser.add_argument(
        'tomail',
        help='メールアドレス'
        )
    parser.add_argument(
        'subject',
        help='件名'
    )
    parser.add_argument(
        'body',
        help='メール本文'
    )    
    args = parser.parse_args() 
    
    main(args.tomail, args.subject, args.body)     