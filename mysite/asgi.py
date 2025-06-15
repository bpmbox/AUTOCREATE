import os
import sys
from django.core.asgi import get_asgi_application

# Laravel風のGradio統合のためのパス追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django_application = get_asgi_application()

# Laravel風のGradio統合を直接実装
sys.path.append('/workspaces/AUTOCREATE')

try:
    print("🚀 Starting Laravel-style Gradio application...")
    
    # FastAPIアプリを作成
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(
        title="🚀 AI Development Platform - Laravel風統合システム",
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
    
    # Laravel風のルーティング（routes/web.py）を追加
    try:
        from routes.web import router as web_router
        app.include_router(web_router, prefix="/api")
        print("✅ Laravel-style web routes loaded")
    except ImportError as e:
        print(f"⚠️ Web routes not loaded: {e}")
    
    # app/Http/Controllers/GradioからGradioインターフェースを取得
    print("🔄 Loading Gradio interfaces from Laravel-style structure...")
    
    # 手動で1個ずつインターフェースを追加
    gradio_interfaces = []
    tab_names = []
    
    # 1. Chat インターフェース (手動追加)
    try:
        print("🔄 Loading Chat interface...")
        from app.Http.Controllers.Gradio.gra_01_chat.Chat import gradio_interface as chat_interface
        gradio_interfaces.append(chat_interface)
        tab_names.append("💬 AIチャット")
        print("✅ Chat interface loaded")
    except Exception as e:
        print(f"❌ Failed to load Chat interface: {e}")
    
    # 2. Files インターフェース (手動追加)
    try:
        print("🔄 Loading Files interface...")
        from app.Http.Controllers.Gradio.gra_05_files.files import gradio_interface as files_interface
        gradio_interfaces.append(files_interface)
        tab_names.append("📁 ファイル管理")
        print("✅ Files interface loaded")
    except Exception as e:
        print(f"❌ Failed to load Files interface: {e}")
    
    # 3. GitHub Issue自動生成 インターフェース (手動追加)
    try:
        print("🔄 Loading GitHub Issue Automation interface...")
        from app.Http.Controllers.Gradio.gra_03_programfromdocs.github_issue_automation import gradio_interface as github_interface
        gradio_interfaces.append(github_interface)
        tab_names.append("🤖 GitHub Issue自動生成")
        print("✅ GitHub Issue Automation interface loaded")
    except Exception as e:
        print(f"❌ Failed to load GitHub Issue Automation interface: {e}")
    
    # TabbedInterfaceを手動で作成
    if gradio_interfaces:
        import gradio as gr
        tabbed_interface = gr.TabbedInterface(gradio_interfaces, tab_names)
        print(f"✅ TabbedInterface created with {len(gradio_interfaces)} interfaces")
    else:
        # フォールバック: シンプルなインターフェース
        def simple_chat(message, history):
            return f"Echo: {message}"
        
        simple_interface = gr.ChatInterface(
            fn=simple_chat,
            title="🚀 Laravel風AIプラットフォーム"
        )
        tabbed_interface = gr.TabbedInterface([simple_interface], ["💬 シンプルチャット"])
        print("⚠️ Using fallback simple interface")
    
    # キューを有効化（ルートパスで動作させるため）
    print("🔄 Enabling queue for root path operation...")
    tabbed_interface.queue()
    print("✅ Queue enabled")
    
    # Gradioをルートパス（/）にマウント
    import gradio as gr
    app = gr.mount_gradio_app(app, tabbed_interface, path="/")
    print("🚀 ✅ Gradio mounted at root path (/) with Laravel-style features!")
    
except Exception as e:
    print(f"❌ Failed to create Laravel-style Gradio app: {e}")
    import traceback
    traceback.print_exc()
    
    # フォールバック: 基本的なFastAPIアプリ
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(
        title="AI Development Platform (Fallback)",
        description="Laravel風のプラットフォーム（フォールバック）"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def fallback_root():
        return {
            "message": "Fallback mode - Gradio integration failed",
            "status": "fallback"
        }
    
    print("⚠️ Using fallback FastAPI app")
