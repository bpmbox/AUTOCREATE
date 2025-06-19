# 🐍 Python版clasp API - 完全セキュア版

Google Apps ScriptをPythonから操作するセキュアなAPIシステム

## ✅ 特徴

- **🔐 完全セキュア**: 認証情報は全て環境変数から取得
- **🌐 GitHub対応**: Secret Scanning対応済み
- **⚡ 高速実行**: OAuth2認証でGAS関数を直接実行
- **🎯 n8n対応**: Webhook/外部システムから利用可能

## 🚀 クイックスタート

### 1. 環境変数設定

`.env` ファイルに以下を追加:

```bash
# Google API Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REFRESH_TOKEN=your_google_refresh_token
GOOGLE_SCRIPT_ID=your_google_apps_script_id
```

### 2. 基本使用

```python
from python_clasp_secure import PythonClaspAPI

# APIインスタンス作成
clasp = PythonClaspAPI()

# 基本テスト
result = clasp.execute_gas_function(function_name="gastest")
print(result)

# 外部IP取得
ip_result = clasp.execute_gas_function(function_name="getExternalIP")
print(f"外部IP: {ip_result.get('result')}")
```

### 3. Google Docs作成

```python
from python_clasp_secure import webhook_google_docs_endpoint

# Google Docs自動作成
doc_result = webhook_google_docs_endpoint(
    title="AUTOCREATEシステムガイド",
    content="カスタム内容"
)

if doc_result["status"] == "success":
    print(f"作成完了: {doc_result['document']['url']}")
```

## 🧪 テスト実行

```bash
# セキュリティテスト
python python_clasp_secure_test.py

# デモ実行
python python_clasp_secure.py
```

## 🌐 n8n/Webhook連携

### Webhook用エンドポイント

```python
# Flask/FastAPI例
@app.post("/webhook/gas-execute")
def execute_gas_function(function_name: str, params: list = None):
    clasp = PythonClaspAPI()
    result = clasp.execute_gas_function(
        function_name=function_name,
        parameters=params
    )
    return result

@app.post("/webhook/create-docs")
def create_docs(title: str = None, content: str = None):
    return webhook_google_docs_endpoint(title=title, content=content)
```

### n8nワークフロー例

1. **HTTP Request Node**: トリガー受信
2. **Function Node**: データ処理
3. **HTTP Request Node**: Python clasp API呼び出し
4. **Send Response**: 結果返送

## 🔧 利用可能な機能

### GAS関数実行
- `gastest()` - 基本テスト
- `getExternalIP()` - 外部IP取得
- `sendLineMessage()` - LINE連携
- `callGradioChatAPI()` - Gradio連携
- `createAUTOCREATESystemGuide()` - Google Docs作成

### API機能
- OAuth2自動認証
- トークン自動更新
- エラーハンドリング
- 実行時間測定

## 🛡️ セキュリティ

### 環境変数使用
```python
# ❌ 危険: ハードコード
client_id = "actual_client_id_here"

# ✅ 安全: 環境変数
client_id = os.getenv('GOOGLE_CLIENT_ID')
```

### .gitignore対応
```gitignore
.env
.env.*
*credentials*
```

## 📊 システム要件

- Python 3.7+
- requests
- python-dotenv
- Google Apps Script プロジェクト
- OAuth2認証設定

## 🔗 関連リンク

- [Google Apps Script](https://script.google.com/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth2 設定ガイド](https://developers.google.com/identity/protocols/oauth2)

## 🎊 AUTOCREATEシステム統合

このPython版clasp APIは、AUTOCREATEシステムの一部として開発されました:

- **pyautogui自動化** + **Python clasp API** = 完全自動化
- **Supabase監視** → **VS Code操作** → **Google Docs作成**
- **n8n連携** → **外部システム統合**

---

⭐ **AUTOCREATE = AI社長 × 無職CTO × Python版clasp API**
