#!/usr/bin/env python3
"""
FastAPI Laravel-style Application with Gradio Integration
========================================================

Laravel風のPythonアプリケーション - 修正版
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


def simple_chat(message, history):
    """シンプルなチャット機能"""
    if not message:
        return history, ""
    
    # 簡単なエコー応答
    response = f"🤖 AI Laravel風システム: {message}への応答です"
    history.append([message, response])
    return history, ""


def create_gradio_interface():
    """Gradioインターフェースを作成"""
    with gr.Blocks(title="🚀 AI Development Platform - Laravel風統合システム") as demo:
        gr.HTML("""
        <div style="text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h1>🚀 AI Development Platform</h1>
            <h2>Laravel風統合システム</h2>
            <p>✨ チャット機能テスト ✨</p>
        </div>
        """)

        chatbot = gr.Chatbot(label="💬 Laravel風AIチャット", height=400)
        msg = gr.Textbox(label="メッセージ", placeholder="Laravel風AIに質問してください...")
        send_btn = gr.Button("送信 📤", variant="primary")

        send_btn.click(simple_chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
        msg.submit(simple_chat, inputs=[msg, chatbot], outputs=[chatbot, msg])

    return demo


def create_fastapi_app():
    """FastAPIアプリケーションを作成"""
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

    # API エンドポイント
    @app.get("/api/status")
    async def api_status():
        return {
            "status": "success",
            "message": "Laravel風AI Development Platform",
            "gradio_mounted": True,
            "features": [
                "💬 AIチャット",
                "🚀 統合管理ダッシュボード",
                "📁 ファイル管理"
            ]
        }

    @app.get("/api/chat")
    async def chat_api():
        return {
            "message": "Chat API is working",
            "endpoints": {
                "chat": "/api/chat",
                "gradio": "/"
            }
        }

    # Gradioインターフェースをマウント
    try:
        gradio_interface = create_gradio_interface()
        app = gr.mount_gradio_app(app, gradio_interface, path="/")
        print("✅ Gradio mounted at root path (/) successfully")
    except Exception as e:
        print(f"❌ Gradio mount failed: {e}")
        
        @app.get("/")
        async def fallback_root():
            return {
                "message": "Laravel風アプリ（フォールバック）",
                "status": "gradio_mount_failed",
                "error": str(e)
            }

    return app


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 AI Development Platform - Laravel風統合システム 起動中！")
    
    try:
        # アプリケーション作成
        app = create_fastapi_app()
        
        print("🌐 Uvicornサーバー起動中...")
        print("📍 アクセスURL: http://localhost:7860")
        print("🔗 API Status: http://localhost:7860/api/status")
        print("💬 Chat API: http://localhost:7860/api/chat")
        
        # サーバー起動
        uvicorn.run(
            app,
            host="0.0.0.0", 
            port=7860, 
            reload=False,
            log_level="info"
        )
            
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()
