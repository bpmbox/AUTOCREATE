#!/usr/bin/env python3
"""
データベーススキーマ完全修正スクリプト
"""
import sqlite3
import os
from datetime import datetime

def recreate_prompts_database():
    """promptsデータベースを完全に再作成"""
    print("🔄 Recreating prompts database with all required columns...")
    
    # データベースファイルパス
    db_path = os.path.join('database', 'prompts.db')
    
    # ディレクトリ作成
    os.makedirs('database', exist_ok=True)
    
    # 既存ファイルを削除
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Old database removed")
    
    # 新しいデータベースを作成
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 必要なカラムをすべて含むテーブルを作成
    cursor.execute('''
        CREATE TABLE prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            github_url TEXT,
            system_type TEXT DEFAULT 'default',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # サンプルデータを挿入
    sample_data = [
        ('テストプロンプト', 'Hello World を表示するPythonスクリプト', 'テスト', 'https://github.com/example/repo', 'lavelo'),
        ('システム作成', 'Webアプリケーションを作成してください', 'システム', 'https://github.com/example/webapp', 'system'),
        ('データ分析', 'CSVファイルを分析してグラフを作成', 'データ', 'https://github.com/example/analysis', 'analysis')
    ]
    
    for data in sample_data:
        cursor.execute('''
            INSERT INTO prompts (title, content, category, github_url, system_type)
            VALUES (?, ?, ?, ?, ?)
        ''', data)
    
    conn.commit()
    conn.close()
    print(f"✅ Database recreated: {db_path}")
    
    # 検証
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(prompts)")
    columns = cursor.fetchall()
    print("📋 Table columns:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    cursor.execute("SELECT COUNT(*) FROM prompts")
    count = cursor.fetchone()[0]
    print(f"📊 Sample records: {count}")
    
    conn.close()

def recreate_github_issues_database():
    """github_issuesデータベースを作成"""
    print("🔄 Creating github_issues database...")
    
    db_path = os.path.join('database', 'github_issues.db')
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE github_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT,
            labels TEXT,
            status TEXT DEFAULT 'open',
            github_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ GitHub issues database created: {db_path}")

if __name__ == "__main__":
    recreate_prompts_database()
    recreate_github_issues_database()
    print("🎉 All databases recreated successfully!")
