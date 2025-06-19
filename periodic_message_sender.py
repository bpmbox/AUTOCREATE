#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 定期メッセージ送信テスト
システムがずっと回り続ける中で定期的にメッセージを送信
"""

import subprocess
import json
import time
from datetime import datetime
import random

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

def send_periodic_message(message, sender="社長"):
    """定期メッセージを送信"""
    data = {
        'messages': message,
        'ownerid': sender,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'{SUPABASE_URL}/rest/v1/chat_history',
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer {SUPABASE_ANON_KEY}',
        '-H', f'apikey: {SUPABASE_ANON_KEY}',
        '-d', json.dumps(data)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"📤 [{current_time}] 送信: {message}")
        return True
    except Exception as e:
        print(f"❌ 送信エラー: {e}")
        return False

def main():
    """定期メッセージ送信メイン"""
    print("🔄 定期メッセージ送信システム開始！")
    print("⏰ 送信間隔: 30秒")
    print("🎯 目標: 連続運用システムの長時間テスト")
    print()
    
    # メッセージパターン
    message_templates = [
        "🕐 {time} - 定期チェック: システムは正常ですか？",
        "📊 {time} - 業務報告: 現在の状況を教えてください",
        "🎯 {time} - 進捗確認: プロジェクトはいかがですか？",
        "💡 {time} - アイデア募集: 何か新しい提案はありますか？",
        "🔍 {time} - 状況確認: 問題は発生していませんか？",
        "⚡ {time} - エネルギー注入: 今日も頑張りましょう！",
        "🚀 {time} - 目標達成: 今日の成果はいかがですか？",
        "🎉 {time} - 祝福: 素晴らしい仕事をありがとう！"
    ]
    
    message_count = 0
    start_time = datetime.now()
    
    try:
        while True:
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # ランダムにメッセージテンプレートを選択
            template = random.choice(message_templates)
            message = template.format(time=current_time)
            
            # メッセージ送信
            if send_periodic_message(message):
                message_count += 1
                
                # 統計表示
                elapsed = datetime.now() - start_time
                elapsed_minutes = elapsed.total_seconds() / 60
                
                print(f"📈 統計: 送信数{message_count}件 | 実行時間{elapsed_minutes:.1f}分")
            
            print(f"😴 30秒待機中... 次回送信: {datetime.now().strftime('%H:%M:%S')}")
            time.sleep(30)  # 30秒間隔
            
    except KeyboardInterrupt:
        elapsed = datetime.now() - start_time
        elapsed_minutes = elapsed.total_seconds() / 60
        print(f"\n🛑 定期送信を停止します")
        print(f"📊 最終統計: 送信数{message_count}件 | 実行時間{elapsed_minutes:.1f}分")

if __name__ == "__main__":
    main()
