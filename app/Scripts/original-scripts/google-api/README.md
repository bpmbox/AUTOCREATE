# 🔧 Google API スクリプト集

Google API操作・統合用スクリプト

## 📋 含まれるスクリプト

### 🐍 Python版clasp API
- `python_clasp_secure.py` - メインAPIシステム（完全セキュア版）
- `python_clasp_api.py` - 従来版API
- `python_clasp_template.py` - テンプレート版

## 🎯 このフォルダーの目的

- **Google Apps Script操作**: Python経由でGAS関数実行
- **OAuth2認証**: セキュアな認証情報管理
- **Google Docs作成**: 自動ドキュメント生成
- **外部システム統合**: n8n/Webhook対応

## 🌟 主な機能

### セキュリティ強化
- 認証情報は100%環境変数管理
- GitHub Secret Scanning対応
- OAuth2自動トークン更新

### 統合機能
- Google Apps Script関数リモート実行
- Google Docs自動作成・編集
- 外部システムからのWebhook呼び出し

## 🚀 使用方法

### 基本的な使用
```python
from python_clasp_secure import PythonClaspAPI

# API初期化
clasp = PythonClaspAPI()

# GAS関数実行
result = clasp.execute_gas_function(function_name="gastest")
```

### Webhook/n8n対応
```python
from python_clasp_secure import webhook_google_docs_endpoint

# Google Docs作成
docs_result = webhook_google_docs_endpoint(title="テストドキュメント")
```

## 📝 新しいスクリプト追加時

```bash
# 新しいGoogle APIスクリプト作成
scripts/google-api/google_new_feature.py
```

## 🔧 環境要件

### 必要な環境変数
```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret  
GOOGLE_REFRESH_TOKEN=your_google_refresh_token
GOOGLE_SCRIPT_ID=your_google_apps_script_id
```

### 依存関係
- Python 3.7+
- requests
- python-dotenv

---

**セキュアで強力なGoogle API操作で、自動化を実現しましょう！**
