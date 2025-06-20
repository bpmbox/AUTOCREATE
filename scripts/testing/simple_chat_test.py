#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 このチャット欄直接登録テスト
シンプルにSupabaseメッセージをここに表示するだけ
"""

import subprocess
import json
import time
from datetime import datetime

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class SimpleDirectChatTest:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        
    def run_curl(self, method, endpoint, data=None):
        """curlでSupabase APIを呼び出し"""
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        
        cmd = [
            "curl", "-s", "-X", method, url,
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            "-H", f"apikey: {SUPABASE_ANON_KEY}"
        ]
        
        if data:
            cmd.extend(["-d", json.dumps(data)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0 and result.stdout:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return None
            return None
        except Exception as e:
            print(f"❌ API呼び出しエラー: {e}")
            return None
    
    def get_new_messages(self):
        """新着メッセージを取得"""
        result = self.run_curl("GET", f"chat_history?order=id.desc&limit=3")
        
        if result and isinstance(result, list):
            new_messages = []
            for msg in result:
                msg_id = msg.get('id', 0)
                if msg_id > self.last_message_id:
                    new_messages.append(msg)
            
            if new_messages:
                self.last_message_id = max(msg.get('id', 0) for msg in new_messages)
            
            return new_messages
        return []
    
    def display_simple_chat_message(self, message):
        """シンプルにチャットメッセージを表示"""
        sender = message.get('ownerid', 'Unknown')
        content = message.get('messages', '')
        created = message.get('created', '')
        
        # GitHub Copilotのメッセージは無視
        if 'copilot' in sender.lower() or 'github' in sender.lower():
            return False
        
        print("\n" + "=" * 80)
        print("📱 チャット欄登録テスト - 新着メッセージ")
        print("=" * 80)
        print(f"👤 送信者: {sender}")
        print(f"🕐 時刻: {created}")
        print(f"💬 メッセージ:")
        print(f"   {content}")
        print("=" * 80)
        print("🤖 GitHub Copilot、上記のメッセージにお答えください！")
        print("=" * 80)
        print()
        
        return True
    
    def start_simple_monitoring(self):
        """シンプル監視開始"""
        print("🎯 このチャット欄直接登録テスト")
        print("📝 機能: Supabaseの新着メッセージをシンプル表示")
        print("🎯 目標: GitHub Copilotがここで直接応答")
        print()
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        displayed_count = 0
        
        print("\n🚀 シンプル監視開始！")
        print("💡 新着メッセージが来るとここに表示されます")
        print()
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] 新着監視中... (表示済み: {displayed_count}件)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        if self.display_simple_chat_message(message):
                            displayed_count += 1
                            print(f"✅ メッセージ表示完了 (#{displayed_count})")
                        
                        time.sleep(1)  # メッセージ間隔
                
                time.sleep(3)  # 3秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総表示件数: {displayed_count}件)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(3)

def main():
    print("🎯 このチャット欄直接登録テスト")
    print("📋 目的: Supabaseメッセージを直接ここに表示")
    print("🤖 GitHub Copilotがリアルタイムで応答可能")
    print()
    
    chat_test = SimpleDirectChatTest()
    chat_test.start_simple_monitoring()

if __name__ == "__main__":
    main()
