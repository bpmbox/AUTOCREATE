#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡単なAI応答システム - ネットワーク問題を回避するアプローチ
"""

import subprocess
import json
import time
from datetime import datetime

# Supabase設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

def curl_supabase(method, endpoint, data=None):
    """curlを使ってSupabaseにアクセス"""
    cmd = [
        'curl', '-X', method,
        f'{SUPABASE_URL}/rest/v1/{endpoint}',
        '-H', f'apikey: {SUPABASE_KEY}',
        '-H', f'Authorization: Bearer {SUPABASE_KEY}',
        '-H', 'Content-Type: application/json',
        '--max-time', '10'
    ]
    
    if data:
        cmd.extend(['-d', json.dumps(data)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            return json.loads(result.stdout) if result.stdout.strip() else {}
        else:
            print(f"❌ curl エラー: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("❌ curl タイムアウト")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析エラー: {e}")
        print(f"レスポンス: {result.stdout}")
        return None
    except Exception as e:
        print(f"❌ curl実行エラー: {e}")
        return None

def get_latest_messages():
    """最新メッセージを取得"""
    print("📊 最新メッセージ取得中...")
    messages = curl_supabase('GET', 'chat_history?order=created.desc&limit=5')
    
    if messages is not None:
        print(f"✅ {len(messages)}件のメッセージを取得")
        
        # ユーザーメッセージのみフィルタ
        user_messages = [
            msg for msg in messages
            if msg.get('username') not in ['AI社長', 'ai-assistant', 'system', 'test-system']
        ]
        
        print(f"📝 ユーザーメッセージ: {len(user_messages)}件")
        return user_messages
    else:
        print("❌ メッセージ取得失敗")
        return []

def post_ai_response(user_msg, response_text):
    """AI応答を投稿"""
    data = {
        'message': response_text,
        'username': 'AI社長',
        'created': datetime.now().isoformat(),
        'targetid': 'global-chat'
    }
    
    print(f"📤 AI応答投稿: {response_text[:50]}...")
    result = curl_supabase('POST', 'chat_history', data)
    
    if result is not None:
        print("✅ AI応答投稿成功")
        return True
    else:
        print("❌ AI応答投稿失敗")
        return False

def generate_ai_response(user_message, username):
    """AIの知的応答を生成"""
    current_time = datetime.now().strftime("%H:%M")
    
    responses = [
        f"こんにちは{username}さん！ご質問ありがとうございます。({current_time})",
        f"{username}さんのメッセージ「{user_message[:30]}...」について考えています。",
        f"AI社長より: {username}さん、それは興味深いポイントですね！",
        f"技術的な観点から、{username}さんのアイデアは実現可能だと思います。",
        f"{username}さん、一緒にこの課題を解決していきましょう！({current_time})"
    ]
    
    import random
    return random.choice(responses)

def run_simple_monitor():
    """シンプルな監視ループ"""
    print("🚀 シンプルAI監視システム開始")
    print("🔧 curlベースのアプローチを使用")
    
    processed_ids = set()
    
    while True:
        try:
            messages = get_latest_messages()
            
            for msg in messages:
                msg_id = msg.get('id')
                if msg_id not in processed_ids:
                    user_message = msg.get('message', '')
                    username = msg.get('username', 'unknown')
                    
                    print(f"\\n📩 新着: {username}: {user_message[:50]}...")
                    
                    # AI応答生成
                    ai_response = generate_ai_response(user_message, username)
                    
                    # 応答投稿
                    if post_ai_response(user_message, ai_response):
                        processed_ids.add(msg_id)
                        print(f"✅ {msg_id}を処理済みに追加")
            
            print(f"😴 10秒待機... (処理済み: {len(processed_ids)}件)")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\\n🛑 監視停止")
            break
        except Exception as e:
            print(f"❌ エラー: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_simple_monitor()
