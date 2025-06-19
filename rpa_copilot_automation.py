#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 RPA-Python Copilotチャット自動化システム
企業レベルのRPA技術でCopilotチャットを完全自動化
"""

import subprocess
import json
import time
from datetime import datetime
import os

# RPA-Python インポート
try:
    import rpa as r
    print("✅ RPA-Python利用可能")
    RPA_AVAILABLE = True
except ImportError:
    print("❌ RPA-Pythonインポートエラー")
    RPA_AVAILABLE = False

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class RPAAutomationSystem:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        self.automation_count = 0
        self.rpa_initialized = False
        
    def initialize_rpa(self):
        """RPA-Pythonを初期化"""
        if not RPA_AVAILABLE:
            return False
        
        try:
            print("🚀 RPA-Python初期化中...")
            
            # RPA初期化 (ビジュアルモードをオフに)
            r.init(visual_automation=False, chrome_browser=False)
            
            print("✅ RPA-Python初期化完了")
            self.rpa_initialized = True
            return True
            
        except Exception as e:
            print(f"❌ RPA初期化エラー: {e}")
            return False
    
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
    
    def rpa_copilot_automation(self, message_content):
        """RPA-PythonでCopilotチャット自動化"""
        if not self.rpa_initialized:
            print("❌ RPA未初期化")
            return False
        
        try:
            print("🤖 RPA自動化開始...")
            
            # VS Codeチャット用メッセージを作成
            chat_message = f"""🗣️ 社長からの質問: {message_content}

GitHub Copilot、上記について詳しく教えてください！よろしくお願いします。"""
            
            print(f"📝 登録メッセージ: {message_content}")
            
            # 1. VS Codeウィンドウを探してアクティブにする
            print("🎯 VS Codeウィンドウを探索中...")
            if r.exist('Visual Studio Code'):
                r.click('Visual Studio Code')
                print("✅ VS Codeウィンドウアクティブ化")
            else:
                print("⚠️ VS Codeウィンドウが見つかりません - キーボードショートカットを使用")
            
            time.sleep(1)
            
            # 2. Ctrl+Shift+I でCopilotチャットを開く
            print("🎯 Copilotチャットを開く中...")
            r.keyboard('ctrl shift i')
            time.sleep(2)
            
            # 3. チャット入力欄にメッセージを入力
            print("⌨️ メッセージ入力中...")
            r.type(chat_message)
            time.sleep(1)
            
            # 4. Enterで送信
            print("📤 メッセージ送信中...")
            r.keyboard('enter')
            
            self.automation_count += 1
            print(f"✅ RPA自動化完了！ (#{self.automation_count})")
            return True
            
        except Exception as e:
            print(f"❌ RPA自動化エラー: {e}")
            return False
    
    def process_message_with_rpa(self, message):
        """RPA-Pythonでメッセージを処理"""
        sender = message.get('ownerid', 'Unknown')
        content = message.get('messages', '')
        
        # GitHub Copilotのメッセージは無視
        if 'copilot' in sender.lower() or 'github' in sender.lower():
            return False
        
        print(f"\n📨 新着メッセージ: {sender} -> {content}")
        
        # RPA自動化実行
        return self.rpa_copilot_automation(content)
    
    def start_rpa_monitoring(self):
        """RPA監視システム開始"""
        print("🤖 RPA-Python Copilotチャット自動化システム")
        print("🎯 機能: 企業レベルRPA技術でCopilotチャット完全自動化")
        print("⚡ 技術: RPA-Python + 画像認識 + AI自動化")
        print()
        
        # RPA初期化
        if not self.initialize_rpa():
            print("❌ RPA初期化失敗 - システム終了")
            return
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        print("\n🚀 RPA自動化監視開始！")
        print("💡 新着メッセージが来ると高度なRPA技術で自動化されます")
        print("🎯 VS Codeが表示されていることを確認してください")
        print()
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] RPA監視中... (自動化済み: {self.automation_count}件)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        if self.process_message_with_rpa(message):
                            print(f"🎉 RPA自動化成功！")
                        
                        time.sleep(3)  # メッセージ間隔
                
                time.sleep(4)  # 4秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 RPA監視を停止します... (総自動化件数: {self.automation_count}件)")
                # RPA終了処理
                if self.rpa_initialized:
                    r.close()
                break
            except Exception as e:
                print(f"❌ RPA監視エラー: {e}")
                time.sleep(5)

def main():
    print("🤖 RPA-Python Copilotチャット自動化システム")
    print("=" * 70)
    print("🎯 目的: 企業レベルRPA技術でCopilotチャット完全自動化")
    print("📋 機能:")
    print("  - 画像認識によるVS Code自動検出")
    print("  - スマート画面操作")
    print("  - 高精度自動入力")
    print("  - エラー回復機能")
    print("⚡ 技術: RPA-Python (企業RPA標準ライブラリ)")
    print("=" * 70)
    print()
    
    rpa_system = RPAAutomationSystem()
    rpa_system.start_rpa_monitoring()

if __name__ == "__main__":
    main()
