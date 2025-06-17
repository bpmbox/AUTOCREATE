#!/usr/bin/env python3
"""
FastAPI Laravel-style Application with Gradio at Root
===================================================

Gradioをルート（/）にマウントするバージョン
"""

import gradio as gr
import os
import shutil
import sys
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def check_missing_databases():
    """不足しているデータベースをチェック"""
    try:
        from config.database import get_db_connection
        
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
    missing = check_missing_databases()
    if missing:
        print(f"⚠️ Missing databases: {missing}")
        try:
            from config.database import ensure_databases_exist
            ensure_databases_exist()
            print("✅ Databases initialized successfully")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    return missing

def initialize_laravel_style_gradio():
    """Laravel風のGradio初期化（完全な起動とキュー防止モード）"""
    try:
        print("🚀 Initializing Laravel-style Gradio (LAUNCH & QUEUE PREVENTION MODE)...")
        
        # データベース初期化
        fix_missing_databases()
        
        # Gradioの起動とキューメソッドを無効化
        import gradio as gr
        
        # launchメソッドを無効化
        def disabled_launch(*args, **kwargs):
            print("⚠️  Individual .launch() calls are DISABLED")
            return None
        
        # queueメソッドを無効化
        def disabled_queue(*args, **kwargs):
            print("⚠️  Individual .queue() calls are DISABLED")
            return None
        
        print("⚠️  INDIVIDUAL LAUNCHES COMPLETELY DISABLED!")
        print("⚠️  QUEUE METHODS COMPLETELY DISABLED!")
        
        # 元のメソッドをバックアップ（統合起動時に復元用）
        if not hasattr(gr.Interface, '_original_launch'):
            gr.Interface._original_launch = gr.Interface.launch
        if not hasattr(gr.TabbedInterface, '_original_launch'):
            gr.TabbedInterface._original_launch = gr.TabbedInterface.launch
        if not hasattr(gr.Blocks, '_original_launch'):
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
        
        # GradioInterfaceServiceを使用してインターフェースを収集
        from app.Services.GradioInterfaceService import GradioInterfaceService
        
        print("🚀 === CREATING UNIFIED TABBED INTERFACE ===")
        service = GradioInterfaceService()
        interfaces = service.collect_interfaces()
        
        if not interfaces:
            print("⚠️ No interfaces collected, creating fallback interface")
            
            def fallback_function(message):
                return "🚨 No Gradio interfaces found. Please check the system configuration."
            
            fallback_interface = gr.Interface(
                fn=fallback_function,
                inputs=gr.Textbox(label="Input", value="System Status Check"),
                outputs=gr.Textbox(label="Output"),
                title="🚨 System Status"
            )
            interfaces = [fallback_interface]
        
        # TabbedInterfaceを作成
        print(f"🎯 Creating TabbedInterface with {len(interfaces)} tabs")
        
        # インターフェース名を取得
        tab_names = []
        for interface in interfaces:
            if hasattr(interface, 'title') and interface.title:
                tab_names.append(interface.title)
            else:
                tab_names.append(f"Tab {len(tab_names) + 1}")
        
        tabbed_interface = gr.TabbedInterface(
            interfaces,
            tab_names=tab_names,
            title="🚀 AI Development Platform - Laravel風統合システム"
        )
        
        # キューを無効化
        if hasattr(tabbed_interface, 'enable_queue'):
            tabbed_interface.enable_queue = False
        if hasattr(tabbed_interface, '_queue'):
            tabbed_interface._queue = None
            
        print("🚀 ✅ UNIFIED TABBED INTERFACE CREATED - Ready for root mounting!")
        
        return tabbed_interface
        
    except Exception as e:
        print(f"❌ Laravel-style Gradio initialization failed: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック用の簡単なインターフェース
        def error_handler(message):
            return f"🚨 Gradio Error: {str(e)}\n\nPlease check the server logs for more details."
        
        fallback_interface = gr.Interface(
            fn=error_handler,
            inputs=gr.Textbox(label="Error Details", value="Gradio initialization failed"),
            outputs=gr.Textbox(label="Status"),
            title="🚨 Gradio Setup Error"
        )
        
        print("⚠️ Fallback interface created")
        return fallback_interface

def create_gradio_root_app():
    """GradioをルートにマウントしたFastAPIアプリケーションを作成"""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import mimetypes
    
    print("🔄 Creating Gradio-first application (Gradio at root)...")
    
    # Gradioインターフェースを作成
    try:
        print("🔄 Starting unified Gradio interface collection...")
        tabbed_interface = initialize_laravel_style_gradio()
        
        # キュー設定を完全に無効化
        try:
            print("🚫 Final queue disabling...")
            if hasattr(tabbed_interface, 'enable_queue'):
                tabbed_interface.enable_queue = False
                print("✅ enable_queue set to False")
            
            if hasattr(tabbed_interface, '_queue'):
                tabbed_interface._queue = None
                print("✅ _queue cleared")
                
            print("⚠️ NO queue() method called - completely disabled")
            
        except Exception as queue_error:
            print(f"⚠️ Queue disable warning: {queue_error}")
        
        # GradioのFastAPIアプリを作成
        try:
            print("🔄 Creating Gradio FastAPI app...")
            
            # TabbedInterfaceからFastAPIアプリを作成
            if hasattr(tabbed_interface, 'interface_list') and len(tabbed_interface.interface_list) > 0:
                print(f"🎯 TabbedInterface with {len(tabbed_interface.interface_list)} tabs detected")
                
                # GradioのFastAPIアプリを直接作成
                gradio_app = gr.routes.App.create_app(tabbed_interface)
                print("✅ Gradio FastAPI app created from TabbedInterface")
                
                # CORS設定を追加
                gradio_app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
                print("✅ CORS middleware added")
                
                # 静的ファイルの設定
                try:
                    # MIME type設定
                    mimetypes.add_type('text/css', '.css')
                    mimetypes.add_type('application/javascript', '.js')
                    mimetypes.add_type('application/json', '.json')
                    
                    gradio_app.mount("/static", StaticFiles(directory="static"), name="static")
                    print("✅ Static files mounted at /static")
                except Exception as static_error:
                    print(f"⚠️ Static files mount failed: {static_error}")
                
                # Laravel風のルーティングをAPIエンドポイントとして追加
                try:
                    from routes.web import router as web_router
                    gradio_app.include_router(web_router, prefix="/api")
                    print("✅ Laravel-style web routes loaded at /api")
                except ImportError as e:
                    print(f"⚠️ Web routes not loaded: {e}")
                
                print("🚀 ✅ Gradio mounted at ROOT with all features!")
                return gradio_app
                
            else:
                print("❌ No interfaces found in TabbedInterface")
                
        except Exception as create_error:
            print(f"❌ Gradio app creation failed: {create_error}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Failed to create Gradio-first app: {e}")
        import traceback
        traceback.print_exc()
    
    # フォールバック: 通常のFastAPIアプリを返す
    print("⚠️ Falling back to standard FastAPI app")
    
    app = FastAPI(
        title="AI Development Platform (Fallback)",
        description="Laravel風のGradio統合プラットフォーム（フォールバック）",
        version="1.0.0"
    )
    
    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 静的ファイルの設定
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Static files mounted (fallback)")
    except Exception as static_error:
        print(f"⚠️ Static files mount failed: {static_error}")
    
    # Laravel風のルーティング設定
    try:
        from routes.web import router as web_router
        app.include_router(web_router)
        print("✅ Laravel-style web routes loaded (fallback)")
    except ImportError as e:
        print(f"❌ Failed to load web routes: {e}")
    
    return app

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 app_gradio_root.py started!")
    print(f"🔍 sys.argv: {sys.argv}")
    
    # SPACE_ID環境変数をチェック
    space_id = os.getenv('SPACE_ID')
    if space_id:
        print(f"🔍 SPACE_ID環境変数: {space_id}")
        print("🤗 Hugging Face Spaces環境で実行中")
    else:
        print("💻 ローカル環境で実行中")
    
    print(f"🔍 Current working directory: {os.getcwd()}")
    
    # 環境固有の設定
    if space_id:
        print("🚀 アプリケーションを開始しています...")
        # Hugging Face Spaces環境
        host = "0.0.0.0"
        port = 7860
        reload = False
    else:
        print("🔧 開発環境でアプリケーションを開始...")
        # 開発環境
        host = "0.0.0.0"
        port = 7860
        reload = True
    
    # アプリケーションを作成
    app = create_gradio_root_app()
    
    print("🌐 Starting uvicorn server...")
    print(f"📍 ホスト: {host}, ポート: {port}")
    if reload:
        print("📍 開発モード: ホットリロードが有効です")
    
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            reload_dirs=["/workspaces/fastapi_django_main_live"] if reload else None
        )
    except Exception as e:
        print(f"❌ サーバー起動エラー: {e}")
        import traceback
        traceback.print_exc()
