# 🚀 Laravel + Docker + LINE ログインマイページシステム

## 🎯 概要
Laravel フレームワークを使用し、Docker で環境構築、LINE ログイン機能を統合したモダンなマイページシステムです。

## ✨ 主要機能
- 📱 LINE ログイン認証
- 👤 ユーザープロフィール管理
- 🏠 レスポンシブマイページ
- 🔐 セキュアな認証システム
- 🐳 Docker による完全環境構築
- 📊 Redis セッション管理
- 🛡️ Laravel Sanctum セキュリティ

## 🛠️ 技術スタック
- **Backend**: PHP 8.2 + Laravel 10.x
- **Database**: MySQL 8.0
- **Cache**: Redis 7.0
- **Frontend**: Blade + Bootstrap 5 + Alpine.js
- **Container**: Docker + Docker Compose
- **Authentication**: LINE Login API + Laravel Sanctum
- **Testing**: PHPUnit + Laravel Dusk

## 🐳 Docker セットアップ

### 前提条件
- Docker Desktop がインストール済み
- Git がインストール済み

### 🚀 クイックスタート
```bash
# リポジトリクローン
git clone [repository-url]
cd php-mypage-laravel-docker-line-login-project

# 環境設定
cp .env.example .env

# Docker コンテナ起動
docker-compose up -d

# Laravel セットアップ
docker-compose exec app composer install
docker-compose exec app php artisan key:generate
docker-compose exec app php artisan migrate:fresh --seed

# アクセス
# http://localhost:8000
```

## 📱 LINE ログイン設定

### 1. LINE Developers Console設定
1. [LINE Developers](https://developers.line.biz/) にアクセス
2. 新しいプロバイダー・チャンネル作成
3. 「LINE Login」チャンネル作成
4. Callback URL設定: `http://localhost:8000/auth/line/callback`

### 2. 環境変数設定
```env
LINE_CLIENT_ID=your_line_client_id
LINE_CLIENT_SECRET=your_line_client_secret
LINE_REDIRECT_URI=http://localhost:8000/auth/line/callback
```

## 🗄️ データベース設計

### Users テーブル
```sql
- id (Primary Key)
- line_user_id (Unique)
- name
- email
- avatar
- line_profile_data (JSON)
- created_at
- updated_at
```

### Sessions テーブル
```sql
- id
- user_id
- payload
- last_activity
```

## 📁 プロジェクト構成

```
📁 php-mypage-laravel-docker-line-login-project/
├── 🐳 docker/
│   ├── app/Dockerfile
│   ├── nginx/default.conf
│   └── mysql/init.sql
├── 🚀 app/
│   ├── Http/Controllers/
│   │   ├── AuthController.php
│   │   ├── LineLoginController.php
│   │   └── MypageController.php
│   ├── Models/
│   │   └── User.php
│   └── Services/
│       └── LineLoginService.php
├── 🗄️ database/
│   ├── migrations/
│   └── seeders/
├── 📱 resources/
│   ├── views/
│   │   ├── auth/
│   │   ├── mypage/
│   │   └── layouts/
│   ├── js/
│   └── css/
├── 🧪 tests/
│   ├── Feature/
│   └── Unit/
├── 🐳 docker-compose.yml
├── 📦 composer.json
├── ⚙️ .env.example
└── 📖 README.md
```

## 🔐 セキュリティ機能
- 🛡️ Laravel Sanctum API認証
- 🔒 CSRF保護
- 🚫 XSS対策
- 💉 SQLインジェクション対策
- 🔐 セッションセキュリティ
- 📱 LINE OAuth 2.0認証
- 🚨 レート制限

## 🧪 テスト実行

### テスト環境設定
```bash
# テスト用環境ファイル作成
cp .env.example .env.testing

# テスト用データベース設定（Supabase Test DB）
# .env.testingファイルを編集:
# DB_DATABASE=laravel_test_db
# SUPABASE_URL=your_supabase_test_url
# SUPABASE_KEY=your_supabase_test_key
```

### テスト実行
```bash
# 🧪 全テスト実行
docker-compose exec app php artisan test

# 🎯 ユニットテストのみ
docker-compose exec app php artisan test --testsuite=Unit

# 🚀 フィーチャーテストのみ
docker-compose exec app php artisan test --testsuite=Feature

# 🔍 特定テストクラス実行
docker-compose exec app php artisan test --filter=LineLoginTest

# 📊 テストカバレッジ付き実行
docker-compose exec app php artisan test --coverage

# 🌐 ブラウザテスト（Laravel Dusk）
docker-compose exec app php artisan dusk

# 📈 パフォーマンステスト
docker-compose exec app php artisan test --group=performance
```

### テストデータベース初期化
```bash
# テスト用データベースリセット
docker-compose exec app php artisan migrate:fresh --env=testing

# テストデータ投入
docker-compose exec app php artisan db:seed --env=testing
```

## 📊 パフォーマンス
- 🚀 Redis キャッシュ
- 📈 Eloquent クエリ最適化
- 🔄 Laravel Queue
- 📦 Asset最適化（Laravel Mix）

## 🚀 デプロイ
```bash
# 本番環境
docker-compose -f docker-compose.prod.yml up -d

# パフォーマンス最適化
docker-compose exec app php artisan config:cache
docker-compose exec app php artisan route:cache
docker-compose exec app php artisan view:cache
```

## 📚 API ドキュメント
- **認証**: `/api/auth/*`
- **ユーザー**: `/api/user/*`
- **マイページ**: `/api/mypage/*`

## 🔧 開発ツール
- **デバッグ**: Laravel Telescope
- **API テスト**: Insomnia/Postman
- **コード品質**: PHPStan + PHP CS Fixer
- **ログ**: Laravel Log Viewer

## 📄 ライセンス
MIT License

## 👥 コントリビューション
プルリクエスト歓迎！開発ガイドラインに従ってください。

---
🤖 **Auto-generated by GitHub Copilot AI**  
📅 **Created**: 2025年6月23日
