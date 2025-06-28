#!/usr/bin/env python3
"""
🚀 AI自動化システム - OpenAPI拡張仕様
====================================

OpenAPI/Swagger仕様を拡張し、他のAIが理解しやすい形式でAPIを提供
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any

def custom_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """カスタムOpenAPIスキーマ生成"""
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="🚀 AI Development Platform - AI自動化API",
        version="1.0.0",
        description="""
# 🤖 AI Development Platform - Automation API

**他のAIシステムが理解・利用可能な自動化APIプラットフォーム**

## 🎯 概要

このAPIは、GitHub Copilot自動化システムをFastAPIエンドポイントとして公開し、
他のAIシステムからプログラマティックにアクセス可能にします。

## 🚀 主要機能

### 1. 完全自動化実行 (`POST /automation/run`)
- ユーザーのメッセージを受け取り
- GitHub Issue作成
- Mermaid図生成
- Copilot統合処理
- 全て自動実行

### 2. GitHub統合 (`POST /automation/issue/create`)
- Issue作成
- ラベル設定
- 担当者アサイン
- GitHub CLI連携

### 3. Mermaid図生成 (`POST /automation/mermaid/generate`)
- フローチャート、シーケンス図など
- 自動ファイル保存
- HTMLプレビュー生成

### 4. リアルタイム監視 (`WS /automation/ws/monitor`)
- WebSocketでのシステム状態監視
- リアルタイムログ配信

## 🤖 AI向け使用例

### Python例
```python
import requests

# 完全自動化実行
response = requests.post(
    "http://localhost:7860/automation/run",
    json={
        "message": "React+TypeScriptでTodoアプリを作成",
        "create_issue": True,
        "generate_mermaid": True
    }
)
print(response.json())
```

### JavaScript例
```javascript
// GitHub Issue作成
const response = await fetch('/automation/issue/create', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        title: 'AI提案: 新機能実装',
        description: '詳細な実装要求...',
        labels: ['enhancement', 'ai-generated']
    })
});
```

### cURL例
```bash
# システム状態確認
curl -X GET "http://localhost:7860/automation/status"

# Mermaid図生成
curl -X POST "http://localhost:7860/automation/mermaid/generate" \\
  -H "Content-Type: application/json" \\
  -d '{"content": "ユーザー認証フロー", "diagram_type": "sequence"}'
```

## 🔧 他のAIシステム向けガイド

### 1. 認証
現在は認証不要です。本番環境では適切な認証を実装してください。

### 2. レート制限
開発環境では制限なし。本番環境では適切なレート制限を設定してください。

### 3. エラーハンドリング
全エンドポイントでHTTPステータスコードとエラーメッセージを返します。

### 4. 非同期処理
長時間処理は `background_tasks` で非同期実行されます。

## 📊 レスポンス形式

全てのレスポンスは以下の形式に従います：

```json
{
  "success": true,
  "message": "処理完了",
  "data": {...},
  "processing_time": 1.23
}
```

## 🔗 関連リソース

- **GitHub**: https://github.com/bpmbox/AUTOCREATE
- **Wiki**: プロジェクトWikiで詳細ドキュメント
- **Issues**: GitHub Issuesでバグ報告・機能要求

## 📞 サポート

質問や問題がある場合は、GitHub Issuesまたは自動化システム経由でお問い合わせください。

---

*このAPIは他のAIシステムからの利用を想定して設計されています*
        """,
        routes=app.routes,
    )
    
    # 追加のAI向けメタデータ
    openapi_schema["info"]["x-ai-compatible"] = True
    openapi_schema["info"]["x-automation-platform"] = "GitHub Copilot + FastAPI"
    openapi_schema["info"]["x-target-audience"] = "AI Systems and Developers"
    
    # AI向けタグの詳細説明
    openapi_schema["tags"] = [
        {
            "name": "AI Automation",
            "description": "AI自動化システムの主要エンドポイント",
            "externalDocs": {
                "description": "詳細ドキュメント",
                "url": "https://github.com/bpmbox/AUTOCREATE/wiki"
            }
        },
        {
            "name": "Laravel API",
            "description": "Laravel風システム管理API",
            "externalDocs": {
                "description": "Laravel風アーキテクチャ",
                "url": "https://laravel.com/docs"
            }
        }
    ]
    
    # AI向けのサンプルワークフロー
    openapi_schema["x-ai-workflows"] = {
        "complete_automation": {
            "description": "完全自動化ワークフロー",
            "steps": [
                {"step": 1, "endpoint": "POST /automation/run", "description": "自動化実行開始"},
                {"step": 2, "endpoint": "GET /automation/status", "description": "ステータス確認"},
                {"step": 3, "endpoint": "WS /automation/ws/monitor", "description": "リアルタイム監視"}
            ]
        },
        "issue_creation": {
            "description": "GitHub Issue作成ワークフロー",
            "steps": [
                {"step": 1, "endpoint": "POST /automation/issue/create", "description": "Issue作成"},
                {"step": 2, "endpoint": "POST /automation/mermaid/generate", "description": "図表生成"},
                {"step": 3, "endpoint": "GET /automation/status", "description": "完了確認"}
            ]
        }
    }
    
    # AI向けのコード例
    openapi_schema["x-code-examples"] = {
        "python": {
            "complete_automation": """
import requests

response = requests.post(
    "http://localhost:7860/automation/run",
    json={
        "message": "新機能を実装してください",
        "create_issue": True,
        "generate_mermaid": True
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"処理完了: {result['message']}")
    if result.get('issue_url'):
        print(f"作成されたIssue: {result['issue_url']}")
""",
            "status_check": """
import requests

response = requests.get("http://localhost:7860/automation/status")
status = response.json()

if status['github_cli_available']:
    print("GitHub CLI利用可能")
if status['supabase_connected']:
    print("Supabase接続済み")
"""
        },
        "javascript": {
            "issue_creation": """
async function createIssue(title, description) {
    const response = await fetch('/automation/issue/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            title: title,
            description: description,
            labels: ['ai-generated']
        })
    });
    
    const result = await response.json();
    if (result.success) {
        console.log('Issue作成成功:', result.issue_url);
    }
}
""",
            "websocket_monitor": """
const ws = new WebSocket('ws://localhost:7860/automation/ws/monitor');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('システム状態:', data);
};

ws.onopen = function() {
    console.log('リアルタイム監視開始');
};
"""
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def setup_enhanced_openapi(app: FastAPI):
    """拡張OpenAPIスキーマの設定"""
    
    def custom_openapi():
        return custom_openapi_schema(app)
    
    app.openapi = custom_openapi
    
    # 追加のメタデータ設定
    app.title = "🚀 AI Development Platform - AI自動化API"
    app.description = "他のAIシステムが理解・利用可能な自動化APIプラットフォーム"
    app.version = "1.0.0"
    
    print("✅ 拡張OpenAPIスキーマ設定完了")
    print("📖 Swagger UI: /docs")
    print("📚 ReDoc: /redoc")
    print("🤖 AI向け拡張仕様を含みます")
