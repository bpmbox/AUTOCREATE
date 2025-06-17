#!/usr/bin/env python3
"""最小限のテーブルクリック修正テスト"""

import gradio as gr

def safe_table_click(evt):
    """安全なテーブルクリック処理"""
    try:
        print(f"Event received: {evt}")
        print(f"Event type: {type(evt)}")
        
        # 安全なインデックス取得
        row_index = 0
        if evt is not None and hasattr(evt, 'index') and evt.index is not None:
            if isinstance(evt.index, (list, tuple)) and len(evt.index) >= 1:
                row_index = evt.index[0]
            elif isinstance(evt.index, int):
                row_index = evt.index
        
        # テストプロンプト
        test_prompts = [
            "# 🚀 Gradio システム\n\nGradioベースのWebアプリケーションを作成してください。",
            "# 🔗 FastAPI システム\n\nFastAPIベースのAPIサーバーを作成してください。", 
            "# 📱 React アプリ\n\nReactベースのフロントエンドを作成してください。"
        ]
        
        if row_index < len(test_prompts):
            content = test_prompts[row_index]
        else:
            content = f"# プロンプト {row_index}\n\n行 {row_index} のテストプロンプトです。"
        
        return content, f"https://github.com/test/row-{row_index}", "web_system"
        
    except Exception as e:
        print(f"Table click error: {e}")
        return f"❌ エラー: {str(e)}", "", "error"

# テーブルデータ
sample_data = [
    ["1", "🚀 Gradio システム", "高", "web_system", "2024-06-17"],
    ["2", "🔗 FastAPI システム", "中", "api_system", "2024-06-17"],
    ["3", "📱 React アプリ", "低", "frontend", "2024-06-17"]
]

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🔧 テーブルクリック修正テスト")
    
    with gr.Row():
        table = gr.Dataframe(
            value=sample_data,
            headers=["ID", "タイトル", "重要度", "タイプ", "日時"],
            interactive=True
        )
    
    with gr.Row():
        output_text = gr.Textbox(label="プロンプト内容", lines=10)
        github_url = gr.Textbox(label="GitHub URL")
        system_type = gr.Textbox(label="システムタイプ")
    
    # テーブルクリックイベント
    table.select(
        fn=safe_table_click,
        outputs=[output_text, github_url, system_type]
    )
    
    gr.Markdown("""
    ## 📋 テスト方法
    1. 上のテーブルの行をクリック
    2. 下のテキストボックスにプロンプトが表示されるかを確認
    3. エラーが発生した場合は詳細が表示されます
    """)

if __name__ == "__main__":
    print("🚀 テーブルクリック修正テスト開始")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
