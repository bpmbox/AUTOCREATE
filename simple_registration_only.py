#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 シンプル登録専用システム
チャットは動かさず、登録だけに特化
"""

import subprocess
import json
import time
from datetime import datetime
import os

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class SimpleRegistrationSystem:
    def __init__(self):
        self.registration_count = 0
        self.registered_users = []
        
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
    
    def register_user(self, username):
        """ユーザー登録"""
        if username in self.registered_users:
            print(f"⚠️ {username} は既に登録済みです")
            return False
        
        # 登録データを作成
        registration_data = {
            "messages": f"🎯 ユーザー登録: {username} がシステムに登録しました",
            "ownerid": "システム",
            "created": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Supabaseに登録
        result = self.run_curl("POST", "chat_history", registration_data)
        
        if result:
            self.registered_users.append(username)
            self.registration_count += 1
            print(f"✅ {username} の登録完了！ (#{self.registration_count})")
            return True
        else:
            print(f"❌ {username} の登録失敗")
            return False
    
    def show_registration_status(self):
        """登録状況を表示"""
        print("\n" + "📝" * 40)
        print("📋 登録状況")
        print("📝" * 40)
        print(f"👥 登録済みユーザー数: {self.registration_count}")
        
        if self.registered_users:
            print("📝 登録済みユーザー:")
            for i, user in enumerate(self.registered_users, 1):
                print(f"   {i}. {user}")
        else:
            print("📝 まだ登録ユーザーはいません")
        
        print("📝" * 40 + "\n")
    
    def start_chat_system(self):
        """チャットシステムを起動"""
        print("\n🚀 チャットシステム起動中...")
        print("🎯 登録が完了したので、チャットシステムに移行します")
        
        try:
            # simple_chat_test.pyを起動
            subprocess.Popen([
                "python", "simple_chat_test.py"
            ])
            print("✅ チャットシステム起動完了！")
            return True
        except Exception as e:
            print(f"❌ チャットシステム起動エラー: {e}")
            return False
    
    def interactive_registration(self):
        """インタラクティブ登録"""
        print("📝 シンプル登録専用システム")
        print("🎯 目的: ユーザー登録のみ（チャット機能なし）")
        print("💡 登録完了後にチャットシステムへ移行")
        print()
        
        while True:
            print("\n📋 コマンド:")
            print("1. 'r [ユーザー名]' - ユーザー登録")
            print("2. 's' - 登録状況表示")
            print("3. 'c' - チャットシステム起動")
            print("4. 'q' - 終了")
            
            try:
                command = input("\n>>> ").strip()
                
                if command.lower() == 'q':
                    print("🛑 システム終了")
                    break
                    
                elif command.lower() == 's':
                    self.show_registration_status()
                    
                elif command.lower() == 'c':
                    if self.registration_count > 0:
                        self.start_chat_system()
                        print("🎯 チャットシステムに移行しました")
                        break
                    else:
                        print("⚠️ まずユーザー登録を行ってください")
                        
                elif command.lower().startswith('r '):
                    username = command[2:].strip()
                    if username:
                        success = self.register_user(username)
                        if success:
                            print(f"🎉 {username} さん、登録ありがとうございます！")
                            self.show_registration_status()
                            
                            # 3人登録されたら自動でチャットシステムへ
                            if self.registration_count >= 3:
                                print("\n🎯 3人の登録が完了しました！")
                                print("🚀 自動的にチャットシステムに移行します...")
                                time.sleep(2)
                                self.start_chat_system()
                                break
                    else:
                        print("❌ ユーザー名を入力してください")
                        
                else:
                    print("❓ 不明なコマンド")
                    
            except KeyboardInterrupt:
                print("\n🛑 システム終了")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")

def main():
    print("📝 シンプル登録専用システム")
    print("=" * 50)
    print("🎯 機能:")
    print("  - ユーザー登録のみ")
    print("  - チャット機能なし")  
    print("  - 登録完了後にチャットシステム起動")
    print("=" * 50)
    print()
    
    registration_system = SimpleRegistrationSystem()
    registration_system.interactive_registration()

if __name__ == "__main__":
    main()
