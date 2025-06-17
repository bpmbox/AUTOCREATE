#!/usr/bin/env python3
"""
GradioコネクションエラーのデバッグとDB修正
"""

import os
import sys
import sqlite3

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def fix_database_paths():
    """データベースパスの問題を修正"""
    print("🔧 Fixing database paths and connections...")
    
    try:
        from config.database import DATABASE_PATHS
        
        # データベースディレクトリを確実に作成
        db_base_dir = os.path.dirname(list(DATABASE_PATHS.values())[0])
        os.makedirs(db_base_dir, exist_ok=True)
        print(f"📁 Database directory ensured: {db_base_dir}")
        
        # 各データベースファイルを作成
        for db_name, db_path in DATABASE_PATHS.items():
            if not os.path.exists(db_path):
                print(f"🔨 Creating missing database: {db_name}")
                
                # データベース接続を作成（ファイルが自動作成される）
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # 基本テーブルを作成
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS test_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                conn.close()
                print(f"✅ Created: {db_path}")
            else:
                print(f"✅ Exists: {db_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database path fix failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gradio_laravel_structure():
    """Laravel風Gradio構造をテスト"""
    print("\n🎨 Testing Laravel-style Gradio structure...")
    
    try:
        # Laravel風GradioControllerのテスト
        from app.Http.Controllers.Gradio.GradioController import GradioController
        controller = GradioController()
        print("✅ Laravel-style GradioController loaded")
        
        # サービス層のテスト
        from app.Services.GradioInterfaceService import GradioInterfaceService
        service = GradioInterfaceService()
        print("✅ GradioInterfaceService loaded")
        
        # 簡単なインターフェーステスト
        interface = controller.create_main_interface()
        print(f"✅ Main interface created: {type(interface)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Laravel-style Gradio test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connections():
    """データベース接続をテスト"""
    print("\n🗄️ Testing database connections...")
    
    try:
        from config.database import get_db_connection, DATABASE_PATHS
        
        # 各データベースの接続テスト
        for db_name in ['chat_history', 'prompts', 'approval_system']:
            try:
                conn = get_db_connection(db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                print(f"✅ {db_name}: {len(tables)} tables")
            except Exception as e:
                print(f"❌ {db_name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """メイン修正プロセス"""
    print("🚀 Gradio Connection Error Fix")
    print("=" * 50)
    
    # 1. データベースパス修正
    db_ok = fix_database_paths()
    
    # 2. Laravel風構造テスト
    laravel_ok = test_gradio_laravel_structure()
    
    # 3. データベース接続テスト
    conn_ok = test_database_connections()
    
    # 結果
    print("\n" + "=" * 50)
    print("🎯 Fix Results:")
    print(f"  Database Paths: {'✅ FIXED' if db_ok else '❌ FAILED'}")
    print(f"  Laravel Structure: {'✅ OK' if laravel_ok else '❌ FAILED'}")
    print(f"  DB Connections: {'✅ OK' if conn_ok else '❌ FAILED'}")
    
    if all([db_ok, laravel_ok, conn_ok]):
        print("\n🎉 Gradio connection errors should be fixed!")
        print("🚀 Try running: make app")
    else:
        print("\n⚠️ Some issues remain. Check the errors above.")

if __name__ == "__main__":
    main()
