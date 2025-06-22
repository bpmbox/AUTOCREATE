# GitHub Copilot 完全自動回答システム - PowerShell版

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host " 🔥 GitHub Copilot 完全自動回答システム 🔥" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✨ 完全自動モードで起動中..." -ForegroundColor Green
Write-Host "📍 固定座標: (1335, 1045)" -ForegroundColor Blue
Write-Host "⚡ 3秒間隔で永続監視" -ForegroundColor Magenta
Write-Host "🤖 手を離してください - 完全自動運転中" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  停止するには Ctrl+C を押してください" -ForegroundColor Red
Write-Host ""

# スクリプトのディレクトリに移動
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
Set-Location "tests\Feature"

# Python スクリプトを完全自動モードで起動
try {
    python copilot_direct_answer.py --auto
}
catch {
    Write-Host "❌ エラーが発生しました: $($_.Exception.Message)" -ForegroundColor Red
}
finally {
    Write-Host ""
    Write-Host "===============================================================" -ForegroundColor Cyan
    Write-Host " 🚪 システム終了" -ForegroundColor Yellow
    Write-Host "===============================================================" -ForegroundColor Cyan
    Read-Host "終了するには何か入力してください"
}
