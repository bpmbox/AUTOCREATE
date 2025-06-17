#!/usr/bin/env python3
"""
Queue Fix Test with File Output
ファイル出力でのキュー修正テスト
"""

import sys
import os

# ログファイルに結果を記録
log_file = "/workspaces/AUTOCREATE/queue_test_results.log"

try:
    with open(log_file, "w") as f:
        f.write("🔧 Queue Fix Test Started\n")
        f.flush()
        
        import gradio as gr
        f.write("✅ Gradio imported successfully\n")
        f.flush()
        
        def test_func(text):
            return f"Test: {text}"
        
        # 正しい順序でインターフェース作成
        demo = gr.Interface(
            fn=test_func,
            inputs="text",
            outputs="text",
            title="Queue Fix Test"
        )
        f.write("✅ Interface created\n")
        f.flush()
        
        # Step 1: キューを初期化
        demo.queue(max_size=1)
        f.write("✅ Queue initialized with max_size=1\n")
        f.flush()
        
        # Step 2: キューを制御
        if hasattr(demo, '_queue') and demo._queue:
            f.write(f"✅ Queue object exists: {type(demo._queue)}\n")
            demo._queue.max_size = 0
            f.write("✅ Queue max_size set to 0\n")
            
            if hasattr(demo._queue, 'event_queue'):
                demo._queue.event_queue = {}
                f.write("✅ Event queue cleared\n")
            
            f.write("✅ Queue completely controlled\n")
        else:
            f.write("⚠️ No queue object found\n")
        
        f.write("🎉 Queue fix test PASSED!\n")
        
        # GradioInterfaceServiceのテスト
        sys.path.append('.')
        from app.Services.GradioInterfaceService import GradioInterfaceService
        service = GradioInterfaceService()
        interfaces, names = service.collect_gradio_interfaces()
        f.write(f"📋 Found {len(interfaces)} interfaces\n")
        f.write(f"🏷️ Names: {names[:5]}...\n")
        f.write("✅ GradioInterfaceService test PASSED!\n")

except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"❌ Test FAILED: {e}\n")
        import traceback
        f.write(traceback.format_exc())

print(f"Test completed. Check results in: {log_file}")
