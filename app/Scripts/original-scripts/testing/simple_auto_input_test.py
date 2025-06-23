#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 シンプル自動入力テスト
pyautogui不要版 - WindowsAPI直接操作
"""

import subprocess
import json
import time
from datetime import datetime
import ctypes
from ctypes import wintypes

# Windows API定数
VK_RETURN = 0x0D
VK_CONTROL = 0x11
VK_SHIFT = 0x10
VK_V = 0x56
VK_I = 0x49

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class SimpleAutoInputTest:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        
        # Windows API関数を取得
        try:
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
            print("✅ Windows API利用可能")
        except:
            print("❌ Windows API利用不可")
            self.user32 = None
        
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
        result = self.run_curl("GET", f"chat_history?order=id.desc&limit=2")
        
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
    
    def copy_to_clipboard_simple(self, text):
        """シンプルなクリップボードコピー"""
        try:
            # 絵文字を除去してシンプルなテキストに
            simple_text = text.encode('ascii', 'ignore').decode('ascii')
            if not simple_text.strip():
                simple_text = "新着メッセージあり"
            
            # echoとclipを使用
            cmd = f'echo {simple_text} | clip'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ クリップボードエラー: {e}")
            return False
    
    def send_simple_keys(self):
        """シンプルなキー送信"""
        if not self.user32:
            return False
        
        try:
            print("⌨️ キー送信開始...")
            time.sleep(1)
            
            # Ctrl+Shift+I (Copilot Chat開く)
            self.user32.keybd_event(VK_CONTROL, 0, 0, 0)  # Ctrl押す
            self.user32.keybd_event(VK_SHIFT, 0, 0, 0)    # Shift押す
            self.user32.keybd_event(VK_I, 0, 0, 0)        # I押す
            time.sleep(0.1)
            self.user32.keybd_event(VK_I, 0, 2, 0)        # I離す
            self.user32.keybd_event(VK_SHIFT, 0, 2, 0)    # Shift離す
            self.user32.keybd_event(VK_CONTROL, 0, 2, 0)  # Ctrl離す
            
            time.sleep(2)  # チャット開くまで待機
            
            # Ctrl+V (貼り付け)
            self.user32.keybd_event(VK_CONTROL, 0, 0, 0)  # Ctrl押す
            self.user32.keybd_event(VK_V, 0, 0, 0)        # V押す
            time.sleep(0.1)
            self.user32.keybd_event(VK_V, 0, 2, 0)        # V離す
            self.user32.keybd_event(VK_CONTROL, 0, 2, 0)  # Ctrl離す
            
            time.sleep(1)
            
            # Enter (送信)
            self.user32.keybd_event(VK_RETURN, 0, 0, 0)   # Enter押す
            time.sleep(0.1)
            self.user32.keybd_event(VK_RETURN, 0, 2, 0)   # Enter離す
            
            print("✅ キー送信完了")
            return True
            
        except Exception as e:
            print(f"❌ キー送信エラー: {e}")
            return False
    
    def create_simple_message(self, original_message, sender):
        """シンプルなメッセージを作成"""
        return f"社長からの質問: {original_message}"
    
    def process_simple_message(self, message):
        """シンプルなメッセージ処理"""
        sender = message.get('ownerid', 'Unknown')
        content = message.get('messages', '')
        
        # GitHub Copilotのメッセージは無視
        if 'copilot' in sender.lower() or 'github' in sender.lower():
            return False
        
        print(f"\n📨 新着: {sender} -> {content}")
        
        # シンプルなメッセージを作成
        simple_message = self.create_simple_message(content, sender)
        
        print("\n" + "🎯" * 50)
        print("自動入力テスト開始")
        print("🎯" * 50)
        print(f"📝 入力予定: {simple_message}")
        
        # クリップボードにコピー
        if self.copy_to_clipboard_simple(simple_message):
            print("✅ クリップボードコピー成功")
            
            # 5秒待機（手動でVS Codeをクリックする時間）
            print("⏰ 5秒後に自動入力開始...")
            print("💡 今すぐVS Codeをクリックしてアクティブにしてください！")
            for i in range(5, 0, -1):
                print(f"⏰ {i}秒...")
                time.sleep(1)
            
            # キー送信
            if self.send_simple_keys():
                print("✅ 自動入力完了")
            else:
                print("❌ 自動入力失敗")
        else:
            print("❌ クリップボードコピー失敗")
        
        print("🎯" * 50)
        print()
        
        return True
    
    def start_simple_test(self):
        """シンプルテスト開始"""
        print("🎯 シンプル自動入力テスト")
        print("📝 機能: Supabaseメッセージ → VS Codeチャットに自動入力")
        print("⚡ 使用技術: Windows API直接操作")
        print()
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        processed_count = 0
        
        print("\n🚀 シンプル監視開始！")
        print("💡 新着メッセージが来ると自動でVS Codeチャットに入力されます")
        print()
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] 監視中... (処理済み: {processed_count}件)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        if self.process_simple_message(message):
                            processed_count += 1
                            print(f"✅ 処理完了 (#{processed_count})")
                        
                        time.sleep(3)  # メッセージ間隔
                
                time.sleep(4)  # 4秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総処理件数: {processed_count}件)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(3)

def main():
    print("🎯 シンプル自動入力テスト")
    print("📋 目的: VS Codeチャットに直接自動入力")
    print("⚡ pyautogui不要 - Windows API使用")
    print()
    
    test_system = SimpleAutoInputTest()
    test_system.start_simple_test()

if __name__ == "__main__":
    main()
