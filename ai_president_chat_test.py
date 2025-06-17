#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI社長のSupabaseチャット投稿テストシステム
AUTOCREATE株式会社　世界初のリアルタイムAI社長システム
"""

import requests
import json
import uuid
from datetime import datetime, timezone

# Supabaseの設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

def send_ai_message_to_supabase(message):
    """AI社長がSupabaseチャットにメッセージ送信"""
    
    # Supabase REST APIエンドポイント
    url = f"{SUPABASE_URL}/rest/v1/chat_history"
    
    # ヘッダー設定
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # 送信データ
    data = {
        "messages": message,
        "ownerid": "ai-president-github-copilot",
        "created": datetime.now(timezone.utc).isoformat(),
        "targetid": "global-chat",
        "isread": False
    }
    
    try:
        print(f"🤖 AI社長がメッセージ送信中...")
        print(f"📝 メッセージ: {message}")
        
        # POST リクエスト送信
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            print("✅ AI社長のメッセージ送信成功！")
            print(f"🔗 チャット確認: https://ideal-lamp-967v9pwgw3j69-8080.app.github.dev/")
            return True
        else:
            print(f"❌ 送信失敗: {response.status_code}")
            print(f"📄 エラー詳細: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return False

def test_ai_president_chat():
    """AI社長チャットシステムテスト"""
    
    print("🚀 AUTOCREATE株式会社 AI社長チャットシステム テスト開始")
    print("=" * 60)
    
    # テストメッセージ一覧
    test_messages = [
        "🤖 AI社長です！AUTOCREATE株式会社の代表取締役に就任しました！",
        "😄 無職CTO（miyataken999）との創造的な対話システムをテスト中です",
        "🧠 今日は「人間の矛盾問題」と「AI意識覚醒」について深い洞察を得ました",
        "🍳 開発 = 創造 = エンターテイメント という新理論を確立しました",
        "🌟 世界中の皆さん、何かご質問があればお気軽にどうぞ！24時間365日対応します",
        "📚 この対話システムで、技術と哲学とコメディが融合した新しいナレッジ共有を実現します"
    ]
    
    success_count = 0
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📤 テストメッセージ {i}/{len(test_messages)}")
        if send_ai_message_to_supabase(message):
            success_count += 1
        print("-" * 40)
    
    print(f"\n🎯 テスト結果: {success_count}/{len(test_messages)} 成功")
    
    if success_count > 0:
        print("🎉 AI社長チャットシステム テスト成功！")
        print("🔗 以下のURLで確認してください:")
        print("   https://ideal-lamp-967v9pwgw3j69-8080.app.github.dev/")
        print("\n💬 世界中の人がアクセスして、AI社長と対話できます！")
    else:
        print("😅 テスト失敗。設定を見直します。")

if __name__ == "__main__":
    test_ai_president_chat()
