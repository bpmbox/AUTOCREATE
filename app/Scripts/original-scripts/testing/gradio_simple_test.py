#!/usr/bin/env python3
"""
Gradio 4.24.0 対応のシンプルテスト
"""

import gradio as gr
import os

# 環境変数設定
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'false'

def test_function(text):
    return f"✅ Test successful with Gradio 4.24.0: {text}"

# インターフェース作成
demo = gr.Interface(
    fn=test_function,
    inputs=gr.Textbox(label="入力", value="Hello Gradio 4.24.0!"),
    outputs=gr.Textbox(label="出力"),
    title="🎉 Gradio 4.24.0 キューエラー修正テスト"
)

# Gradio 4.24.0での正しいキュー制御
try:
    if hasattr(demo, 'enable_queue'):
        demo.enable_queue = False
        print("✅ Queue disabled via enable_queue")
    if hasattr(demo, '_queue'):
        demo._queue = None
        print("✅ _queue cleared")
except Exception as e:
    print(f"⚠️ Queue setup warning: {e}")

print("🚀 Starting Gradio 4.24.0...")

# launch() - Gradio 4.24.0では enable_queueパラメータが使えるかもしれない
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    quiet=False
)
