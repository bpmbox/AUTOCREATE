def load_prompt_to_textbox(evt: gr.SelectData):
    """テーブルクリック時にプロンプト内容をテキストボックスに読み込む"""
    try:
        print(f"🖱️ テーブルクリック検出: {evt.index}")
        
        if evt.index is not None and len(evt.index) >= 1:
            row_index = evt.index[0]
            print(f"📍 クリック行インデックス: {row_index}")
            
            # 拡張テスト用プロンプト
            test_prompts = {
                0: """# 🚀 Gradio システム生成プロンプト

## 概要
Gradioインターフェースを作成してください。

## 機能要件
- ファイルアップロード機能
- テキスト入力・出力
- リアルタイム処理
- 美しいUI

## 実装例
```python
import gradio as gr

def process_input(text):
    return f'処理結果: {text.upper()}'

gradio_interface = gr.Interface(
    fn=process_input,
    inputs=gr.Textbox(label="入力"),
    outputs=gr.Textbox(label="出力"),
    title="テストシステム"
)
```

## 追加要件
- エラーハンドリング
- ログ出力
- レスポンシブデザイン""",

                1: """# 🔗 FastAPI システム生成プロンプト

## 概要  
FastAPIを使用したWebAPIシステムを作成してください。

## 機能要件
- REST API エンドポイント
- データベース連携
- 認証・認可機能
- Swagger ドキュメント自動生成

## 実装例
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Test API")

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
```

## 追加要件
- バリデーション
- エラーハンドリング
- テストコード""",

                2: """# 📱 React フロントエンド生成プロンプト

## 概要
モダンなReactアプリケーションを作成してください。

## 機能要件
- レスポンシブデザイン
- 状態管理 (Redux/Context)
- ルーティング
- API連携

## 実装例
```jsx
import React, { useState } from 'react';

function App() {
  const [data, setData] = useState('');
  
  const handleSubmit = async () => {
    // API呼び出し処理
    const response = await fetch('/api/data');
    const result = await response.json();
    setData(result.message);
  };

  return (
    <div className="App">
      <h1>React Application</h1>
      <button onClick={handleSubmit}>
        データ取得
      </button>
      <p>{data}</p>
    </div>
  );
}

export default App;
```

## 追加要件
- TypeScript対応
- テストコード
- パフォーマンス最適化"""
            }
            
            # テスト用プロンプトを返す
            if row_index in test_prompts:
                content = test_prompts[row_index]
                print(f"✅ テストプロンプト{row_index + 1}を返します（{len(content)}文字）")
                return content, f"https://github.com/test/system-{row_index}", "web_system"
            else:
                # 範囲外の場合は汎用プロンプトを返す
                content = f"""# 📋 汎用プロンプト（行{row_index}）

## 概要
クリックされた行: {row_index}

## 内容
これは行{row_index}用の汎用プロンプトです。
お好みのシステムを作成してください。

## 技術要件
- Python 3.11+
- 適切なフレームワーク選択
- エラーハンドリング
- ドキュメント作成

## プロンプト例
システムの種類を選択して、詳細な仕様を記述してください。"""
                print(f"✅ 汎用プロンプト（行{row_index}）を返します")
                return content, "", "general"
        else:
            print(f"⚠️ 無効なインデックス: {evt.index}")
            content = """# ⚠️ インデックスエラー

無効なテーブルインデックスです。
最初の行を選択してください。

## 対処方法
1. テーブルの行をクリックしてください
2. 有効な行を選択してください"""
            return content, "", "general"
                
    except Exception as e:
        print(f"❌ プロンプト読み込みエラー: {e}")
        print(f"❌ エラータイプ: {type(e)}")
        import traceback
        traceback.print_exc()
        
        # エラー詳細を含むプロンプトを返す
        error_content = f"""# ❌ エラー詳細

## エラー内容
{str(e)}

## エラータイプ  
{type(e)}

## 対処方法
1. ページを再読み込み
2. 別の行をクリック
3. システム管理者に連絡

## デバッグ情報
- Event Index: {evt.index if hasattr(evt, 'index') else 'None'}
- Function: load_prompt_to_textbox"""
        return error_content, "", "error"
    
    print("🔄 予期しないパス - デフォルト値を返します")
    return "# 🔄 デフォルトプロンプト\n\nプロンプトの読み込み処理が予期しないパスを通りました。", "", "general"
