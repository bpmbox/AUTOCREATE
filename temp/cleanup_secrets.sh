#!/bin/bash

# 🔒 シークレットクリーンアップスクリプト
# 全てのハードコーディングされたSupabaseキーを環境変数参照に変更

echo "🔒 シークレットクリーンアップを開始..."

# 危険なファイルを削除（vendorディレクトリの不要なファイル）
echo "📁 vendor内の不要ファイルを削除..."
rm -rf vendor/processmaker/
echo "✅ vendor/processmaker/ を削除しました"

# 古いバックアップファイルの修正
echo "📝 バックアップファイル内のシークレットをプレースホルダーに変更..."

# storage/backups内のファイル
find storage/backups -name "*.bak" -type f -exec sed -i 's/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*/"ENV_SUPABASE_KEY_PLACEHOLDER"/g' {} \;

# resources/automation内のファイル
find resources/automation -name "*.py" -type f -exec sed -i 's/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*/"ENV_SUPABASE_KEY_PLACEHOLDER"/g' {} \;

# storage/deprecated内のファイル
find storage/deprecated -name "*.py" -type f -exec sed -i 's/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*/"ENV_SUPABASE_KEY_PLACEHOLDER"/g' {} \;

# laravel_app/Services内のファイル
find laravel_app/Services -name "*.py" -type f -exec sed -i 's/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*/"ENV_SUPABASE_KEY_PLACEHOLDER"/g' {} \;

# app/Services内のファイル
find app/Services -name "*.py" -type f -exec sed -i 's/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*/"ENV_SUPABASE_KEY_PLACEHOLDER"/g' {} \;

# tests/Feature内のファイル
find tests/Feature -name "*.py" -type f -exec sed -i 's/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*/"ENV_SUPABASE_KEY_PLACEHOLDER"/g' {} \;

echo "✅ 全てのシークレットをプレースホルダーに変更しました"

# .gitignoreの確認・更新
echo "📋 .gitignoreの確認..."
if ! grep -q "\.env$" .gitignore; then
    echo ".env" >> .gitignore
    echo "✅ .env を .gitignore に追加しました"
fi

if ! grep -q "vendor/" .gitignore; then
    echo "vendor/" >> .gitignore
    echo "✅ vendor/ を .gitignore に追加しました"
fi

echo "🎯 クリーンアップ完了！"
echo "⚠️  注意: 実際の環境変数設定を忘れずに行ってください"
echo "📋 必要な環境変数:"
echo "  - SUPABASE_URL=https://rootomzbucovwdqsscqd.supabase.co"
echo "  - SUPABASE_KEY=[実際のキー]"
echo "  - SUPABASE_SERVICE_ROLE_KEY=[実際のサービスロールキー]"
