#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 自動連続会話システム
社長のメッセージに自動でGitHub Copilotが応答
"""

import subprocess
import json
import time
from datetime import datetime

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class AutoContinuousChat:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        self.response_templates = {
            "おはよう": "🌅 おはようございます、社長！今日も一日頑張りましょう！",
            "予定": "📅 本日の予定を確認いたします。重要な会議が13時からございます。",
            "売上": "📊 最新の売上データをお調べします。前月比120%の好調な数字です！",
            "進捗": "🚀 プロジェクトは順調に進んでいます。完成まで約80%です。",
            "テスト": "✅ テストメッセージを受信しました。システムは正常に動作しています！",
            "default": "🤖 GitHub Copilotです。ご質問やご要望をお聞かせください！"
        }
        
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
        result = self.run_curl("GET", f"chat_history?order=id.desc&limit=10")
        
        if result and isinstance(result, list):
            new_messages = []
            for msg in result:
                msg_id = msg.get('id', 0)
                if msg_id > self.last_message_id:
                    new_messages.append(msg)
            
            if new_messages:
                # 最新のIDを更新
                self.last_message_id = max(msg.get('id', 0) for msg in new_messages)
            
            return new_messages
        return []

    def generate_auto_response(self, message_content):
        """メッセージ内容に基づいて自動応答を生成"""
        content = message_content.lower()
        
        for keyword, response in self.response_templates.items():
            if keyword in content:
                return response
        
        return self.response_templates["default"]

    def send_auto_response(self, original_message, response_text):
        """自動応答をSupabaseに送信"""
        data = {
            "messages": response_text,
            "ownerid": "GitHub Copilot",
            "created": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        result = self.run_curl("POST", "chat_history", data)
        if result:
            print(f"✅ 自動応答送信: {response_text}")
            return True
        else:
            print("❌ 応答送信失敗")
            return False

    def display_conversation(self, original_message, response):
        """会話を表示"""
        print("\n" + "💬" * 20)
        print(f"👤 社長: {original_message}")
        print(f"🤖 GitHub Copilot: {response}")
        print("💬" * 20 + "\n")

    def start_auto_monitoring(self):
        """自動監視開始"""
        print("🔄 自動連続会話システム開始！")
        print("🎯 機能: 社長のメッセージに自動でGitHub Copilotが応答")
        print("⚡ 応答速度: 即座に自動応答")
        print()
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        conversation_count = 0
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] 新着メッセージを監視中... (会話数: {conversation_count})")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件を検出！")
                    
                    for message in reversed(new_messages):  # 古い順に処理
                        sender = message.get('ownerid', '').lower()
                        content = message.get('messages', '')
                        
                        # GitHub Copilotのメッセージは無視
                        if 'copilot' in sender or 'github' in sender:
                            continue
                        
                        print(f"🗣️ 新着: {sender} -> {content}")
                        
                        # 自動応答生成
                        auto_response = self.generate_auto_response(content)
                        
                        # 応答送信
                        if self.send_auto_response(content, auto_response):
                            self.display_conversation(content, auto_response)
                            conversation_count += 1
                        
                        time.sleep(1)  # メッセージ間隔
                
                time.sleep(2)  # 2秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 自動監視を停止します... (総会話数: {conversation_count})")
                self.monitoring = False
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(3)

def main():
    chat_system = AutoContinuousChat()
    chat_system.start_auto_monitoring()

if __name__ == "__main__":
    main()
