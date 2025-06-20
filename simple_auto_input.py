#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Selenium Webブラウザ自動操作システム
ブラウザのチャット入力欄に自動でメッセージを入力
"""

import time
import subprocess
import json
from datetime import datetime

# Seleniumのインストール確認
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    print("✅ Selenium利用可能")
except ImportError:
    print("❌ Seleniumがインストールされていません")
    print("📦 簡易版システムを使用します")

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class SimpleAutoInput:
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
        result = self.run_curl("GET", f"chat_history?order=id.desc&limit=5")
        
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
    
    def generate_response(self, message_content):
        """メッセージに対する応答を生成"""
        content = message_content.lower()
        
        responses = {
            "おはよう": "🌅 おはようございます！今日も良い一日にしましょう！",
            "こんにちは": "👋 こんにちは！お疲れ様です！",
            "進捗": "📈 プロジェクトは順調に進んでいます！",
            "売上": "💰 売上は好調です！詳細をお調べします。",
            "会議": "📅 会議の準備は完了しています！",
            "テスト": "🧪 テストメッセージ受信！システム正常動作中！",
            "今日": "📅 今日のスケジュールを確認いたします！",
            "予定": "📋 予定表をチェックして回答いたします！"
        }
        
        for keyword, response in responses.items():
            if keyword in content:
                return response
        
        return f"🤖 「{message_content}」について承知いたしました！GitHub Copilotが対応中です。"
    
    def simulate_auto_input(self, response_text):
        """自動入力をシミュレート（ターミナル表示）"""
        print("\n" + "⌨️" * 40)
        print("🖥️ 【自動入力シミュレーション】")
        print("⌨️" * 40)
        print("🎯 動作: ブラウザの入力欄をクリック")
        print("⌨️ 入力: ", end="")
        
        # 文字を一文字ずつ表示してタイピング効果
        for char in response_text:
            print(char, end="", flush=True)
            time.sleep(0.05)  # タイピング速度
        
        print("\n🎯 動作: Enterキーで送信")
        print("⌨️" * 40)
        print("✅ 自動入力完了！")
        print("⌨️" * 40 + "\n")
        
        return True
    
    def open_browser_instructions(self):
        """ブラウザ操作の指示を表示"""
        print("\n📋 ブラウザ操作指示:")
        print("=" * 50)
        print("1. 🌐 ブラウザでチャットページを開いてください")
        print("2. 📱 チャット画面を表示してください")
        print("3. ⌨️ このシステムが入力欄に自動で応答を入力します")
        print("4. 🛑 停止はCtrl+Cで行ってください")
        print("=" * 50 + "\n")
    
    def start_simple_monitoring(self):
        """簡易監視システム開始"""
        print("🖥️ 簡易版 ブラウザ自動入力システム")
        print("🎯 機能: 新着メッセージ検出 → 自動応答をシミュレート")
        
        self.open_browser_instructions()
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        input_count = 0
        
        print("\n🚀 監視開始！")
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] 新着メッセージ監視中... (自動入力: {input_count}回)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        sender = message.get('ownerid', '').lower()
                        content = message.get('messages', '')
                        
                        # GitHub Copilotのメッセージは無視
                        if 'copilot' in sender or 'github' in sender:
                            continue
                        
                        print(f"\n🗣️ 新着メッセージ: {sender} -> {content}")
                        
                        # 応答生成
                        response = self.generate_response(content)
                        print(f"🤖 生成された応答: {response}")
                        
                        # 自動入力シミュレーション
                        if self.simulate_auto_input(response):
                            input_count += 1
                            print(f"✅ 自動入力シミュレーション成功 (#{input_count})")
                        
                        time.sleep(2)  # メッセージ間隔
                
                time.sleep(3)  # 3秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総自動入力: {input_count}回)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(5)

def main():
    print("🖥️ ブラウザ自動入力システム")
    print("📋 動作モード: 簡易版（入力シミュレーション）")
    print()
    
    auto_input = SimpleAutoInput()
    auto_input.start_simple_monitoring()

if __name__ == "__main__":
    main()
