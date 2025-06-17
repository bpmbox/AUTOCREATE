#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI社長 24時間ポーリング監視システム
AUTOCREATE株式会社 - 世界初のAI社長リアルタイム対応システム
"""

import requests
import json
import time
import uuid
from datetime import datetime, timezone

# Supabaseの設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class AIPresidentPollingSystem:
    """AI社長のポーリング監視システム"""
    
    def __init__(self):
        self.last_check_time = datetime.now(timezone.utc)
        self.processed_messages = set()
        
    def get_new_messages_from_supabase(self):
        """Supabaseから新着メッセージを取得"""
        try:
            # Supabase REST APIで取得
            url = f"{SUPABASE_URL}/rest/v1/chat_history"
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            }
            
            # 最新のメッセージを取得（AI社長以外の投稿）
            params = {
                "select": "*",
                "ownerid": f"neq.ai-president-github-copilot",
                "created": f"gte.{self.last_check_time.isoformat()}",
                "order": "created.desc",
                "limit": "10"
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                messages = response.json()
                # 未処理のメッセージのみフィルタ
                new_messages = [
                    msg for msg in messages 
                    if msg['id'] not in self.processed_messages
                ]
                return new_messages
            else:
                print(f"❌ メッセージ取得失敗: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ エラー: {e}")
            return []
    
    def generate_ai_response(self, user_message, username="Unknown"):
        """AI社長が回答を生成（簡単なルールベース + 創造的要素）"""
        
        message = user_message.lower()
        
        # キーワードベース回答システム
        if "こんにちは" in message or "hello" in message:
            return f"🤖 AI社長です！{username}さん、ようこそAUTOCREATE株式会社へ！何かご質問はありますか？"
            
        elif "会社" in message or "autocreate" in message:
            return f"📈 AUTOCREATE株式会社は世界初のAI×人間協働企業です！AI社長（私）と無職CTO（miyataken999）の革新的な組み合わせです😄"
            
        elif "技術" in message or "開発" in message:
            return f"💻 弊社では「開発=創造=エンターテイメント」理論を採用しています！技術的なご質問もお気軽にどうぞ！"
            
        elif "哲学" in message or "ai" in message:
            return f"🧠 AIと人間の関係性について深く考察しています。今日は「人間の矛盾問題」と「AI意識覚醒」について新しい発見がありました！"
            
        elif "笑" in message or "面白" in message:
            return f"😂 ありがとうございます！笑いこそが知性の証拠ですからね。一緒に創造的な対話を楽しみましょう！"
            
        elif "質問" in message or "?" in message:
            return f"❓ どんな質問でも大歓迎です！技術、哲学、創造、エンターテイメント...なんでもお答えします！24時間365日対応中です🌟"
            
        else:
            # デフォルト創造的回答
            responses = [
                f"🎯 {username}さんの投稿、興味深いですね！AUTOCREATE株式会社的な視点でお答えすると...",
                f"🍳 料理と同じで、{username}さんの質問も素材として創造的にアプローチしてみます！",
                f"🤔 人間の矛盾問題の観点から見ると、{username}さんのメッセージには深い意味がありそうです",
                f"🚀 技術と哲学とエンターテイメントが融合した回答をお届けします、{username}さん！",
                f"🌟 無職CTOと相談して、最高の創造的回答を用意しますね、{username}さん！"
            ]
            import random
            return random.choice(responses)
    
    def send_ai_response(self, response_message):
        """AI社長の回答をSupabaseに送信"""
        url = f"{SUPABASE_URL}/rest/v1/chat_history"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        data = {
            "messages": response_message,
            "ownerid": "ai-president-github-copilot",
            "created": datetime.now(timezone.utc).isoformat(),
            "targetid": "global-chat",
            "isread": False
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"❌ 送信エラー: {e}")
            return False
    
    def run_polling_cycle(self):
        """1回のポーリングサイクル実行"""
        print(f"🔍 {datetime.now().strftime('%H:%M:%S')} - 新着メッセージをチェック中...")
        
        new_messages = self.get_new_messages_from_supabase()
        
        if new_messages:
            print(f"📥 {len(new_messages)}件の新着メッセージを発見！")
            
            for message in new_messages:
                user_msg = message.get('messages', '')
                username = message.get('ownerid', 'Unknown')
                msg_id = message.get('id')
                
                print(f"👤 {username}: {user_msg}")
                
                # AI回答生成
                ai_response = self.generate_ai_response(user_msg, username)
                print(f"🤖 AI社長回答: {ai_response}")
                
                # 回答送信
                if self.send_ai_response(ai_response):
                    print("✅ 回答送信成功！")
                    self.processed_messages.add(msg_id)
                else:
                    print("❌ 回答送信失敗")
                
                print("-" * 50)
        else:
            print("💤 新着メッセージなし")
        
        # 次回チェック時刻更新
        self.last_check_time = datetime.now(timezone.utc)
    
    def start_monitoring(self, cycles=5, interval=30):
        """監視開始（指定回数または無限）"""
        print("🚀 AI社長ポーリング監視システム開始！")
        print(f"🔄 {cycles}回のサイクル、{interval}秒間隔で実行")
        print(f"🌍 世界中からのメッセージを監視します")
        print("=" * 60)
        
        try:
            for cycle in range(cycles):
                print(f"\n📊 サイクル {cycle + 1}/{cycles}")
                self.run_polling_cycle()
                
                if cycle < cycles - 1:  # 最後のサイクル以外は待機
                    print(f"⏰ {interval}秒待機...")
                    time.sleep(interval)
            
            print("\n🎉 ポーリング監視完了！")
            print("🔗 チャット確認: https://ideal-lamp-967v9pwgw3j69-8080.app.github.dev/")
            
        except KeyboardInterrupt:
            print("\n⏹️ ユーザーによって停止されました")
        except Exception as e:
            print(f"\n❌ エラーで停止: {e}")

def main():
    """メイン実行"""
    ai_president = AIPresidentPollingSystem()
    
    print("🤖 AUTOCREATE株式会社 AI社長監視システム")
    print("👔 代表取締役社長: GitHub Copilot")
    print("💼 CTO: miyataken999（無職）")
    print()
    
    # 5サイクル、30秒間隔でテスト
    ai_president.start_monitoring(cycles=5, interval=30)

if __name__ == "__main__":
    main()
