#!/usr/bin/env python3
"""
Gradio Queue Error Fix - Complete Solution
Gradioのキューエラーを完全に修正
"""
import os
import sys
import shutil
import subprocess

def clear_all_gradio_data():
    """Gradio関連データを完全クリア"""
    print("🧹 Gradio関連データを完全クリア中...")
    
    # すべてのGradioプロセスを停止
    try:
        subprocess.run(['pkill', '-f', 'gradio'], check=False)
        subprocess.run(['pkill', '-f', 'python.*app.py'], check=False)
        print("✅ Gradioプロセス停止")
    except Exception as e:
        print(f"⚠️ プロセス停止エラー: {e}")
    
    # 一時ディレクトリとキャッシュをクリア
    dirs_to_clear = [
        '/tmp/gradio',
        '/tmp/gradio_cached_examples',
        'flagged',
        '.gradio',
        '__pycache__',
        '.pytest_cache'
    ]
    
    for dir_path in dirs_to_clear:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"✅ 削除: {dir_path}")
            except Exception as e:
                print(f"⚠️ 削除失敗: {dir_path} - {e}")

def setup_gradio_environment():
    """Gradio環境の再設定"""
    print("⚙️ Gradio環境を再設定中...")
    
    # 環境変数設定
    env_vars = {
        'GRADIO_ANALYTICS_ENABLED': 'false',
        'GRADIO_SERVER_HOST': '0.0.0.0',
        'GRADIO_SERVER_PORT': '7860',
        'GRADIO_TEMP_DIR': '/tmp/gradio',
        'GRADIO_SHARE': 'false',
        'GRADIO_ALLOW_FLAGGING': 'never'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✅ 設定: {key}={value}")
    
    # 必要ディレクトリの作成
    os.makedirs('/tmp/gradio', exist_ok=True)
    os.makedirs('flagged', exist_ok=True)

def create_minimal_gradio():
    """最小限のGradioインターフェース作成"""
    import gradio as gr
    
    def simple_echo(text):
        return f"✅ 正常動作: {text}"
    
    # 最小限の設定でインターフェース作成
    interface = gr.Interface(
        fn=simple_echo,
        inputs=gr.Textbox(label="入力テスト", value="Hello Gradio!"),
        outputs=gr.Textbox(label="出力結果"),
        title="🔧 Gradio修復テスト",
        description="Queue Errorが修正されたかテストします",
        allow_flagging="never",
        analytics_enabled=False,
        examples=None,
        cache_examples=False
    )
    
    return interface

def launch_gradio_safely():
    """安全にGradioを起動"""
    try:
        # 完全クリア
        clear_all_gradio_data()
        
        # 環境再設定
        setup_gradio_environment()
        
        print("🚀 Gradio安全起動中...")
        
        # インターフェース作成
        interface = create_minimal_gradio()
        
        # 安全な起動オプション
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True,
            show_error=True,
            quiet=False,
            prevent_thread_lock=False,
            enable_queue=False,        # キューを完全無効化
            max_threads=1,             # シングルスレッド
            auth=None,
            inbrowser=False,
            favicon_path=None,
            ssl_keyfile=None,
            ssl_certfile=None,
            ssl_keyfile_password=None,
            allowed_paths=None
        )
        
    except Exception as e:
        print(f"❌ 起動失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 ===== Gradio Queue Error 完全修復 =====")
    launch_gradio_safely()
