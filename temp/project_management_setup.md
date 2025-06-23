# 🎯 AUTOCREATE プロジェクト管理設定

## 📋 プロジェクト概要
- **プロジェクト名:** AUTOCREATE
- **プロジェクト番号:** #5
- **URL:** https://github.com/orgs/bpmbox/projects/5
- **可視性:** Private
- **作成日:** 2025-06-24

## 🏗️ プロジェクト構成

### 🔧 カスタムフィールド
1. **進捗状況** (Single Select)
   - 計画中
   - 開発中
   - テスト中
   - 完了
   - 保留

2. **優先度** (Single Select)
   - 緊急
   - 高
   - 中
   - 低

3. **カテゴリ** (Single Select)
   - フロントエンド
   - バックエンド
   - インフラ
   - AI自動化
   - 統合
   - ドキュメント
   - テスト

### 📊 デフォルトフィールド
- Title (プロジェクトフィールド)
- Assignees (プロジェクトフィールド)
- Status (プロジェクトシングル選択フィールド)
- Labels (プロジェクトフィールド)
- Linked pull requests (プロジェクトフィールド)
- Milestone (プロジェクトフィールド)
- Repository (プロジェクトフィールド)
- Reviewers (プロジェクトフィールド)
- Parent issue (プロジェクトフィールド)
- Sub-issues progress (プロジェクトフィールド)

## 📋 追加済みIssue一覧

### 🎯 メイン機能
- **Issue #39**: フロントエンド統合完了 (フロントエンド/完了)
- **Issue #38**: PHPバルクバッチ処理サンプル (バックエンド/完了)
- **Issue #37**: PHPバルクバッチ処理サンプル (バックエンド/完了)

### 🌐 WordPress・PHP関連
- **Issue #36**: WordPress proxy呼び出し (バックエンド/開発中)
- **Issue #35**: WordPress proxy呼び出し (バックエンド/開発中)
- **Issue #34**: Laravel LINE Login (バックエンド/開発中)
- **Issue #33**: PHP mypage laravel (バックエンド/開発中)
- **Issue #32**: PHP Laravel + Docker (インフラ/開発中)
- **Issue #31**: PHPマイページ完全実装 (バックエンド/開発中)
- **Issue #30**: PHPマイページ完全実装 (バックエンド/開発中)

## 🚀 プロジェクト管理コマンド

### 新しいIssueをプロジェクトに追加
```bash
gh project item-add 5 --owner bpmbox --url https://github.com/bpmbox/AUTOCREATE/issues/[ISSUE_NUMBER]
```

### プロジェクトの内容を確認
```bash
gh project view 5 --owner bpmbox
```

### 新しいフィールドを追加
```bash
gh project field-create 5 --owner bpmbox --name "フィールド名" --data-type "SINGLE_SELECT" --single-select-options "選択肢1,選択肢2,選択肢3"
```

### プロジェクトのアイテムを更新
```bash
gh project item-edit --id [ITEM_ID] --field-id [FIELD_ID] --single-select-option-id [OPTION_ID]
```

## 🎯 今後の管理方針

### 📊 カテゴリ別分類
1. **フロントエンド**: React、HTML、CSS、JavaScript関連
2. **バックエンド**: PHP、Python、Laravel、API関連
3. **インフラ**: Docker、サーバー、データベース関連
4. **AI自動化**: AI機能、自動化スクリプト関連
5. **統合**: 外部サービス連携、API統合関連
6. **ドキュメント**: README、マニュアル、仕様書関連
7. **テスト**: テストコード、品質保証関連

### 🔄 進捗管理
- **計画中**: 要件定義、設計段階
- **開発中**: 実装・コーディング段階
- **テスト中**: テスト・検証段階
- **完了**: 実装完了、本番運用
- **保留**: 一時停止、課題待ち

### ⚡ 優先度管理
- **緊急**: 本番障害、セキュリティ問題
- **高**: 重要機能、期限あり
- **中**: 通常機能、改善
- **低**: 将来的な機能、最適化

## 🔗 関連リンク
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [AUTOCREATE Repository](https://github.com/bpmbox/AUTOCREATE)
- [Project Board](https://github.com/orgs/bpmbox/projects/5)
