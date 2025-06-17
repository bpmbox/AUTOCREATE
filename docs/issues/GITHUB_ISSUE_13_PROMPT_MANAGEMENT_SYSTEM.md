# GITHUB ISSUE #13: プロンプト管理＆自動システム生成 (Lavelo AI)

## 📋 Issue概要
AI×人間協働開発のためのプロンプト管理・自動システム生成・Laravel統合システムの実装

## 🎯 目標
1. **プロンプト管理システム**: 再利用可能なプロンプトライブラリ構築
2. **自動システム生成**: GPT-ENGINEERによるコード自動生成
3. **Laravel統合**: 生成されたシステムの自動Controller統合
4. **GitHub連携**: 自動リポジトリアップロード・バージョン管理

## 🚀 主要機能

### 📝 プロンプト管理
- [x] SQLiteデータベースでプロンプト保存・管理
- [x] タイトル・内容・GitHub URL・システムタイプ分類
- [x] プロンプト一覧表示・選択・編集機能
- [x] システムタイプ別分類（general, web_system, api_system, interface_system, line_system）

### ⚡ 自動システム生成
- [x] GPT-ENGINEERとの統合
- [x] プロンプトからコード自動生成
- [x] フォルダ名指定・出力先管理
- [x] 生成結果の詳細ログ表示

### 🔧 Laravel統合
- [x] Gradioインターフェースとして統合済み
- [x] [`mysite/asgi.py`](mysite/asgi.py )での自動読み込み
- [x] 18個のタブの1つとして「💾 プロンプト管理システム」を追加
- [x] Laravel風のディレクトリ構造（[`app/Http/Controllers/Gradio/gra_03_programfromdocs/lavelo.py`](app/Http/Controllers/Gradio/gra_03_programfromdocs/lavelo.py )）

### 🌐 GitHub連携
- [ ] GitHub Token管理
- [ ] 自動リポジトリ作成・アップロード
- [ ] バージョン管理・コミットメッセージ自動生成
- [ ] Google Chat通知システム

## 📁 ファイル構成

### 🎯 メインシステム
```
app/Http/Controllers/Gradio/gra_03_programfromdocs/
├── lavelo.py                    # メインGradioインターフェース
├── system_automation.py         # システム自動化処理
└── [生成されるシステムフォルダ]/
```

### 🗄️ データベース
```
database/
└── prompts.db                   # プロンプト管理用SQLite
    ├── prompts テーブル
    │   ├── id (PRIMARY KEY)
    │   ├── title (プロンプトタイトル)
    │   ├── content (プロンプト内容)
    │   ├── github_url (関連GitHub URL)
    │   ├── system_type (システムタイプ)
    │   └── created_at (作成日時)
```

### 🔗 統合ポイント
```
mysite/asgi.py                   # Gradio自動読み込み
├── lavelo統合済み
└── 18タブ統合システム
```

## 🔧 実装状況

### ✅ 完了済み
1. **Gradioインターフェース実装**: 完全なUI/UX構築済み
2. **データベース設計**: SQLite + 自動初期化機能
3. **Laravel統合**: asgi.pyでの自動読み込み完了
4. **プロンプト管理**: CRUD機能完全実装
5. **システム生成基盤**: GPT-ENGINEER統合準備完了

### 🚧 進行中
1. **GitHub自動連携**: Token管理・自動アップロード機能
2. **Controller自動統合**: 生成システムの自動Laravel統合
3. **Google Chat通知**: チーム連携通知システム

### 📋 次のステップ
1. **ポート競合解決**: 既存プロセス停止・新システム起動
2. **GitHub Token設定**: 自動アップロード機能テスト
3. **実システム生成テスト**: 実際のプロンプトでシステム生成
4. **Laravel Controller統合テスト**: 生成システムの自動統合確認

## 💡 AI×人間協働ポイント
- **Human (miyataken999)**: プロンプト設計・要件定義・品質チェック
- **AI (GitHub Copilot)**: コード生成・システム統合・自動化処理
- **協働効果**: 人間の創造性 × AIの実装力 = 高速プロトタイピング

## 🎯 期待される成果
1. **開発効率向上**: プロンプト再利用による高速開発
2. **品質向上**: 標準化されたシステム生成プロセス
3. **知識蓄積**: プロンプトライブラリによる開発ノウハウ共有
4. **自動化**: 人手を介さない継続的システム生成

## 🚀 実行コマンド
```bash
# システム起動
python3 app.py

# アクセス
http://localhost:7860
# 「💾 プロンプト管理システム」タブを選択
```

---

**作成日**: 2025年6月16日  
**担当**: miyataken999 (無職CTO) + GitHub Copilot (AI社長)  
**優先度**: High  
**ステータス**: 実装完了・テスト開始段階
