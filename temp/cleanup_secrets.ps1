# 🔒 シークレットクリーンアップスクリプト (PowerShell版)
# 全てのハードコーディングされたSupabaseキーを環境変数参照に変更

Write-Host "🔒 シークレットクリーンアップを開始..." -ForegroundColor Green

# 危険なファイルを削除（vendorディレクトリの不要なファイル）
Write-Host "📁 vendor内の不要ファイルを削除..." -ForegroundColor Yellow
if (Test-Path "vendor\processmaker") {
    Remove-Item -Recurse -Force "vendor\processmaker"
    Write-Host "✅ vendor\processmaker\ を削除しました" -ForegroundColor Green
}

# パターンマッチングでシークレットを置換する関数
function Replace-SecretsInFiles {
    param(
        [string]$Path,
        [string]$Pattern
    )
    
    if (Test-Path $Path) {
        Get-ChildItem -Path $Path -Recurse -Include $Pattern | ForEach-Object {
            $content = Get-Content $_.FullName -Raw
            if ($content -match 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.') {
                $content = $content -replace 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[^"]*', 'ENV_SUPABASE_KEY_PLACEHOLDER'
                Set-Content -Path $_.FullName -Value $content
                Write-Host "📝 修正: $($_.Name)" -ForegroundColor Cyan
            }
        }
    }
}

Write-Host "📝 バックアップファイル内のシークレットをプレースホルダーに変更..." -ForegroundColor Yellow

# 各ディレクトリの処理
Replace-SecretsInFiles -Path "storage\backups" -Pattern "*.bak"
Replace-SecretsInFiles -Path "resources\automation" -Pattern "*.py"
Replace-SecretsInFiles -Path "storage\deprecated" -Pattern "*.py"
Replace-SecretsInFiles -Path "laravel_app\Services" -Pattern "*.py"
Replace-SecretsInFiles -Path "app\Services" -Pattern "*.py"
Replace-SecretsInFiles -Path "tests\Feature" -Pattern "*.py"

Write-Host "✅ 全てのシークレットをプレースホルダーに変更しました" -ForegroundColor Green

# .gitignoreの確認・更新
Write-Host "📋 .gitignoreの確認..." -ForegroundColor Yellow
$gitignoreContent = ""
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
}

$needsUpdate = $false
if ($gitignoreContent -notlike "*`.env`*") {
    $gitignoreContent += "`n.env"
    $needsUpdate = $true
    Write-Host "✅ .env を .gitignore に追加" -ForegroundColor Green
}

if ($gitignoreContent -notlike "*vendor/`*") {
    $gitignoreContent += "`nvendor/"
    $needsUpdate = $true
    Write-Host "✅ vendor/ を .gitignore に追加" -ForegroundColor Green
}

if ($needsUpdate) {
    Set-Content -Path ".gitignore" -Value $gitignoreContent.Trim()
}

Write-Host "🎯 クリーンアップ完了！" -ForegroundColor Green
Write-Host "⚠️  注意: 実際の環境変数設定を忘れずに行ってください" -ForegroundColor Yellow
Write-Host "📋 必要な環境変数:" -ForegroundColor Cyan
Write-Host "  - SUPABASE_URL=https://rootomzbucovwdqsscqd.supabase.co" -ForegroundColor White
Write-Host "  - SUPABASE_KEY=[実際のキー]" -ForegroundColor White
Write-Host "  - SUPABASE_SERVICE_ROLE_KEY=[実際のサービスロールキー]" -ForegroundColor White
