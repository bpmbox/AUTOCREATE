# JIRA統合 完全セットアップガイド

## 📋 概要

このガイドでは、AUTOCREATEプロジェクトにJIRA統合機能を設定する方法を説明します。

## 🎯 実現される機能

- ✅ **自動チケット作成**: AUTOCREATE開発タスクの自動生成
- ✅ **プロジェクト管理**: JIRA内でのタスク進捗管理
- ✅ **統合ワークフロー**: Notion + GitHub + JIRAの連携
- ✅ **品質管理**: 標準化されたチケットテンプレート

## 🔧 セットアップ手順

### 1. JIRA Cloudアカウント準備

#### アカウント作成・確認
```bash
# JIRAアカウントの作成または確認
# https://www.atlassian.com/software/jira/free にアクセス
# 無料アカウントを作成（最大10ユーザーまで無料）
```

#### ドメイン確認
- JIRAのURL形式: `https://your-domain.atlassian.net`
- 例: `https://autocreate-team.atlassian.net`

### 2. API Token作成

#### 手順
1. **アカウント設定にアクセス**
   ```
   https://id.atlassian.com/manage-profile/security/api-tokens
   ```

2. **新しいAPIトークンを作成**
   - 「APIトークンを作成」をクリック
   - ラベル: `AUTOCREATE Integration`
   - 作成されたトークンをコピーして保存

3. **トークンの保存**
   ```bash
   # 重要: トークンは一度しか表示されません
   # 安全な場所に保存してください
   ```

### 3. JIRAプロジェクト作成

#### プロジェクト作成手順
1. **JIRA管理画面にアクセス**
   ```
   https://your-domain.atlassian.net
   ```

2. **新しいプロジェクトを作成**
   - プロジェクト名: `AUTOCREATE`
   - プロジェクトキー: `AUTOCREATE`
   - プロジェクトタイプ: `Kanban`

3. **プロジェクト設定確認**
   ```bash
   # プロジェクトキーとボードIDを確認
   # URL例: https://your-domain.atlassian.net/projects/AUTOCREATE/board/1
   ```

### 4. 環境変数設定

#### .envファイル更新
```bash
# JIRAセクションを以下のように更新
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@domain.com
JIRA_API_TOKEN=your_generated_api_token_here
JIRA_PROJECT_KEY=AUTOCREATE
JIRA_BOARD_ID=1
```

#### 設定例
```bash
# 実際の設定例（値は各自のものに置き換えてください）
JIRA_URL=https://autocreate-team.atlassian.net
JIRA_USERNAME=team@autocreate.com
JIRA_API_TOKEN=ATATT3xFfGF0...（実際のトークン）
JIRA_PROJECT_KEY=AUTOCREATE
JIRA_BOARD_ID=1
```

### 5. 設定テスト

#### 接続テスト実行
```bash
# 基本的な設定確認
make jira-status

# 詳細な診断実行
make jira-diagnostics

# API接続テスト
make jira-test
```

#### 期待される出力
```
✅ JIRA API接続成功！
   👤 ユーザー: Your Name
   📧 メール: your-email@domain.com
```

## 🚀 使用方法

### チケット作成

#### 開発タスクチケット作成
```bash
# AUTOCREATE開発用のチケットを一括作成
make jira-create-tickets
```

#### ビジネスプロセスチケット作成
```bash
# プロセス改善用チケットを作成
python jira_ticket_creator.py
# 選択肢 2 を選択
```

#### 統合展開
```bash
# Notion + GitHub + JIRA の統合展開
make triple-deploy
```

### 作成されるチケット例

| チケットタイプ | 内容 | 優先度 |
|---------------|------|--------|
| 🎯 Notion統合システム | Notion API統合実装 | High |
| 🌐 Chrome拡張機能 | XPath設定管理システム | High |
| 📚 ナレッジベース | 自動生成システム | Medium |
| 🛡️ セキュリティ | 認証・権限管理 | High |
| 📊 ダッシュボード | プロジェクト管理UI | Medium |

## 🛠️ トラブルシューティング

### よくある問題と解決方法

#### 1. 認証エラー
```bash
❌ JIRA API接続失敗: 401
```

**解決方法:**
- API Tokenが正しく設定されているか確認
- JIRAのユーザー名（メールアドレス）が正しいか確認
- .envファイルの再読み込み

#### 2. プロジェクトが見つからない
```bash
❌ Project 'AUTOCREATE' not found
```

**解決方法:**
- JIRAでプロジェクトが作成されているか確認
- プロジェクトキーが正しいか確認
- ユーザーにプロジェクトアクセス権限があるか確認

#### 3. チケット作成失敗
```bash
❌ JIRAチケット作成失敗: 400
```

**解決方法:**
- Issue Typeが存在するか確認（Task, Story, Epic）
- Priority設定が正しいか確認（High, Medium, Low）
- プロジェクト設定でCustom Fieldsの確認

### デバッグコマンド

```bash
# 設定確認
make jira-status

# 詳細診断
make jira-diagnostics

# ヘルプ表示
make jira-setup-guide

# ログ確認
python jira_ticket_creator.py
```

## 📊 効果測定

### 期待される効果

| 指標 | 効果 |
|------|------|
| チケット作成時間 | 95%削減 |
| 標準化レベル | 100%統一 |
| プロジェクト可視性 | 90%向上 |
| チーム生産性 | 40%向上 |

### 測定方法

1. **作成前後の時間測定**
   - 手動作成: 30分/チケット
   - 自動作成: 1分/8チケット

2. **品質指標**
   - テンプレート準拠率: 100%
   - 情報漏れ: 0件
   - フォーマット統一: 100%

## 🔄 継続的改善

### 定期メンテナンス

1. **月次レビュー**
   - チケットテンプレートの見直し
   - 新しい業務プロセスの追加
   - 効果測定とレポート

2. **チーム フィードバック**
   - 使いやすさの確認
   - 機能要望の収集
   - 改善提案の実装

### 拡張可能性

- **他システム連携**: Slack、Teams通知
- **自動化拡張**: GitHub Actions連携
- **レポート機能**: Power BI、Tableau連携
- **AI統合**: チケット内容の自動最適化

## 📚 参考資料

### 公式ドキュメント
- [JIRA REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)
- [JIRA Cloud Administration](https://support.atlassian.com/jira-cloud-administration/)

### 内部ドキュメント
- `NOTION_INTEGRATION_SUCCESS.md`: Notion統合の成功事例
- `RESOURCE_FIRST_SUCCESS_REPORT.md`: 統合展開の実績
- `Makefile`: 利用可能なコマンド一覧

## 🎯 次のステップ

1. **設定完了後**
   ```bash
   make jira-create-tickets
   ```

2. **統合テスト**
   ```bash
   make triple-deploy
   ```

3. **運用開始**
   - チームへの展開
   - 効果測定開始
   - 継続的改善プロセス開始

---

**📞 サポート**
設定でお困りの場合は、`make jira-setup-guide` でヘルプを表示するか、AUTOCREATE開発チームにお問い合わせください。
