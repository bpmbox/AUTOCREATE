# 🚀 Laravel + Docker + LINE Login マイページシステム

## 📋 プロジェクト概要

LINE Login認証を使用したLaravel Dockerマイページシステムです。

### ✨ 主要機能
- 🔐 LINE Login OAuth 2.0 認証
- 👤 ユーザープロフィール管理
- 📱 レスポンシブデザイン
- 🐳 Docker完全対応
- 🔧 Laravel 10.x最新版

### 🛠️ 技術スタック
- **Backend**: Laravel 10.x
- **Database**: MySQL 8.0
- **WebServer**: Nginx
- **PHP**: 8.2+
- **Container**: Docker & Docker Compose
- **Authentication**: LINE Login API

## 🚀 クイックスタート

### 1️⃣ 環境設定
```bash
# 環境ファイルコピー
cp .env.example .env

# LINE Login設定
# .envファイルを編集してLINE_CHANNEL_IDとLINE_CHANNEL_SECRETを設定
```

### 2️⃣ Docker起動
```bash
# コンテナ起動
docker-compose up -d

# Laravel依存関係インストール
docker-compose exec app composer install

# Laravel初期設定
docker-compose exec app php artisan key:generate
docker-compose exec app php artisan migrate
```

### 3️⃣ アクセス
- **Application**: http://localhost:8080
- **phpMyAdmin**: http://localhost:8081

## 📁 プロジェクト構造

```
php-mypage-laravel-trudtdock-line-login-project/
├── 📋 README.md
├── 🐳 docker-compose.yml
├── 🔧 .env.example
├── 📁 docker/
│   ├── app/
│   │   └── Dockerfile
│   └── nginx/
│       └── default.conf
├── 📁 app/
│   └── Http/
│       └── Controllers/
│           └── Auth/
│               └── LineLoginController.php
├── 📁 database/
│   └── migrations/
│       └── 2024_01_01_000000_create_line_users_table.php
├── 📁 resources/
│   └── views/
│       ├── auth/
│       │   └── login.blade.php
│       └── mypage/
│           └── index.blade.php
└── 📁 routes/
    └── web.php
```

## 🔐 LINE Login設定

### 1️⃣ LINE Developers Console
1. https://developers.line.biz/console/ にアクセス
2. 新しいチャンネル作成
3. チャンネルIDとチャンネルシークレット取得

### 2️⃣ 環境変数設定
```env
LINE_CHANNEL_ID=your_channel_id
LINE_CHANNEL_SECRET=your_channel_secret
LINE_CALLBACK_URL=http://localhost:8080/auth/line/callback
```

## 🚀 デプロイメント

### 開発環境
```bash
docker-compose up -d
```

### 本番環境
```bash
# 本番用設定
cp .env.production .env
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 カスタマイズ

### テーマ変更
- `resources/views/layouts/app.blade.php` を編集
- CSS: `public/css/app.css`
- JavaScript: `public/js/app.js`

### データベース
- マイグレーション: `database/migrations/`
- モデル: `app/Models/`

## 📝 API仕様

### 認証エンドポイント
- `GET /auth/line` - LINE Login開始
- `GET /auth/line/callback` - LINE Loginコールバック
- `POST /logout` - ログアウト

### ユーザー管理
- `GET /mypage` - マイページ表示
- `PUT /mypage/profile` - プロフィール更新
- `GET /api/user` - ユーザー情報取得

## 🧪 テスト

```bash
# 単体テスト実行
docker-compose exec app php artisan test

# 特定テスト実行
docker-compose exec app php artisan test --filter=LineLoginTest
```

## 📊 ログ監視

```bash
# アプリケーションログ
docker-compose logs -f app

# Nginxログ
docker-compose logs -f nginx

# MySQLログ
docker-compose logs -f mysql
```

## 🔒 セキュリティ

- CSRF保護有効
- SQL インジェクション対策
- XSS防止
- HTTPS推奨 (本番環境)

## 🆘 トラブルシューティング

### よくある問題

1. **PORT 8080が使用中**
   ```bash
   # ポート変更
   docker-compose down
   # docker-compose.ymlのポート番号変更
   docker-compose up -d
   ```

2. **LINE Login エラー**
   - チャンネル設定確認
   - コールバックURL確認
   - .env設定確認

3. **データベース接続エラー**
   ```bash
   # コンテナ再起動
   docker-compose restart mysql
   ```

## 📞 サポート

- 📧 Email: support@example.com
- 📚 Documentation: [Laravel公式ドキュメント](https://laravel.com/docs)
- 🐙 Issues: [GitHub Issues](https://github.com/yourusername/yourproject/issues)

## 📄 ライセンス

MIT License

---

🎯 **開発者向け**: `docker-compose up -d` → http://localhost:8080 でアクセス！
