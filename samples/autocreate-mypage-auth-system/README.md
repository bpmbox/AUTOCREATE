# 🔐 MyPage統合認証システム

[![CI](https://github.com/autocreate/mypage-auth-system/actions/workflows/ci.yml/badge.svg)](https://github.com/autocreate/mypage-auth-system/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/autocreate/mypage-auth-system/branch/main/graph/badge.svg)](https://codecov.io/gh/autocreate/mypage-auth-system)
[![Latest Version](https://img.shields.io/packagist/v/autocreate/mypage-auth-system.svg)](https://packagist.org/packages/autocreate/mypage-auth-system)
[![License](https://img.shields.io/packagist/l/autocreate/mypage-auth-system.svg)](https://packagist.org/packages/autocreate/mypage-auth-system)

LINE・Firebase・TrustDock統合認証 + 予約管理 + WIKI RAG AI搭載の完全なMyPageシステム

## ✨ 特徴

- 🔐 **統合認証**: LINE・Firebase・TrustDock対応
- 📱 **レスポンシブUI**: 美しいダッシュボード
- 🤖 **AI統合**: WIKI RAG検索機能
- 📅 **予約管理**: 完全な予約システム
- 🧪 **テスト完備**: 95%+ カバレッジ
- 🚀 **本番対応**: Docker・CI/CD完備

## 🚀 クイックスタート

### インストール

```bash
composer require autocreate/mypage-auth-system
```

### セットアップ

```bash
# 設定ファイル公開
php artisan vendor:publish --provider="AutoCreate\MyPageAuth\ServiceProvider"

# マイグレーション実行
php artisan migrate

# フロントエンドアセット公開
php artisan vendor:publish --tag=mypage-auth-assets
npm install && npm run build
```

### 基本設定

```php
// config/mypage-auth.php
return [
    'providers' => [
        'line' => [
            'client_id' => env('LINE_CLIENT_ID'),
            'client_secret' => env('LINE_CLIENT_SECRET'),
        ],
        'firebase' => [
            'project_id' => env('FIREBASE_PROJECT_ID'),
            'service_account' => env('FIREBASE_SERVICE_ACCOUNT_PATH'),
        ],
        'trustdock' => [
            'api_key' => env('TRUSTDOCK_API_KEY'),
            'webhook_secret' => env('TRUSTDOCK_WEBHOOK_SECRET'),
        ],
    ],
];
```

## 📚 使用方法

### 認証機能

```php
use AutoCreate\MyPageAuth\Services\AuthService;

class LoginController extends Controller
{
    public function __construct(
        private AuthService $authService
    ) {}
    
    public function loginWithLine(Request $request)
    {
        $user = $this->authService->loginWithLine($request->access_token);
        return redirect()->route('dashboard');
    }
}
```

### 本人確認機能

```php
use AutoCreate\MyPageAuth\Services\TrustDockService;

class IdentityController extends Controller
{
    public function submitVerification(Request $request, TrustDockService $trustDock)
    {
        $verification = $trustDock->createVerification([
            'type' => 'basic',
            'documents' => $request->file('documents'),
        ]);
        
        return response()->json($verification);
    }
}
```

### WIKI RAG検索

```php
use AutoCreate\MyPageAuth\Services\WikiRagService;

class WikiRagController extends Controller
{
    public function query(Request $request, WikiRagService $wikiRag)
    {
        $results = $wikiRag->query($request->query, auth()->id());
        return response()->json($results);
    }
}
```

## 🎨 UI コンポーネント

### Vue.js コンポーネント

```vue
<template>
    <WikiRagChat 
        :user-id="userId"
        :api-endpoint="'/api/wiki-rag/query'"
        @query-sent="handleQuerySent"
    />
</template>

<script>
import { WikiRagChat } from 'autocreate-mypage-auth';

export default {
    components: { WikiRagChat },
    // ...
}
</script>
```

### Blade テンプレート

```blade
@extends('mypage-auth::layouts.dashboard')

@section('content')
    @include('mypage-auth::components.identity-verification')
    @include('mypage-auth::components.reservation-calendar')
@endsection
```

## 🧪 テスト

```bash
# 全テスト実行
composer test

# カバレッジ確認
composer test-coverage

# 静的解析
composer phpstan

# コードスタイル修正
composer php-cs-fixer-fix
```

## 📖 ドキュメント

- [インストールガイド](docs/installation.md)
- [設定方法](docs/configuration.md)
- [API仕様](docs/api.md)
- [カスタマイズ](docs/customization.md)
- [トラブルシューティング](docs/troubleshooting.md)

## 🛠️ 開発

```bash
# 開発環境セットアップ
git clone https://github.com/autocreate/mypage-auth-system.git
cd mypage-auth-system
composer install
npm install

# テスト実行
composer test

# 開発サーバー起動
php artisan serve
```

## 🤝 コントリビューション

コントリビューションを歓迎します！

1. Fork する
2. Feature ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Request を作成

## 📄 ライセンス

このプロジェクトは [MIT ライセンス](LICENSE) の下で公開されています。

## 🙏 謝辞

- [Laravel](https://laravel.com/) - 素晴らしいフレームワーク
- [LINE Developers](https://developers.line.biz/) - LINE Login API
- [Firebase](https://firebase.google.com/) - 認証・データベースサービス
- [TrustDock](https://trustdock.io/) - 本人確認サービス

---

**AutoCreate Team** によって作成・メンテナンスされています。
