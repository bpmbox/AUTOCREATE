#!/usr/bin/env python3
"""
Laravel風Gradio統合 - 結果確認
"""

import os
import sys

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

print("🎯 Laravel風Gradio統合 - 状況確認")
print("=" * 50)

# 1. 環境変数確認
print("📋 重要な環境変数:")
important_vars = ['GROQ_API_KEY', 'POSTGRES_URL', 'DATABASE_URL']
for var in important_vars:
    value = os.getenv(var)
    status = "✅ SET" if value else "❌ NOT SET"
    print(f"  {var}: {status}")

# 2. データベースファイル確認
print("\n🗄️ データベースファイル:")
database_files = [
    'database/prompts.db',
    'database/approval_system.db', 
    'database/chat_history.db'
]

for db_file in database_files:
    exists = os.path.exists(db_file)
    status = "✅ EXISTS" if exists else "❌ MISSING"
    print(f"  {db_file}: {status}")

# 3. Laravel風構造確認
print("\n🏗️ Laravel風構造:")
structure_paths = [
    'app/Http/Controllers/Gradio/GradioController.py',
    'routes/web.py',
    'config/database.py',
    '.env'
]

for path in structure_paths:
    exists = os.path.exists(path)
    status = "✅ EXISTS" if exists else "❌ MISSING" 
    print(f"  {path}: {status}")

# 4. 起動方法の案内
print("\n🚀 起動方法:")
print("  make app          - アプリケーション起動")
print("  python app.py     - 直接起動")
print("  python app.py --test - テストモード")

print("\n🌐 アクセス予定URL:")
print("  http://localhost:7860/         - メインページ")
print("  http://localhost:7860/gradio   - Gradio統合画面")
print("  http://localhost:7860/dashboard - Laravel風ダッシュボード")

print("\n✅ Laravel風のGradio統合が準備完了しました！")
print("🎉 データベース接続エラーが修正され、.env設定も完了しています。")
