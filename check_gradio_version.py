#!/usr/bin/env python3
"""
Gradio バージョン確認
"""

try:
    import gradio as gr
    print(f"✅ Gradio version: {gr.__version__}")
    
    # キューの仕様確認
    import inspect
    
    # Interface.queueメソッドのシグネチャを確認
    if hasattr(gr.Interface, 'queue'):
        queue_signature = inspect.signature(gr.Interface.queue)
        print(f"📋 Interface.queue signature: {queue_signature}")
    
    # TabbedInterface.queueメソッドのシグネチャを確認
    if hasattr(gr.TabbedInterface, 'queue'):
        tabbed_queue_signature = inspect.signature(gr.TabbedInterface.queue)
        print(f"📋 TabbedInterface.queue signature: {tabbed_queue_signature}")
    
    # Blocks.queueメソッドのシグネチャを確認
    if hasattr(gr.Blocks, 'queue'):
        blocks_queue_signature = inspect.signature(gr.Blocks.queue)
        print(f"📋 Blocks.queue signature: {blocks_queue_signature}")
        
    # _queue属性の存在確認
    demo = gr.Interface(fn=lambda x: x, inputs="text", outputs="text")
    print(f"🔍 Interface has _queue: {hasattr(demo, '_queue')}")
    print(f"🔍 Interface _queue value: {getattr(demo, '_queue', 'None')}")
    
    # キューメソッドの実行テスト
    try:
        demo.queue()
        print(f"✅ demo.queue() executed successfully")
        print(f"🔍 After queue() - _queue: {getattr(demo, '_queue', 'None')}")
        print(f"🔍 _queue type: {type(getattr(demo, '_queue', None))}")
    except Exception as e:
        print(f"❌ demo.queue() error: {e}")
        
    # バージョン別の処理
    version = gr.__version__
    major, minor, patch = map(int, version.split('.'))
    
    if major >= 4 and minor >= 32:
        print("🎯 Gradio 4.32+ detected - newer queue system")
    elif major >= 4 and minor >= 20:
        print("🎯 Gradio 4.20-4.31 detected - intermediate queue system")
    else:
        print("🎯 Gradio < 4.20 detected - legacy queue system")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# ファイルに書き出し
with open('/workspaces/AUTOCREATE/gradio_version_info.txt', 'w') as f:
    import sys
    import io
    
    # 標準出力をキャプチャ
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        import gradio as gr
        print(f"Gradio version: {gr.__version__}")
        
        # キューの仕様確認
        demo = gr.Interface(fn=lambda x: x, inputs="text", outputs="text")
        print(f"Interface has _queue: {hasattr(demo, '_queue')}")
        
        try:
            demo.queue()
            print(f"demo.queue() successful")
            print(f"_queue after queue(): {getattr(demo, '_queue', 'None')}")
        except Exception as e:
            print(f"demo.queue() error: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # 標準出力を元に戻してファイルに書き込み
    sys.stdout = old_stdout
    f.write(captured_output.getvalue())

print("✅ Version info written to gradio_version_info.txt")
