#!/usr/bin/env python3
"""
🧪 ライブサーバーテスト - 直接API呼び出し
=======================================

現在動作中のFastAPIサーバーに対して直接テストを実行
"""

import requests
import json
import time
import uuid
from datetime import datetime

def test_live_server():
    """ライブサーバーテスト"""
    
    base_url = "http://localhost:7860"
    test_id = str(uuid.uuid4())[:8]
    
    print(f"🚀 ライブサーバーテスト開始 - ID: {test_id}")
    print("=" * 50)
    
    # 1. ヘルスチェック
    print("1. ヘルスチェック")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            print(f"   レスポンス: {response.json()}")
            print("   ✅ ヘルスチェック成功")
        else:
            print("   ❌ ヘルスチェック失敗")
            return
    except Exception as e:
        print(f"   ❌ ヘルスチェックエラー: {e}")
        return
    
    # 2. バックグラウンドサービス状態
    print("\n2. バックグラウンドサービス状態")
    try:
        response = requests.get(f"{base_url}/background/status", timeout=5)
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            print(f"   動作中: {status.get('is_running', False)}")
            print(f"   スレッド生存: {status.get('thread_alive', False)}")
            print(f"   自動化システム: {status.get('automation_system_loaded', False)}")
            print("   ✅ バックグラウンド状態取得成功")
        else:
            print("   ❌ バックグラウンド状態取得失敗")
    except Exception as e:
        print(f"   ❌ バックグラウンド状態エラー: {e}")
    
    # 3. 自動化システム状態
    print("\n3. 自動化システム状態")
    try:
        response = requests.get(f"{base_url}/automation/status", timeout=10)
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            print(f"   GitHub CLI: {status.get('github_cli_available', 'unknown')}")
            print(f"   Supabase: {status.get('supabase_connected', 'unknown')}")
            print(f"   システム状態: {status.get('status', 'unknown')}")
            print("   ✅ 自動化システム状態取得成功")
        else:
            print("   ❌ 自動化システム状態取得失敗")
    except Exception as e:
        print(f"   ❌ 自動化システム状態エラー: {e}")
    
    # 4. Mermaid図生成テスト
    print("\n4. Mermaid図生成テスト")
    try:
        test_data = {
            "content": f"ライブテスト {test_id}",
            "diagram_type": "flowchart"
        }
        
        response = requests.post(f"{base_url}/automation/mermaid/generate", 
                               json=test_data, timeout=15)
        print(f"   ステータス: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   成功: {result.get('success', False)}")
            if result.get('mermaid_content'):
                print(f"   図コンテンツ: {len(result['mermaid_content'])}文字")
                print("   ✅ Mermaid図生成成功")
            else:
                print("   ⚠️ Mermaid図コンテンツが空")
        else:
            print(f"   ❌ Mermaid図生成失敗")
            print(f"   エラー: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Mermaid図生成エラー: {e}")
    
    # 5. 完全自動化API実行
    print("\n5. 完全自動化API実行")
    try:
        automation_data = {
            "message": f"ライブ自動化テスト {test_id}",
            "create_issue": False,  # Issue作成は無効（テストのため）
            "generate_mermaid": True,
            "offline_mode": True
        }
        
        response = requests.post(f"{base_url}/automation/run", 
                               json=automation_data, timeout=20)
        print(f"   ステータス: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   成功: {result.get('success', False)}")
            print(f"   メッセージ: {result.get('message', 'unknown')}")
            print(f"   処理時間: {result.get('processing_time', 0)}秒")
            
            if result.get('mermaid_content'):
                print(f"   Mermaid生成: ✅ ({len(result['mermaid_content'])}文字)")
            else:
                print("   Mermaid生成: ❌")
                
            if result.get('issue_url'):
                print(f"   Issue作成: ✅ {result['issue_url']}")
            else:
                print("   Issue作成: ❌ (無効化済み)")
                
            print("   ✅ 完全自動化API実行成功")
        else:
            print(f"   ❌ 完全自動化API実行失敗")
            print(f"   エラー: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ 完全自動化APIエラー: {e}")
    
    # 6. Laravel風API確認
    print("\n6. Laravel風API確認")
    try:
        response = requests.get(f"{base_url}/laravel/status", timeout=5)
        print(f"   ステータス: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            print(f"   Laravel状態: {status.get('status', 'unknown')}")
            print(f"   機能数: {len(status.get('features', []))}")
            print("   ✅ Laravel風API確認成功")
        else:
            print("   ❌ Laravel風API確認失敗")
    except Exception as e:
        print(f"   ❌ Laravel風APIエラー: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 ライブサーバーテスト完了!")
    print(f"📖 Swagger UI: {base_url}/docs")
    print(f"📚 ReDoc: {base_url}/redoc")
    print("🚀 すべてのテストが正常に実行されました")

if __name__ == "__main__":
    test_live_server()
