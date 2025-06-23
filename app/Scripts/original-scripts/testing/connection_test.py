#!/usr/bin/env python3
"""
Laravel風Gradio統合テスト
"""

import sys
import os
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def test_connections():
    """データベースとAPI接続をテスト"""
    print("🔍 Connection Testing Started...")
    print("=" * 50)
    
    # 環境変数確認
    print("📋 Environment Variables Check:")
    important_vars = [
        'GROQ_API_KEY', 'POSTGRES_URL', 'LINE_CHANNEL_ACCESS_TOKEN',
        'GITHUB_TOKEN', 'DATABASE_URL'
    ]
    
    for var in important_vars:
        value = os.getenv(var)
        if value:
            # APIキーなどは最初と最後の数文字のみ表示
            if 'key' in var.lower() or 'token' in var.lower():
                display_value = f"{value[:8]}...{value[-8:]}" if len(value) > 16 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: Not set")
    
    print("\n🗄️ Database Connection Test:")
    try:
        # SQLiteデータベーステスト
        from config.database import get_db_connection, DATABASE_PATHS
        
        # データベースディレクトリの存在確認
        db_dir = os.path.dirname(list(DATABASE_PATHS.values())[0])
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"  📁 Created database directory: {db_dir}")
        
        # データベース初期化
        from database.init_databases import create_databases
        create_databases()
        print("  ✅ Database initialization completed")
        
        # 接続テスト
        conn = get_db_connection('chat_history')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
        table_count = cursor.fetchone()[0]
        conn.close()
        print(f"  ✅ SQLite connection successful - {table_count} tables found")
        
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🌐 Laravel-style Gradio Test:")
    try:
        from app.Http.Controllers.Gradio.GradioController import GradioController
        controller = GradioController()
        print("  ✅ GradioController imported successfully")
        
        # 簡単なインターフェーステスト
        interface = controller.create_main_interface()
        print(f"  ✅ Main interface created: {type(interface)}")
        
    except Exception as e:
        print(f"  ❌ Gradio controller test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🔗 API Connection Test:")
    try:
        import requests
        
        # 簡単なHTTPテスト（Google API）
        response = requests.get("https://www.googleapis.com/", timeout=5)
        if response.status_code == 200:
            print("  ✅ Internet connection working")
        else:
            print(f"  ⚠️ Internet connection issue: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Internet connection test failed: {e}")
    
    print("\n🎯 Web Routes Integration Test:")
    try:
        from routes.web import initialize_gradio_with_error_handling
        print("  ✅ Web routes function imported successfully")
        print("  ℹ️ Gradio initialization test skipped (time-consuming)")
        
    except Exception as e:
        print(f"  ❌ Web routes test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎉 Connection test completed!")
    print("Ready to run Laravel-style Gradio application!")

if __name__ == "__main__":
    test_connections()
