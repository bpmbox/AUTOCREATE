#!/usr/bin/env python3
"""
チャット機能テスト用 FastAPI + Gradio アプリ
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPIアプリの作成
app = FastAPI(
    title="🎯 AUTOCREATE チャットテスト",
    description="Laravel風 AI開発プラットフォーム - チャット機能テスト版",
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
async def root():
    return {
        "message": "🎯 AUTOCREATE チャットテスト サーバー",
        "status": "✅ 動作中",
        "available_endpoints": [
            "/",
            "/api/status",
            "/api/chat",
            "/automation/trigger"
        ],
        "chat_interfaces": [
            "gra_01_chat",
            "gra_02_openInterpreter", 
            "gra_05_files",
            "gra_08_hasula"
        ]
    }

@app.get("/api/status")
async def status():
    return {
        "server": "running",
        "chat_system": "active",
        "time": "2025-06-28"
    }

@app.post("/api/chat")
async def chat_endpoint(message: dict):
    """簡単なチャットエンドポイント"""
    user_message = message.get("message", "")
    
    return {
        "user_message": user_message,
        "ai_response": f"📝 受信しました: {user_message}",
        "timestamp": "2025-06-28 18:45:00",
        "system": "Laravel風 AI チャット"
    }

@app.post("/automation/trigger")
async def automation_trigger(data: dict):
    """自動化トリガーエンドポイント"""
    return {
        "status": "triggered",
        "data": data,
        "message": "🚀 自動化システムがトリガーされました"
    }

# Gradio インターフェースを追加
try:
    import gradio as gr
    
    def chat_function(message, history):
        """Gradio チャット関数"""
        response = f"🤖 AI応答: {message}"
        history.append([message, response])
        return "", history
    
    # Gradio ChatInterface
    chat_interface = gr.ChatInterface(
        fn=chat_function,
        title="🎯 AUTOCREATE AI チャット",
        description="Laravel風 AI開発プラットフォーム - チャット機能",
    )
    
    # FastAPIにGradioをマウント
    app = gr.mount_gradio_app(app, chat_interface, path="/chat")
    print("✅ Gradio チャットインターフェースを追加しました")
    
except ImportError:
    print("⚠️ Gradioが見つかりません。FastAPIのみで動作します。")
    print("💡 インストール: pip install gradio")

if __name__ == "__main__":
    print("🚀 チャット機能テストサーバーを起動中...")
    print("📱 アクセス URL:")
    print("   - メイン: http://localhost:8000")
    print("   - ステータス: http://localhost:8000/api/status") 
    print("   - チャット API: http://localhost:8000/api/chat")
    
    uvicorn.run(
        "chat_test_app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
