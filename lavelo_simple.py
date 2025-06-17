#!/usr/bin/env python3
"""
Lavelo AI システム - 簡単版（依存関係エラー回避）
Gradio UIからSupabaseプロンプト管理とgpt-engineer連携
"""

import gradio as gr
import sys
import os
from datetime import datetime

# プロジェクトルートをパスに追加
project_root = "/workspaces/AUTOCREATE"
sys.path.append(project_root)

# 記憶自動化システムの統合
try:
    from memory_automation_system import MemoryAutomationSystem, Memory
    MEMORY_SYSTEM_AVAILABLE = True
    print("✅ Memory automation system imported successfully")
    memory_system = MemoryAutomationSystem()
except ImportError as e:
    print(f"⚠️ Memory automation system not available: {e}")
    MEMORY_SYSTEM_AVAILABLE = False
    memory_system = None

# Supabase接続
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'YOUR_SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'YOUR_SUPABASE_KEY') 
    SUPABASE_AVAILABLE = SUPABASE_URL != 'YOUR_SUPABASE_URL' and SUPABASE_KEY != 'YOUR_SUPABASE_KEY'
    if SUPABASE_AVAILABLE:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connection established")
    else:
        print("⚠️ Supabase credentials not configured")
        supabase = None
except ImportError:
    print("⚠️ Supabase client not available")
    SUPABASE_AVAILABLE = False
    supabase = None

def get_memories_from_supabase(memory_type: str = None, limit: int = 50):
    """Supabaseから記憶を取得"""
    try:
        if not SUPABASE_AVAILABLE or not supabase:
            print("⚠️ Supabase not available")
            return []
        
        query = supabase.table('chat_history').select('*')
        
        if memory_type:
            query = query.eq('memory_type', memory_type)
        
        result = query.order('created_at', desc=True).limit(limit).execute()
        return result.data if result.data else []
        
    except Exception as e:
        print(f"❌ Supabase取得エラー: {e}")
        return []

def update_prompt_display():
    """プロンプト表示の更新"""
    try:
        print("🔄 プロンプト表示を更新中...")
        memories = get_memories_from_supabase(memory_type=None, limit=50)
        
        if memories:
            table_data = []
            for memory in memories:
                date_str = (memory.get('created_at') or '')[:16] if memory.get('created_at') else ""
                memory_type = memory.get('memory_type', 'general')
                importance = memory.get('importance_score', 0)
                
                type_icon = {
                    'lavelo_prompts': '📝',
                    'prompt': '📝', 
                    'code': '💻',
                    'general': '📄'
                }.get(memory_type, '📄')
                
                status_icon = '🔥' if importance >= 80 else '⭐' if importance >= 60 else '📋'
                
                table_data.append([
                    memory['id'],
                    f"{type_icon} {memory.get('title', '無題')}", 
                    f"重要度: {importance}",
                    f"タイプ: {memory_type}",
                    date_str
                ])
            
            return table_data
        else:
            return [["データなし", "", "", "", ""]]
            
    except Exception as e:
        print(f"❌ Display update error: {e}")
        return [["エラー", str(e), "", "", ""]]

def load_prompt_to_textbox(evt: gr.SelectData):
    """テーブルクリック時にプロンプト内容をテキストボックスに読み込む（修正版）"""
    try:
        print(f"🖱️ テーブルクリック検出: {evt}")
        
        # row_indexの安全な取得
        row_index = 0  # デフォルト値
        
        if evt is not None and hasattr(evt, 'index') and evt.index is not None:
            if isinstance(evt.index, (list, tuple)) and len(evt.index) >= 1:
                row_index = evt.index[0]
            elif isinstance(evt.index, int):
                row_index = evt.index
            else:
                print(f"⚠️ Unexpected index format: {evt.index}")
        else:
            print("⚠️ Using fallback row_index = 0")
        
        print(f"📍 使用する行インデックス: {row_index}")
        
        # Supabaseからデータ取得を試みる
        try:
            memories = get_memories_from_supabase(memory_type=None, limit=50)
            
            if memories and row_index < len(memories):
                memory = memories[row_index]
                content = memory.get('content', '')
                
                if content:
                    print(f"✅ Supabaseプロンプト取得成功（{len(content)}文字）")
                    github_url = memory.get('metadata', {}).get('github_url', '') if isinstance(memory.get('metadata'), dict) else ''
                    system_type = memory.get('memory_type', 'general')
                    return content, github_url, system_type
        
        except Exception as supabase_error:
            print(f"⚠️ Supabase取得エラー: {supabase_error}")
        
        # フォールバック：テストプロンプト
        test_prompts = {
            0: """# 🚀 Gradio システム生成プロンプト

## 概要
Gradioインターフェースを作成してください。

## 機能要件
- ファイルアップロード機能
- テキスト入力・出力
- リアルタイム処理
- 美しいUI

## 実装例
```python
import gradio as gr

def process_input(text):
    return f'処理結果: {text.upper()}'

interface = gr.Interface(
    fn=process_input,
    inputs=gr.Textbox(label="入力"),
    outputs=gr.Textbox(label="出力"),
    title="テストシステム"
)
```

## 追加要件
- エラーハンドリング
- ログ出力
- レスポンシブデザイン""",

            1: """# 🔗 FastAPI システム生成プロンプト

## 概要  
FastAPIを使用したWebAPIシステムを作成してください。

## 機能要件
- REST API エンドポイント
- データベース連携
- 認証・認可機能
- Swagger ドキュメント自動生成

## 実装例
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Test API")

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
```""",

            2: """# 📱 React フロントエンド生成プロンプト

## 概要
モダンなReactアプリケーションを作成してください。

## 機能要件
- レスポンシブデザイン
- 状態管理
- ルーティング
- API連携

## 実装例
```jsx
import React, { useState } from 'react';

function App() {
  const [data, setData] = useState('');
  
  return (
    <div className="App">
      <h1>React Application</h1>
      <input 
        value={data} 
        onChange={(e) => setData(e.target.value)} 
      />
    </div>
  );
}
```"""
        }
        
        if row_index in test_prompts:
            content = test_prompts[row_index]
            print(f"✅ テストプロンプト{row_index + 1}を返します")
            return content, "", "general"
        else:
            content = f"# 📋 汎用プロンプト（行{row_index}）\n\nこれは行{row_index}用のプロンプトです。"
            return content, "", "general"
            
    except Exception as e:
        print(f"❌ プロンプト読み込みエラー: {e}")
        error_content = f"""# ❌ エラー詳細

## エラー内容
{str(e)}

## エラータイプ  
{type(e)}

## 対処方法
1. ページを再読み込み
2. 別の行をクリック
3. システム管理者に連絡

## 一時的な回避策
以下のテストプロンプトが利用可能です：
1. 🚀 Gradio システム生成
2. 🔗 FastAPI システム生成  
3. 📱 React フロントエンド生成"""
        return error_content, "", "error"

def dummy_process(prompt_text, folder_name, github_token):
    """ダミーのシステム生成処理"""
    return f"""🚀 システム生成実行中...

📝 プロンプト: {prompt_text[:100]}...
📁 フォルダ: {folder_name}
🔑 GitHub連携: {'有効' if github_token else '無効'}

⚠️ これはテスト版です。実際のgpt-engineer連携は本番環境でのみ動作します。

✅ 処理完了（模擬）
"""

# Gradio UIの構築
def create_interface():
    with gr.Blocks(title="💾 Lavelo AI システム - 簡易版", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 💾 Lavelo AI システム - プロンプト管理とコード生成")
        gr.Markdown("Supabaseベースのプロンプト管理システム（簡易版）")
        
        with gr.Tab("📋 プロンプト管理"):
            with gr.Row():
                refresh_btn = gr.Button("🔄 更新", variant="secondary")
            
            prompt_table = gr.Dataframe(
                value=update_prompt_display(),
                headers=["ID", "タイトル", "重要度", "タイプ", "作成日時"],
                interactive=True,
                wrap=True
            )
            
            with gr.Row():
                with gr.Column(scale=3):
                    prompt_input = gr.Textbox(
                        label="プロンプト内容",
                        lines=15,
                        placeholder="テーブルから行をクリックしてプロンプトを選択するか、直接入力してください..."
                    )
                with gr.Column(scale=1):
                    selected_github_url = gr.Textbox(label="GitHub URL", interactive=False)
                    selected_system_type = gr.Textbox(label="システムタイプ", interactive=False)
            
            with gr.Row():
                folder_name = gr.Textbox(label="フォルダ名", value="generated_systems")
                github_token = gr.Textbox(label="GitHub Token", value="", type="password")
            
            execute_btn = gr.Button("🚀 システム生成実行", variant="primary", size="lg")
            result_output = gr.Textbox(label="実行結果", lines=8, interactive=False)
        
        # イベントハンドラー
        def safe_load_prompt(evt):
            try:
                return load_prompt_to_textbox(evt)
            except Exception as e:
                print(f"❌ Safe wrapper error: {e}")
                return f"❌ プロンプト読み込みエラー: {str(e)}", "", "error"
        
        prompt_table.select(
            fn=safe_load_prompt,
            outputs=[prompt_input, selected_github_url, selected_system_type]
        )
        
        refresh_btn.click(
            fn=update_prompt_display,
            outputs=prompt_table
        )
        
        execute_btn.click(
            fn=dummy_process,
            inputs=[prompt_input, folder_name, github_token],
            outputs=result_output
        )
        
        gr.Markdown("""
        ## 📋 使用方法
        1. **更新ボタン**でSupabaseからプロンプトを取得
        2. **テーブル行をクリック**してプロンプトを選択
        3. **システム生成実行**でコード生成開始
        
        ⚠️ これは簡易版です。完全版では実際のgpt-engineer連携が動作します。
        """)
    
    return app

if __name__ == "__main__":
    print("🚀 Lavelo AI システム（簡易版）起動中...")
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
