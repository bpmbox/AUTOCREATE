#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Copilot監視対応版 - 出力を詳しく表示してCopilotが監視できるようにする
"""

import subprocess
import json
import time
from datetime import datetime, timedelta

# Supabase設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class CopilotMonitorableAI:
    def __init__(self):
        self.processed_message_ids = set()
        self.startup_time = datetime.now()
        self.loop_count = 0
        
    def curl_request(self, method, endpoint, data=None):
        """curlを使ってSupabaseにリクエスト送信"""
        cmd = [
            'curl', '-X', method,
            f'{SUPABASE_URL}/rest/v1/{endpoint}',
            '-H', f'apikey: {SUPABASE_KEY}',
            '-H', f'Authorization: Bearer {SUPABASE_KEY}',
            '-H', 'Content-Type: application/json',
            '--max-time', '10',
            '--silent'
        ]
        
        if data:
            cmd.extend(['-d', json.dumps(data)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
            elif result.returncode == 0:
                return {}
            else:
                print(f"❌ curl エラー (code {result.returncode}): {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ curl実行エラー: {e}")
            return None

    def get_new_user_messages(self):
        """新しいユーザーメッセージを取得"""
        self.loop_count += 1
        current_time = datetime.now().strftime('%H:%M:%S')
        
        print(f"\n{'='*60}")
        print(f"🔍 ループ {self.loop_count} - Supabaseポーリング中... ({current_time})")
        print(f"   起動時刻: {self.startup_time.strftime('%H:%M:%S')}")
        print(f"   処理済み: {len(self.processed_message_ids)}件")
        
        # 起動時刻以降のメッセージを取得
        startup_iso = self.startup_time.isoformat()
        endpoint = f'chat_history?created=gte.{startup_iso}&order=created.desc&limit=10'
        
        messages = self.curl_request('GET', endpoint)
        
        if messages is not None:
            print(f"📋 取得したメッセージ総数: {len(messages)}件")
            
            # ユーザーメッセージのみ（AI・システムメッセージ除外）
            user_messages = [
                msg for msg in messages 
                if msg.get('username') not in ['ai-assistant', 'system', 'AI社長', 'test-system']
                and msg.get('id') not in self.processed_message_ids
            ]
            
            print(f"📝 新規ユーザーメッセージ: {len(user_messages)}件")
            
            # 詳細表示
            if user_messages:
                print("🔍 新規メッセージ詳細:")
                for i, msg in enumerate(user_messages, 1):
                    msg_id = msg.get('id')
                    username = msg.get('username', 'unknown')
                    content = msg.get('message', '')
                    timestamp = msg.get('created', '')
                    
                    print(f"   {i}. ID:{msg_id} [{username}] at {timestamp[:19]}")
                    print(f"      内容: {content[:100]}...")
                    
                    # ★★★ GitHub Copilotが監視できるように質問内容を明確に出力 ★★★
                    print(f"\n   🤖 COPILOT_MONITOR: 新着質問検出")
                    print(f"   📩 質問者: {username}")
                    print(f"   📝 質問内容: {content}")
                    print(f"   🕐 受信時刻: {timestamp}")
                    print(f"   💭 この質問に対する回答を生成します...")
            
            return user_messages
        else:
            print("❌ メッセージ取得失敗")
            return []

    def generate_intelligent_response(self, user_message, sender, timestamp):
        """質問内容を解析して知的応答を生成"""
        print(f"\n🧠 AI回答生成開始...")
        print(f"   質問解析中: {user_message[:50]}...")
        
        current_time = datetime.now().strftime("%H:%M")
        msg_lower = user_message.lower()
        
        # 技術的な質問を詳細に解析
        if any(keyword in msg_lower for keyword in ['python', 'プログラミング', 'コード', 'エラー']):
            response = f"{sender}さん、Pythonについてのご質問ですね！具体的なエラーメッセージや実装したい機能を教えてください。効率的な解決方法をお教えします。({current_time})"
            print(f"   🐍 Python関連の質問と判定")
        elif any(keyword in msg_lower for keyword in ['javascript', 'js', '非同期']):
            response = f"{sender}さん、JavaScriptについてのご質問ですね！非同期処理、Promise、async/awaitなど、どの部分でお困りですか？具体的にサポートします。({current_time})"
            print(f"   🟨 JavaScript関連の質問と判定")
        elif any(keyword in msg_lower for keyword in ['データベース', 'sql', 'database']):
            response = f"{sender}さん、データベースについてのご相談ですね！スキーマ設計、クエリ最適化、パフォーマンス改善など、どの観点からお手伝いしましょうか？({current_time})"
            print(f"   🗄️ データベース関連の質問と判定")
        elif any(keyword in msg_lower for keyword in ['？', '?', '教えて', 'どう']):
            response = f"{sender}さんのご質問「{user_message[:30]}...」について、詳しくお答えします。より具体的な内容を教えていただければ、最適な解決策をご提案できます。({current_time})"
            print(f"   ❓ 一般的な質問と判定")
        else:
            response = f"{sender}さん、「{user_message[:40]}...」についてのご相談ですね！どのような観点からサポートが必要でしょうか？技術的な実装、設計方針、ベストプラクティスなど、お気軽にお聞かせください。({current_time})"
            print(f"   💬 一般的なメッセージと判定")
        
        print(f"   ✅ 回答生成完了: {len(response)}文字")
        return response

    def post_ai_response(self, response_text):
        """AI応答をSupabaseに投稿"""
        print(f"\n📤 AI応答をSupabaseに投稿中...")
        print(f"   回答内容: {response_text[:100]}...")
        
        data = {
            'message': response_text,
            'username': 'AI社長',
            'created': datetime.now().isoformat(),
            'targetid': 'global-chat',
        }
        
        result = self.curl_request('POST', 'chat_history', data)
        
        if result is not None:
            print("   ✅ AI応答投稿成功！")
            return True
        else:
            print("   ❌ AI応答投稿失敗")
            return False
    
    def run_monitoring(self):
        """メイン監視ループ - GitHub Copilotが監視可能な詳細出力付き"""
        print("🚀 GitHub Copilot監視対応版 AI社長システム開始！")
        print("💬 詳細ログでCopilotが監視可能な形式で出力中...")
        print("🔗 チャット: http://localhost:8080")
        print("🔧 GitHub Copilotによるリアルタイム監視対応")
        
        while True:
            try:
                # 新しいユーザーメッセージをチェック
                new_messages = self.get_new_user_messages()
                
                for msg in new_messages:
                    message_id = msg.get('id')
                    user_message = msg.get('message', '')
                    sender = msg.get('username', 'unknown')
                    timestamp = msg.get('created', '')
                    
                    print(f"\n📩 ★★★ 新着質問処理開始 ★★★")
                    print(f"   メッセージID: {message_id}")
                    print(f"   送信者: {sender}")
                    print(f"   時刻: {timestamp[:19]}")
                    print(f"   質問全文: {user_message}")
                    
                    # 知的な応答を生成
                    ai_response = self.generate_intelligent_response(user_message, sender, timestamp)
                    
                    # 応答を投稿
                    if self.post_ai_response(ai_response):
                        # 処理済みとしてマーク
                        self.processed_message_ids.add(message_id)
                        print(f"   ✅ メッセージID {message_id} を処理済みに追加")
                        print(f"   📊 処理済み総数: {len(self.processed_message_ids)}件")
                        
                        # 短い間隔を空けて次の処理へ
                        time.sleep(2)
                    
                    print(f"   ★★★ 質問処理完了 ★★★")
                    
                next_check_time = (datetime.now() + timedelta(seconds=5)).strftime('%H:%M:%S')
                print(f"\n😴 5秒待機中... 次回チェック: {next_check_time}")
                print(f"{'='*60}")
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 AI社長監視システム停止")
                break
            except Exception as e:
                print(f"❌ システムエラー: {e}")
                print("🔄 5秒後に監視を再開...")
                time.sleep(5)

def main():
    """メイン実行関数"""
    ai_responder = CopilotMonitorableAI()
    ai_responder.run_monitoring()

if __name__ == "__main__":
    main()
