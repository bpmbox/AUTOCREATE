#!/usr/bin/env python3
"""
Gradio Queue Error Fix
Gradioのキューエラーを修正するスクリプト
"""
import gradio as gr
import os
import sys
import asyncio
import tempfile
import shutil

def clear_gradio_cache():
    """Gradioキャッシュのクリア"""
    print("🧹 Gradioキャッシュをクリア中...")
    
    # Gradioの一時ディレクトリをクリア
    temp_dirs = [
        '/tmp/gradio',
        '/tmp/gradio_*',
        os.path.expanduser('~/.gradio'),
        './flagged',
        './gradio_cached_examples'
    ]
    
    for temp_dir in temp_dirs:
        try:
            if os.path.exists(temp_dir):
                if os.path.isdir(temp_dir):
                    shutil.rmtree(temp_dir)
                    print(f"✅ クリア済み: {temp_dir}")
                else:
                    os.remove(temp_dir)
                    print(f"✅ 削除済み: {temp_dir}")
        except Exception as e:
            print(f"⚠️ クリアできませんでした {temp_dir}: {e}")

def create_fixed_gradio_interface():
    """修正されたGradioインターフェースを作成"""
    print("🔧 修正されたGradioインターフェースを作成中...")
    
    # キューエラーを防ぐための設定
    os.environ['GRADIO_ANALYTICS_ENABLED'] = 'false'
    os.environ['GRADIO_TEMP_DIR'] = '/tmp/gradio_fixed'
    
    # 一時ディレクトリを作成
    os.makedirs('/tmp/gradio_fixed', exist_ok=True)
    
    def simple_echo(text):
        """シンプルなエコー関数（キューエラーなし）"""
        try:
            return f"✅ Gradio動作正常: {text}"
        except Exception as e:
            return f"❌ エラー: {str(e)}"
    
    # キューを無効にしたインターフェース
    try:
        interface = gr.Interface(
            fn=simple_echo,
            inputs=gr.Textbox(
                label="テスト入力",
                placeholder="何か入力してください...",
                value="Hello Gradio Fixed!"
            ),
            outputs=gr.Textbox(label="テスト出力"),
            title="🔧 Gradio Queue Error Fix Test",
            description="キューエラーを修正したGradioインターフェースです。",
            allow_flagging="never",
            analytics_enabled=False,
            live=False  # リアルタイム更新を無効化
        )
        
        print("✅ インターフェース作成成功")
        return interface
        
    except Exception as e:
        print(f"❌ インターフェース作成失敗: {e}")
        return None

def launch_fixed_gradio():
    """修正されたGradioを起動"""
    print("🚀 修正されたGradioを起動中...")
    
    # キャッシュクリア
    clear_gradio_cache()
    
    # インターフェース作成
    interface = create_fixed_gradio_interface()
    
    if interface:
        try:
            # キューを無効にして起動
            interface.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,
                debug=False,
                show_error=True,
                quiet=False,
                prevent_thread_lock=False,
                enable_queue=False,  # キューを無効化
                max_threads=1,
                favicon_path=None,
                ssl_keyfile=None,
                ssl_certfile=None,
                ssl_keyfile_password=None,
                file_directories=None,
                auth=None
            )
        except Exception as e:
            print(f"❌ Gradio起動失敗: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ インターフェースが作成されませんでした")

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 Gradio Queue Error Fix")
    print("=" * 50)
    launch_fixed_gradio()
