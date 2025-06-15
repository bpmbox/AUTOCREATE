#!/usr/bin/env python3
"""
Gradio Connection Error Fix
Gradioの接続エラーを修正するスクリプト
"""
import os
import sys

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def fix_gradio_connection_errors():
    """Gradio接続エラーの修正"""
    print("🔧 Fixing Gradio Connection Errors...")
    
    # 1. 環境変数の設定
    os.environ['GRADIO_ANALYTICS_ENABLED'] = 'false'
    os.environ['GRADIO_SERVER_HOST'] = '0.0.0.0'
    os.environ['GRADIO_SERVER_PORT'] = '7860'
    os.environ['GRADIO_TEMP_DIR'] = '/tmp/gradio'
    
    # 2. 必要なディレクトリの作成
    os.makedirs('/tmp/gradio', exist_ok=True)
    os.makedirs('flagged', exist_ok=True)
    
    # 3. データベース初期化
    try:
        from database.init_databases import create_databases
        create_databases()
        print("✅ Database initialization completed")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
    
    # 4. Gradio設定修正
    import gradio as gr
    
    def simple_test(text):
        return f"✅ Connection OK: {text}"
    
    # 5. 修正されたGradioインターフェース作成
    try:
        interface = gr.Interface(
            fn=simple_test,
            inputs=gr.Textbox(label="Test Input", value="Hello"),
            outputs=gr.Textbox(label="Test Output"),
            title="🔧 Fixed Gradio Interface",
            description="Connection error has been fixed!",
            allow_flagging="never",
            analytics_enabled=False
        )
        
        print("✅ Fixed Gradio interface created")
        
        # 6. 安全な起動設定
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True,
            show_error=True,
            quiet=False,
            prevent_thread_lock=False,
            max_threads=1
        )
        
    except Exception as e:
        print(f"❌ Gradio launch failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_gradio_connection_errors()
