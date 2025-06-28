#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
詳細会話履歴をナレッジベースに登録するスクリプト
複数のナレッジ管理システムに同時登録
"""

import json
import requests
from datetime import datetime
from pathlib import Path

def load_detailed_conversation():
    """詳細会話履歴JSONを読み込み"""
    json_path = Path("conversation_logs/copilot_detailed_conversation_20250624_064500.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ JSON読み込みエラー: {str(e)}")
        return None

def create_knowledge_summary(conversation_data):
    """ナレッジ用サマリーを生成"""
    
    if not conversation_data:
        return None
    
    summary = f"""
# React+Vite+shadcn UI 完全実装ナレッジ

## 📋 概要
{conversation_data.get('session_summary', '')}

## 🛠️ 技術スタック
- **フロントエンド**: {conversation_data['technical_stack_detailed']['frontend']['framework']}, {conversation_data['technical_stack_detailed']['frontend']['build_tool']}, {conversation_data['technical_stack_detailed']['frontend']['language']}
- **UI**: {conversation_data['technical_stack_detailed']['frontend']['ui_library']}
- **バックエンド**: {conversation_data['technical_stack_detailed']['backend_integration']['database']}
- **開発サーバー**: {conversation_data['technical_stack_detailed']['development_environment']['server']} (ポート{conversation_data['technical_stack_detailed']['development_environment']['port']})

## 🎯 解決した主要問題

"""
    
    for problem in conversation_data.get('problems_solved', []):
        summary += f"### {problem['problem']}\n"
        summary += f"**解決策**: {problem['solution']}\n"
        summary += f"**影響度**: {problem['impact']}\n\n"
    
    summary += "## ✅ 主要達成事項\n\n"
    
    for achievement in conversation_data.get('achievements_detailed', []):
        summary += f"### {achievement['category']}\n"
        for item in achievement['items']:
            summary += f"- {item}\n"
        summary += "\n"
    
    summary += f"""
## 🔗 関連ファイル・URL
"""
    
    for file in conversation_data.get('files_created_modified', []):
        summary += f"- `{file}`\n"
    
    summary += "\n"
    
    for url in conversation_data.get('urls_and_endpoints', []):
        summary += f"- {url}\n"
    
    summary += f"""

## 📝 実装手順（重要）
1. 環境変数設定（.env にVITE_接頭辞）
2. ルートpackage.jsonスクリプト追加
3. Viteキャッシュクリア・ポート設定
4. React+shadcn UI統合
5. Supabase連携設定
6. ChatWindow実装・テスト

## 🚀 次のステップ
"""
    
    for step in conversation_data.get('next_steps', []):
        summary += f"- {step}\n"
    
    return summary

def save_to_notion_knowledge(summary):
    """Notionナレッジベースに保存"""
    
    notion_token = "secret_HjYjpBAegpFTTeYCDiW6ZEeeLS9E4HqvyF95N8o8ag7"
    database_id = "215fd0b5bf7d806999f3dc4db1937b76"
    
    # Notionのデータベース構造を確認してからプロパティを調整
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # まずデータベース構造を取得
    try:
        db_response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )
        
        if db_response.status_code == 200:
            db_info = db_response.json()
            print("✅ Notionデータベース構造取得成功")
            properties = db_info.get('properties', {})
            print(f"📋 利用可能プロパティ: {list(properties.keys())}")
            
            # 利用可能なプロパティに基づいてデータを構築
            page_data = {
                "parent": {"database_id": database_id},
                "properties": {},
                "children": [{
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": summary[:2000]}  # 最初の2000文字
                        }]
                    }
                }]
            }
            
            # タイトルプロパティを設定
            title_prop = None
            for prop_name, prop_info in properties.items():
                if prop_info.get('type') == 'title':
                    title_prop = prop_name
                    break
            
            if title_prop:
                page_data["properties"][title_prop] = {
                    "title": [{
                        "text": {"content": "React+Vite+shadcn UI実装ナレッジ"}
                    }]
                }
            
            # ページ作成
            create_response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=page_data
            )
            
            if create_response.status_code == 200:
                page_url = create_response.json().get("url", "")
                print(f"✅ Notionナレッジ保存成功: {page_url}")
                return True
            else:
                print(f"❌ Notionページ作成失敗: {create_response.text}")
                return False
        
        else:
            print(f"❌ Notionデータベース取得失敗: {db_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Notion保存エラー: {str(e)}")
        return False

def save_to_supabase_knowledge(summary):
    """Supabaseに技術ナレッジとして保存"""
    
    supabase_url = "https://rootomzbucovwdqsscqd.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"
    
    headers = {
        'apikey': supabase_key,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {supabase_key}',
    }
    
    data = {
        'ownerid': 'GitHub-Copilot-AI-Knowledge',
        'messages': summary,
        'created': datetime.now().isoformat(),
        'targetid': 'technical-knowledge',
        'isread': False,
        'status': 'knowledge-base',
        'tmp_file': 'react-vite-shadcn-implementation-guide'
    }
    
    try:
        response = requests.post(
            f"{supabase_url}/rest/v1/chat_history",
            headers=headers,
            json=data
        )
        
        if response.status_code in [200, 201]:
            print("✅ Supabaseナレッジ保存成功")
            return True
        else:
            print(f"❌ Supabase保存失敗: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase保存エラー: {str(e)}")
        return False

def save_to_local_markdown(summary):
    """ローカルにMarkdownナレッジとして保存"""
    
    knowledge_dir = Path("knowledge_base")
    knowledge_dir.mkdir(exist_ok=True)
    
    filename = f"react_vite_shadcn_implementation_{datetime.now().strftime('%Y%m%d')}.md"
    filepath = knowledge_dir / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ ローカルMarkdownナレッジ保存成功: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ ローカル保存エラー: {str(e)}")
        return False

def main():
    """メイン実行関数"""
    print("📚 詳細会話履歴をナレッジベース化開始")
    print("=" * 60)
    
    # 1. 詳細会話履歴を読み込み
    print("\n📖 詳細会話履歴読み込み中...")
    conversation_data = load_detailed_conversation()
    
    if not conversation_data:
        print("❌ 会話データの読み込みに失敗しました")
        return False
    
    print("✅ 会話データ読み込み成功")
    
    # 2. ナレッジサマリー生成
    print("\n🔄 ナレッジサマリー生成中...")
    summary = create_knowledge_summary(conversation_data)
    
    if not summary:
        print("❌ サマリー生成に失敗しました")
        return False
    
    print("✅ ナレッジサマリー生成成功")
    
    # 3. 複数箇所に保存
    results = []
    
    print("\n💾 ローカルMarkdownに保存中...")
    results.append(save_to_local_markdown(summary))
    
    print("\n📊 Supabaseナレッジベースに保存中...")
    results.append(save_to_supabase_knowledge(summary))
    
    print("\n📝 Notionナレッジベースに保存中...")
    results.append(save_to_notion_knowledge(summary))
    
    # 結果表示
    print("\n" + "=" * 60)
    success_count = sum(results)
    print(f"✅ ナレッジ保存完了: {success_count}/3 箇所に正常保存")
    
    if success_count >= 2:
        print("🎉 重要な技術ナレッジが正常に保存されました！")
        print("📚 このナレッジは今後の開発で再利用可能です")
    else:
        print("⚠️  一部の保存先でエラーが発生しました")
    
    return success_count > 0

if __name__ == "__main__":
    main()
