#!/usr/bin/env python3
"""
軽量版 Gradio チャットアプリケーション
========================================================
ローディング問題解決版
"""

import gradio as gr
import random
from datetime import datetime

def simple_chat(message, history):
    """軽量なチャット応答"""
    if not message or not message.strip():
        return history, ""
    
    # タイムスタンプ
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # シンプルな応答
    responses = [
        f"✅ メッセージ受信: {message}",
        f"🤖 応答しました: {message}",
        f"💬 チャット機能テスト完了",
        f"🚀 システム正常動作中",
        f"📝 入力内容: {message}"
    ]
    
    response = random.choice(responses)
    
    # 履歴更新
    if history is None:
        history = []
    
    history.append([message, f"[{timestamp}] {response}"])
    
    return history, ""

# シンプルなGradioインターフェース
with gr.Blocks(
    title="軽量チャット",
    theme=gr.themes.Default()
) as app:
    
    gr.Markdown("# 🚀 軽量版チャットシステム")
    gr.Markdown("ローディング問題解決版")
    
    with gr.Column():
        chatbot = gr.Chatbot(
            label="チャット",
            height=400,
            type="tuples",
            show_copy_button=True
        )
        
        with gr.Row():
            msg = gr.Textbox(
                placeholder="メッセージを入力...",
                container=False,
                scale=4
            )
            submit = gr.Button("送信", variant="primary", scale=1)
        
        clear = gr.Button("クリア", variant="secondary")
    
    # イベント設定
    submit.click(simple_chat, [msg, chatbot], [chatbot, msg])
    msg.submit(simple_chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: ([], ""), outputs=[chatbot, msg])

if __name__ == "__main__":
    print("🚀 軽量チャットアプリ起動中...")
    print("📡 URL: http://localhost:7860")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_error=True,
        quiet=False,
        inbrowser=False  # 自動ブラウザ起動を無効
    )
