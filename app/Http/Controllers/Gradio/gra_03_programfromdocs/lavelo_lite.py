#!/usr/bin/env python3
"""
Lavelo AI システム - 軽量版テスト
AUTOCREATE株式会社 - AI×人間協働開発システム
"""
import gradio as gr
import os
from datetime import datetime

# 軽量版のSupabase接続（必要最小限）
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://rootomzbucovwdqsscqd.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8')

def test_supabase_connection():
    """Supabase接続テスト"""
    try:
        import requests
        url = f"{SUPABASE_URL}/rest/v1/chat_history?select=id&limit=1"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}'
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return f"✅ Supabase接続成功 - {len(response.json())}件のデータ確認"
        else:
            return f"❌ 接続エラー: {response.status_code}"
    except Exception as e:
        return f"❌ 接続エラー: {e}"

def save_test_prompt(title, content):
    """テストプロンプト保存"""
    try:
        import requests
        url = f"{SUPABASE_URL}/rest/v1/chat_history"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'ownerid': 'lavelo_test',
            'messages': f"Test Prompt: {title}\n\n{content}",
            'targetid': 'test_prompt',
            'created': datetime.now().isoformat(),
            'status': 'test',
            'group_name': 'lavelo_prompts'
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 201:
            return f"✅ プロンプト保存成功: {title}"
        else:
            return f"❌ 保存エラー: {response.status_code}"
    except Exception as e:
        return f"❌ 保存エラー: {e}"

def get_test_prompts():
    """テストプロンプト一覧取得"""
    try:
        import requests
        url = f"{SUPABASE_URL}/rest/v1/chat_history?select=*&group_name=eq.lavelo_prompts&order=created.desc&limit=10"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}'
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            table_data = []
            for row in data:
                table_data.append([
                    row['id'],
                    f"📝 {(row.get('messages') or '')[:40]}...",
                    row.get('group_name', 'general'),
                    row.get('status', 'available'),
                    (row.get('created') or '')[:16]
                ])
            return table_data if table_data else [["データなし", "", "", "", ""]]
        else:
            return [["エラー", f"HTTP {response.status_code}", "", "", ""]]
    except Exception as e:
        return [["エラー", str(e), "", "", ""]]

# Gradioインターフェース作成
with gr.Blocks(title="🚀 Lavelo AI - 軽量版") as gradio_interface:
    gr.Markdown("# 🚀 Lavelo AI システム（軽量版テスト）")
    gr.Markdown("Supabaseプロンプト管理・システム生成のテスト版")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📚 Supabaseプロンプト一覧")
            
            # 接続テスト
            connection_btn = gr.Button("🔗 Supabase接続テスト", variant="secondary")
            connection_result = gr.Textbox(label="接続結果", interactive=False)
            
            # プロンプト一覧
            prompt_table = gr.Dataframe(
                headers=["ID", "タイトル", "グループ", "ステータス", "作成日時"],
                datatype=["number", "str", "str", "str", "str"],
                value=[["テスト中...", "", "", "", ""]],
                interactive=False
            )
            
            refresh_btn = gr.Button("🔄 一覧更新", variant="secondary")
            
        with gr.Column(scale=1):
            gr.Markdown("## 💾 プロンプト保存テスト")
            
            test_title = gr.Textbox(label="テストタイトル", value="軽量版テスト")
            test_content = gr.Textbox(
                label="テスト内容",
                lines=5,
                value="これは軽量版のテストプロンプトです。\nGradioインターフェースが正常に動作するかテストしています。"
            )
            
            save_test_btn = gr.Button("💾 テスト保存", variant="primary")
            save_result = gr.Textbox(label="保存結果", interactive=False)
            
            gr.Markdown("## 📋 システム情報")
            gr.Markdown(f"""
            - **Supabase URL**: {SUPABASE_URL[:30]}...
            - **接続状態**: 準備中
            - **バージョン**: 軽量版 v1.0
            """)
    
    # イベントハンドラー
    connection_btn.click(
        fn=test_supabase_connection,
        outputs=connection_result
    )
    
    refresh_btn.click(
        fn=get_test_prompts,
        outputs=prompt_table
    )
    
    save_test_btn.click(
        fn=save_test_prompt,
        inputs=[test_title, test_content],
        outputs=save_result
    ).then(
        fn=get_test_prompts,
        outputs=prompt_table
    )

# 自動検出用メタデータ
interface_title = "🚀 Lavelo AI - 軽量版"
interface_description = "Supabaseプロンプト管理システム（軽量版テスト）"

if __name__ == "__main__":
    print("🚀 Lavelo AI 軽量版テスト起動中...")
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
