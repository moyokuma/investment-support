# 仮想通貨価格取得ツール (CoinGecko API & Microsoft Graph Email)

このツールは、CoinGecko APIを使用してビットコイン（BTC）とイーサリアム（ETH）の現在価格（日本円）を取得し、あらかじめ設定した閾値を超えた場合に Microsoft Graph API を通じてメール通知を行います。

## 事前準備

1. **CoinGecko APIキーの取得**
   https://www.coingecko.com/en/api でAPIキーを取得してください。

2. **Microsoft Graph API の設定 (Azure Portal)**
   - Azure Portal (https://portal.azure.com) でアプリ登録を行ってください。
   - `Mail.Send` アプリケーション許可 (Application Permission) を付与し、管理者の同意を得てください。
   - クライアントID、テナントID、クライアントシークレットを取得してください。

3. **設定ファイル (config.json) の作成**
   プロジェクトのルートディレクトリに `config.json` を作成し、以下の内容を記述してください。

   ```json
   {
     "coingecko_api_key": "YOUR_COINGECKO_API_KEY",
     "microsoft_graph": {
       "tenant_id": "YOUR_TENANT_ID",
       "client_id": "YOUR_CLIENT_ID",
       "client_secret": "YOUR_CLIENT_SECRET",
       "sender_email": "sender@yourdomain.com",
       "recipient_email": "receiver@anydomain.com"
     },
     "thresholds": {
       "bitcoin": 10000000,
       "ethereum": 500000
     }
   }
   ```

   ※ `config.json` は `.gitignore` に含まれているため、GitHubにはプッシュされません。

4. **仮想環境の作成と有効化**
   - **Windows:** `python -m venv venv` -> `.\venv\Scripts\activate`
   - **macOS / Linux:** `python3 -m venv venv` -> `source venv/bin/activate`

5. **ライブラリのインストール**
   ```bash
   pip install -r requirements.txt
   ```

## 実行方法

```bash
python get_crypto_price.py
```

## 注意事項

- APIキーやシークレットを公開リポジトリに絶対にプッシュしないでください。
- 閾値（`thresholds`）は日本円で指定してください。
