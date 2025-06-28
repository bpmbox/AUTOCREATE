# 🏠 PHP マイページシステム

## 🎯 概要
PHPを使用したセキュアなユーザーマイページシステムです。
ユーザー認証、プロフィール管理、セッション管理を実装しています。

## ✨ 機能
- 👤 ユーザー登録・ログイン
- 🏠 マイページ表示
- ✏️ プロフィール編集
- 🔑 パスワード変更
- 🔐 セッション管理
- 🛡️ セキュリティ対策（CSRF、XSS対策）

## 🛠️ 技術仕様
- ⚡ PHP 8.x
- 🗄️ MySQL 8.x
- 🎨 Bootstrap 5（レスポンシブデザイン）
- 🔐 セキュアセッション管理
- 💉 PDO使用（SQLインジェクション対策）

## 🚀 セットアップ

### 1️⃣ データベース設定
```sql
-- データベース作成
CREATE DATABASE mypage_system;
USE mypage_system;

-- ユーザーテーブル作成
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- セッションテーブル作成
CREATE TABLE sessions (
    id VARCHAR(128) PRIMARY KEY,
    user_id INT,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 2️⃣ 設定ファイル編集
`config/database.php` でデータベース接続情報を設定

### 3️⃣ 実行
```bash
php -S localhost:8000
```

## 📁 ファイル構成
```
📁 php-mypage-project/
├── 📁 config/
│   ├── 🔧 database.php      # DB設定
│   └── 🔧 session.php       # セッション設定
├── 📁 includes/
│   ├── 🔐 auth.php          # 認証関数
│   ├── 🛡️ security.php      # セキュリティ関数
│   └── ✅ validation.php    # バリデーション
├── 📁 public/
│   ├── 🎨 css/             # スタイルシート
│   ├── ⚡ js/              # JavaScript
│   └── 📷 uploads/         # アップロード画像
├── 📁 views/
│   ├── 🚪 login.php        # ログインページ
│   ├── 📝 register.php     # 登録ページ
│   ├── 🏠 mypage.php       # マイページ
│   └── ✏️ edit_profile.php # プロフィール編集
├── 📁 tests/               # テストファイル
├── 🚀 index.php           # エントリーポイント
└── 📖 README.md
```

## 🛡️ セキュリティ機能
- 🔒 パスワードハッシュ化（password_hash）
- 🛡️ CSRF トークン保護
- 🚫 XSS対策（htmlspecialchars）
- 💉 SQLインジェクション対策（PDO prepared statements）
- 🔐 セッションハイジャック対策
- ✅ 入力値検証

## 📖 使用方法
1. 📝 ユーザー登録（register.php）
2. 🚪 ログイン（login.php）
3. 🏠 マイページ表示（mypage.php）
4. ✏️ プロフィール編集（edit_profile.php）

## 📄 ライセンス
MIT License
