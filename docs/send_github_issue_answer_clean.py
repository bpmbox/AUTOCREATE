#!/usr/bin/env python3
"""
GitHub Issue登録についてSupabaseに回答を送信
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

# 環境変数読み込み
load_dotenv()

def send_github_issue_answer():
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not all([supabase_url, supabase_key]):
            print("❌ 環境変数が設定されていません")
            return False
        
        supabase = create_client(supabase_url, supabase_key)
        
        # GitHub Issue登録についての詳細回答
        answer = """🤖 GitHub Copilotからの回答

質問「gitissueにも登録しよう」について詳しくご説明いたします：

## 🐛 GitHub Issue登録の方法

### 1. **手動でIssue作成**
1. GitHubリポジトリページにアクセス
2. "Issues" タブをクリック
3. "New issue" ボタンを押す
4. タイトルと詳細を入力
5. ラベル・担当者を設定
6. "Submit new issue" で作成

### 2. **GitHub CLI使用**
```bash
# GitHub CLIをインストール
winget install GitHub.cli

# 認証
gh auth login

# Issue作成
gh issue create --title "タイトル" --body "詳細内容" --label "bug,enhancement"
```

### 3. **API経由で自動作成**
```python
import requests

def create_github_issue(repo, title, body, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': title,
        'body': body,
        'labels': ['auto-created', 'copilot-system']
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

## 🚀 このプロジェクト用のIssue例

### おすすめタイトル:
- 🤖 GitHub Copilot自動回答システム改善
- 📡 外部システム連携API実装
- 🔐 セキュリティ強化対応
- 📊 ログ・監視機能追加

### 推奨ラベル:
- enhancement (機能追加)
- bug (バグ修正)
- automation (自動化関連)
- copilot (GitHub Copilot関連)
- supabase (Supabase関連)

## 🔧 すぐに実行できるコマンド

```bash
# GitHub CLIでIssue作成
gh issue create --title "🤖 Copilot自動回答システム改善" --body "Supabaseとの連携をより安定化させる" --label "enhancement,automation"

# 複数Issue一括作成
gh issue create --title "📊 監視ダッシュボード作成" --label "enhancement"
gh issue create --title "🔐 認証システム強化" --label "security"
```

現在のプロジェクトの進捗に合わせて、どのようなIssueを作成されたいでしょうか？具体的な内容をお聞かせいただければ、すぐにIssue登録のお手伝いをいたします！

🎯 お役に立てれば幸いです！"""

        # Supabaseに回答を投稿
        result = supabase.table('chat_history').insert({
            'ownerid': 'GitHub Copilot Assistant',
            'messages': answer,
            'created': datetime.now().isoformat()
        }).execute()
        
        print('✅ GitHub Issue登録についての回答をSupabaseに送信しました！')
        if result.data:
            print(f'📊 投稿ID: {result.data[0]["id"]}')
        print('🎯 回答内容を送信完了')
        
        return True
        
    except Exception as e:
        print(f'❌ エラー: {e}')
        return False

if __name__ == "__main__":
    send_github_issue_answer()
