#!/usr/bin/env python3
"""
超軽量版 Gradio チャット
========================
ローディング問題完全解決版
"""

import gradio as gr
from datetime import datetime

# Gradio 5.x対応のチャット関数
def chat_fn(message, history):
    """新しいGradio形式対応のチャット関数"""
    if not message:
        return ""
    
    time_str = datetime.now().strftime("%H:%M:%S")
    response = f"[{time_str}] ✅ 受信: {message}"
    
    return response

# 最小構成のインターフェース
demo = gr.ChatInterface(
    fn=chat_fn,
    title="🚀 超軽量チャット",
    description="ローディング問題解決版",
    examples=["こんにちは", "テストメッセージ", "動作確認"],
    cache_examples=False
)

if __name__ == "__main__":
    print("🚀 超軽量チャット起動中...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,  # 異なるポート使用
        share=False,
        inbrowser=False,
        show_error=True
    )
