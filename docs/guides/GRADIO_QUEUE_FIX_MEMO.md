# Gradio キューエラー解決メモ

## 問題
- Gradio 4.31.5で「Event not found in queue」エラーが頻発
- キューの初期化順序や設定方法が複雑

## 解決方法
**Gradio 4.24.0にダウングレード** することで問題解決

```bash
pip install gradio==4.24.0
```

## バージョン固定
requirements.txtで以下のように固定：

```
gradio==4.24.0
```

## Gradio 4.24.0での正しいキュー無効化方法

### 1. Interface/TabbedInterface作成時
```python
demo = gr.Interface(...)

# キュー無効化
if hasattr(demo, 'enable_queue'):
    demo.enable_queue = False
if hasattr(demo, '_queue'):
    demo._queue = None
```

### 2. launch()時の設定
```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    quiet=False
    # enable_queue=False は 4.24.0では不要
)
```

## 適用箇所
以下のファイルで修正済み：

1. `app/Services/GradioInterfaceService.py`
   - `_process_interface()` メソッド
   - `create_tabbed_interface()` メソッド

2. `final_gradio_test.py`
   - テスト用インターフェースのキュー無効化

3. `gradio_simple_test.py`
   - シンプルテスト用スクリプト

4. `app/Http/Controllers/Gradio/GradioController.py`
   - メインインターフェース作成時のキュー無効化
   - setup_gradio_interfaces()メソッド

5. `requirements.txt`
   - gradio==4.24.0 に固定

## 結果
✅ 「Event not found in queue」エラーが解消
✅ Gradioインターフェースが正常に動作
✅ FastAPI + Gradio統合が安定動作

## 今後の注意
- Gradio 4.25以降にアップデートする際は、キューシステムの変更に注意
- 新しいバージョンでテストしてから本番適用すること
