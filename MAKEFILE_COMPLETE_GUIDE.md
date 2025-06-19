# 🤖 AUTOCREATE Makefile 完全ガイド

AUTOCREATEシステムの全機能を操作するMakefileコマンド集

## 📋 目次

- [🚀 クイックスタート](#-クイックスタート)
- [📱 Chrome拡張機能](#-chrome拡張機能)
- [🤖 AI・自動化システム](#-ai自動化システム)
- [🌐 Google API操作](#-google-api操作)
- [📚 ナレッジマネジメント](#-ナレッジマネジメント)
- [🔗 外部連携](#-外部連携)
- [🧪 テスト・デバッグ](#-テストデバッグ)
- [🛠️ 開発・メンテナンス](#️-開発メンテナンス)

---

## 🚀 クイックスタート

### 最重要コマンド（今すぐ使える）

```bash
# 🏃‍♂️ すぐに始められるコマンド
make app                    # FastAPIアプリケーション起動
make chrome-ext             # AI CEO Chrome拡張機能
make gui                    # AI GUI desktop環境
make wiki-rag               # WIKI RAG知識システム
make help                   # 全コマンド一覧表示
```

### システム概要確認

```bash
make config-check           # 環境設定確認
make integration-status     # 全連携サービス状態
make safe-test             # 安全な統合テスト（dry-run）
```

---

## 📱 Chrome拡張機能

### 基本操作

```bash
make chrome-ext             # Chrome拡張機能起動
make chrome-ext-test        # テストページ + Supabase連携
make chrome-ext-status      # 拡張機能の状態確認
```

### 高度な機能

```bash
make chrome-ext-ai-test     # AI応答機能テスト
make chrome-ext-xpath-config # XPath設定マネージャー
make chrome-ext-typeerror-test # TypeError修正検証
make chrome-ext-error-status # 現在のエラー状況
```

### 特徴
- **リアルタイムAI応答**: ChatGPT連携でWebページから直接質問
- **Supabase連携**: データベースと完全同期
- **自動化対応**: pyautogui自動化システムとの統合

---

## 🤖 AI・自動化システム

### AI-Human協業システム

```bash
make ai-human-bpms          # AI-Human BPMS システム起動
make bpms-analyze           # 人間の認知能力・ワークフロー解析
make bpms-optimize          # 人間フレンドリーなワークフロー生成
make bpms-monitor           # 人間-AI協業効果監視
make cognitive-check        # 人間の認知負荷確認・休憩提案
```

### RPA・OCR自動化

```bash
make ocr-gradio             # OCR Gradio インターフェース
make ocr-rpa-demo           # RPA自動化デモ
make screenshot-ocr         # スクリーンショット → OCR解析
make ocr-pipeline           # OCR分析パイプライン全体テスト
make vnc-auto               # VNCデスクトップ自動化デモ
```

### n8n自動化ワークフロー

```bash
make n8n-setup              # n8nワークフロー統合設定
make n8n-test               # n8n API接続テスト
make n8n-create             # AUTOCREATE AIワークフロー作成
make n8n-list               # 全n8nワークフロー一覧
make n8n-webhook            # n8n統合用WebhookURL取得
```

---

## 🌐 Google API操作

### Python版clasp API（完全セキュア版）

```bash
make gas-python-clasp       # Python版clasp API システム
make gas-docs-create        # Google Docs自動作成
make gas-test-existing      # 既存GASプロジェクト確認
make gas-oauth-test         # OAuth2認証テスト
```

### Google Apps Script

```bash
make gas-login              # Google Apps Script CLI認証
make gas-push               # GAS OCR API アップロード
```

### 特徴
- **完全セキュア**: 認証情報は100%環境変数管理
- **n8n対応**: Webhook経由で外部システムから利用可能
- **OAuth2自動認証**: トークン自動更新対応

---

## 📚 ナレッジマネジメント

### WIKI RAG システム

```bash
make wiki-rag               # WIKI RAG システム（port 7860）
make wiki-rag-lite          # WIKI RAG Lite版
make wiki-rag-cli           # コマンドライン版WIKI RAG
make wiki-rag-build         # 知識ベース構築・再構築
make wiki-rag-chat          # 対話型AIチャットインターフェース
```

### Notion統合

```bash
make notion-demo            # デモモード（ページレイアウト確認）
make notion-test            # Notion API接続テスト
make notion-sample          # サンプルページ作成
make notion-autocreate      # AUTOCREATE知識ページ作成
make notion-technical       # 技術ドキュメント作成
make notion-knowledge-base  # 包括的知識ベース作成（5ページ）
make notion-business-knowledge # ビジネス向け知識（4ページ）
make notion-workspace       # Notionワークスペース探索
```

---

## 🔗 外部連携

### GitHub統合

```bash
make create-github-issue    # AI-Human BPMS用GitHubイシュー作成
make github-issue-ai-bpms   # AI-Human BPMS特化イシュー
make github-issue-status    # GitHubリポジトリ・イシュー状況確認
make create-developer-issue # n8n/BPMN/Mermaid付きイシュー作成
```

### JIRA統合

```bash
make jira-test              # JIRA API接続テスト
make jira-create-tickets    # AUTOCREATEプロジェクトチケット作成
make jira-diagnostics       # 完全JIRA診断
```

### トリプルデプロイ

```bash
make triple-deploy          # Notion + GitHub + JIRA 完全デプロイ
make resource-first-deploy  # ビジネス・開発者リソース両方デプロイ
```

---

## 🧪 テスト・デバッグ

### 統合テスト

```bash
make test                   # 全テスト実行
make ci-test                # CI/CD自動テスト
make ci-quick               # 高速CIテスト（GitHubイシューなし）
make ci-full                # 完全CIパイプライン（GitHubイシュー付き）
make ci-comprehensive       # 包括的コントローラーテスト
make ci-real-api            # 実際のGradio APIテスト
```

### 安全テスト

```bash
make safe-test              # 安全な統合テスト（dry-runモード）
make dry-run-all            # 全統合を実行せずにテスト
```

### デバッグモード

```bash
make debug                  # デバッグモード（reload無し）
make dev                    # 開発モード（hot reload付き）
```

---

## 🛠️ 開発・メンテナンス

### アプリケーション管理

```bash
make app                    # FastAPIアプリケーション（自動port 7860停止）
make server                 # ASGIサーバー直接起動（uvicorn）
make stop-port              # port 7860で動作中のプロセス停止
```

### GUI・デスクトップ環境

```bash
make gui                    # AI GUIデスクトップ環境（port 6080）
make gui-auto               # GUI自動起動（ブラウザ自動開始）
make gui-simple             # シンプルGUI環境（port 6081）
make gui-stop               # GUIデスクトップ環境停止
make gui-restart            # GUIデスクトップ環境再起動
make gui-logs               # GUIログ表示
```

### システム管理

```bash
make install                # Poetry依存関係インストール
make requirements           # requirements.txtから依存関係インストール
make clean                  # 一時ファイル・キャッシュクリーンアップ
```

### GitFlow開発フロー

```bash
make gitflow-setup          # GitFlow協業システム初期化
make feature-start name=機能名 # 新機能開発開始
make feature-finish name=機能名 # 機能開発完了
make collab-commit message='メッセージ' # 協業コミット
```

---

## 🎯 利用シナリオ別コマンド

### 🏃‍♂️ 初回セットアップ

```bash
make install                # 依存関係インストール
make config-check           # 設定確認
make safe-test              # 安全テスト
make app                    # アプリケーション起動
```

### 🎨 デモ・プレゼンテーション用

```bash
make chrome-ext             # Chrome拡張機能デモ
make ai-human-bpms          # AI-Human協業デモ
make ocr-rpa-demo           # RPA自動化デモ
make wiki-rag               # 知識システムデモ
```

### 🧑‍💻 開発作業用

```bash
make dev                    # 開発モード
make git-flow-setup         # Git協業設定
make feature-start name=新機能 # 機能開発開始
make test                   # テスト実行
```

### 🌐 外部連携・統合用

```bash
make gas-python-clasp       # Google API操作
make n8n-create             # ワークフロー自動化
make triple-deploy          # 全サービス統合デプロイ
```

### 🔧 トラブルシューティング

```bash
make integration-status     # 全サービス状況確認
make safe-test              # 安全診断
make clean                  # システムクリーンアップ
make stop-port              # ポート競合解決
```

---

## 🔧 環境要件

### 必要な環境変数（.envファイル）

```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Google API（Python版clasp用）
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REFRESH_TOKEN=your_google_refresh_token
GOOGLE_SCRIPT_ID=your_google_apps_script_id

# GitHub
GITHUB_TOKEN=your_github_token
GITHUB_USER=your_github_user
GITHUB_REPO=your_github_repo

# JIRA
JIRA_URL=your_jira_url
JIRA_USERNAME=your_jira_username
JIRA_API_TOKEN=your_jira_token

# Notion
NOTION_TOKEN=your_notion_token
```

### システム要件

- **Python 3.7+**
- **Node.js 14+**
- **Docker** (GUI機能用)
- **Chrome/Chromium** (拡張機能用)

---

## 🎊 特別な機能

### 🤖 AI社長 × 無職CTO システム

AUTOCREATEシステムの核心である「AI社長 × 無職CTO」協業モデル：

1. **AI社長**: 戦略的判断・リソース配分・外部交渉
2. **無職CTO**: 技術実装・システム設計・コード開発
3. **完全自動化**: pyautogui + Google API + n8n統合

### 🌟 革新的な統合機能

- **リアルタイム監視**: Supabase ↔ VS Code ↔ GitHub Copilot
- **知識統合**: WIKI RAG + Notion + Google Docs
- **ワークフロー自動化**: n8n + Google Apps Script + JIRA
- **セキュア設計**: 全認証情報は環境変数管理

---

## 📞 サポート・トラブルシューティング

### よくある問題

1. **ポート競合**: `make stop-port` でport 7860を解放
2. **認証エラー**: `.env`ファイルの設定確認
3. **依存関係エラー**: `make install` で再インストール
4. **GUI表示されない**: Docker設定確認

### ヘルプ・情報表示

```bash
make help                   # 全コマンド一覧
make config-check           # 設定診断
make integration-status     # サービス状況
```

---

**⭐ AUTOCREATE = AI社長 × 無職CTO × Makefile自動化の革新的トリプルコラボ ⭐**

このMakefileガイドで、AUTOCREATEの全機能を活用して、究極の外部連携pyautogui自動化システムを体験してください！
