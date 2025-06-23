#!/usr/bin/env python3
"""
GitHub Pages設定 & Secrets管理のナレッジを詳細Issueとして登録するスクリプト
"""

import os
import requests
import json
from datetime import datetime

def create_github_issue():
    """GitHub Issueを作成"""
    
    # GitHub API設定
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable not set")
        return False
    
    REPO = "bpmbox/AUTOCREATE"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Issue詳細内容
    issue_data = {
        "title": "🚀 GitHub Pages設定完全ガイド: React+Vite+shadcn UI + Secrets管理",
        "body": """## 📋 概要

React+Vite+shadcn UIアプリケーションをGitHub Pagesで公開し、GitHub SecretsでAPIキーを安全に管理する完全手順をドキュメント化。

## 🎯 学習ポイント

### 1. 🏗️ GitHub Pages基本設定
- `/docs`フォルダを使用したGitHub Pages設定
- `main`ブランチからの静的サイト公開
- Reactアプリの本番ビルド設定

### 2. ⚙️ Vite設定最適化
```typescript
// vite.config.ts
export default defineConfig(({ mode }) => ({
  base: mode === 'production' ? '/AUTOCREATE/chat/' : '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: mode === 'production' ? 'terser' : false,
  },
}));
```

### 3. 🚫 Jekyll無効化
```bash
# docs/.nojekyll ファイル作成
touch docs/.nojekyll
```
**重要**: GitHub PagesでReactアプリを正常動作させるため必須

### 4. 🔧 サブモジュール問題解決
```bash
# 古いサブモジュール削除
git submodule deinit -f AUTOCREATE.wiki
git rm -f AUTOCREATE.wiki

# 正しいサブモジュール再追加
git submodule add https://github.com/bpmbox/AUTOCREATE.wiki.git wiki
```

### 5. 🔐 GitHub Secrets管理
**設定したAPIキー一覧:**
- `HF_TOKEN` - Hugging Face API Token
- `GROQ_API_KEY` - Groq API Key
- `OPENAI_API_KEY` - OpenAI API Key
- `SUPABASE_URL` - Supabase Project URL
- `SUPABASE_KEY` - Supabase Anon Key
- `NOTION_TOKEN` - Notion Integration Token

### 6. 🤖 GitHub CLI自動化
```bash
# 一括Secrets設定
gh secret set HF_TOKEN --body "hf_xxxxxxxxxxxx"
gh secret set GROQ_API_KEY --body "gsk_xxxxxxxxxxxx"
gh secret set SUPABASE_URL --body "https://xxxxxxxxxxxx.supabase.co"
```

## 🛠️ 実装手順

### ステップ1: Viteビルド設定
1. `vite.config.ts`でGitHub Pages用base path設定
2. 本番ビルド用terser設定
3. `npm run build:prod`で本番ビルド

### ステップ2: GitHub Pages準備
1. `docs/`ディレクトリ作成
2. ビルド結果を`docs/chat/`にコピー
3. `.nojekyll`ファイル追加

### ステップ3: サブモジュール修正
1. 競合するサブモジュール削除
2. 正しいWikiサブモジュール追加
3. `.gitmodules`確認

### ステップ4: Secrets設定
1. `.env`ファイルからAPIキー抽出
2. GitHub CLI or Web UIでSecrets設定
3. GitHub Actions再実行

### ステップ5: 動作確認
1. GitHub Actions成功確認
2. `https://bpmbox.github.io/AUTOCREATE/`アクセス
3. `https://bpmbox.github.io/AUTOCREATE/chat/`でチャットアプリ確認

## 🚨 トラブルシューティング

### 404エラー対策
- [ ] Jekyll無効化 (`.nojekyll`追加)
- [ ] 正しいbase path設定
- [ ] GitHub Pages設定確認

### サブモジュールエラー
- [ ] `.gitmodules`の整合性確認
- [ ] 古いサブモジュール参照削除
- [ ] 正しいサブモジュールURL設定

### Secrets関連エラー
- [ ] GitHub Push Protection対応
- [ ] `.env`ファイルを`.gitignore`で除外
- [ ] 必要なAPIキーをSecretsに設定

## 📊 結果

✅ **成功項目:**
- React+Vite+shadcn UIアプリのGitHub Pages公開
- 9個のAPIキーをSecrets安全管理
- サブモジュール問題完全解決
- GitHub CLI自動化スクリプト作成

🔗 **公開URL:**
- メインページ: https://bpmbox.github.io/AUTOCREATE/
- AIチャットアプリ: https://bpmbox.github.io/AUTOCREATE/chat/

## 🎓 学習価値

このプロセスで学んだ重要な技術:
1. **GitHub Pages最適化** - 静的サイト公開のベストプラクティス
2. **Secrets管理** - セキュアなAPIキー管理手法
3. **CI/CD統合** - GitHub ActionsとSecrets連携
4. **サブモジュール運用** - 複雑なGitリポジトリ構成管理
5. **自動化スクリプト** - GitHub CLI活用による効率化

## 📝 次回への改善点

- [ ] GitHub Actions workflowの最適化
- [ ] 環境別Secrets管理戦略
- [ ] 自動テスト・デプロイパイプライン構築
- [ ] セキュリティスキャン自動化

---

**作成日**: 2025-06-24  
**タグ**: `github-pages`, `react`, `vite`, `secrets`, `automation`, `devops`  
**優先度**: High  
**ステータス**: ✅ 完了""",
        "labels": ["documentation", "github-pages", "automation", "devops", "enhancement"]
    }
    
    # GitHub Issue作成
    url = f"https://api.github.com/repos/{REPO}/issues"
    
    print("🚀 GitHub Issue作成中...")
    print(f"📋 タイトル: {issue_data['title']}")
    
    response = requests.post(url, headers=headers, json=issue_data)
    
    if response.status_code == 201:
        issue = response.json()
        print(f"✅ GitHub Issue作成成功!")
        print(f"🔗 URL: {issue['html_url']}")
        print(f"📊 Issue #{issue['number']}")
        return issue
    else:
        print(f"❌ GitHub Issue作成失敗: {response.status_code}")
        print(f"📝 エラー: {response.text}")
        return None

if __name__ == "__main__":
    print("🎯 GitHub Pages設定ナレッジをIssue登録")
    print("=" * 50)
    
    issue = create_github_issue()
    
    if issue:
        print("\n🎉 ナレッジ登録完了!")
        print("📚 今回の学習内容が詳細ドキュメントとして保存されました")
        print("🔄 今後のプロジェクトで参照・活用可能です")
    else:
        print("\n❌ ナレッジ登録失敗")
        print("🔧 手動でGitHub Issueを作成してください")
