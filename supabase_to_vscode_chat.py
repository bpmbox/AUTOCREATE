#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Supabase → VS Code GitHub Copilot 質問投稿システム
Supabaseの新着メッセージをVS Codeのチャットに自動投稿
"""

import subprocess
import json
import time
from datetime import datetime
import os

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class SupabaseToVSCodeChat:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        self.chat_file_path = "vscode_chat_input.txt"
        
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
    
    def create_chat_prompt(self, message_content, sender):
        """GitHub Copilot用のチャットプロンプトを生成"""
        prompt = f"""
🗣️ 社長からの新着メッセージ:
送信者: {sender}
時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
内容: {message_content}

🤖 GitHub Copilot、上記のメッセージに対して適切な応答をお願いします。
ビジネスコンテキストを考慮して、丁寧で有用な回答をしてください。
"""
        return prompt
    
    def post_to_vscode_chat_terminal(self, prompt):
        """VS Codeターミナルに目立つ形で質問を表示"""
        separator = "🚨" * 60
        
        print(f"\n{separator}")
        print("🤖 【GitHub Copilotへの質問】")
        print(separator)
        print(prompt)
        print(separator)
        print("⌨️ GitHub Copilot、上記の質問にお答えください！")
        print(separator)
        print()
        
        return True
    
    def create_vscode_chat_file(self, prompt):
        """VS Code用のチャットファイルを作成"""
        try:
            with open(self.chat_file_path, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"📁 チャットファイル作成: {self.chat_file_path}")
            return True
        except Exception as e:
            print(f"❌ ファイル作成エラー: {e}")
            return False
    
    def simulate_keyboard_input(self, text):
        """キーボード入力をシミュレート（ターミナル表示）"""
        print("\n" + "⌨️" * 50)
        print("🖱️ 【VS Code操作シミュレーション】")
        print("⌨️" * 50)
        print("🎯 動作: Ctrl+Shift+P でコマンドパレットを開く")
        print("🎯 動作: 'Chat: Open Chat' を検索")
        print("🎯 動作: チャット入力欄をクリック")
        print("⌨️ 入力予定テキスト:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        print("🎯 動作: Enterキーで送信")
        print("⌨️" * 50)
        print("✅ VS Codeチャット投稿完了（シミュレート）")
        print("⌨️" * 50 + "\n")
        
        return True
    
    def send_vscode_command(self, message_content):
        """VS Codeコマンドを試行"""
        try:
            # VS Codeでチャットを開くコマンドを試行
            result = subprocess.run([
                "code", "--command", "workbench.action.chat.open"
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print("✅ VS Codeチャット開始コマンド成功")
                return True
            else:
                print("⚠️ VS Codeコマンド失敗、シミュレーションモードに切り替え")
                return False
        except Exception as e:
            print(f"⚠️ VS Codeコマンドエラー: {e}")
            return False
    
    def process_new_message(self, message):
        """新着メッセージを処理してVS Codeチャットに投稿"""
        sender = message.get('ownerid', 'Unknown')
        content = message.get('messages', '')
        
        # GitHub Copilotのメッセージは無視
        if 'copilot' in sender.lower() or 'github' in sender.lower():
            return False
        
        print(f"📨 新着メッセージ処理: {sender} -> {content}")
        
        # チャットプロンプトを生成
        prompt = self.create_chat_prompt(content, sender)
        
        # VS Codeターミナルに表示
        self.post_to_vscode_chat_terminal(prompt)
        
        # チャットファイルを作成
        self.create_vscode_chat_file(prompt)
        
        # VS Codeコマンドを試行
        vscode_success = self.send_vscode_command(content)
        
        # キーボード入力をシミュレート
        self.simulate_keyboard_input(prompt)
        
        return True
    
    def start_monitoring(self):
        """監視開始"""
        print("🤖 Supabase → VS Code GitHub Copilot 質問投稿システム")
        print("🎯 機能: Supabaseの新着メッセージをVS Codeチャットに自動投稿")
        print("📋 動作:")
        print("  1. Supabaseで新着メッセージ検出")
        print("  2. VS Codeターミナルに目立つ形で表示")
        print("  3. チャットファイル作成")
        print("  4. VS Codeコマンド実行試行")
        print("  5. キーボード操作シミュレート")
        print()
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        processed_count = 0
        
        print("\n🚀 監視開始！")
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] 新着メッセージ監視中... (処理済み: {processed_count}件)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        if self.process_new_message(message):
                            processed_count += 1
                            print(f"✅ メッセージ処理完了 (#{processed_count})")
                        
                        time.sleep(2)  # メッセージ間隔
                
                time.sleep(3)  # 3秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総処理件数: {processed_count}件)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(5)

def main():
    print("🤖 Supabase → VS Code GitHub Copilot 質問投稿システム")
    print("📋 目的: 社長のSupabaseメッセージをVS Codeで自動質問投稿")
    print()
    
    chat_system = SupabaseToVSCodeChat()
    chat_system.start_monitoring()

if __name__ == "__main__":
    main()
