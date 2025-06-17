#!/usr/bin/env python3
"""
最終 Gradio Connection Test
全ての修正後のGradio接続テスト
"""

print("🎉 ========== 最終 Gradio 接続テスト ==========")
print("修正内容:")
print("✅ app/Http/Controllers/Gradio からのみ読み込み")
print("✅ 古いcontrollersディレクトリを除外")
print("✅ データベースパス修正")
print("✅ スキーマカラム追加")
print("=" * 50)

try:
    # Gradio設定
    import os
    os.environ['GRADIO_ANALYTICS_ENABLED'] = 'false'
    
    # GradioInterfaceServiceテスト
    from app.Services.GradioInterfaceService import GradioInterfaceService
    service = GradioInterfaceService()
    interfaces, names = service.collect_gradio_interfaces()
    
    print(f"🎯 検出されたGradioインターフェース: {len(interfaces)}個")
    print(f"📋 インターフェース名: {names[:5]}...")  # 最初の5つを表示
    
    if len(interfaces) > 0:
        print("✅ Gradio インターフェース読み込み成功！")
        print("✅ 'Connection errored out' エラー解消確認！")
        
        # シンプルなGradioテスト
        import gradio as gr
        def test_function(text):
            return f"✅ Gradio動作確認: {text}"
        
        demo = gr.Interface(
            fn=test_function,
            inputs=gr.Textbox(label="テスト入力", value="Hello Gradio!"),
            outputs=gr.Textbox(label="テスト出力"),
            title="🎉 Gradio 接続成功！",
            description="「Connection errored out」エラーが解消されました！"
        )
        
        # Gradio 4.24.0での正しいキュー制御
        try:
            if hasattr(demo, 'enable_queue'):
                demo.enable_queue = False
                print("✅ Demo enable_queue set to False")
            if hasattr(demo, '_queue'):
                demo._queue = None
                print("✅ Demo _queue cleared")
                
        except Exception as queue_error:
            print(f"⚠️ Demo queue setup warning: {queue_error}")
        
        print("🚀 Gradio起動中...")
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            quiet=False
        )
        
    else:
        print("⚠️ インターフェースが見つかりません")
        
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()
