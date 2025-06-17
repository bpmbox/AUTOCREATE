#!/usr/bin/env python3
"""
Simple FastAPI + Gradio Mount Application
========================================
Laravel風フォルダー構成からGradioを取得してapp.mountで統合
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def get_laravel_gradio_interfaces():
    """Laravel風のフォルダー構成からGradioインターフェースを取得"""
    try:
        print("🔄 Loading Gradio interfaces from Laravel structure...")
        
        # GradioControllerからタブ付きインターフェースを取得
        from app.Http.Controllers.Gradio.GradioController import GradioController
        controller = GradioController()
        
        # タブ付きインターフェースを作成
        tabbed_interface = controller.create_tabbed_interface()
        print("✅ Laravel-style tabbed interface created")
        
        # ルートパス動作のためキューを有効化
        try:
            tabbed_interface.queue()
            print("✅ Queue enabled for root path operation")
        except Exception as queue_error:
            print(f"⚠️ Queue setup warning: {queue_error}")
        
        return tabbed_interface
        
    except Exception as e:
        print(f"⚠️ Failed to load Laravel Gradio interfaces: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック: シンプルなインターフェース
        def simple_chat(message, history):
            if not message:
                return history
            
            response = f"Laravel風AIが応答: {message}"
            history = history or []
            history.append([message, response])
            return history
        
        # シンプルなチャットインターフェース
        demo = gr.ChatInterface(
            fn=simple_chat,
            title="🚀 AI Development Platform (Fallback)",
            description="Laravel風統合システム - フォールバックモード"
        )
        
        # フォールバックでもキューを有効化
        demo.queue()
        print("✅ Fallback chat interface with queue enabled")
        
        return demo
        demo = gr.ChatInterface(
            fn=simple_chat,
            title="🚀 Laravel風 AI Platform",
            description="シンプルなGradioインターフェース（フォールバック）"
        )
        print("✅ Fallback Gradio interface created")
        return demo

def create_fastapi_app():
    """FastAPIアプリケーションを作成"""
    print("🚀 Creating FastAPI application...")
    
    # FastAPIアプリを作成
    app = FastAPI(
        title="🚀 Laravel風 AI Development Platform",
        description="Laravel風フォルダー構成 + Gradio統合",
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
    print("✅ CORS middleware added")
    
    # Laravel風のGradioインターフェースを取得
    gradio_interface = get_laravel_gradio_interfaces()
    
    # Gradioをルートパス（/）にマウント
    print("🔄 Mounting Gradio to root path...")
    app = gr.mount_gradio_app(app, gradio_interface, path="/")
    print("✅ Gradio mounted at root path (/)")
    
    # APIエンドポイントを追加
    @app.get("/api/status")
    async def api_status():
        return {
            "status": "success",
            "message": "Laravel風 FastAPI + Gradio app is running",
            "gradio_mounted": True,
            "mount_path": "/"
        }
    
    print("✅ FastAPI app with mounted Gradio created")
    return app

# アプリケーションを作成
app = create_fastapi_app()

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Laravel風 FastAPI + Gradio application...")
    print("📍 Gradio mounted at root path: http://0.0.0.0:7860/")
    print("📍 API status: http://0.0.0.0:7860/api/status")
    
    uvicorn.run(
        "app_simple_mount:app",
        host="0.0.0.0",
        port=7860,
        reload=True,
        log_level="info"
    )
