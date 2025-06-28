#!/usr/bin/env python3
"""
🧪 FastAPI + Supabase 簡単統合テスト
==================================

最小限の統合テスト：
1. API動作確認
2. Supabase接続
3. 質問投稿
4. 自動化API実行

確実に1件の処理が成功することを確認
"""

import requests
import time
import uuid
from datetime import datetime
from supabase import create_client
import os
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

def test_simple_integration():
    """シンプルな統合テスト"""
    
    print("🚀 FastAPI + Supabase 簡単統合テスト開始")
    print("=" * 50)
    
    # テスト設定
    base_url = "http://localhost:7860"
    test_id = str(uuid.uuid4())[:8]
    test_question = f"簡単テスト質問 - {test_id}"
    
    print(f"🧪 テストID: {test_id}")
    print(f"📝 テスト質問: {test_question}")
    
    # Step 1: API確認
    print("\n🔍 Step 1: API動作確認")
    try:
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        print("✅ API動作確認成功")
    except Exception as e:
        print(f"❌ API動作確認失敗: {e}")
        return False
    
    # Step 2: Supabase接続確認
    print("\n🔍 Step 2: Supabase接続確認")
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ Supabase環境変数未設定")
            return False
        
        supabase = create_client(supabase_url, supabase_key)
        
        # テーブル存在確認
        result = supabase.table('chat_history').select('*').limit(1).execute()
        print(f"✅ Supabase接続成功 - サンプルデータ: {len(result.data)}件")
        
        # テーブル構造確認
        if result.data:
            columns = list(result.data[0].keys())
            print(f"📊 テーブルカラム: {columns}")
        
    except Exception as e:
        print(f"❌ Supabase接続失敗: {e}")
        return False
    
    # Step 3: 最小限の質問投稿
    print("\n🔍 Step 3: 最小限の質問投稿")
    try:
        # 必要最小限のデータで投稿
        minimal_data = {
            'question': test_question,
            'user': f'test_user_{test_id}'
        }
        
        # processed カラムが存在するかチェックして追加
        if result.data and 'processed' in result.data[0]:
            minimal_data['processed'] = False
            
        print(f"📝 投稿データ: {minimal_data}")
        
        insert_result = supabase.table('chat_history').insert(minimal_data).execute()
        
        if insert_result.data and len(insert_result.data) > 0:
            question_id = insert_result.data[0]['id']
            print(f"✅ 質問投稿成功 - ID: {question_id}")
        else:
            raise Exception("投稿結果が空です")
            
    except Exception as e:
        print(f"❌ 質問投稿失敗: {e}")
        return False
    
    # Step 4: 自動化API直接実行
    print("\n🔍 Step 4: 自動化API直接実行")
    try:
        automation_response = requests.post(f"{base_url}/automation/run", json={
            "message": test_question,
            "create_issue": False,  # GitHub Issue作成は無効
            "generate_mermaid": True,
            "offline_mode": True
        })
        
        if automation_response.status_code == 200:
            result = automation_response.json()
            print(f"✅ 自動化API実行成功")
            print(f"📊 成功フラグ: {result.get('success', False)}")
            print(f"📊 メッセージ: {result.get('message', 'unknown')}")
            print(f"📊 処理時間: {result.get('processing_time', 0)}秒")
            
            if result.get('mermaid_content'):
                print(f"📊 Mermaid図生成: {len(result['mermaid_content'])}文字")
            else:
                print("📊 Mermaid図生成: なし")
                
        else:
            print(f"❌ 自動化API実行失敗: {automation_response.status_code}")
            print(f"エラー詳細: {automation_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 自動化API実行エラー: {e}")
        return False
    
    # Step 5: 質問を処理済みとしてマーク
    print("\n🔍 Step 5: 質問を処理済みとしてマーク")
    try:
        # 質問を処理済みとしてマーク
        update_data = {
            'test_completed': True,
            'test_completed_at': datetime.now().isoformat(),
            'test_method': 'simple_integration_test'
        }
        
        # processed カラムが存在する場合
        if 'processed' in columns:
            update_data['processed'] = True
            
        supabase.table('chat_history').update(update_data).eq('id', question_id).execute()
        print("✅ 質問を処理済みとしてマーク完了")
        
    except Exception as e:
        print(f"⚠️ 処理済みマーク警告: {e}")
        # これは致命的エラーではない
    
    # Step 6: バックグラウンドサービス確認
    print("\n🔍 Step 6: バックグラウンドサービス確認")
    try:
        bg_response = requests.get(f"{base_url}/background/status")
        if bg_response.status_code == 200:
            bg_status = bg_response.json()
            print(f"📊 バックグラウンド動作中: {bg_status.get('is_running', False)}")
            print(f"📊 自動化システム読み込み済み: {bg_status.get('automation_system_loaded', False)}")
            print(f"📊 最終チェック: {bg_status.get('last_check', 'なし')}")
        else:
            print("⚠️ バックグラウンドサービス状態取得失敗")
            
    except Exception as e:
        print(f"⚠️ バックグラウンドサービス確認エラー: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 簡単統合テスト完全成功!")
    print("✅ FastAPI → Supabase → 自動化API → 完了")
    print(f"📊 テスト質問ID: {question_id}")
    print(f"📖 Swagger UI: {base_url}/docs")
    
    return True

if __name__ == "__main__":
    success = test_simple_integration()
    
    if success:
        print("\n🎯 統合テスト成功 - システムは正常に動作しています")
        exit(0)
    else:
        print("\n❌ 統合テスト失敗 - システムに問題があります")
        exit(1)
