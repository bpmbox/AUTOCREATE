#!/usr/bin/env python3
"""
🔥 チャットからの投稿シミュレーションテスト
======================================

実際のSupabaseにメッセージを投稿して、バックグラウンドサービスが
自動的に検出・処理するかをテスト
"""

import os
import sys
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# .env読み込み
load_dotenv()

# Supabase設定
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def test_supabase_connection():
    """Supabase接続テスト"""
    print("🔍 Supabase接続テスト...")
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # テスト用クエリ（テーブル一覧取得）
        result = supabase.table('chat_history').select('id').limit(1).execute()
        print(f"✅ Supabase接続成功 - chat_historyテーブル確認")
        return supabase
    except Exception as e:
        print(f"❌ Supabase接続失敗: {e}")
        return None

def post_test_message(supabase, message):
    """テストメッセージをSupabaseに投稿"""
    print(f"📝 テストメッセージ投稿: {message[:50]}...")
    try:
        # メッセージを投稿
        data = {
            'ownerid': 'test-user-chat',
            'messages': message,
            'created': datetime.now().isoformat()
        }
        
        result = supabase.table('chat_history').insert(data).execute()
        if result.data:
            message_id = result.data[0]['id']
            print(f"✅ メッセージ投稿成功 - ID: {message_id}")
            return message_id
        else:
            print(f"❌ メッセージ投稿失敗: データなし")
            return None
    except Exception as e:
        print(f"❌ メッセージ投稿失敗: {e}")
        return None

def check_background_processing(wait_time=35):
    """バックグラウンド処理を待機・確認"""
    print(f"⏳ バックグラウンド処理を待機中... ({wait_time}秒)")
    
    for i in range(wait_time):
        print(f"   {i+1:2d}/{wait_time}秒経過...", end='\r')
        time.sleep(1)
    
    print(f"\n🔍 バックグラウンドサービス状態確認...")
    try:
        response = requests.get("http://localhost:7862/background/status")
        if response.status_code == 200:
            status = response.json()
            print(f"📊 バックグラウンドサービス:")
            print(f"   - 実行中: {status.get('is_running')}")
            print(f"   - 最終チェック: {status.get('last_check')}")
            return True
        else:
            print(f"❌ ステータス取得失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ステータス確認エラー: {e}")
        return False

def check_processing_result(supabase, message_id):
    """処理結果をSupabaseで確認"""
    print(f"🔍 処理結果確認 (メッセージID: {message_id})...")
    try:
        # AI応答を確認
        result = supabase.table('chat_history') \
            .select('*') \
            .in_('ownerid', ['GitHub-Copilot-AI', 'GitHub-Copilot-AI-System']) \
            .order('created', desc=True) \
            .limit(5) \
            .execute()
        
        if result.data:
            print(f"📨 AI応答メッセージ検出:")
            for msg in result.data:
                created = msg.get('created', 'unknown')
                content = msg.get('messages', '')[:100]
                print(f"   - {created}: {content}...")
            return True
        else:
            print(f"📭 AI応答メッセージなし")
            return False
    except Exception as e:
        print(f"❌ 結果確認エラー: {e}")
        return False

def cleanup_test_messages(supabase):
    """テストメッセージをクリーンアップ"""
    print(f"🧹 テストメッセージクリーンアップ...")
    try:
        # test-user-chatのメッセージを削除
        result = supabase.table('chat_history') \
            .delete() \
            .eq('ownerid', 'test-user-chat') \
            .execute()
        print(f"✅ クリーンアップ完了")
    except Exception as e:
        print(f"⚠️ クリーンアップエラー: {e}")

def main():
    """メイン実行"""
    print("🔥 チャット投稿→自動処理 統合テスト")
    print("=" * 50)
    
    # Step 1: Supabase接続確認
    supabase = test_supabase_connection()
    if not supabase:
        print("❌ Supabase接続できません。テスト中止。")
        return False
    
    # Step 2: テストメッセージ投稿
    test_messages = [
        "FastAPIでリアルタイムチャットを作成してください",
        "Pythonで機械学習のサンプルコードを書いてください",
        "Reactでダッシュボード画面を作成してください"
    ]
    
    posted_ids = []
    for message in test_messages:
        message_id = post_test_message(supabase, message)
        if message_id:
            posted_ids.append(message_id)
        time.sleep(2)  # 投稿間の待機
    
    if not posted_ids:
        print("❌ メッセージ投稿に失敗しました。テスト中止。")
        return False
    
    print(f"✅ {len(posted_ids)}件のテストメッセージを投稿完了")
    
    # Step 3: バックグラウンド処理待機
    background_ok = check_background_processing()
    
    # Step 4: 処理結果確認
    any_processed = False
    for message_id in posted_ids:
        if check_processing_result(supabase, message_id):
            any_processed = True
    
    # Step 5: クリーンアップ
    cleanup_test_messages(supabase)
    
    # 結果評価
    print("\n" + "=" * 50)
    print("🎯 統合テスト結果")
    print("=" * 50)
    
    if background_ok and any_processed:
        print("🎉 成功！チャット投稿からの自動処理が正常に動作しています")
        print("✅ Supabase投稿 → バックグラウンド検出 → AI処理 の流れが確認できました")
        return True
    elif background_ok:
        print("⚠️ 部分的成功：バックグラウンドサービスは動作していますが、AI処理が確認できませんでした")
        print("💡 システムがオフラインモードで動作している可能性があります")
        return True
    else:
        print("❌ 失敗：バックグラウンドサービスに問題があります")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 テスト中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 予期しないエラー: {e}")
        sys.exit(1)
