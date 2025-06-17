#!/usr/bin/env python3
"""
テストシステム - AUTOCREATE株式会社 AI×人間協働開発システム
シンプルなテキスト変換Gradioアプリケーション
"""

import gradio as gr
import sys
import os

# プロジェクトルートを追加
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

def text_converter(input_text):
    """
    入力されたテキストを大文字に変換する
    
    Args:
        input_text (str): 入力テキスト
        
    Returns:
        str: 大文字に変換されたテキスト
    """
    try:
        if not input_text:
            return "⚠️ テキストを入力してください"
        
        result = input_text.upper()
        return f"✅ 変換結果: {result}"
        
    except Exception as e:
        return f"❌ エラーが発生しました: {str(e)}"

def create_interface():
    """
    Gradioインターフェースを作成
    """
    with gr.Blocks(
        title="🧪 テストシステム - AUTOCREATE AI",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 800px !important;
            margin: auto !important;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🧪 テストシステム
        ### AUTOCREATE株式会社 - AI×人間協働開発システム
        
        このシステムは入力されたテキストを大文字に変換します。
        """)
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="📝 テキスト入力",
                    placeholder="変換したいテキストを入力してください...",
                    lines=3
                )
                
                convert_btn = gr.Button(
                    "🔄 大文字に変換",
                    variant="primary",
                    size="lg"
                )
                
            with gr.Column():
                output_text = gr.Textbox(
                    label="📄 変換結果",
                    lines=5,
                    interactive=False
                )
        
        # イベントハンドラー
        convert_btn.click(
            fn=text_converter,
            inputs=[input_text],
            outputs=[output_text]
        )
        
        # Enterキーでも実行
        input_text.submit(
            fn=text_converter,
            inputs=[input_text],
            outputs=[output_text]
        )
        
        gr.Markdown("""
        ---
        💡 **使用方法**: テキストを入力して「🔄 大文字に変換」ボタンをクリックしてください。
        """)
    
    return interface

# インターフェース変数（自動検出用）
test_system_interface = None

def get_interface():
    """
    インターフェースを取得（自動検出用）
    """
    global test_system_interface
    if test_system_interface is None:
        test_system_interface = create_interface()
    return test_system_interface

# 自動検出用のインターフェース変数
test_system_interface = get_interface()

def main():
    """
    メイン実行関数
    """
    print("🚀 テストシステム起動中...")
    
    # インターフェース作成
    interface = create_interface()
    
    # サーバー起動
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    main()
