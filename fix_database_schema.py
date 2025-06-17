#!/usr/bin/env python3
"""
Database Schema Update Script
データベーススキーマを更新して不足しているカラムを追加
"""
import sqlite3
import os
from datetime import datetime

def update_database_schema():
    """データベーススキーマを更新"""
    
    # データベースパス
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'prompts.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 現在のテーブル構造を確認
        cursor.execute("PRAGMA table_info(prompts)")
        columns = cursor.fetchall()
        
        existing_columns = [col[1] for col in columns]
        print(f"📋 Current columns: {existing_columns}")
        
        # 不足しているカラムを追加
        updates_needed = []
        
        if 'github_url' not in existing_columns:
            updates_needed.append(('github_url', 'TEXT'))
        
        if 'system_type' not in existing_columns:
            updates_needed.append(('system_type', 'TEXT DEFAULT "general"'))
        
        if 'tags' not in existing_columns:
            updates_needed.append(('tags', 'TEXT'))
        
        if 'status' not in existing_columns:
            updates_needed.append(('status', 'TEXT DEFAULT "active"'))
        
        if 'priority' not in existing_columns:
            updates_needed.append(('priority', 'INTEGER DEFAULT 1'))
        
        if 'author' not in existing_columns:
            updates_needed.append(('author', 'TEXT'))
        
        if 'description' not in existing_columns:
            updates_needed.append(('description', 'TEXT'))
        
        # カラムを追加
        for column_name, column_type in updates_needed:
            try:
                cursor.execute(f"ALTER TABLE prompts ADD COLUMN {column_name} {column_type}")
                print(f"✅ Added column: {column_name} ({column_type})")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️ Column {column_name} already exists")
                else:
                    print(f"❌ Error adding column {column_name}: {e}")
        
        # 更新された構造を確認
        cursor.execute("PRAGMA table_info(prompts)")
        updated_columns = cursor.fetchall()
        
        print(f"📋 Updated columns: {[col[1] for col in updated_columns]}")
        
        conn.commit()
        conn.close()
        
        print("✅ Database schema update completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database schema update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_data():
    """サンプルデータを作成"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'prompts.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # サンプルデータを挿入
        sample_data = [
            (
                "システム管理プロンプト",
                "システム全体の管理と監視を行うプロンプト",
                "system",
                datetime.now(),
                datetime.now(),
                "https://github.com/example/system-prompt",
                "admin",
                "admin",
                "管理者用,システム管理",
                "active",
                1,
                "システム管理者向けの基本プロンプト"
            ),
            (
                "開発者支援プロンプト", 
                "開発者の作業を支援するプロンプト",
                "development",
                datetime.now(),
                datetime.now(),
                "https://github.com/example/dev-prompt",
                "developer",
                "開発チーム",
                "開発,支援,コーディング",
                "active",
                2,
                "開発者向けのコーディング支援プロンプト"
            )
        ]
        
        # INSERT文を実行
        cursor.executemany("""
            INSERT OR REPLACE INTO prompts 
            (title, content, category, created_at, updated_at, github_url, system_type, author, tags, status, priority, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        
        conn.commit()
        conn.close()
        
        print("✅ Sample data created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 Database Schema Update")
    print("=" * 50)
    
    if update_database_schema():
        print("\n" + "=" * 50)
        print("📊 Creating Sample Data")
        print("=" * 50)
        create_sample_data()
    else:
        print("❌ Schema update failed, skipping sample data creation")
