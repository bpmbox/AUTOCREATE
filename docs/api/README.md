# 🌐 API ドキュメント

AUTOCREATEシステムのAPI仕様・使用方法

## 📋 利用可能なAPI

### 🐍 Python版clasp API（完全セキュア版）
- `PYTHON_CLASP_SECURE_README.md` - Google Apps Script操作API

## 🎯 このフォルダーの目的

- **API仕様**: 各APIの詳細な使用方法
- **認証方法**: セキュアな認証情報管理
- **実装例**: 実際のコード例・サンプル
- **統合ガイド**: 外部システムとの連携方法

## 🔧 対象API

### Google API統合
- **Google Apps Script**: Python版clasp API
- **Google Docs**: 自動ドキュメント作成
- **Google Sheets**: スプレッドシート操作
- **OAuth2認証**: セキュアな認証システム

### 外部連携API
- **n8n Webhook**: ワークフロー自動化
- **Supabase**: データベース連携
- **GitHub**: リポジトリ・Issue操作

## 📝 新しいAPI追加時

```bash
# 新しいAPIドキュメント作成
docs/api/NEW_API_README.md
```

### APIドキュメントのテンプレート

```markdown
# 🌐 [API名] 使用ガイド

## 📝 概要
[APIの説明・目的]

## 🔐 認証
[認証方法・設定]

## 🚀 基本使用方法
[基本的な使い方]

## 📊 API仕様
[詳細な仕様・パラメーター]

## 💡 実装例
[実際のコード例]

## 🌐 外部連携
[他システムとの統合方法]
```

---

**セキュアで強力なAPIで、システム統合を実現しましょう！**
