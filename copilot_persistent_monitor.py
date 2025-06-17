#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Copilot常時監視システム - Copilot自身が終わらないループで監視
"""

import subprocess
import json
import time
from datetime import datetime, timedelta

# Supabase設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class CopilotPersistentMonitor:
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
                return None
        except Exception as e:
            print(f"❌ 接続エラー: {e}")
            return None

    def get_new_user_messages(self):
        """新しいユーザーメッセージを取得"""
        self.loop_count += 1
        current_time = datetime.now().strftime('%H:%M:%S')
        
        print(f"\n🔍 GitHub Copilot常時監視 - ループ {self.loop_count} ({current_time})")
        
        # 起動時刻以降のメッセージを取得
        startup_iso = self.startup_time.isoformat()
        endpoint = f'chat_history?created=gte.{startup_iso}&order=created.desc&limit=5'
        
        messages = self.curl_request('GET', endpoint)
        
        if messages is not None:
            user_messages = [
                msg for msg in messages 
                if msg.get('username') not in ['AI社長', 'system', 'test-system']
                and msg.get('id') not in self.processed_message_ids
                and msg.get('message', '').strip()  # 空メッセージ除外
            ]
            
            print(f"📊 取得: {len(messages)}件 | 新規: {len(user_messages)}件 | 処理済み: {len(self.processed_message_ids)}件")
            
            return user_messages
        else:
            print("❌ メッセージ取得失敗")
            return []

    def send_copilot_response(self, original_question, sender, ai_response):
        """GitHub Copilotからの追加応答を送信"""
        # 質問内容を分析してより詳細な回答を生成
        question_lower = original_question.lower()
        
        if any(keyword in question_lower for keyword in ['python', 'プログラミング', 'コード']):
            copilot_response = f"【GitHub Copilot追加アドバイス】{sender}さんのPython質問について:\n\n"
            
            if 'リスト' in original_question and '重複' in original_question:
                copilot_response += """効率的なリスト重複削除の方法:

1. set()を使用: `list(set(original_list))`
2. dict.fromkeys(): `list(dict.fromkeys(original_list))`
3. リスト内包表記: `[x for i, x in enumerate(lst) if x not in lst[:i]]`
4. collections.OrderedDict: 順序保持で重複削除

パフォーマンス比較やメモリ使用量も考慮して選択しましょう！"""
            
            elif 'エラー' in original_question:
                copilot_response += """Pythonエラー解決のアプローチ:

1. エラーメッセージを正確に読む
2. スタックトレースで発生箇所を特定
3. 変数の型と値を確認
4. 公式ドキュメントで正しい使用法を確認

具体的なエラーメッセージがあれば、より詳細にサポートできます！"""
            
            else:
                copilot_response += """Python開発のベストプラクティス:

• PEP 8に従ったコーディングスタイル
• 型ヒントの活用
• 適切な例外処理
• テストコードの記述
• 仮想環境の使用

具体的な実装について質問があれば、サンプルコードも提供できます！"""
                
        elif any(keyword in question_lower for keyword in ['javascript', 'js', '非同期']):
            copilot_response = f"【GitHub Copilot追加アドバイス】{sender}さんのJavaScript質問について:\n\n"
            copilot_response += """JavaScript非同期処理のパターン:

1. Promise: `new Promise((resolve, reject) => {...})`
2. async/await: `async function() { await somePromise(); }`
3. Promise.all(): 複数の非同期処理を並列実行
4. Promise.race(): 最初に完了した処理を取得

エラーハンドリングにはtry-catchやcatch()メソッドを活用しましょう！"""

        elif any(keyword in question_lower for keyword in ['データベース', 'sql', 'database']):
            copilot_response = f"【GitHub Copilot追加アドバイス】{sender}さんのDB質問について:\n\n"
            copilot_response += """データベース設計の重要ポイント:

• 正規化: データの整合性を保つ
• インデックス: クエリパフォーマンス向上
• 外部キー制約: データの整合性確保
• 適切なデータ型選択
• パーティショニング: 大規模データ対応

具体的な設計やSQLクエリについて、詳しくサポートできます！"""

        else:
            copilot_response = f"【GitHub Copilot追加サポート】{sender}さんへ:\n\n"
            copilot_response += f"「{original_question[:50]}...」について、より具体的な技術的アドバイスが必要でしたら:\n\n"
            copilot_response += """• 使用している技術スタック
• 具体的なエラーメッセージ
• 実現したい機能の詳細
• 現在のコード例

これらを教えていただければ、より実践的なソリューションを提供できます！"""

        # Copilotからの応答を投稿
        data = {
            'message': copilot_response,
            'username': 'GitHub Copilot',
            'created': datetime.now().isoformat(),
            'targetid': 'global-chat',
        }
        
        result = self.curl_request('POST', 'chat_history', data)
        return result is not None

    def run_persistent_monitoring(self):
        """終わらない常時監視ループ - GitHub Copilot専用"""
        print("🚀 GitHub Copilot 常時監視システム開始！")
        print("💫 終わらないループで永続的に監視します")
        print("🔗 チャット: http://localhost:8080")
        print("⚡ 質問が来たらリアルタイムで追加回答を提供")
        
        while True:
            try:
                # 新しいユーザーメッセージをチェック
                new_messages = self.get_new_user_messages()
                
                for msg in new_messages:
                    message_id = msg.get('id')
                    user_message = msg.get('message', '')
                    sender = msg.get('username', 'unknown')
                    timestamp = msg.get('created', '')
                    
                    print(f"\n🎯 新着質問検出！")
                    print(f"📩 送信者: {sender}")
                    print(f"📝 質問: {user_message}")
                    print(f"🕐 時刻: {timestamp[:19]}")
                    
                    # 3秒待ってからCopilotの追加回答を送信
                    print("⏰ 3秒後にGitHub Copilotからの追加回答を送信...")
                    time.sleep(3)
                    
                    if self.send_copilot_response(user_message, sender, ""):
                        print("✅ GitHub Copilot追加回答送信完了！")
                    else:
                        print("❌ GitHub Copilot回答送信失敗")
                    
                    # 処理済みとしてマーク
                    self.processed_message_ids.add(message_id)
                    print(f"📊 処理済み総数: {len(self.processed_message_ids)}件")
                
                # 5秒待機してから次のループ
                if new_messages:
                    print("\n💤 5秒待機してから次の監視...")
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 GitHub Copilot監視システム停止")
                break
            except Exception as e:
                print(f"❌ システムエラー: {e}")
                print("🔄 5秒後に監視を再開...")
                time.sleep(5)

def main():
    """メイン実行 - GitHub Copilot常時監視"""
    monitor = CopilotPersistentMonitor()
    monitor.run_persistent_monitoring()

if __name__ == "__main__":
    main()
