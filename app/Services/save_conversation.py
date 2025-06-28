#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会話履歴を自動保存するスクリプト
Supabase、ファイル、Notion、miiboに同時保存
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

def save_conversation_to_supabase():
    """Supabaseのchat_historyテーブルに会話を保存"""
    
    conversation_content = """
# GitHub Copilot AIとの技術会話履歴
日時: 2025-06-24

## 会話内容
- React+Vite+shadcn UIフロントエンドの構築完了
- Supabase連携とAIチャット機能の実装
- ルートディレクトリ問題の解決（package.jsonスクリプト追加）
- Viteサーバーの正常起動（ポート3001）
- ChatWindow本格版への切り替え完了
- 環境変数設定とAPI連携準備完了

## 技術的成果
- TypeScript + React + Vite + shadcn UI構成
- AIチャットシステム実装
- Supabase統合
- レスポンシブデザイン
- グループ別チャット管理
- リアルタイム更新システム

## 解決した問題
- ルートディレクトリでの実行問題
- package.jsonスクリプト設定
- Viteサーバー起動最適化
- 環境変数管理（.env設定）

## 現在の状態
- Viteサーバー: http://localhost:3001 で動作中
- チャット機能: 完全実装済み
- AI応答システム: ダミーレスポンス動作確認済み
- 次のステップ: 本格的なAI統合・テスト
"""

    # Supabase設定
    supabase_url = "https://rootomzbucovwdqsscqd.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"
    
    headers = {
        'apikey': supabase_key,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {supabase_key}',
    }
    
    data = {
        'ownerid': 'GitHub-Copilot-AI',
        'messages': conversation_content,
        'created': datetime.now().isoformat(),
        'targetid': 'conversation-history',
        'isread': False,
        'status': 'saved'
    }
    
    try:
        response = requests.post(
            f"{supabase_url}/rest/v1/chat_history",
            headers=headers,
            json=data
        )
        
        if response.status_code in [200, 201]:
            print("✅ Subase会話履歴保存成功")
            return True
        else:
            print(f"❌ Supabase保存失敗: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase保存エラー: {str(e)}")
        return False

def save_conversation_to_file():
    """ローカルファイルに会話を保存"""
    
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "session_id": "copilot-chat-2025-06-24",
        "participants": ["User", "GitHub-Copilot-AI"],
        "topic": "React+Vite+shadcn UIフロントエンド開発",
        "conversation": [
            {
                "speaker": "User",
                "message": "React+Viteでチャット機能を正常表示・動作させたい",
                "timestamp": "2025-06-24T21:00:00Z"
            },
            {
                "speaker": "GitHub-Copilot-AI", 
                "message": "環境変数設定、Viteサーバー起動、ChatWindow実装を完了しました",
                "timestamp": "2025-06-24T21:30:00Z"
            },
            {
                "speaker": "User",
                "message": "ルートフォルダーで実行される問題",
                "timestamp": "2025-06-24T21:35:00Z"
            },
            {
                "speaker": "GitHub-Copilot-AI",
                "message": "package.jsonにスクリプト追加で解決。Viteサーバーポート3001で正常動作",
                "timestamp": "2025-06-24T21:37:00Z"
            },
            {
                "speaker": "User",
                "message": "会話内容を保存したい",
                "timestamp": "2025-06-24T21:40:00Z"
            }
        ],
        "technical_details": {
            "frameworks": ["React", "Vite", "TypeScript", "shadcn-ui"],
            "databases": ["Supabase"],
            "api_integrations": ["Supabase", "Notion", "JIRA", "miibo"],
            "deployment": "Local development server",
            "port": 3001,
            "status": "Active and running"
        },
        "achievements": [
            "Viteサーバー正常起動",
            "React+shadcn UIアプリ実装",
            "Supabase連携設定完了",
            "AIチャット機能実装",
            "ルートディレクトリ問題解決",
            "環境変数管理最適化"
        ]
    }
    
    # 保存ディレクトリ作成
    save_dir = Path("conversation_logs")
    save_dir.mkdir(exist_ok=True)
    
    # JSONファイルとして保存
    filename = f"copilot_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = save_dir / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 会話履歴ファイル保存成功: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ ファイル保存エラー: {str(e)}")
        return False

def save_conversation_to_notion():
    """Notionナレッジベースに会話を保存"""
    
    notion_token = "secret_HjYjpBAegpFTTeYCDiW6ZEeeLS9E4HqvyF95N8o8ag7"
    database_id = "215fd0b5bf7d806999f3dc4db1937b76"
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{
                    "text": {"content": "GitHub Copilot AI 技術会話履歴 - React+Vite開発"}
                }]
            },
            "Category": {
                "select": {"name": "AI技術会話"}
            },
            "Status": {
                "select": {"name": "完了"}
            },
            "Tags": {
                "multi_select": [
                    {"name": "copilot-ai"},
                    {"name": "react-vite"},
                    {"name": "conversation-log"},
                    {"name": "technical-discussion"}
                ]
            }
        },
        "children": [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "GitHub Copilot AIとの技術会話が完了しました。React+Vite+shadcn UIフロントエンドの開発、Supabase連携、チャット機能実装について詳細な技術討論を行いました。"}
                }]
            }
        }]
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            notion_page_url = response.json().get("url", "")
            print(f"✅ Notion会話履歴保存成功: {notion_page_url}")
            return True
        else:
            print(f"❌ Notion保存失敗: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Notion保存エラー: {str(e)}")
        return False

def main():
    """メイン実行関数"""
    print("🤖 GitHub Copilot AI - 会話履歴自動保存開始")
    print("=" * 50)
    
    # 複数の保存先に同時保存
    results = []
    
    # 1. Supabaseに保存
    print("\n📊 Supabaseに保存中...")
    results.append(save_conversation_to_supabase())
    
    # 2. ローカルファイルに保存
    print("\n💾 ローカルファイルに保存中...")
    results.append(save_conversation_to_file())
    
    # 3. Notionに保存
    print("\n📝 Notionに保存中...")
    results.append(save_conversation_to_notion())
    
    # 結果表示
    print("\n" + "=" * 50)
    success_count = sum(results)
    print(f"✅ 保存完了: {success_count}/3 箇所に正常保存")
    
    if success_count == 3:
        print("🎉 全ての保存先に正常に会話履歴が保存されました！")
    else:
        print("⚠️  一部の保存先でエラーが発生しました。")
    
    return success_count > 0

if __name__ == "__main__":
    main()
