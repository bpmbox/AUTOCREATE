#!/usr/bin/env python3
"""
Gradio Root Application
======================

Gradioを直接ルート（/）で起動するシンプルなアプリケーション
"""

import gradio as gr
import os
import sys
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def create_simple_gradio_app():
    """シンプルなGradioアプリケーションを作成"""
    print("🔄 Creating simple Gradio application...")
    
    # データベース初期化
    try:
        missing = check_missing_databases()
        if missing:
            print(f"⚠️ Missing databases: {missing}")
            fix_missing_databases()
        print("✅ Database check completed")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")

def check_missing_databases():
    """不足しているデータベースをチェック"""
    try:
        required_dbs = [
            'prompts.db',
            'approval_system.db', 
            'chat_history.db',
            'conversation_history.db',
            'github_issues.db',
            'users.db'
        ]
        
        missing = []
        db_dir = os.path.join(project_root, 'database')
        
        for db_name in required_dbs:
            db_path = os.path.join(db_dir, db_name)
            if not os.path.exists(db_path):
                missing.append(db_name.replace('.db', ''))
        
        return missing
        
    except Exception as e:
        print(f"⚠️ Database check error: {e}")
        return []

def fix_missing_databases():
    """不足しているデータベースを修正"""
    try:
        # 簡単なデータベースファイルを作成
        db_dir = os.path.join(project_root, 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        required_dbs = [
            'prompts.db',
            'approval_system.db',
            'chat_history.db',
            'conversation_history.db',
            'github_issues.db',
            'users.db'
        ]
        
        for db_name in required_dbs:
            db_path = os.path.join(db_dir, db_name)
            if not os.path.exists(db_path):
                # 空のSQLiteデータベースファイルを作成
                import sqlite3
                conn = sqlite3.connect(db_path)
                conn.close()
                print(f"✅ Created {db_name}")
        
        print("✅ Database files created")
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
    
    # Gradioの起動とキューメソッドを無効化
    def disabled_launch(*args, **kwargs):
        print("⚠️ Individual .launch() calls are DISABLED")
        return None
    
    def disabled_queue(*args, **kwargs):
        print("⚠️ Individual .queue() calls are DISABLED")
        return None
    
    # 元のメソッドをバックアップ
    if not hasattr(gr.Interface, '_original_launch'):
        gr.Interface._original_launch = gr.Interface.launch
        gr.TabbedInterface._original_launch = gr.TabbedInterface.launch
        gr.Blocks._original_launch = gr.Blocks.launch
    
    # 個別起動を無効化
    gr.Interface.launch = disabled_launch
    gr.TabbedInterface.launch = disabled_launch
    gr.Blocks.launch = disabled_launch
    
    # キューメソッドを無効化
    gr.Interface.queue = disabled_queue
    gr.TabbedInterface.queue = disabled_queue
    gr.Blocks.queue = disabled_queue
    
    print("🔒 Gradio launch & queue methods OVERRIDDEN!")
    
    # インターフェースを収集
    try:
        from app.Services.GradioInterfaceService import GradioInterfaceService
        
        service = GradioInterfaceService()
        interfaces, interface_names = service.collect_gradio_interfaces()  # 正しいメソッド名を使用
        
        if not interfaces:
            print("⚠️ No interfaces collected, creating demo interface")
            
            def demo_function(message):
                return f"✅ Demo response to: {message}\n\nGradio is working at root!"
            
            demo_interface = gr.Interface(
                fn=demo_function,
                inputs=gr.Textbox(label="Input Message", value="Hello Gradio!"),
                outputs=gr.Textbox(label="Output"),
                title="🚀 Gradio Root Demo"
            )
            interfaces = [demo_interface]
            interface_names = ["🚀 Gradio Root Demo"]
        
        print(f"✅ Collected {len(interfaces)} interfaces")
        
        # TabbedInterfaceを作成
        if len(interfaces) == 1:
            # 単一インターフェースの場合
            final_interface = interfaces[0]
            print("📱 Using single interface")
        else:
            # 複数インターフェースの場合はTabbedInterface
            final_interface = gr.TabbedInterface(
                interfaces,
                tab_names=interface_names,
                title="🚀 AI Development Platform"
            )
            print(f"📑 Using TabbedInterface with {len(interfaces)} tabs")
        
        # キューを無効化
        if hasattr(final_interface, 'enable_queue'):
            final_interface.enable_queue = False
        if hasattr(final_interface, '_queue'):
            final_interface._queue = None
        
        print("✅ Final interface created with queue disabled")
        return final_interface
        
    except Exception as e:
        print(f"❌ Interface collection failed: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバックインターフェース
        def error_handler(message):
            return f"🚨 Error: {str(e)}\n\nPlease check server logs."
        
        return gr.Interface(
            fn=error_handler,
            inputs=gr.Textbox(label="Error Details", value="Interface collection failed"),
            outputs=gr.Textbox(label="Status"),
            title="🚨 System Error"
        )

if __name__ == "__main__":
    print("🚀 Starting Gradio Root Application...")
    print(f"🔍 Current directory: {os.getcwd()}")
    
    # アプリケーションを作成
    app = create_simple_gradio_app()
    
    # 環境設定
    space_id = os.getenv('SPACE_ID')
    if space_id:
        print(f"🤗 Running in Hugging Face Spaces: {space_id}")
        server_port = 7860
        server_name = "0.0.0.0"
        share = False
    else:
        print("💻 Running locally")
        server_port = 7860
        server_name = "0.0.0.0"  
        share = False
    
    print(f"🌐 Starting server on {server_name}:{server_port}")
    
    # launchメソッドを復元（統合起動用）
    if hasattr(gr.TabbedInterface, '_original_launch'):
        gr.TabbedInterface.launch = gr.TabbedInterface._original_launch
    if hasattr(gr.Interface, '_original_launch'):
        gr.Interface.launch = gr.Interface._original_launch
    if hasattr(gr.Blocks, '_original_launch'):
        gr.Blocks.launch = gr.Blocks._original_launch
    
    print("🔓 Launch methods restored for final launch")
    
    try:
        # Gradioを直接起動（ルートにマウント）
        app.launch(
            server_name=server_name,
            server_port=server_port,
            share=share,
            inbrowser=False,
            show_error=True,
            quiet=False,
            max_threads=10
        )
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        import traceback
        traceback.print_exc()
