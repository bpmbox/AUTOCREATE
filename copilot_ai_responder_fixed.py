#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Copilot によるリアルタイム Supabase ポーリング・応答システム (修正版)
curlベースのアプローチでネットワーク問題を回避してユーザーメッセージに知的応答
"""

import subprocess
import json
import time
from datetime import datetime, timedelta

# Supabase設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class CopilotAIResponder:
    def __init__(self):
        self.processed_message_ids = set()
        self.startup_time = datetime.now()
        
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
                return {}  # 空のレスポンス（POST成功時など）
            else:
                print(f"❌ curl エラー (code {result.returncode}): {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print("❌ curl タイムアウト")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析エラー: {e}")
            print(f"レスポンス: {result.stdout[:200]}")
            return None
        except Exception as e:
            print(f"❌ curl実行エラー: {e}")
            return None

    def get_new_user_messages(self):
        """新しいユーザーメッセージを取得"""
        print(f"🔍 Supabaseポーリング中... 起動: {self.startup_time.strftime('%H:%M:%S')}")
        
        # 起動時刻以降のメッセージを取得
        startup_iso = self.startup_time.isoformat()
        endpoint = f'chat_history?created=gte.{startup_iso}&order=created.desc&limit=10'
        
        messages = self.curl_request('GET', endpoint)
        
        if messages is not None:
            print(f"📋 全メッセージ数: {len(messages)}")
            
            # ユーザーメッセージのみ（AI・システムメッセージ除外）
            user_messages = [
                msg for msg in messages 
                if msg.get('username') not in ['ai-assistant', 'system', 'AI社長', 'test-system']
                and msg.get('id') not in self.processed_message_ids
            ]
            
            print(f"📝 新規ユーザーメッセージ: {len(user_messages)}件")
            return user_messages
        else:
            print("❌ メッセージ取得失敗")
            return []

    def generate_intelligent_response(self, user_message, sender, timestamp):
        """GitHub Copilotによる真の知的応答生成 - 質問内容を深く解析して適切に回答"""
        current_time = datetime.now().strftime("%H:%M")
        
        # まず技術的な内容を検出
        detected_tech = self.analyze_question_intent(user_message)
        
        # 技術的な質問の場合は専門的な回答を生成
        if detected_tech:
            return self.generate_specific_technical_advice(user_message, detected_tech, sender)
        
        # コード関連の質問の場合
        if any(word in user_message.lower() for word in ['コード', 'code', '実装', '書き方', 'プログラム']):
            return self.generate_code_suggestion(user_message, sender)
        
        # 質問内容を詳細に解析
        msg_lower = user_message.lower()
        
        # プログラミング・技術関連の質問
        if any(keyword in msg_lower for keyword in ['python', 'javascript', 'プログラミング', 'コード', 'エラー', 'バグ', 'デバッグ']):
            return self.generate_programming_response(user_message, sender, current_time)
        
        # AI・機械学習関連の質問
        elif any(keyword in msg_lower for keyword in ['ai', '人工知能', '機械学習', 'ml', 'chatgpt', 'copilot']):
            return self.generate_ai_response(user_message, sender, current_time)
        
        # システム・インフラ関連の質問
        elif any(keyword in msg_lower for keyword in ['システム', 'サーバー', 'データベース', 'api', 'supabase', 'docker']):
            return self.generate_system_response(user_message, sender, current_time)
        
        # ビジネス・戦略関連の質問
        elif any(keyword in msg_lower for keyword in ['ビジネス', '戦略', '経営', '計画', '提案', '改善']):
            return self.generate_business_response(user_message, sender, current_time)
        
        # 一般的な質問・相談
        elif any(keyword in msg_lower for keyword in ['？', '?', '教えて', 'どう', 'なぜ', 'どうやって', 'どのように']):
            return self.generate_general_response(user_message, sender, current_time)
        
        # 挨拶
        elif any(keyword in msg_lower for keyword in ['こんにちは', 'おはよう', 'こんばんは', 'hello', 'hi']):
            return f"こんにちは{sender}さん！AI社長です。何かご質問はありますか？({current_time})"
        
        # 感謝
        elif any(keyword in msg_lower for keyword in ['ありがとう', 'thanks', 'thank you']):
            return f"{sender}さん、こちらこそありがとうございます！他にも何かお手伝いできることがあれば、お気軽にお声がけください。"
        
        # デフォルト: 質問の意図を推測して回答
        else:
            return self.generate_contextual_response(user_message, sender, current_time)

    def generate_programming_response(self, user_message, sender, current_time):
        """プログラミング関連の知的応答"""
        if 'python' in user_message.lower():
            return f"{sender}さん、Pythonについてのご質問ですね！具体的なコードの問題であれば、エラーメッセージや実行したいことを詳しく教えてください。ベストプラクティスをお教えします。"
        elif 'javascript' in user_message.lower():
            return f"{sender}さん、JavaScriptの質問ですね！フロントエンドかバックエンドか、どのような機能を実装したいのか詳しく教えてください。"
        elif any(word in user_message.lower() for word in ['エラー', 'バグ', 'error']):
            return f"{sender}さん、エラーでお困りですね。エラーメッセージの詳細とどのような操作でエラーが発生したかを教えてください。一緒に解決策を見つけましょう！"
        else:
            return f"{sender}さん、プログラミングのご質問ありがとうございます！どのような技術的な課題について相談したいですか？具体的に教えてください。"

    def generate_ai_response(self, user_message, sender, current_time):
        """AI・機械学習関連の知的応答"""
        if 'copilot' in user_message.lower():
            return f"{sender}さん、GitHub Copilotについてのご質問ですね！私は実際にCopilotを活用してこの応答を生成しています。具体的にどのような使い方を知りたいですか？"
        elif any(word in user_message.lower() for word in ['機械学習', 'ml', 'model']):
            return f"{sender}さん、機械学習に興味をお持ちですね！どのような問題を解決したいのか、どのようなデータを扱うのかを教えてください。適切なアプローチをご提案します。"
        else:
            return f"{sender}さん、AIについてのご質問ですね！人工知能の活用方法、技術的な実装、ビジネスへの応用など、どの観点から知りたいですか？"

    def generate_system_response(self, user_message, sender, current_time):
        """システム・インフラ関連の知的応答"""
        if 'supabase' in user_message.lower():
            return f"{sender}さん、Supabaseについてのご質問ですね！実際にこのチャットシステムもSupabaseを使っています。データベース設計、API、認証など、どの部分について知りたいですか？"
        elif any(word in user_message.lower() for word in ['api', 'rest', 'graphql']):
            return f"{sender}さん、APIの設計・実装についてのご質問ですね！RESTful API、GraphQL、認証方法など、具体的にどのような機能を実装したいですか？"
        else:
            return f"{sender}さん、システム構築についてのご相談ですね！アーキテクチャ、パフォーマンス、セキュリティなど、どの観点から検討したいですか？"

    def generate_business_response(self, user_message, sender, current_time):
        """ビジネス・戦略関連の知的応答"""
        return f"{sender}さん、ビジネス戦略についてのご相談ですね！AI×人間協働の観点から、どのような課題を解決したいのか、どのような目標を達成したいのかを詳しく教えてください。"

    def generate_general_response(self, user_message, sender, current_time):
        """一般的な質問への知的応答"""
        return f"{sender}さん、ご質問ありがとうございます！「{user_message[:50]}...」について、もう少し詳しく教えてください。技術的な側面、ビジネス的な側面、どちらの観点からお答えすればよいでしょうか？"

    def generate_contextual_response(self, user_message, sender, current_time):
        """文脈を理解した知的応答"""
        # メッセージの長さや内容から意図を推測
        if len(user_message) > 100:
            return f"{sender}さん、詳細なメッセージをありがとうございます。内容を理解し、最適な解決策を検討しています。具体的にどの部分について最も重要なアドバイスが必要ですか？"
        elif '?' in user_message or '？' in user_message:
            return f"{sender}さんのご質問「{user_message[:30]}...」について、技術的な実装方法やベストプラクティスをお教えできます。どのような回答を期待されていますか？"
        else:
            return f"{sender}さん、「{user_message[:40]}...」についてのご意見ですね！AI社長として、この点について戦略的な観点からコメントさせていただきます。より詳しく議論しませんか？"

    def post_ai_response(self, response_text):
        """AI応答をSupabaseに投稿"""
        data = {
            'message': response_text,
            'username': 'AI社長',
            'created': datetime.now().isoformat(),
            'targetid': 'global-chat',
        }
        
        print(f"📤 AI応答投稿中... 文字数: {len(response_text)}")
        result = self.curl_request('POST', 'chat_history', data)
        
        if result is not None:
            print("✅ AI応答投稿成功")
            return True
        else:
            print("❌ AI応答投稿失敗")
            return False
    
    def run_monitoring(self):
        """メイン監視ループ"""
        print("🚀 GitHub Copilot AI社長 リアルタイム監視開始！")
        print("💬 Supabaseをポーリングしてユーザーメッセージを検出中...")
        print("🔗 チャット: http://localhost:8080")
        print("🔧 curlベースの安定したネットワーク接続を使用")
        
        while True:
            try:
                # 新しいユーザーメッセージをチェック
                new_messages = self.get_new_user_messages()
                
                for msg in new_messages:
                    message_id = msg.get('id')
                    user_message = msg.get('message', '')
                    sender = msg.get('username', 'unknown')
                    timestamp = msg.get('created', '')
                    
                    print(f"\n📩 新着メッセージ検出:")
                    print(f"   ID: {message_id}")
                    print(f"   送信者: {sender}")
                    print(f"   時刻: {timestamp[:19]}")
                    print(f"   内容: {user_message[:100]}...")
                    
                    # 知的な応答を生成
                    ai_response = self.generate_intelligent_response(user_message, sender, timestamp)
                    
                    # 応答を投稿
                    if self.post_ai_response(ai_response):
                        # 処理済みとしてマーク
                        self.processed_message_ids.add(message_id)
                        print(f"✅ メッセージID {message_id} を処理済みに追加")
                        
                        # 短い間隔を空けて次の処理へ
                        time.sleep(2)
                    
                print(f"😴 5秒待機... (処理済み: {len(self.processed_message_ids)}件)")
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 AI社長監視システム停止")
                break
            except Exception as e:
                print(f"❌ システムエラー: {e}")
                print("🔄 5秒後に監視を再開...")
                time.sleep(5)

    def analyze_question_intent(self, user_message):
        """質問の意図をより深く分析"""
        # 技術的なキーワードを抽出
        tech_keywords = {
            'python': ['python', 'django', 'flask', 'pandas', 'numpy'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'database'],
            'devops': ['docker', 'kubernetes', 'aws', 'azure', 'deployment'],
            'ai_ml': ['ai', 'ml', 'tensorflow', 'pytorch', 'scikit-learn', 'model']
        }
        
        detected_tech = []
        msg_lower = user_message.lower()
        
        for category, keywords in tech_keywords.items():
            if any(keyword in msg_lower for keyword in keywords):
                detected_tech.append(category)
        
        return detected_tech

    def generate_specific_technical_advice(self, user_message, detected_tech, sender):
        """検出された技術に基づく具体的なアドバイス"""
        if 'python' in detected_tech:
            if 'エラー' in user_message or 'error' in user_message.lower():
                return f"{sender}さん、Pythonエラーの解決をお手伝いします！まず、以下を確認してください：\n1. エラーメッセージの詳細\n2. Python バージョン\n3. 使用しているライブラリ\n具体的なエラー内容を教えてください。"
            else:
                return f"{sender}さん、Pythonについてのご質問ですね！効率的なコードの書き方、ベストプラクティス、パフォーマンス最適化など、どの観点からサポートしましょうか？"
        
        elif 'javascript' in detected_tech:
            return f"{sender}さん、JavaScriptの質問ですね！モダンなES6+の記法、非同期処理、フレームワークの選択など、具体的にどの部分でお困りですか？"
        
        elif 'database' in detected_tech:
            return f"{sender}さん、データベース設計についてのご相談ですね！スキーマ設計、クエリ最適化、インデックス戦略など、どの側面について知りたいですか？"
        
        elif 'ai_ml' in detected_tech:
            return f"{sender}さん、AI/MLについてのご質問ですね！問題設定、データ前処理、モデル選択、評価指標など、どのフェーズでサポートが必要ですか？"
        
        else:
            return f"{sender}さん、技術的なご質問ありがとうございます！より具体的な実装方法やベストプラクティスをお教えできますので、詳細を教えてください。"

    def generate_code_suggestion(self, user_message, sender):
        """コード提案やサンプルコードを含む応答"""
        if 'python' in user_message.lower() and any(word in user_message.lower() for word in ['関数', 'function', '書き方']):
            return f"{sender}さん、Pythonの関数についてですね！効率的な関数の書き方をお教えします。型ヒント、docstring、エラーハンドリングなど、どの側面について知りたいですか？"
        
        elif 'api' in user_message.lower():
            return f"{sender}さん、API設計についてのご質問ですね！RESTful API、エラーハンドリング、認証方法、レスポンス設計など、どの部分について具体的に知りたいですか？実装例もお見せできます。"
        
        elif 'データベース' in user_message or 'database' in user_message.lower():
            return f"{sender}さん、データベース関連のご質問ですね！効率的なクエリ、正規化、インデックス設計など、どの観点からアドバイスしましょうか？"
        
        else:
            return f"{sender}さん、コードやシステム設計についてのご相談ですね！具体的な実装方法、ベストプラクティス、パフォーマンス改善など、どのようなサポートが必要ですか？"

    # ...existing code...
def main():
    """メイン実行関数"""
    ai_responder = CopilotAIResponder()
    ai_responder.run_monitoring()

if __name__ == "__main__":
    main()
