#!/usr/bin/env python3
"""
FastAPI Laravel-style Application with Gradio Integration
========================================================

Laravel風のPythonアプリケーション
改善されたGradio読み込みとデータベース接続エラー修正
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


def initialize_laravel_style_gradio():
    """Laravel風のGradio初期化"""
    try:
        # 環境変数の設定（個別起動完全防止）
        os.environ['GRADIO_ANALYTICS_ENABLED'] = 'false'
        os.environ['GRADIO_SERVER_HOST'] = '0.0.0.0'
        os.environ['GRADIO_SERVER_PORT'] = '7860'
        os.environ['GRADIO_ROOT_PATH'] = ''  # ルートパス設定（空文字でルート）

        # 自動起動を完全に無効化（強化版 + 内部メソッドオーバーライド）
        os.environ['GRADIO_AUTO_LAUNCH'] = 'false'
        os.environ['GRADIO_SHARE'] = 'false'
        os.environ['GRADIO_DISABLE_LAUNCH'] = 'true'  # 起動完全無効化
        os.environ['GRADIO_LAUNCH_PREVENT'] = 'true'  # 起動防止フラグ

        # キュー無効化環境変数を追加
        os.environ['GRADIO_ENABLE_QUEUE'] = 'false'  # キュー完全無効化
        os.environ['GRADIO_QUEUE_DISABLED'] = 'true'  # キュー無効フラグ

        # Gradioの内部起動メソッドを無効化
        import gradio as gr

        # Interface.launchメソッドを無効化
        def disabled_launch(self, *args, **kwargs):
            print(
                f"🚫 LAUNCH PREVENTED for {getattr(self, 'title', 'Interface')}")
            return None

        # TabbedInterface.launchメソッドを無効化
        def disabled_tabbed_launch(self, *args, **kwargs):
            print(f"🚫 TABBED LAUNCH PREVENTED")
            return None

        # Blocks.launchメソッドを無効化
        def disabled_blocks_launch(self, *args, **kwargs):
            print(f"🚫 BLOCKS LAUNCH PREVENTED")
            return None

        # Queue メソッドも無効化
        def disabled_queue(self, *args, **kwargs):
            print(
                f"🚫 QUEUE PREVENTED for {getattr(self, 'title', 'Interface')}")
            return self  # チェインメソッドなのでselfを返す

        # 起動メソッドをオーバーライド
        if hasattr(gr.Interface, 'launch'):
            gr.Interface.launch = disabled_launch
        if hasattr(gr.TabbedInterface, 'launch'):
            gr.TabbedInterface.launch = disabled_tabbed_launch
        if hasattr(gr.Blocks, 'launch'):
            gr.Blocks.launch = disabled_blocks_launch

        # Queueメソッドをオーバーライド
        if hasattr(gr.Interface, 'queue'):
            gr.Interface.queue = disabled_queue
        if hasattr(gr.TabbedInterface, 'queue'):
            gr.TabbedInterface.queue = disabled_queue
        if hasattr(gr.Blocks, 'queue'):
            gr.Blocks.queue = disabled_queue

        print("🚀 Initializing Laravel-style Gradio (LAUNCH & QUEUE PREVENTION MODE)...")
        print("⚠️  INDIVIDUAL LAUNCHES COMPLETELY DISABLED!")
        print("⚠️  QUEUE METHODS COMPLETELY DISABLED!")
        print("🔒 Gradio launch & queue methods OVERRIDDEN!")

        # データベース初期化
        from database.init_databases import create_databases
        missing_dbs = check_missing_databases()
        if missing_dbs:
            print(f"⚠️ Missing databases: {missing_dbs}")
            create_databases()
            print("✅ Databases initialized successfully")
        else:
            print("✅ All databases are present")

        # Laravel風Controller経由でGradio初期化
        from routes.web import initialize_gradio_with_error_handling
        tabbed_interface = initialize_gradio_with_error_handling()

        # 追加のキュー無効化処理（フロントエンド側も対応）
        try:
            # Gradioの内部設定でキューを完全無効化
            if hasattr(tabbed_interface, 'config'):
                if isinstance(tabbed_interface.config, dict):
                    tabbed_interface.config['enable_queue'] = False
                    print("✅ Frontend queue disabled via config")

            # イベントハンドラのキューも無効化
            for tab in getattr(tabbed_interface, 'interface_list', []):
                if hasattr(tab, 'enable_queue'):
                    tab.enable_queue = False
                if hasattr(tab, '_queue'):
                    tab._queue = None
            print("✅ All tab queues disabled")
        except Exception as config_error:
            print(f"⚠️ Additional queue config warning: {config_error}")

        print("✅ Laravel-style Gradio initialization completed")

        # 統合起動専用の復元関数を定義
        def restore_launch_for_unified():
            """統合起動時のみlaunchメソッドを復元（queueは復元しない）"""
            import gradio as gr

            # 元のlaunchメソッドを復元（バックアップから）
            if hasattr(gr.Interface, '_original_launch'):
                gr.Interface.launch = gr.Interface._original_launch
            if hasattr(gr.TabbedInterface, '_original_launch'):
                gr.TabbedInterface.launch = gr.TabbedInterface._original_launch
            if hasattr(gr.Blocks, '_original_launch'):
                gr.Blocks.launch = gr.Blocks._original_launch

            # queueメソッドは復元しない（常に無効のまま）
            print("🔓 Launch methods RESTORED (queue methods stay DISABLED)")

        # 元のlaunchメソッドをバックアップ（queueはバックアップしない）
        if not hasattr(gr.Interface, '_original_launch'):
            gr.Interface._original_launch = gr.Interface.launch
        if not hasattr(gr.TabbedInterface, '_original_launch'):
            gr.TabbedInterface._original_launch = gr.TabbedInterface.launch
        if not hasattr(gr.Blocks, '_original_launch'):
            gr.Blocks._original_launch = gr.Blocks.launch

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
            inputs=gr.Textbox(label="Error Details",
                              value="Gradio initialization failed"),
            outputs=gr.Textbox(label="Status"),
            title="🚨 Gradio Setup Error"
        )

        # キュー設定は個別インスタンスでは行わない
        print("⚠️ Fallback interface created - NO QUEUE SETUP")

        return fallback_interface


def create_fastapi_with_gradio():
    """GradioをルートにマウントしたLaravel風アプリケーションを作成"""
    print("🔄 Creating Laravel-style Gradio application (Gradio at root)...")

    # まずGradioインターフェースを作成
    try:
        print("🔄 Starting unified Gradio interface collection...")
        tabbed_interface = initialize_laravel_style_gradio()

        if tabbed_interface is None:
            raise Exception("Failed to create tabbed interface")

        # キュー設定を完全に無効化
        try:
            print("🚫 Disabling ALL queue functionality...")
            if hasattr(tabbed_interface, 'enable_queue'):
                tabbed_interface.enable_queue = False
                print("✅ App: enable_queue set to False")

            # TabbedInterfaceのキューを適切に初期化
            if not hasattr(tabbed_interface, '_queue'):
                tabbed_interface._queue = None
                print("✅ App: _queue initialized as None")

            # 各インターフェースのキューも無効化
            if hasattr(tabbed_interface, 'interface_list'):
                for interface in tabbed_interface.interface_list:
                    if hasattr(interface, 'enable_queue'):
                        interface.enable_queue = False
                    if not hasattr(interface, '_queue'):
                        interface._queue = None
                print(
                    f"✅ App: All {len(tabbed_interface.interface_list)} interfaces queue disabled")

            print("⚠️ App: NO queue() method called - completely disabled")

        except Exception as queue_error:
            print(f"⚠️ App: Queue disable warning: {queue_error}")

        # 直接FastAPIアプリを作成し、そこにGradioをマウント
        try:
            print("🔄 Creating Gradio FastAPI app for root path mounting...")

            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware

            # 新しいFastAPIアプリを作成
            gradio_app = FastAPI(
                title="🚀 AI Development Platform - Laravel風統合システム",
                description="Laravel風のGradio統合プラットフォーム - ルートパスでGradio動作",
                version="1.0.0"
            )

            # CORS設定を追加
            gradio_app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            print("✅ FastAPI app created and CORS configured")

            # 静的ファイルの設定
            from fastapi.staticfiles import StaticFiles
            import mimetypes

            try:
                # MIME type設定
                mimetypes.add_type('text/css', '.css')
                mimetypes.add_type('application/javascript', '.js')
                mimetypes.add_type('application/json', '.json')

                gradio_app.mount(
                    "/static", StaticFiles(directory="static"), name="static")
                print("✅ Static files mounted at /static on Gradio app")
            except Exception as static_error:
                print(f"⚠️ Static files mount failed: {static_error}")

            # Laravel風のルーティングをAPIエンドポイントとして追加
            try:
                from routes.web import router as web_router
                gradio_app.include_router(web_router, prefix="/api")
                print("✅ Laravel-style web routes loaded at /api on Gradio app")
            except ImportError as e:
                print(f"⚠️ Web routes not loaded: {e}")

            # 追加のAPIエンドポイント（Laravel風）
            try:
                # データベース関連のAPIルート
                from fastapi import APIRouter
                laravel_api = APIRouter(
                    prefix="/laravel", tags=["Laravel API"])

                @laravel_api.get("/status")
                async def laravel_status():
                    return {
                        "status": "success",
                        "message": "Laravel-style API is working with Gradio",
                        "gradio_mounted": True,
                        "gradio_path": "/",
                        "app_mode": "full_laravel_gradio",
                        "endpoints": [
                            "/api/*",
                            "/laravel/status",
                            "/laravel/db-status"
                        ]
                    }

                @laravel_api.get("/db-status")
                async def database_status():
                    try:
                        missing_dbs = check_missing_databases()
                        return {
                            "status": "success",
                            "databases": {
                                "missing": missing_dbs,
                                "total_required": 6,
                                "available": 6 - len(missing_dbs)
                            }
                        }
                    except Exception as e:
                        return {
                            "status": "error",
                            "message": str(e)
                        }

                gradio_app.include_router(laravel_api)
                print("✅ Laravel-style API endpoints added")

            except Exception as api_error:
                print(f"⚠️ Laravel API setup failed: {api_error}")

            # GradioインターフェースをFastAPIにマウント（ルートパス）
            import gradio as gr
            gradio_app = gr.mount_gradio_app(
                gradio_app, tabbed_interface, path="/")
            print("✅ Gradio mounted to FastAPI app at root path /")

            print("🚀 ✅ Gradio mounted at ROOT (/) with Laravel-style features!")
            return gradio_app

        except Exception as create_error:
            print(f"❌ Gradio app creation failed: {create_error}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"❌ Failed to create Gradio-first app: {e}")
        import traceback
        traceback.print_exc()

    # フォールバック: 通常のFastAPIアプリを返す
    print("⚠️ Falling back to standard FastAPI app with Laravel features")

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="AI Development Platform (Laravel Fallback)",
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
    from fastapi.staticfiles import StaticFiles
    import mimetypes

    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('application/json', '.json')

    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Static files mounted (fallback)")
    except Exception as static_error:
        print(f"⚠️ Static files mount failed: {static_error}")

    # Laravel風のルーティング設定
    try:
        from routes.web import router as web_router
        app.include_router(web_router, prefix="/api")
        print("✅ Laravel-style web routes loaded at /api (fallback)")
    except ImportError as e:
        print(f"❌ Failed to load web routes: {e}")

    # フォールバック用のエンドポイント
    @app.get("/")
    async def fallback_root():
        return {
            "message": "Laravel風アプリ（フォールバック）",
            "status": "fallback"
        }

    return app


def initialize_laravel_style_gradio():
        gr.HTML("""
        <div style="text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h1>🚀 AI Development Platform</h1>
            <h2>Laravel風統合システム</h2>
            <p>✨ 15のGradioインターフェースを統合 ✨</p>
        </div>
        """)

        chatbot = gr.Chatbot(label="💬 Laravel風AIチャット", height=400)
        msg = gr.Textbox(label="メッセージ", placeholder="Laravel風AIに質問してください...")
        send_btn = gr.Button("送信 📤", variant="primary")

        send_btn.click(simple_chat, inputs=[
                       msg, chatbot], outputs=[chatbot, msg])
        msg.submit(simple_chat, inputs=[msg, chatbot], outputs=[chatbot, msg])

        print("✅ Simple Gradio interface created successfully")

        # FastAPIアプリを作成
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI(
            title="AI Development Platform - Laravel風",
            description="Laravel風のGradio統合プラットフォーム",
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

        # GradioをFastAPIにマウント（ルートパス）
        app = gr.mount_gradio_app(app, demo, path="/")
        print("✅ Gradio mounted at root path (/) successfully")

        # 静的ファイルの設定
        from fastapi.staticfiles import StaticFiles
        try:
            app.mount("/static", StaticFiles(directory="static"), name="static")
            print("✅ Static files mounted at /static")
        except Exception as static_error:
            print(f"⚠️ Static files mount failed: {static_error}")

        # Laravel風のAPIエンドポイント
        @app.get("/api/status")
        async def api_status():
            return {
                "status": "success",
                "message": "Laravel風AI Development Platform",
                "gradio_mounted": True,
                "root_path": "/",
                "features": [
                    "📄 ドキュメント生成",
                    "🌐 HTML表示",
                    "🚀 統合管理ダッシュボード",
                    "💬 AIチャット",
                    "📁 ファイル管理"
                ]
            }

        @app.get("/api/laravel/info")
        async def laravel_info():
            return {
                "framework": "Laravel-style Python",
                "platform": "FastAPI + Gradio",
                "interfaces": 15,
                "databases": ["SQLite", "PostgreSQL"],
                "features": "AI Development Platform"
            }

        print("✅ Laravel-style API endpoints added")
        print("🚀 ✅ Laravel-style Gradio app created successfully at ROOT PATH!")

        return app

    except Exception as e:
        print(f"❌ Failed to create Laravel-style Gradio app: {e}")
        import traceback
        traceback.print_exc()
        
        # 最小限のフォールバック
        print("⚠️ Falling back to standard FastAPI app with Laravel features")
        
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(
            title="AI Development Platform (Laravel Fallback)",
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
        
        @app.get("/")
        async def fallback_root():
            return {"message": "Laravel風アプリ（フォールバック）", "status": "fallback"}
        
        @app.get("/api/status")
        async def api_status():
            return {"status": "ok", "mode": "fallback"}
        
        @app.post("/automation/trigger")
        async def automation_trigger(request: dict):
            return {"message": "自動化トリガー（フォールバック）", "received": request}
        
        return app
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 静的ファイルの設定
    from fastapi.staticfiles import StaticFiles
    import mimetypes
    
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('application/json', '.json')
    
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Static files mounted (fallback)")
    except Exception as static_error:
        print(f"⚠️ Static files mount failed: {static_error}")
    
    # Laravel風のルーティング設定
    try:
        from routes.web import router as web_router
        app.include_router(web_router, prefix="/api")
        print("✅ Laravel-style web routes loaded at /api (fallback)")
    except ImportError as e:
        print(f"❌ Failed to load web routes: {e}")
    
    return app
    
    # Gradioインターフェースをマウント（統合起動・重複防止）
    if not hasattr(app, '_gradio_mounted'):
        try:
            print("🔄 Starting unified Gradio interface collection...")
            tabbed_interface = initialize_laravel_style_gradio()
            
            # 統合起動時のみlaunchメソッドを復元
            import gradio as gr
            if hasattr(gr.TabbedInterface, '_original_launch'):
                gr.TabbedInterface.launch = gr.TabbedInterface._original_launch
                print("🔓 Launch method RESTORED for unified TabbedInterface")
            
            # キュー設定を完全に無効化（過去の設定に戻す）
            try:
                print("🚫 Disabling ALL queue functionality...")
                # キューを完全に無効化
                if hasattr(tabbed_interface, 'enable_queue'):
                    tabbed_interface.enable_queue = False
                    print("✅ App: enable_queue set to False")
                
                if hasattr(tabbed_interface, '_queue'):
                    tabbed_interface._queue = None
                    print("✅ App: _queue cleared")
                    
                # queue()メソッドも呼び出さない
                print("⚠️ App: NO queue() method called - completely disabled")
                
            except Exception as queue_error:
                print(f"⚠️ App: Queue disable warning: {queue_error}")
            
            # 安全なマウント方法（循環参照を回避）
            try:
                print("🔄 Creating safe Gradio mount...")
                
                # 1. 単純な最初のインターフェースのみをマウント（安全）
                if hasattr(tabbed_interface, 'interface_list') and tabbed_interface.interface_list:
                    first_interface = tabbed_interface.interface_list[0]
                    print(f"🎯 Using first interface: {first_interface.title}")
                    
                    # 安全なマウント方法
                    gradio_app = gr.routes.App.create_app(first_interface)
                    app.mount("/gradio", gradio_app)
                    print("✅ First interface mounted successfully")
                    
                    # 他のインターフェースも個別にマウント
                    for i, interface in enumerate(tabbed_interface.interface_list[1:], 1):
                        try:
                            mount_path = f"/gradio_{i}"
                            individual_app = gr.routes.App.create_app(interface)
                            app.mount(mount_path, individual_app)
                            print(f"✅ Interface {i} mounted at {mount_path}")
                        except Exception as individual_error:
                            print(f"⚠️ Individual interface {i} mount failed: {individual_error}")
                else:
                    print("❌ No interfaces available for mounting")
                    
            except Exception as mount_error:
                print(f"❌ Safe mount failed: {mount_error}")
                # 最後の手段：非常に簡単なインターフェース
                try:
                    def simple_test(text):
                        return f"Echo: {text}"
                    
                    simple_interface = gr.Interface(
                        fn=simple_test,
                        inputs=gr.Textbox(label="Input"),
                        outputs=gr.Textbox(label="Output"),
                        title="🚀 Simple Test Interface"
                    )
                    
                    simple_app = gr.routes.App.create_app(simple_interface)
                    app.mount("/gradio", simple_app)
                    print("✅ Emergency simple interface mounted")
                except Exception as emergency_error:
                    print(f"❌ Emergency mount also failed: {emergency_error}")
            
            app._gradio_mounted = True  # 重複防止フラグ
            
            print("� ✅ SAFE Gradio mounted at /gradio (avoiding circular references)!")
        except Exception as e:
            print(f"❌ Failed to mount Gradio: {e}")
    else:
        print("⚠️ Gradio already mounted - preventing duplicate mount")

    return app

def test_laravel_gradio_integration():
    """Laravel風のGradio統合をテスト"""
    print("🚀 Testing Laravel-style Gradio Integration...")
    print("="*50)
    
    # 1. データベース接続テスト
    print("\n1. Database Connection Test:")
    try:
        from config.database import get_db_connection, DATABASE_PATHS
        for db_name, db_path in DATABASE_PATHS.items():
            exists = os.path.exists(db_path)
            status = "✅ EXISTS" if exists else "❌ MISSING"
            print(f"   {db_name}: {status}")
        
        # 接続テスト
        conn = get_db_connection('chat_history')
        conn.close()
        print("   ✅ Database connection successful")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    # 2. Laravel風Controller テスト
    print("\n2. Laravel-style Controller Test:")
    try:
        from app.Http.Controllers.Gradio.GradioController import GradioController
        controller = GradioController()
        print("   ✅ GradioController loaded successfully")
        print(f"   Controller type: {type(controller)}")
    except Exception as e:
        print(f"   ❌ Controller error: {e}")
    
    # 3. Gradio初期化テスト
    print("\n3. Gradio Initialization Test:")
    try:
        interface = initialize_laravel_style_gradio()
        print(f"   ✅ Gradio interface created: {type(interface)}")
    except Exception as e:
        print(f"   ❌ Gradio initialization error: {e}")
    
    # 4. FastAPI統合テスト
    print("\n4. FastAPI Integration Test:")
    try:
        app = create_fastapi_with_gradio()
        print(f"   ✅ FastAPI app created: {type(app)}")
        print(f"   Routes count: {len(app.routes)}")
    except Exception as e:
        print(f"   ❌ FastAPI integration error: {e}")
    
    print("\n" + "="*50)
    print("🎯 Laravel-style Gradio Integration Test Completed!")

def test_connections():
    """データベースとAPI接続をテスト"""
    print("🔍 Connection Testing Started...")
    print("=" * 50)
    
    # 環境変数確認
    print("📋 Environment Variables Check:")
    important_vars = [
        'GROQ_API_KEY', 'POSTGRES_URL', 'LINE_CHANNEL_ACCESS_TOKEN',
        'GITHUB_TOKEN', 'DATABASE_URL'
    ]
    
    for var in important_vars:
        value = os.getenv(var)
        if value:
            # APIキーなどは最初と最後の数文字のみ表示
            if 'key' in var.lower() or 'token' in var.lower():
                display_value = f"{value[:8]}...{value[-8:]}" if len(value) > 16 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: Not set")
    
    print("\n🗄️ Database Connection Test:")
    try:
        # SQLiteデータベーステスト
        from config.database import get_db_connection, DATABASE_PATHS
        
        # データベースディレクトリの存在確認
        db_dir = os.path.dirname(list(DATABASE_PATHS.values())[0])
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"  📁 Created database directory: {db_dir}")
        
        # データベース初期化
        from database.init_databases import main as init_db
        init_db()
        print("  ✅ Database initialization completed")
        
        # 接続テスト
        conn = get_db_connection('chat_history')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
        table_count = cursor.fetchone()[0]
        conn.close()
        print(f"  ✅ SQLite connection successful - {table_count} tables found")
        
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
    
    print("\n🌐 Laravel-style Gradio Test:")
    try:
        from app.Http.Controllers.Gradio.GradioController import GradioController
        controller = GradioController()
        print("  ✅ GradioController imported successfully")
        
        # 簡単なインターフェーステスト
        interface = controller.create_main_interface()
        print(f"  ✅ Main interface created: {type(interface)}")
        
    except Exception as e:
        print(f"  ❌ Gradio controller test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🔗 API Connection Test:")
    try:
        import requests
        
        # 簡単なHTTPテスト（Google API）
        response = requests.get("https://www.googleapis.com/", timeout=5)
        if response.status_code == 200:
            print("  ✅ Internet connection working")
        else:
            print(f"  ⚠️ Internet connection issue: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Internet connection test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Connection test completed!")

# デバッグサーバーの設定
def setup_debug_server():
    """デバッグサーバーをセットアップ"""
    try:
        import debugpy
        if not debugpy.is_client_connected():
            print("🔧 デバッグサーバーを起動中...")
            debugpy.listen(("0.0.0.0", 5678))
            print("✅ デバッグサーバーがポート5678で待機中")
            print("💡 VS Codeで 'Remote Attach' を使用してアタッチできます")
        else:
            print("🔗 デバッグクライアントが既に接続されています")
    except ImportError:
        print("⚠️  debugpy がインストールされていません。通常のデバッグモードで継続します")
    except Exception as e:
        print(f"⚠️  デバッグサーバー起動エラー: {e}")

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
from groq import Groq

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Any, Coroutine, List

from starlette.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from groq import AsyncGroq, AsyncStream, Groq
from groq.lib.chat_completion_chunk import ChatCompletionChunk
from groq.resources import Models
from groq.types import ModelList
from groq.types.chat.completion_create_params import Message

import async_timeout
import asyncio
from interpreter import interpreter
import os

GENERATION_TIMEOUT_SEC = 60

if __name__ == "__main__":
    import sys
    
    print("🚀 AI Development Platform - Laravel風統合システム 起動中！")
    print(f"🔍 実行引数: {sys.argv}")
    print(f"🔍 SPACE_ID環境変数: {os.getenv('SPACE_ID')}")
    print(f"🔍 カレントディレクトリ: {os.getcwd()}")
    
    # テストモードの確認
    if "--test" in sys.argv:
        print("🧪 テストモード実行中")
        test_connections()
        sys.exit(0)
    
    # デバッグモードかどうかを判定
    is_debug = "--debug" in sys.argv or any("debugpy" in arg for arg in sys.argv)
    
    # デバッグモードの場合、デバッグサーバーをセットアップ
    if is_debug:
        setup_debug_server()
        print("🐛 デバッグモード: デバッガーアタッチ待機中...")
    
    # 実行環境の表示
    if os.getenv("SPACE_ID"):
        print("🤗 Hugging Face Spaces環境で実行中")
    else:
        print("💻 ローカル開発環境で実行中")
    
    try:
        print("🚀 Laravel風統合システムを開始しています...")
        
        # 新しい基盤システムの初期化
        print("🔧 システム監視・API基盤の初期化...")
        
        # データベース初期化
        from database.init_databases import create_databases
        missing_dbs = check_missing_databases()
        if missing_dbs:
            print(f"⚠️ 不足データベース: {missing_dbs}")
            create_databases()
            print("✅ データベース初期化完了")
        else:
            print("✅ 全データベース確認済み")
        
        # Laravel風Gradio初期化テスト
        print("🧪 Laravel風 Gradio 統合システム初期化テスト...")
        try:
            tabbed_interface = initialize_laravel_style_gradio()
            print(f"✅ Laravel風 Gradio 初期化成功: {type(tabbed_interface)}")
        except Exception as e:
            print(f"❌ Laravel風 Gradio 初期化失敗: {e}")
            import traceback
            traceback.print_exc()
        
        # 基盤システムの起動確認
        print("🔧 基盤システム起動確認...")
        print("  📊 システム監視: gra_11_system_monitor")
        print("  🌐 API基盤: routes/api.py")
        print("  🔗 Laravel風ルーティング: mysite/asgi.py")
        
        # デバッグサーバーのセットアップ
        if is_debug:
            setup_debug_server()
        
        print("🌐 Uvicornサーバー起動中...")
        print("📍 アクセスURL: http://localhost:7860")
        print("📊 システム監視: http://localhost:7863")
        print("🌐 API基盤テスト: http://localhost:8001")
        
        if is_debug:
            print("🐛 デバッグモード: リロード無効・ブレークポイント有効")
            # デバッグモード: reloadを無効にしてブレークポイントを使用可能に
            import uvicorn
            uvicorn.run(
                "mysite.asgi:app", 
                host="0.0.0.0", 
                port=7860, 
                reload=False,  # デバッグ時はリロード無効
                log_level="debug",
                access_log=True,
                use_colors=True
            )
        else:
            print("📍 開発モード: ホットリロード有効・高速開発")
            # 開発モード: reloadを有効にして高速開発
            import uvicorn
            uvicorn.run(
                "mysite.asgi:app", 
                host="0.0.0.0", 
                port=7860, 
                reload=True,  # 開発時はリロード有効
                log_level="debug",
                access_log=True,
                use_colors=True,
                reload_dirs=["/workspaces/AUTOCREATE"]
            )
            
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 トラブルシューティング:")
        print("1. 依存関係確認: pip install -r requirements.txt")
        print("2. データベース確認: python3 app.py --test")
        print("3. デバッグモード: python3 app.py --debug")
        print("4. システム監視確認: python3 app/Http/Controllers/Gradio/gra_11_system_monitor/system_monitor.py")
