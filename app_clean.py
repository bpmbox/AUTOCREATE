#!/usr/bin/env python3
"""
修正版 FastAPI + Gradio チャットアプリケーション
========================================================
Gradio JavaScript エラー修正版
"""

import gradio as gr
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# FastAPIアプリ作成
app = FastAPI(title="Laravel風 Chat API", version="1.0.0")

def simple_chat_response(message, history):
    """シンプルなチャット応答"""
    if not message:
        return history, ""
    
    # 現在時刻を取得
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 簡単なレスポンス生成
    responses = [
        f"こんにちは！あなたのメッセージ「{message}」を受け取りました。",
        f"面白い質問ですね: {message}",
        f"「{message}」について考えてみましょう。",
        f"なるほど、{message}ですね。詳しく教えてください。",
        f"チャット機能が正常に動作しています！メッセージ: {message}"
    ]
    
    import random
    response = random.choice(responses)
    
    # 履歴に追加
    if history is None:
        history = []
    
    history.append([message, f"[{timestamp}] {response}"])
    
    return history, ""

# Gradioインターフェース作成（修正版）
def create_gradio_interface():
    """エラー修正版のGradioインターフェース"""
    
    with gr.Blocks(
        title="🚀 Laravel風 Chat System",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        """
    ) as interface:
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🚀 Laravel風 AI チャットシステム</h1>
            <p>修正版 - Gradio JavaScript エラー解決済み</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=4):
                chatbot = gr.Chatbot(
                    label="💬 チャット履歴",
                    height=500,
                    show_label=True,
                    container=True
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="メッセージを入力",
                        placeholder="ここにメッセージを入力してください...",
                        scale=4,
                        container=False
                    )
                    send_btn = gr.Button("送信", variant="primary", scale=1)
                
                clear_btn = gr.Button("履歴クリア", variant="secondary")
            
            with gr.Column(scale=1):
                gr.HTML("""
                <div style="padding: 20px; background: #f0f0f0; border-radius: 10px;">
                    <h3>🎯 機能テスト</h3>
                    <ul>
                        <li>✅ メッセージ送信</li>
                        <li>✅ 自動応答</li>
                        <li>✅ 履歴管理</li>
                        <li>✅ API連携</li>
                    </ul>
                </div>
                """)
        
        # イベントハンドラー
        send_btn.click(
            simple_chat_response,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        msg_input.submit(
            simple_chat_response,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        clear_btn.click(
            lambda: ([], ""),
            outputs=[chatbot, msg_input]
        )
    
    return interface

# APIエンドポイント
@app.get("/api/status")
async def get_status():
    """システム状態確認"""
    return JSONResponse({
        "status": "active",
        "message": "Laravel風チャットシステムが正常に動作中",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-fixed"
    })

@app.post("/api/chat")
async def chat_api(message: dict):
    """チャットAPI"""
    try:
        user_message = message.get("message", "")
        if not user_message:
            return JSONResponse({
                "error": "メッセージが空です",
                "success": False
            }, status_code=400)
        
        # 簡単な応答生成
        response = f"API経由で受信: {user_message}"
        
        return JSONResponse({
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
    
    except Exception as e:
        return JSONResponse({
            "error": str(e),
            "success": False
        }, status_code=500)

# Gradioアプリの作成
gradio_app = create_gradio_interface()

# FastAPIとGradioを統合
app = gr.mount_gradio_app(app, gradio_app, path="/")

if __name__ == "__main__":
    print("🚀 修正版 Laravel風チャットアプリ起動中...")
    print("📡 アクセス URL: http://localhost:7860")
    print("🔧 API エンドポイント: http://localhost:7860/api/status")
    print("💬 チャット API: http://localhost:7860/api/chat")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860,
        reload=False,  # リロード無効（安定性向上）
        log_level="info"
    )
