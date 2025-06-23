#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テストメッセージ送信用スクリプト
"""

import requests
import json
import time
from datetime import datetime

# Supabase設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

def send_test_message():
    """テストメッセージを送信"""
    
    # 連続テスト用メッセージリスト
    test_messages = [
        "🧪 テスト1: AIは連続で応答できますか？",
        "🔥 テスト2: プログラミングの質問です",
        "💡 テスト3: システム設計について教えて",
        "⚡ テスト4: 最新技術トレンドは？",
        "🎯 テスト5: 最終テストです！"
    ]
    
    for i, message in enumerate(test_messages, 1):
        message_data = {
            "messages": message,
            "ownerid": f"test-user-{i}",
            "created": datetime.now().isoformat()
        }
        
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            print(f"📤 テストメッセージ{i}送信中...")
            print(f"内容: {message}")
            
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/chat_history",
                headers=headers,
                json=message_data
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ テストメッセージ{i}送信成功！")
                # 少し待機してから次のメッセージ
                time.sleep(2)
            else:
                print(f"❌ 送信失敗: {response.status_code}")
                print(f"エラー: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 送信エラー: {e}")
            return False
    
    print("🎉 全テストメッセージ送信完了！AIの連続応答を確認してください！")
    return True

if __name__ == "__main__":
    send_test_message()
