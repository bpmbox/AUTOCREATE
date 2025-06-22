#!/usr/bin/env python3
"""
Supabase Database Schema Explorer
データベース構造を確認してMermaid図を生成
"""

import psycopg2
import json
from datetime import datetime

# Supabase接続情報
DB_CONFIG = {
    'host': 'aws-0-ap-northeast-1.pooler.supabase.com',
    'user': 'postgres.rootomzbucovwdqsscqd',
    'password': 'nD2EGLowld3noFW2',
    'port': 6543,
    'database': 'postgres'
}

def get_database_schema():
    """データベーススキーマを取得"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # public schema のテーブル一覧取得
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        schema_info = {}
        
        for (table_name,) in tables:
            print(f"📋 テーブル: {table_name}")
            
            # テーブルのカラム情報取得
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cursor.fetchall()
            schema_info[table_name] = []
            
            for col in columns:
                column_info = {
                    'name': col[0],
                    'type': col[1],
                    'nullable': col[2],
                    'default': col[3],
                    'max_length': col[4]
                }
                schema_info[table_name].append(column_info)
                print(f"  - {col[0]}: {col[1]} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        conn.close()
        return schema_info
        
    except Exception as e:
        print(f"❌ データベース接続エラー: {e}")
        return None

def generate_mermaid_erd(schema_info):
    """MermaidのERD図を生成"""
    if not schema_info:
        return None
    
    mermaid_content = """erDiagram
"""
    
    # テーブル定義
    for table_name, columns in schema_info.items():
        mermaid_content += f"    {table_name.upper()} {{\n"
        
        for col in columns:
            # データ型の簡略化
            data_type = col['type']
            if 'character' in data_type or 'text' in data_type:
                data_type = 'string'
            elif 'integer' in data_type or 'bigint' in data_type:
                data_type = 'int'
            elif 'timestamp' in data_type:
                data_type = 'datetime'
            elif 'boolean' in data_type:
                data_type = 'bool'
            
            # Primary Key判定（idカラムまたはそれらしいもの）
            pk_indicator = ""
            if col['name'] == 'id' or col['name'].endswith('_id'):
                if col['name'] == 'id':
                    pk_indicator = " PK"
                else:
                    pk_indicator = " FK"
            
            # NOT NULL表示
            null_indicator = "" if col['nullable'] == 'YES' else " NOT_NULL"
            
            mermaid_content += f"        {data_type} {col['name']}{pk_indicator}{null_indicator}\n"
        
        mermaid_content += "    }\n\n"
    
    # リレーション（推測）
    relationships = []
    for table_name, columns in schema_info.items():
        for col in columns:
            # Foreign Key推測（_idで終わる且つ他テーブル名に一致）
            if col['name'].endswith('_id') and col['name'] != 'id':
                potential_parent = col['name'][:-3]  # _idを除去
                # 複数形を単数形に変換（簡易）
                if potential_parent.endswith('s'):
                    potential_parent = potential_parent[:-1]
                
                for other_table in schema_info.keys():
                    if potential_parent.lower() in other_table.lower():
                        relationships.append(f"    {other_table.upper()} ||--o{{ {table_name.upper()} : has")
                        break
    
    # リレーション追加
    for rel in relationships:
        mermaid_content += rel + "\n"
    
    return mermaid_content

def main():
    print("🔍 Supabase Database Schema Explorer")
    print("=" * 50)
    
    # スキーマ取得
    print("📡 データベースに接続中...")
    schema_info = get_database_schema()
    
    if schema_info:
        print("\n🎨 Mermaid ERD図を生成中...")
        mermaid_erd = generate_mermaid_erd(schema_info)
        
        if mermaid_erd:
            # ファイルに保存
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"supabase_schema_{timestamp}.md"
            
            content = f"""# Supabase Database Schema - public

## 📊 Database ERD

```mermaid
{mermaid_erd}
```

## 📋 Table Details

"""
            
            # テーブル詳細情報追加
            for table_name, columns in schema_info.items():
                content += f"### 🗃️ {table_name}\n\n"
                content += "| Column | Type | Nullable | Default |\n"
                content += "|--------|------|----------|----------|\n"
                
                for col in columns:
                    default_val = col['default'] if col['default'] else '-'
                    content += f"| {col['name']} | {col['type']} | {col['nullable']} | {default_val} |\n"
                
                content += "\n"
            
            content += f"""
---
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Database**: {DB_CONFIG['host']}  
**Schema**: public
"""
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Mermaid ERD図を保存しました: {filename}")
            print("\n🎨 Mermaid ERD:")
            print("=" * 50)
            print(mermaid_erd)
            
        else:
            print("❌ Mermaid図の生成に失敗しました")
    else:
        print("❌ スキーマ情報の取得に失敗しました")

if __name__ == "__main__":
    main()
