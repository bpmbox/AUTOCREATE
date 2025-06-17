# Laravel WIKI RAG統合サンプル

## 📋 概要
このプロジェクトは、Laravel WebアプリケーションにWIKI RAGシステムを統合するサンプル実装です。

## 🎯 特徴
- **Laravel 10.x** 対応
- **WIKI RAG API** 統合
- **レスポンシブUI** (Bootstrap 5)
- **リアルタイム検索** (Ajax)
- **結果キャッシュ** (Redis対応)
- **多言語対応** (日本語・英語)

## 🔧 技術スタック
- **Backend**: Laravel 10.x, PHP 8.1+
- **Frontend**: Blade Templates, Bootstrap 5, jQuery
- **API**: RESTful API (FastAPI Backend)
- **Cache**: Redis (オプション)
- **Database**: MySQL/PostgreSQL (ログ・統計用)

## 📂 プロジェクト構造
```
laravel-wiki-rag/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── WikiRagController.php
│   │   │   └── ApiController.php
│   │   ├── Requests/
│   │   │   └── WikiRagRequest.php
│   │   └── Middleware/
│   │       └── WikiRagMiddleware.php
│   ├── Services/
│   │   ├── WikiRagService.php
│   │   └── CacheService.php
│   ├── Models/
│   │   ├── WikiQuery.php
│   │   └── QueryResult.php
│   └── Providers/
│       └── WikiRagServiceProvider.php
├── resources/
│   ├── views/
│   │   ├── wiki-rag/
│   │   │   ├── index.blade.php
│   │   │   ├── results.blade.php
│   │   │   └── chat.blade.php
│   │   └── layouts/
│   │       └── app.blade.php
│   ├── js/
│   │   └── wiki-rag.js
│   └── css/
│       └── wiki-rag.css
├── routes/
│   ├── web.php
│   └── api.php
├── config/
│   └── wiki-rag.php
├── database/
│   └── migrations/
│       ├── create_wiki_queries_table.php
│       └── create_query_results_table.php
├── tests/
│   ├── Feature/
│   │   └── WikiRagTest.php
│   └── Unit/
│       └── WikiRagServiceTest.php
├── composer.json
├── package.json
├── .env.example
├── artisan
└── README.md
```

## 🚀 インストール手順

### 1. 前提条件
- PHP 8.1以上
- Composer
- Node.js & npm
- MySQL/PostgreSQL (オプション)
- Redis (オプション)

### 2. プロジェクトセットアップ
```bash
# Laravelプロジェクト作成
composer create-project laravel/laravel laravel-wiki-rag
cd laravel-wiki-rag

# 依存関係インストール
composer install
npm install

# 環境設定
cp .env.example .env
php artisan key:generate

# データベース設定 (オプション)
php artisan migrate

# アセットビルド
npm run build
```

### 3. WIKI RAG API設定
```bash
# .env ファイルに追加
WIKI_RAG_API_URL=http://localhost:8000
WIKI_RAG_API_KEY=your-api-key
WIKI_RAG_CACHE_ENABLED=true
WIKI_RAG_CACHE_TTL=3600
```

## 📚 使い方

### 基本的な使用方法
1. `php artisan serve` でサーバー起動
2. `http://localhost:8000/wiki-rag` にアクセス
3. 検索クエリを入力してWIKI RAG検索実行

### API エンドポイント
- `GET /wiki-rag` - 検索画面表示
- `POST /wiki-rag/search` - 検索実行
- `GET /api/wiki-rag/query` - API検索

## 🎨 UI機能
- **検索フォーム**: リアルタイム検索
- **結果表示**: スコア付き結果リスト
- **チャット形式**: 対話的な検索体験
- **レスポンシブ**: モバイル対応

## 🔧 カスタマイズ

### 設定ファイル
`config/wiki-rag.php` で各種設定をカスタマイズ可能

### View カスタマイズ
`resources/views/wiki-rag/` でUI をカスタマイズ

### サービス拡張
`app/Services/WikiRagService.php` でビジネスロジック拡張

## 🧪 テスト
```bash
# 単体テスト実行
php artisan test

# 特定テスト実行
php artisan test --filter WikiRagTest
```

## 📈 パフォーマンス
- **キャッシュ**: Redis使用で高速応答
- **非同期処理**: キュー対応
- **ページネーション**: 大量結果の効率表示

## 🔒 セキュリティ
- **CSRF保護**: Laravel標準機能
- **入力値検証**: FormRequestクラス
- **API認証**: Bearer token対応

## 🤝 コントリビューション
1. Fork this repository
2. Create feature branch
3. Commit your changes
4. Push to the branch
5. Create Pull Request

## 📄 ライセンス
MIT License

## 🔗 関連リンク
- [Laravel Documentation](https://laravel.com/docs)
- [WIKI RAG System](../scripts/wiki_rag_system.py)
- [GitHub Issues](https://github.com/bpmbox/AUTOCREATE/issues/10)

---
**Developed by**: AUTOCREATE AI-CEO  
**Version**: 1.0.0  
**Last Updated**: June 15, 2025
