import os
import sys
import json
import requests
from typing import Dict, Any
from coingecko_sdk import Coingecko
from msal import ConfidentialClientApplication

def load_config(file_path: str = "config.json") -> Dict[str, Any]:
    """設定ファイルを読み込みます"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"エラー: 設定ファイル '{file_path}' が見つかりません。")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"エラー: '{file_path}' の形式が正しくありません。")
        sys.exit(1)

def send_email_via_graph(config: Dict[str, Any], subject: str, body: str) -> None:
    """Microsoft Graph APIを使用してメールを送信します"""
    ms_config = config.get("microsoft_graph", {})
    client_id = ms_config.get("client_id")
    tenant_id = ms_config.get("tenant_id")
    client_secret = ms_config.get("client_secret")
    sender_email = ms_config.get("sender_email")
    recipient_email = ms_config.get("recipient_email")

    if not all([client_id, tenant_id, client_secret, sender_email, recipient_email]):
        print("警告: Microsoft Graph の設定が不足しているため、メールを送信できません。")
        return

    # MSALでアクセストークンを取得
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
    token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    if "access_token" not in token_response:
        print(f"エラー: アクセストークンの取得に失敗しました: {token_response.get('error_description')}")
        return

    access_token = token_response["access_token"]
    
    # メール送信APIのリクエスト
    endpoint = f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient_email
                    }
                }
            ]
        }
    }

    response = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json=email_data
    )

    if response.status_code == 202:
        print(f"メール通知を送信しました: {recipient_email}")
    else:
        print(f"エラー: メールの送信に失敗しました ({response.status_code}): {response.text}")

def fetch_crypto_prices() -> None:
    config = load_config()

    # CoinGecko APIキー
    api_key = config.get("coingecko_api_key")
    if not api_key:
        print("エラー: 'coingecko_api_key' が設定ファイルに記述されていません。")
        sys.exit(1)

    client = Coingecko(
        demo_api_key=api_key,
        environment="demo"
    )

    try:
        price_data = client.simple.price.get(
            ids="bitcoin,ethereum",
            vs_currencies="jpy"
        )

        print("=== 現在の仮想通貨価格 (JPY) ===")
        thresholds = config.get("thresholds", {})
        alert_messages = []

        for coin_id in ["bitcoin", "ethereum"]:
            try:
                # price_data['bitcoin'].jpy の形式でアクセス
                coin_data = price_data[coin_id]
                price = coin_data.jpy
                
                print(f"{coin_id.capitalize():<10}: ¥{price:,.0f}")
                
                # 閾値判定
                threshold = thresholds.get(coin_id)
                if threshold and price >= threshold:
                    msg = f"通知: {coin_id.capitalize()} の価格が閾値 ¥{threshold:,.0f} を超えました (現在: ¥{price:,.0f})"
                    alert_messages.append(msg)
                    print(f"  [ALERT] {msg}")
            except (KeyError, AttributeError):
                print(f"{coin_id.capitalize():<10}: データの取得に失敗しました。")

        # 閾値を超えた場合にメール送信
        if alert_messages:
            subject = "【仮想通貨アラート】価格が閾値を超えました"
            body = "\n".join(alert_messages)
            send_email_via_graph(config, subject, body)

    except Exception as e:
        print(f"APIリクエスト中にエラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_crypto_prices()
