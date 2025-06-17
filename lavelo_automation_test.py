#!/usr/bin/env python3
"""
Lavelo AI 自動化テストスクリプト
AUTOCREATE株式会社 - AI×人間協働開発システム
"""
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# プロジェクトルートを追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def run_automation_test(prompt_name=None, test_mode="basic"):
    """
    Lavelo AI システムの自動化テストを実行
    """
    print(f"🚀 Lavelo AI 自動化テスト開始")
    print(f"📝 プロンプト: {prompt_name or 'デフォルト'}")
    print(f"🔧 テストモード: {test_mode}")
    print(f"⏰ 開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 環境変数設定
        os.environ['SUPABASE_URL'] = 'https://rootomzbucovwdqsscqd.supabase.co'
        os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8'
        
        print("✅ 環境変数設定完了")
        
        # Lavelo AIシステムのインポートとテスト
        if test_mode == "import_test":
            print("🧪 インポートテスト実行中...")
            test_import_lavelo()
        
        elif test_mode == "supabase_test":
            print("🔍 Supabaseテスト実行中...")
            test_supabase_connection()
        
        elif test_mode == "memory_test":
            print("🧠 記憶システムテスト実行中...")
            test_memory_functions()
        
        elif test_mode == "full_test":
            print("🎯 完全テスト実行中...")
            test_import_lavelo()
            test_supabase_connection()
            test_memory_functions()
            
        else:  # basic test
            print("📋 基本テスト実行中...")
            test_basic_functionality()
        
        print("\n" + "=" * 60)
        print("🎉 自動化テスト完了!")
        return True
        
    except Exception as e:
        print(f"\n❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import_lavelo():
    """Lavelo AIシステムのインポートテスト"""
    try:
        from app.Http.Controllers.Gradio.gra_03_programfromdocs.lavelo import (
            get_memories_from_supabase,
            save_prompt_to_supabase,
            update_prompt_display,
            SUPABASE_AVAILABLE
        )
        print("✅ Lavelo AIシステム インポート成功")
        print(f"   Supabase接続状態: {'可能' if SUPABASE_AVAILABLE else '不可'}")
        return True
    except Exception as e:
        print(f"❌ インポートエラー: {e}")
        return False

def test_supabase_connection():
    """Supabase接続テスト"""
    try:
        from supabase import create_client, Client
        
        SUPABASE_URL = os.getenv('SUPABASE_URL')
        SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 簡単なクエリテスト
        result = supabase.table('chat_history').select('id').limit(1).execute()
        print(f"✅ Supabase接続成功 - {len(result.data)}件のデータ確認")
        return True
        
    except Exception as e:
        print(f"❌ Supabase接続エラー: {e}")
        return False

def test_memory_functions():
    """記憶システム機能テスト"""
    try:
        from app.Http.Controllers.Gradio.gra_03_programfromdocs.lavelo import (
            get_memories_from_supabase,
            save_prompt_to_supabase,
            update_prompt_display
        )
        
        # 記憶取得テスト
        memories = get_memories_from_supabase(limit=3)
        print(f"✅ 記憶取得テスト成功 - {len(memories)}件")
        
        # 記憶保存テスト
        test_title = f"🧪 自動化テスト_{datetime.now().strftime('%H%M%S')}"
        save_result = save_prompt_to_supabase(
            test_title, 
            "自動化テストによる記憶保存テストです。"
        )
        print(f"✅ 記憶保存テスト: {save_result}")
        
        # 表示更新テスト
        display_data = update_prompt_display()
        print(f"✅ 表示更新テスト成功 - {len(display_data)}行")
        
        return True
        
    except Exception as e:
        print(f"❌ 記憶システムテストエラー: {e}")
        return False

def test_basic_functionality():
    """基本機能テスト"""
    print("🔍 基本機能確認中...")
    
    # Python基本機能
    print("  - Python実行環境: ✅")
    
    # 必要モジュール確認
    try:
        import requests
        import json
        from datetime import datetime
        print("  - 必要モジュール: ✅")
    except ImportError as e:
        print(f"  - 必要モジュール: ❌ {e}")
        return False
    
    # 環境変数確認
    if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'):
        print("  - 環境変数: ✅")
    else:
        print("  - 環境変数: ❌")
        return False
    
    print("✅ 基本機能テスト完了")
    return True

def main():
    parser = argparse.ArgumentParser(description='Lavelo AI 自動化テストシステム')
    parser.add_argument('--prompt', type=str, help='テスト用プロンプト名')
    parser.add_argument('--mode', type=str, default='basic', 
                       choices=['basic', 'import_test', 'supabase_test', 'memory_test', 'full_test'],
                       help='テストモード')
    
    args = parser.parse_args()
    
    success = run_automation_test(args.prompt, args.mode)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
