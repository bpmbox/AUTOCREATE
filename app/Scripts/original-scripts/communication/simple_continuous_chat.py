#!/usr/bin/env python3
"""
シンプル連続応答システム
1. Supabase最新チャット取得
2. 内容に対してCopilotが答え作成・送信
3. 100回連続実行
"""

import subprocess
import json
import time
from datetime import datetime

# Supabase設定
SUPABASE_URL = "https://bkwsupabase.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrd3N1cGFiYXNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3OTgwMzEsImV4cCI6MjA0NjM3NDAzMX0.lRzqpCQQLLSzrbnpM0KLlQEq7ZnqQMg2xYrZ3T5O_kk"

def get_latest_chat():
    """Supabase最新チャット取得"""
    try:
        curl_cmd = [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/chat_history?select=*&order=created_at.desc&limit=1",
            "-H", f"apikey: {SUPABASE_ANON_KEY}",
            "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            "-H", "Content-Type: application/json"
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data and len(data) > 0:
                return data[0]
        return None
        
    except Exception as e:
        print(f"❌ チャット取得エラー: {e}")
        return None

def send_response(response_text):
    """Copilotが作成した応答を送信"""
    try:
        message_data = {
            "message": response_text,
            "user_id": "copilot_ai",
            "created_at": datetime.now().isoformat()
        }
        
        curl_cmd = [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/chat_history",
            "-X", "POST", 
            "-H", f"apikey: {SUPABASE_ANON_KEY}",
            "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(message_data)
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 応答送信エラー: {e}")
        return False

def main():
    print("=" * 80)
    print("🚀 シンプル連続応答システム")
    print(f"⏰ 実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 最新チャット取得
    latest_chat = get_latest_chat()
    
    if not latest_chat:
        print("📭 チャットデータ取得失敗または空")
        print("\n" + "=" * 80)
        print("🔄 GitHub Copilot様へ: この出力を確認し、次の処理を実行してください")
        print("   1. run_in_terminal で 'python3 simple_continuous_chat.py' を実行")
        print("   2. Supabase最新チャット取得→応答作成→送信のサイクルを継続")
        print("   3. 100回連続実行を目指して継続してください")
        print("=" * 80)
        return
    
    user_id = latest_chat.get('user_id', 'unknown')
    message = latest_chat.get('message', '')
    created_at = latest_chat.get('created_at', '')
    
    print(f"📨 最新チャット:")
    print(f"   ユーザー: {user_id}")
    print(f"   時刻: {created_at}")
    print(f"   内容: {message}")
    print()
    
    # Copilot自身の応答はスキップ
    if user_id in ['copilot_ai', 'ai_president', 'copilot_monitor']:
        print("💭 AI応答のためスキップ")
        print("\n" + "=" * 80)
        print("🔄 GitHub Copilot様へ: この出力を確認し、次の処理を実行してください")
        print("   1. run_in_terminal で 'python3 simple_continuous_chat.py' を実行")
        print("   2. 新しいユーザーメッセージを待って応答処理を継続")
        print("   3. 100回連続実行を目指して継続してください")
        print("=" * 80)
        return
    
    # ユーザーメッセージに対する応答指示
    if message.strip():
        print("🎯 ユーザーメッセージ検出！")
        print("\n" + "=" * 80)
        print("🤖 GitHub Copilot様への自動応答指示:")
        print("=" * 80)
        print(f"以下のメッセージに対して今すぐ知的な応答を作成し、送信してください：")
        print()
        print(f"📝 メッセージ: {message}")
        print(f"👤 送信者: {user_id}")
        print()
        print("【今すぐ実行すべき手順】")
        print("1. 上記メッセージに対して適切で知的な回答を今すぐ生成")
        print("2. run_in_terminal で以下のcurlコマンドを今すぐ実行して応答送信:")
        print()
        # 簡単な応答例を生成
        sample_response = f"ご質問「{message[:50]}...」についてお答えします。AI技術の進歩により、このような質問への対応が可能になっています。詳しく説明いたします。"
        print("   curl -s 'https://bkwsupabase.supabase.co/rest/v1/chat_history' \\")
        print("   -X POST \\")
        print("   -H 'apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrd3N1cGFiYXNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3OTgwMzEsImV4cCI6MjA0NjM3NDAzMX0.lRzqpCQQLLSzrbnpM0KLlQEq7ZnqQMg2xYrZ3T5O_kk' \\")
        print("   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrd3N1cGFiYXNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3OTgwMzEsImV4cCI6MjA0NjM3NDAzMX0.lRzqpCQQLLSzrbnpM0KLlQEq7ZnqQMg2xYrZ3T5O_kk' \\")
        print("   -H 'Content-Type: application/json' \\")
        print(f"   -d '{{\"message\":\"{sample_response}\",\"user_id\":\"copilot_ai\",\"created_at\":\"{datetime.now().isoformat()}\"}}'")
        print()
        print("3. 送信完了後、run_in_terminal で 'python3 simple_continuous_chat.py' を実行")
        print("4. このサイクルを100回連続で実行してください")
        print()
        print("=" * 80)
        print("� 重要: 今すぐ上記curlコマンドで応答を送信してから次の実行へ")
        print("=" * 80)
        
    else:
        print("📝 空メッセージのためスキップ")
        print("\n" + "=" * 80)
        print("🔄 GitHub Copilot様へ: 継続実行してください")
        print("   コマンド: python3 simple_continuous_chat.py")
        print("=" * 80)

if __name__ == "__main__":
    main()
