# 仮想通貨価格監視ツール (CoinGecko API & Microsoft Graph Email)

このツールは、CoinGecko APIを使用してビットコイン（BTC）とイーサリアム（ETH）の現在価格（日本円）を取得し、あらかじめ設定した**閾値を下回った場合**に Microsoft Graph API を通じてメール通知を行います。

## 事前準備

1. **CoinGecko APIキーの取得**
   https://www.coingecko.com/en/api でAPIキーを取得してください（Demo APIキー）。

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
       "bitcoin": 8000000,
       "ethereum": 300000
     }
   }
   ```

   ※ `config.json` は `.gitignore` に含まれているため、GitHubにはプッシュされません。

4. **仮想環境の作成と有効化**
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

5. **ライブラリのインストール**
   仮想環境が有効な状態で、以下のコマンドを実行してください。
   ```bash
   pip install -r requirements.txt
   ```

## 自動実行の設定 (Windows)

Windows のタスクスケジューラを使用して、09:00 から 23:00 の間で 3 時間ごとに自動実行するように設定できます。

1. **管理者として PowerShell を起動**し、プロジェクトディレクトリへ移動します。
2. 以下のコマンドを実行して、タスクを登録します。
   ```powershell
   .\setup_crypto_task.ps1
   ```

### タスクの削除
自動実行を停止したい場合は、以下のコマンドを実行してください。
```powershell
.\remove_crypto_task.ps1
```

## 仕様

- **判定基準**: 現在価格が `config.json` で指定した `thresholds` の値を**下回った場合**（`<=`）に通知します。
- **通知方法**: Microsoft Graph API を使用して、指定されたメールアドレスにアラートを送信します。

## 注意事項

- APIキーやシークレットを公開リポジトリに絶対にプッシュしないでください。
- 閾値（`thresholds`）は日本円で指定してください。
