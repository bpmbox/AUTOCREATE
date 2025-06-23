#!/usr/bin/env python3
"""
🎯 ユーザー挨拶対応システム

ユーザーからの挨拶に対する自動応答プログラム
GitHub Issue: user-greeting-hello
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ supabaseパッケージが必要です: pip install supabase")
    exit(1)

class GreetingResponder:
    def __init__(self):
        """挨拶対応システム初期化"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if self.supabase_url and self.supabase_key:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
        else:
            self.supabase = None
            print("⚠️ Supabase設定なし - ローカル実行モード")
    
    def generate_greeting_response(self, user_name="user"):
        """挨拶に対する応答を生成"""
        current_time = datetime.now()
        hour = current_time.hour
        
        # 時間帯に応じた挨拶
        if 5 <= hour < 12:
            time_greeting = "おはようございます"
        elif 12 <= hour < 18:
            time_greeting = "こんにちは"
        else:
            time_greeting = "こんばんは"
        
        response = f"""こんにちは、{user_name}さん！

{time_greeting}！AI自動応答システムです。

🎯 **システム情報**
- 現在時刻: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
- 対応言語: 日本語・英語
- 稼働状況: 正常動作中

💡 **対応可能な内容**
- プログラム作成（Python、PHP、JavaScript等）
- 技術的な質問・相談
- システム開発のアドバイス
- 自動化スクリプト作成
- データ処理・API連携

🚀 **ご利用方法**
具体的なご要望やご質問をお聞かせください。
例：
- "Pythonでファイル処理のプログラムを作って"
- "PHPでデータベース接続のサンプルが欲しい"
- "JavaScriptでAPI呼び出しの方法を教えて"

何かお手伝いできることがあれば、お気軽にお声がけください！"""
          return response
    
    def send_to_supabase(self, response, original_user="user"):
        """Supabaseに応答を送信"""
        if not self.supabase:
            print("📝 ローカル出力:")
            print(response)
            return True
        
        try:
            data = {
                'ownerid': 'AI-Assistant',
                'messages': response
            }
            
            result = self.supabase.table('chat_history').insert(data).execute()
            print("✅ Supabaseに応答を送信しました")
            return True
            
        except Exception as e:
            print(f"❌ Supabase送信エラー: {e}")
            print("📝 ローカル出力:")
            print(response)
            return False
    
    def process_greeting(self, user_name="user"):
        """挨拶処理の実行"""
        print(f"🎯 {user_name}さんからの挨拶を処理中...")
        
        # 応答生成
        response = self.generate_greeting_response(user_name)
        
        # Supabaseに送信
        success = self.send_to_supabase(response, user_name)
        
        if success:
            print("✅ 挨拶対応完了")
        else:
            print("⚠️ 挨拶対応完了（送信エラーあり）")
        
        return response

def main():
    """メイン実行"""
    print("🎯 ユーザー挨拶対応システム")
    print("=" * 50)
    
    # 挨拶対応システム初期化
    responder = GreetingResponder()
    
    # ユーザーからの「こんにちわ」に対応
    response = responder.process_greeting("user")
    
    print("\n📊 処理結果:")
    print("=" * 50)
    print(response)
    print("=" * 50)
    print("✨ 処理完了")

if __name__ == "__main__":
    main()
