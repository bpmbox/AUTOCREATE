#!/usr/bin/env python3
"""
🚀 リアルタイム チャット監視テスト
============================

実際にチャットメッセージを投稿して、
リアルタイムでシステムの反応を確認
"""

import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

def post_chat_message(message):
    """チャットメッセージを投稿"""
    try:
        supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        
        data = {
            'ownerid': 'real-user-test',
            'messages': message,
            'created': datetime.now().isoformat()
        }
        
        result = supabase.table('chat_history').insert(data).execute()
        if result.data:
            message_id = result.data[0]['id']
            print(f"✅ メッセージ投稿: ID {message_id}")
            print(f"📝 内容: {message}")
            return message_id
        return None
    except Exception as e:
        print(f"❌ 投稿エラー: {e}")
        return None

def check_system_status():
    """システム状態をチェック"""
    try:
        response = requests.get("http://localhost:7862/automation/status")
        if response.status_code == 200:
            status = response.json()
            return status.get('status') == 'healthy'
        return False
    except:
        return False

def main():
    print("🚀 リアルタイム チャット監視テスト")
    print("=" * 40)
    
    if not check_system_status():
        print("❌ システムが稼働していません")
        return
    
    print("✅ システム稼働確認")
    print("📝 チャットメッセージを投稿します...")
    print()
    
    # 実際のチャットメッセージを投稿
    test_message = "PythonでWebAPIを作成してください。FastAPIを使って、ユーザー管理機能を含むシステムを構築したいです。"
    
    message_id = post_chat_message(test_message)
    
    if message_id:
        print(f"\n⏰ 投稿時刻: {datetime.now().strftime('%H:%M:%S')}")
        print("🔄 バックグラウンドサービスが30秒以内に検出・処理します...")
        print("💡 システムログを確認してください")
        
        # 30秒待機しながら進捗表示
        for i in range(30):
            print(f"⏳ 待機中... {i+1}/30秒", end='\r')
            time.sleep(1)
        
        print("\n✅ 処理期間完了")
        print("📊 Swagger UI で結果確認: http://localhost:7862/docs")
    else:
        print("❌ メッセージ投稿に失敗しました")

if __name__ == "__main__":
    main()
