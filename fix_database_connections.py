#!/usr/bin/env python3
"""
SQLite/DuckDB Connection Fix
SQLiteとDuckDBの接続エラーを修正するスクリプト
"""
import os
import sys
import sqlite3
import subprocess

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def check_database_connections():
    """データベース接続の確認"""
    print("🔍 Checking SQLite/DuckDB connections...")
    
    # 1. SQLite接続テスト
    try:
        from config.database import get_db_connection, DATABASE_PATHS
        
        print("📊 SQLite Database Status:")
        for db_name, db_path in DATABASE_PATHS.items():
            try:
                if os.path.exists(db_path):
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    conn.close()
                    print(f"  ✅ {db_name}: {len(tables)} tables")
                else:
                    print(f"  ❌ {db_name}: File not found - {db_path}")
            except Exception as e:
                print(f"  ⚠️ {db_name}: Connection error - {e}")
    
    except Exception as e:
        print(f"❌ SQLite configuration error: {e}")
    
    # 2. DuckDB接続テスト
    try:
        import duckdb
        print("🦆 DuckDB Connection Test:")
        
        # DuckDBファイルの場所確認
        duckdb_files = [
            "./workspace/mydatabase.duckdb",
            "./workspace/sample.duckdb",
            "workspace/mydatabase.duckdb",
            "workspace/sample.duckdb"
        ]
        
        for db_file in duckdb_files:
            try:
                if os.path.exists(db_file):
                    conn = duckdb.connect(db_file)
                    tables = conn.execute("SHOW TABLES").fetchall()
                    conn.close()
                    print(f"  ✅ {db_file}: {len(tables)} tables")
                else:
                    print(f"  ⚠️ {db_file}: File not found")
            except Exception as e:
                print(f"  ❌ {db_file}: Connection error - {e}")
                
        # メモリ内DuckDBテスト
        try:
            conn = duckdb.connect(":memory:")
            conn.execute("CREATE TABLE test (id INTEGER, name VARCHAR)")
            conn.execute("INSERT INTO test VALUES (1, 'test')")
            result = conn.execute("SELECT * FROM test").fetchall()
            conn.close()
            print(f"  ✅ Memory DuckDB: Working ({len(result)} test records)")
        except Exception as e:
            print(f"  ❌ Memory DuckDB: Error - {e}")
            
    except ImportError:
        print("❌ DuckDB not installed")
    except Exception as e:
        print(f"❌ DuckDB test error: {e}")

def fix_database_connections():
    """データベース接続の修正"""
    print("🔧 Fixing database connections...")
    
    # 1. 必要なディレクトリを作成
    directories = [
        "database",
        "workspace", 
        "flagged",
        "chroma"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  📁 Created/verified directory: {directory}")
    
    # 2. SQLiteデータベースを初期化
    try:
        from database.init_databases import create_databases
        print("  🔄 Initializing SQLite databases...")
        result = create_databases()
        if result:
            print("  ✅ SQLite databases initialized successfully")
        else:
            print("  ⚠️ SQLite initialization had some issues")
    except Exception as e:
        print(f"  ❌ SQLite initialization failed: {e}")
    
    # 3. DuckDBファイルを作成
    try:
        import duckdb
        print("  🔄 Initializing DuckDB databases...")
        
        duckdb_files = [
            "workspace/mydatabase.duckdb",
            "workspace/sample.duckdb"
        ]
        
        for db_file in duckdb_files:
            try:
                # ディレクトリ作成
                os.makedirs(os.path.dirname(db_file), exist_ok=True)
                
                # DuckDBファイル作成
                conn = duckdb.connect(db_file)
                conn.execute("CREATE TABLE IF NOT EXISTS test_table (id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
                conn.execute("INSERT INTO test_table (id) VALUES (1)")
                conn.close()
                print(f"  ✅ Created/verified: {db_file}")
            except Exception as e:
                print(f"  ❌ Failed to create {db_file}: {e}")
                
    except ImportError:
        print("  ⚠️ DuckDB not available, installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "duckdb"], check=True)
            print("  ✅ DuckDB installed successfully")
        except Exception as e:
            print(f"  ❌ Failed to install DuckDB: {e}")
    except Exception as e:
        print(f"  ❌ DuckDB initialization failed: {e}")
    
    # 4. 権限設定
    try:
        # データベースファイルの権限を設定
        for root, dirs, files in os.walk("database"):
            for file in files:
                if file.endswith(".db"):
                    file_path = os.path.join(root, file)
                    os.chmod(file_path, 0o666)
        
        for root, dirs, files in os.walk("workspace"):
            for file in files:
                if file.endswith(".duckdb"):
                    file_path = os.path.join(root, file)
                    os.chmod(file_path, 0o666)
        
        print("  ✅ Database file permissions updated")
    except Exception as e:
        print(f"  ⚠️ Permission update warning: {e}")

def test_gradio_with_fixed_databases():
    """修正されたデータベースでGradioをテスト"""
    print("🧪 Testing Gradio with fixed databases...")
    
    try:
        import gradio as gr
        
        def database_status_check():
            """データベース状態確認"""
            status = []
            
            # SQLite確認
            try:
                from config.database import DATABASE_PATHS
                for db_name, db_path in DATABASE_PATHS.items():
                    if os.path.exists(db_path):
                        status.append(f"✅ SQLite {db_name}: OK")
                    else:
                        status.append(f"❌ SQLite {db_name}: Missing")
            except Exception as e:
                status.append(f"❌ SQLite error: {e}")
            
            # DuckDB確認
            try:
                import duckdb
                conn = duckdb.connect(":memory:")
                conn.execute("SELECT 1")
                status.append("✅ DuckDB: OK")  
                conn.close()
            except Exception as e:
                status.append(f"❌ DuckDB error: {e}")
            
            return "\n".join(status)
        
        # テスト用インターフェース
        interface = gr.Interface(
            fn=database_status_check,
            inputs=None,
            outputs=gr.Textbox(label="Database Status", lines=10),
            title="🔧 Database Connection Fix Test",
            description="Click Submit to check database connections",
            allow_flagging="never"
        )
        
        print("✅ Test Gradio interface created with database fix")
        return interface
        
    except Exception as e:
        print(f"❌ Gradio test interface creation failed: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 SQLite/DuckDB Connection Fix")
    print("=" * 60)
    
    # 1. 現在の状態確認
    check_database_connections()
    print()
    
    # 2. 修正実行
    fix_database_connections()
    print()
    
    # 3. 修正後の確認
    print("🔍 Post-fix verification:")
    check_database_connections()
    print()
    
    # 4. Gradioテスト
    if "--test-gradio" in sys.argv:
        interface = test_gradio_with_fixed_databases()
        if interface:
            print("🚀 Starting test Gradio interface...")
            interface.launch(server_name="0.0.0.0", server_port=7860)
