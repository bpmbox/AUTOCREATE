# 🚀 GitHub Issue作成テンプレート - GitHub CLI対応

## 基本的なIssue作成

```bash
# 基本形
gh issue create --repo "bpmbox/AUTOCREATE" \
  --title "🎯 実装要求タイトル" \
  --body "実装の詳細説明" \
  --label "ai-automation"

# 文字化け対策版 (PowerShell)
$env:PYTHONUTF8=1; gh issue create --repo "bpmbox/AUTOCREATE" --title "タイトル" --body "内容" --label "ai-automation"
```

## 実装完了報告用Issue

```bash
# 完了報告Issue
gh issue create --repo "bpmbox/AUTOCREATE" \
  --title "✅ [プロジェクト名] - 完全実装完了" \
  --body "# 実装完了報告

## 成果物
- プロジェクトフォルダ: [フォルダ名]
- 実装ファイル数: [ファイル数]
- テスト結果: [テスト結果]
- リポジトリURL: [URL]

## 技術的詳細
- 使用技術: [技術スタック]
- 実装時間: [時間]
- 特記事項: [特記事項]

---
🤖 Created by: GitHub Copilot AI
📅 Date: $(Get-Date -Format 'yyyy-MM-dd')
⚡ Execution Time: [実行時間]
🎯 Success Rate: 100%
" \
  --label "ai-automation"
```

## Copilot用プロンプトテンプレート

GitHub Copilotに送信する際のプロンプトに含めるべき内容：

```
📋 GitHub CLI実行指示

1. Issue作成コマンド:
gh issue create --repo "bpmbox/AUTOCREATE" --title "🎯 [質問内容] - 実装要求" --body "[詳細説明]" --label "ai-automation"

2. 文字化け対策:
$env:PYTHONUTF8=1 を設定してから実行

3. 完了報告Issue:
gh issue create --repo "bpmbox/AUTOCREATE" --title "✅ [質問内容] - 完全実装完了" --body "[実装結果詳細]" --label "ai-automation"

🔥 重要: GitHub CLI認証確認
gh auth status

🎯 必須ラベル: "ai-automation"
🏛️ 対象リポジトリ: bpmbox/AUTOCREATE
```

## エラー対処

### 認証エラー
```bash
gh auth login
```

### 文字化けエラー
```powershell
$env:PYTHONUTF8=1
chcp 65001
```

### リポジトリアクセスエラー
```bash
gh auth refresh -s repo
```
