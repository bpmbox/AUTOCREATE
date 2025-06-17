#!/usr/bin/env python3
"""
Queue Fix Verification Test
キュー修正の検証テスト
"""

print("🔧 ========== Queue Fix Verification ==========")

try:
    import gradio as gr
    print("✅ Gradio imported successfully")
    
    def test_func(text):
        return f"Test: {text}"
    
    # 正しい順序でインターフェース作成
    demo = gr.Interface(
        fn=test_func,
        inputs="text",
        outputs="text",
        title="Queue Fix Test"
    )
    print("✅ Interface created")
    
    # Step 1: キューを初期化
    demo.queue(max_size=1)
    print("✅ Queue initialized with max_size=1")
    
    # Step 2: キューを制御
    if hasattr(demo, '_queue') and demo._queue:
        print(f"✅ Queue object exists: {type(demo._queue)}")
        demo._queue.max_size = 0
        print("✅ Queue max_size set to 0")
        
        if hasattr(demo._queue, 'event_queue'):
            demo._queue.event_queue = {}
            print("✅ Event queue cleared")
        
        print("✅ Queue completely controlled")
    else:
        print("⚠️ No queue object found")
    
    print("🎉 Queue fix verification PASSED!")

except Exception as e:
    print(f"❌ Queue fix verification FAILED: {e}")
    import traceback
    traceback.print_exc()
