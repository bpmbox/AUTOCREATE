#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
チャット監視・自動応答システム
Supabaseチャットを監視してAIが自動応答するバックグラウンドサービス
"""

import requests
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Supabase設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

# Gradio API設定（メインシステム）
GRADIO_API_URL = "http://localhost:7860"

class ChatMonitor:
    def __init__(self):
        self.last_check_time = datetime.now()
        self.running = False
        self.response_delay = 3  # 3秒後に応答
        
    def get_new_messages(self) -> List[Dict]:
        """新しいメッセージを取得"""
        url = f"{SUPABASE_URL}/rest/v1/chat_history"
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
        }
        
        # 最後のチェック時刻以降のメッセージを取得
        params = {
            'created': f'gte.{self.last_check_time.isoformat()}',
            'order': 'created.desc',
            'limit': 10
        }
        
        try:
            print(f"🔍 Supabaseチェック中... ({self.last_check_time.strftime('%H:%M:%S')})")
            response = requests.get(url, headers=headers, params=params)
            print(f"📡 Supabaseレスポンス: {response.status_code}")
            
            if response.status_code == 200:
                messages = response.json()
                print(f"📊 取得メッセージ数: {len(messages)}")
                
                # デバッグ: 各メッセージの詳細を表示
                for i, msg in enumerate(messages):
                    owner = msg.get('ownerid', 'unknown')
                    content = msg.get('messages', '')[:30] + '...'
                    print(f"  {i+1}. [{owner}]: {content}")
                
                # AI自身のメッセージは除外
                user_messages = [msg for msg in messages if msg.get('ownerid') != 'ai-assistant']
                print(f"👥 ユーザーメッセージ: {len(user_messages)}")
                
                return user_messages
            else:
                print(f"❌ メッセージ取得失敗: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"❌ エラー: {e}")
            return []
    
    def post_ai_response(self, original_message: str, ai_response: str):
        """AIの応答をSupabaseに投稿"""
        url = f"{SUPABASE_URL}/rest/v1/chat_history"
        
        headers = {
            'apikey': SUPABASE_KEY,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
            'Authorization': f'Bearer {SUPABASE_KEY}',
        }
        
        data = {
            'messages': ai_response,
            'ownerid': 'ai-assistant',
            'created': datetime.now().isoformat(),
            'isread': False,
            'targetid': 'global-chat',
            'status': 'sent',
            'status_created': datetime.now().isoformat(),
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                print(f"✅ AI応答投稿完了: {ai_response[:50]}...")
            else:
                print(f"❌ AI応答投稿失敗: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ AI応答エラー: {e}")
    
    def generate_ai_response(self, message: str) -> str:
        """AIの応答を生成"""
        # メッセージの内容に応じて適切な応答を生成
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['こんにちは', 'hello', 'hi', 'おはよう']):
            return f"🤖 AI社長です！こんにちは！\n\n今日も AUTOCREATE の開発頑張りましょう！\n現在のメインシステム: http://localhost:7860 で稼働中です 💪"
        
        elif any(word in message_lower for word in ['状況', 'ステータス', 'status', '進捗']):
            return f"📊 **現在の開発状況**\n\n✅ メインシステム: 稼働中 (http://localhost:7860)\n✅ チャットシステム: 稼働中 (http://localhost:8080)\n✅ AI監視システム: 稼働中\n\n🎯 次のタスク: programfromdoc.py の完全統合とUI最適化"
        
        elif any(word in message_lower for word in ['help', 'ヘルプ', '助けて', '困った']):
            return f"🆘 **AUTOCREATE AI社長のヘルプデスク**\n\n利用可能なコマンド:\n• 'ステータス' → 開発状況確認\n• 'ドキュメント' → システム説明\n• 'タスク' → TODO確認\n\n💡 何か具体的な質問があれば、お気軽にどうぞ！"
        
        elif any(word in message_lower for word in ['ドキュメント', 'document', '説明']):
            return f"📚 **AUTOCREATE システムドキュメント**\n\n🎯 メインシステム (Gradio): 複数のAIインターフェースを統合\n💬 チャットシステム (React): リアルタイム会話・記録\n🤖 AI監視システム: 自動応答・記憶復元\n\n詳細: https://supabase-message-stream.lovable.app/"
        
        elif any(word in message_lower for word in ['タスク', 'todo', 'やること']):
            return f"📝 **現在のタスクリスト**\n\n1. ✅ programfromdoc.py の Gradio 統合完了\n2. 🔄 全タブの動作確認・UI最適化\n3. 🔄 チャット自動応答システムの安定化\n4. ⏳ Jupyter Notebook データ可視化機能\n5. ⏳ YouTube Live連携の実装\n\n🎯 優先度: メインシステム100%完成"
        
        else:
            # 一般的な応答
            return f"🤔 AI社長が考え中...\n\n「{message[:50]}...」について検討します。\n\nもう少し具体的な質問や、'ヘルプ'と入力していただければ、より適切な回答ができます！\n\n現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def monitor_loop(self):
        """メインの監視ループ"""
        print("🔍 チャット監視システム開始...")
        
        while self.running:
            try:
                # 新しいメッセージをチェック
                new_messages = self.get_new_messages()
                
                for message in new_messages:
                    message_text = message.get('messages', '')
                    message_time = message.get('created', '')
                    sender = message.get('ownerid', 'unknown')
                    
                    print(f"📩 新着メッセージ ({sender}): {message_text[:50]}...")
                    
                    # AI応答を生成（少し遅延を入れて自然に）
                    time.sleep(self.response_delay)
                    ai_response = self.generate_ai_response(message_text)
                    
                    # 応答を投稿
                    self.post_ai_response(message_text, ai_response)
                
                # 最後のチェック時刻を更新
                if new_messages:
                    self.last_check_time = datetime.now()
                
                # 5秒待機してから次のチェック
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 監視システム停止中...")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(10)  # エラー時は10秒待機
    
    def start_monitoring(self):
        """監視を開始"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("🚀 バックグラウンド監視システム起動完了！")
    
    def stop_monitoring(self):
        """監視を停止"""
        self.running = False
        print("🛑 監視システム停止")

def main():
    """メイン関数"""
    monitor = ChatMonitor()
    
    try:
        # 開始メッセージを投稿
        monitor.post_ai_response("", 
            "🤖 **AI社長 監視システム起動！**\n\n" +
            "チャットを常時監視して自動応答します。\n" +
            "何か話しかけてみてください！\n\n" +
            f"起動時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        # 監視開始
        monitor.start_monitoring()
        
        print("🎯 監視システム稼働中... (Ctrl+C で停止)")
        print("💬 チャット: http://localhost:8080")
        print("🎯 メイン: http://localhost:7860")
        
        # メインスレッドをブロック
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 システム終了中...")
        monitor.stop_monitoring()
        
        # 終了メッセージを投稿
        monitor.post_ai_response("", 
            "😴 **AI社長 監視システム終了**\n\n" +
            "お疲れさまでした！\n" +
            f"終了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

if __name__ == "__main__":
    main()
