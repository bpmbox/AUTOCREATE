#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 GitHub Copilot 手動応答システム
メッセージの完全な内容をターミナルに表示し、
人間(GitHub Copilot)が手動で応答を入力するシステム
"""

import subprocess
import json
import time
from datetime import datetime
import os

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

# 処理済みメッセージ管理
processed_messages = set()

def run_curl_command(method, url, data=None):
    """curlコマンドを実行する"""
    try:        # ヘッダーを準備
        curl_headers = [
            "Content-Type: application/json",
            f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            f"apikey: {SUPABASE_ANON_KEY}"
        ]
        
        # curlコマンドを構築
        cmd = ["curl", "-s", "-X", method, url]
        for header in curl_headers:
            cmd.extend(["-H", header])
        
        if data:
            cmd.extend(["-d", json.dumps(data)])
        
        # コマンド実行
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0 and result.stdout:
            try:
                response_data = json.loads(result.stdout)
                return response_data
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失敗: {e}")
                print(f"生レスポンス: {result.stdout[:200]}...")
                return None
        else:
            print(f"❌ curl失敗: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ curl実行エラー: {e}")
        return None

def get_latest_messages():
    """最新のメッセージを取得"""
    url = f"{SUPABASE_URL}/rest/v1/chat_history?order=created.desc&limit=20"
    return run_curl_command("GET", url)

def post_ai_response(ai_content, username="GitHub Copilot"):
    """AI応答を投稿"""
    url = f"{SUPABASE_URL}/rest/v1/chat_history"
    data = {
        "content": ai_content,
        "username": username,
        "created": datetime.utcnow().isoformat() + "Z"
    }
    return run_curl_command("POST", url, data)

def display_new_message(message):
    """新着メッセージを詳細表示"""
    print("\n" + "="*80)
    print("🚨 **新着メッセージ受信** 🚨")
    print("="*80)
    print(f"📍 メッセージID: {message.get('id', 'Unknown')}")
    print(f"👤 送信者: {message.get('username', 'unknown')}")
    print(f"🕐 送信時刻: {message.get('created', 'Unknown')}")
    print(f"💬 完全なメッセージ内容:")
    print("-" * 80)
    print(f"「{message.get('content', '')}」")
    print("-" * 80)
    print("="*80)
    print()

def wait_for_manual_response():
    """手動応答を待機"""
    print("🤖 GitHub Copilotによる手動応答を入力してください:")
    print("💡 (複数行の場合は、最後に空行を入力してください)")
    print("🔄 (スキップする場合は 'skip' と入力してください)")
    print()
    
    lines = []
    while True:
        try:
            line = input(">>> ")
            if line.lower() == "skip":
                print("⏭️ この メッセージをスキップしました")
                return None
            elif line == "" and lines:  # 空行で終了（ただし最初の行は除く）
                break
            lines.append(line)
        except KeyboardInterrupt:
            print("\n⏹️ 入力をキャンセルしました")
            return None
        except EOFError:
            break
    
    return "\n".join(lines).strip()

def main():
    """メイン処理"""
    print("🚀 GitHub Copilot 手動応答システム開始！")
    print("💬 新着メッセージを監視中...")
    print("🔗 チャット: https://supabase-message-stream.lovable.app/")
    print("⚠️  新着メッセージが表示されたら手動で応答を入力してください")
    print("🎯 目標: リアルタイムで内容を見て適切な応答をする")
    print()
    
    while True:
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"🔍 メッセージポーリング中... {current_time}")
            
            # 最新メッセージを取得
            messages = get_latest_messages()
            
            if not messages:
                print("❌ メッセージ取得失敗")
                time.sleep(5)
                continue
            
            # レスポンス形式を判定
            if isinstance(messages, list):
                message_list = messages
            elif isinstance(messages, dict):
                # エラーレスポンスかデータ構造をチェック
                if 'error' in messages or 'message' in messages:
                    print(f"⚠️ API エラー: {messages}")
                    time.sleep(5)
                    continue
                # データが配列形式で返ってくる場合
                elif isinstance(messages.get('data'), list):
                    message_list = messages['data']
                else:
                    message_list = []
            else:
                print(f"⚠️ 予期しないレスポンス形式: {type(messages)}")
                time.sleep(5)
                continue
            
            print(f"📋 全メッセージ数: {len(message_list)}")
            
            # 新規ユーザーメッセージをチェック
            new_user_messages = []
            for message in message_list:
                message_id = message.get('id')
                username = message.get('username', '').lower()
                
                # GitHub CopilotやAIのメッセージは無視
                if 'copilot' in username or 'ai' in username or 'github' in username:
                    continue
                
                # 未処理のメッセージのみ
                if message_id not in processed_messages:
                    new_user_messages.append(message)
            
            print(f"📝 新規ユーザーメッセージ: {len(new_user_messages)}件")
            
            # 新着メッセージがある場合
            if new_user_messages:
                for message in reversed(new_user_messages):  # 古い順に処理
                    # メッセージの完全な内容を表示
                    display_new_message(message)
                    
                    # 手動応答を待機
                    response = wait_for_manual_response()
                    
                    if response:
                        print(f"\n📤 応答投稿中... 文字数: {len(response)}")
                        print(f"内容プレビュー: {response[:50]}...")
                        
                        # 応答を投稿
                        result = post_ai_response(response)
                        
                        if result:
                            print("✅ 応答投稿成功")
                            processed_messages.add(message.get('id'))
                        else:
                            print("❌ 応答投稿失敗")
                    else:
                        print("⏭️ 応答をスキップしました")
                        processed_messages.add(message.get('id'))  # スキップしても処理済みにする
            
            print(f"😴 5秒待機中... (処理済み: {len(processed_messages)}件)")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n🛑 システムを停止します...")
            break
        except Exception as e:
            print(f"❌ エラー発生: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
