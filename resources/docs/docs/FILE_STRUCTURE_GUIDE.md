# 📁 AUTOCREATE ファイル構造ガイド

プロジェクトのファイル構成を整理・体系化しました

## 📋 ディレクトリ構造

```
AUTOCREATE/
├── 📚 docs/                     # ドキュメント・資料
│   ├── guides/                  # ガイド・使用方法
│   ├── api/                     # API ドキュメント
│   ├── issues/                  # GitHub Issue関連
│   └── business/                # ビジネス関連資料
├── 🔧 scripts/                  # スクリプト・ツール
│   ├── google-api/              # Google API関連
│   ├── automation/              # 自動化スクリプト
│   └── testing/                 # テスト関連
├── 🌐 wikis/                    # Wiki・知識ベース（既存）
├── 🐍 app/                      # アプリケーションコード（Laravel風）
├── 🎨 laravalmypage/            # Laravel風ページ
└── ⚙️ その他設定ファイル
```

## 📚 docs/ - ドキュメント

### guides/ - ガイド・マニュアル
- `MAKEFILE_COMPLETE_GUIDE.md` - Makefileコマンド完全ガイド（100+コマンド）

### api/ - API ドキュメント
- `PYTHON_CLASP_SECURE_README.md` - Python版clasp API使用方法

### issues/ - GitHub Issue関連
- `GITHUB_ISSUE_GOOGLE_API_GAS_PROJECT.md` - Google API GASプロジェクト
- `GITHUB_ISSUE_EXTERNAL_INTEGRATION.md` - 外部連携
- `GITHUB_ISSUE_MANUAL.md` - Issue作成マニュアル

### business/ - ビジネス関連
- `AUTOCREATE_COMPANY_BUSINESS_PLAN.md` - 会社ビジネスプラン

## 🔧 scripts/ - スクリプト・ツール

### google-api/ - Google API関連
- `python_clasp_secure.py` - Python版clasp API（メイン）
- `python_clasp_api.py` - 従来版API
- `python_clasp_template.py` - テンプレート版

### automation/ - 自動化スクリプト
- pyautogui関連スクリプト
- RPA自動化ツール
- システム連携スクリプト

### testing/ - テスト関連
- `python_clasp_secure_test.py` - Python clasp APIテスト
- その他テストファイル

## 🌟 ファイル管理方針

### 📝 ドキュメント (`docs/`)
- **用途**: 説明書・ガイド・マニュアル
- **形式**: Markdown (.md)
- **分類**: 機能・目的別フォルダー分け

### 🔧 スクリプト (`scripts/`)
- **用途**: 実行可能なプログラム・ツール
- **形式**: Python (.py), Shell (.sh), PowerShell (.ps1)
- **分類**: 技術分野別フォルダー分け

### 🌐 Wiki (`wikis/`)
- **用途**: 詳細な技術知識・アーキテクチャ
- **形式**: GitHub Wiki形式
- **特徴**: 既存構造を維持

## 🎯 ファイル配置ルール

### 新しいファイルの配置

#### ドキュメント・説明書 → `docs/`
```bash
# ガイド・マニュアル
docs/guides/FEATURE_NAME_GUIDE.md

# API ドキュメント
docs/api/API_NAME_README.md

# GitHub Issue
docs/issues/GITHUB_ISSUE_TOPIC.md

# ビジネス関連
docs/business/BUSINESS_DOCUMENT.md
```

#### 実行スクリプト → `scripts/`
```bash
# Google API関連
scripts/google-api/google_feature.py

# 自動化スクリプト
scripts/automation/automation_feature.py

# テストスクリプト
scripts/testing/test_feature.py
```

## 🚀 メリット

### 📁 整理された構造
- **見つけやすい**: カテゴリ別に整理
- **管理しやすい**: 目的別フォルダー分け
- **拡張しやすい**: 新機能追加時の配置が明確

### 🔍 検索・メンテナンス
- **ファイル検索**: フォルダー単位で絞り込み可能
- **関連ファイル**: 同じフォルダーに集約
- **依存関係**: 明確な分離

### 👥 チーム開発
- **役割分担**: 担当領域が明確
- **新メンバー**: 構造が理解しやすい
- **コードレビュー**: 変更範囲が特定しやすい

## 🎊 次のステップ

### 1. 残りファイルの整理
```bash
# 既存ファイルの分類・移動
make file-organize
```

### 2. Makefileコマンド更新
```bash
# 新しいパス対応
make update-makefile-paths
```

### 3. ドキュメント充実
```bash
# 各フォルダーにREADME追加
make create-folder-readmes
```

---

**⭐ AUTOCREATE = AI社長 × 無職CTO × 整理された構造管理 ⭐**

この新しいファイル構造により、プロジェクトの管理・拡張・メンテナンスが大幅に改善されました！
