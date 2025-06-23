# 🧪 テスト実行ガイド

## 📋 事前準備

### 1. Supabaseテスト用データベース設定
```bash
# 1. Supabase ダッシュボードでテスト用プロジェクト作成
# 2. テスト用データベースURL・APIキー取得
# 3. .env.testingファイルに設定
```

### 2. 環境設定
```bash
# テスト用環境ファイル設定
cp .env.example .env.testing

# テスト用データベース接続情報を編集
# SUPABASE_URL=https://your-test-project.supabase.co
# SUPABASE_KEY=your_test_supabase_key
```

## 🚀 テスト実行コマンド

### 基本テスト実行
```bash
# 🔥 全テスト実行
docker-compose exec app php artisan test

# 🎯 ユニットテストのみ
docker-compose exec app php artisan test --testsuite=Unit

# 🚀 フィーチャーテストのみ  
docker-compose exec app php artisan test --testsuite=Feature

# 📊 詳細出力付き
docker-compose exec app php artisan test --verbose

# 🔍 特定テストクラス実行
docker-compose exec app php artisan test tests/Feature/LineLoginTest.php

# 📈 テストカバレッジ
docker-compose exec app php artisan test --coverage
```

### 個別テスト実行
```bash
# LINE Login テスト
docker-compose exec app php artisan test --filter=LineLoginTest

# LINE User モデルテスト
docker-compose exec app php artisan test --filter=LineUserModelTest

# 認証テスト
docker-compose exec app php artisan test --filter=authentication

# データベーステスト
docker-compose exec app php artisan test --filter=database
```

### パフォーマンステスト
```bash
# ⚡ 並列テスト実行
docker-compose exec app php artisan test --parallel

# 🎭 特定グループのテスト
docker-compose exec app php artisan test --group=auth
docker-compose exec app php artisan test --group=api

# 🔥 失敗時停止
docker-compose exec app php artisan test --stop-on-failure
```

## 🗄️ データベース管理

### テストデータベース初期化
```bash
# マイグレーション実行
docker-compose exec app php artisan migrate --env=testing

# マイグレーション＋シーダー実行
docker-compose exec app php artisan migrate:fresh --seed --env=testing

# テストデータベースリセット
docker-compose exec app php artisan migrate:reset --env=testing
```

### テストデータ作成
```bash
# ファクトリーでテストデータ生成
docker-compose exec app php artisan tinker --env=testing
# > LineUser::factory()->count(10)->create();
```

## 📊 テスト結果の確認

### レポート生成
```bash
# HTMLテストレポート生成
docker-compose exec app php artisan test --coverage-html coverage-report

# XMLレポート生成
docker-compose exec app php artisan test --coverage-xml coverage-xml

# JSON出力
docker-compose exec app php artisan test --log-json test-results.json
```

### 継続的インテグレーション
```bash
# CI用テスト実行
docker-compose exec app php artisan test --no-interaction --coverage-text

# 本番環境テスト
docker-compose exec app php artisan test --env=production
```

## 🔧 トラブルシューティング

### よくある問題
1. **データベース接続エラー**
   ```bash
   # テスト用データベース確認
   docker-compose exec app php artisan migrate:status --env=testing
   ```

2. **権限エラー**
   ```bash
   # ストレージ権限修正
   docker-compose exec app chmod -R 777 storage bootstrap/cache
   ```

3. **キャッシュクリア**
   ```bash
   # テスト用キャッシュクリア
   docker-compose exec app php artisan cache:clear --env=testing
   ```

## 📈 成功指標

### テスト通過基準
- ✅ 全ユニットテスト通過（80%以上）
- ✅ 全統合テスト通過
- ✅ テストカバレッジ 85%以上
- ✅ LINE Login機能テスト通過
- ✅ データベース整合性テスト通過
- ✅ セキュリティテスト通過

---

🧪 **テスト駆動開発で品質保証！**
