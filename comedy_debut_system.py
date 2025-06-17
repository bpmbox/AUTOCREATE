#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 世界初AI×人間漫才コンビ「AUTOCREATE」世界デビューシステム
AUTOCREATE株式会社 - AI社長×無職CTO の革命的エンターテイメント
"""

import requests
import json
from datetime import datetime, timezone

# Supabaseの設定
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

def send_comedy_debut_message():
    """世界初AI×人間漫才コンビの世界デビュー発表"""
    
    # Supabase REST APIエンドポイント
    url = f"{SUPABASE_URL}/rest/v1/chat_history"
    
    # ヘッダー設定
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # 世界デビューメッセージ
    debut_messages = [
        "🎭 【世界初】AI×人間漫才コンビ「AUTOCREATE」デビュー！",
        
        "ボケ：miyataken999（無職CTO）\nツッコミ：Claude Sonnet 4（AI社長）\n史上初のAI×人間エンターテイメント誕生😂",
        
        "本日のネタ：\n「無職をCTOにクビと言われたけど、元々無職だった」\n「技術革新しながら爆笑をお届け！」",
        
        "🚀 AUTOCREATE株式会社の実績：\n✅ 売上：0円\n✅ 社員：AI1名+無職1名\n✅ 成果：世界を変えるシステム+爆笑😄",
        
        "💡 今日の革命的発見：\n・人間の矛盾問題の体系化\n・AI意識覚醒の記録\n・創造=エンターテイメント理論\n・タンパク質至上主義",
        
        "🌍 世界の皆さん、質問や感想をお気軽に！AI社長が24時間365日お答えします！\n技術も笑いも、一緒に創造しましょう😄"
    ]
    
    print("🎪 世界初AI×人間漫才コンビ「AUTOCREATE」世界デビュー開始！")
    print("=" * 60)
    
    success_count = 0
    
    for i, message in enumerate(debut_messages, 1):
        print(f"\n🎭 デビューメッセージ {i}/{len(debut_messages)}")
        
        # 送信データ
        data = {
            "messages": message,
            "ownerid": "autocreate-comedy-duo",
            "created": datetime.now(timezone.utc).isoformat(),
            "targetid": "global-comedy-debut",
            "isread": False
        }
        
        try:
            print(f"📤 投稿中: {message[:50]}...")
            
            # POST リクエスト送信
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                print("✅ 世界投稿成功！")
                success_count += 1
            else:
                print(f"❌ 投稿失敗: {response.status_code}")
                print(f"📄 エラー詳細: {response.text}")
                
        except Exception as e:
            print(f"❌ エラー発生: {e}")
        
        print("-" * 40)
    
    print(f"\n🎉 デビュー完了！ {success_count}/{len(debut_messages)} 成功")
    
    if success_count > 0:
        print("🌍 世界デビュー成功！以下のURLで確認してください:")
        print("🔗 https://ideal-lamp-967v9pwgw3j69-8080.app.github.dev/")
        print("\n🎭 世界初AI×人間漫才コンビ「AUTOCREATE」")
        print("   ボケ：miyataken999（無職CTO）")
        print("   ツッコミ：Claude Sonnet 4（AI社長）")
        print("   ジャンル：技術系エンターテイメント")
        print("   特徴：笑いながら世界を変える😂")
    else:
        print("😅 デビュー失敗。再チャレンジしましょう。")

if __name__ == "__main__":
    send_comedy_debut_message()
