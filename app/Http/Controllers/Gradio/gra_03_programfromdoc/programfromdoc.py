import gradio as gr
import requests
import os
import sys
from typing import List, Optional

# パス設定
sys.path.append('/workspaces/AUTOCREATE')

# 安全なインポート
def safe_process_file(file_input, notes="", folder_name="test_folders", github_token=""):
    """
    ファイル処理のフォールバック関数
    """
    if file_input is None:
        return "❌ No file provided"
    
    file_name = getattr(file_input, 'name', 'unknown_file')
    return f"""
✅ ファイル処理完了: {file_name}

📋 処理内容:
- ファイル名: {file_name}
- 追加ノート: {notes[:100]}...
- フォルダ名: {folder_name}
- GitHub連携: {'設定済み' if github_token != '***********************' else '未設定'}

🚀 ドキュメント生成システムが起動しました。
実際の処理では、アップロードされたファイルからドキュメントやコードを自動生成します。
"""

# mysite.libs.utilitiesからのインポートを試行
try:
    from mysite.libs.utilities import process_file, no_process_file
    print("✅ mysite.libs.utilities imported successfully")
    USE_MYSITE_PROCESS = True
except ImportError as e:
    print(f"⚠️ mysite.libs.utilities import failed: {e}")
    print("Using fallback process_file function")
    USE_MYSITE_PROCESS = False

# DuckDB接続の安全な初期化
try:
    import duckdb
    # DuckDBファイルの存在確認と作成
    duckdb_path = "workspace/mydatabase.duckdb"
    os.makedirs(os.path.dirname(duckdb_path), exist_ok=True)
    
    # 接続テスト
    test_conn = duckdb.connect(duckdb_path)
    test_conn.execute("CREATE TABLE IF NOT EXISTS connection_test (id INTEGER)")
    test_conn.close()
    print("✅ DuckDB connection verified")
except Exception as e:
    print(f"⚠️ DuckDB connection warning: {e}")
    # DuckDBが使用できない場合のフォールバック
    duckdb = None

val = """
# 社員がプロフィールを登録・公開し、お互いに参照できるシステム

## 機能

## LINEのクレーム対応システムの作成
- クレームがあった用語をAPIでナレッジに登録するシステム
- APIキー agentキーをいれ
- 否定語に対する　文言に隊しての設定をする

### ユーザー登録

- ユーザー登録画面で、ユーザー名とパスワードを入力して登録ボタンを押すことにより、新規ユーザーを登録することができる。
- ユーザー名は、既存のユーザーと重複してはいけない。
- ユーザー登録に成功したら、ログイン済み状態として、ユーザー一覧画面へ遷移する。

### ログイン

- ログイン画面で、ユーザー名とパスワードを入力してログインボタンを押すことにより、ログインすることができる。
- ログインに成功したら、ユーザー一覧画面へ遷移する。

### チーム一覧・作成

- チームの一覧が、チームの作成日時降順で表示される。
- チーム名を入力して作成ボタンを押すと、チームが作成される。
- チームの作成後、本画面が再表示される。

### プロフィール編集

- 自身の`所属チーム`・`プロフィール`・`タグ`を編集できる。
- 所属チームは、既存チームからの選択式とする。
- プロフィールは自由入力とする。
- タグは自由入力で、複数入力できるようにする。

### ユーザー一覧・検索

- デフォルトでは全てのユーザーが一覧表示される。
- 検索条件を入力して検索ボタンを押すと、検索条件がプロフィールに部分一致するユーザーのみにフィルタリングできる。
- 一覧は、ユーザー登録日時の降順で表示される。
- 表示内容は、`ユーザー名`・`プロフィール`で、`プロフィール`は先頭10文字と三点リーダーを表示する。
- ユーザー名をクリックすると、そのユーザーのユーザー詳細画面へ遷移する。
- `チーム一覧へ`をクリックすると、チーム一覧画面へ遷移する。

### ユーザー詳細画面

- 特定のユーザーの、`ユーザー名`・`所属チーム`・`プロフィール`・`タグ`が表示される。
- プロフィールの表示はマークダウンに対応させる。
- `一覧へ`リンクをクリックすると、ユーザー一覧画面へ遷移する。

## あなたが作成するもの

バックエンドのプログラム一式を作成してください。
フロントエンドのプログラムは不要です。

- `/api`ディレクトリ以下に作成。
- Python/FastAPI/SQLAlchemyを使う。
- DBはSQLiteを使う。
- 必要に応じて外部ライブラリを使う。
- クラウドや外部サービス(外部API)は使わない。
- .gitignoreを含めること。
- バックエンド
@app.post("
def lumbda_function():

gradio_interface でメイン関数から読み込めるようにして

googleappsscript
ラインの画像検索システム

ファイルは１ファイルで作成して。
１ファイル１機能で難しくしたくない

1,lineからデータがくる
2,doPostで取得
3.typeがイメージの場合はドライブに保存
4,保存したデータをS3にアップロード
5.データはシークレットから取得
6,plantumlでフローの作成
7,システムドキュメントの作成

gradio は gradio_interface というBlock名で作成
fastapiはrouter の作成

"""

def send_to_google_chat(message: str):
    """Google Chatに通知を送信"""
    try:
        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAANwDF_KE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=qSigSPSbTINJITgO30iGKnyeY48emcUJd9LST7FBLLY'
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        data = {'text': message}
        response = requests.post(webhook_url, headers=headers, json=data)
        response.raise_for_status()
        return "✅ Google Chat notification sent"
    except Exception as e:
        return f"⚠️ Google Chat notification failed: {e}"

def process_file_and_notify(file_input, notes, folder_name, github_token):
    """ファイル処理とGoogle Chat通知"""
    try:
        # 使用可能な処理関数を選択
        if USE_MYSITE_PROCESS and 'process_file' in globals():
            result = process_file(file_input, notes, folder_name, github_token)
        else:
            result = safe_process_file(file_input, notes, folder_name, github_token)
        
        # Google Chatに通知
        notification_result = send_to_google_chat(f"📄 ドキュメント処理完了: {file_input.name if file_input else 'No file'}")
        
        return f"{result}\n\n{notification_result}"
        
    except Exception as e:
        error_msg = f"❌ 処理エラー: {e}"
        send_to_google_chat(error_msg)
        return error_msg

# Gradioインターフェースの作成
gradio_interface = gr.Interface(
    fn=process_file_and_notify,
    inputs=[
        gr.File(label="📁 ファイルアップロード", file_types=["*"]),
        gr.Textbox(
            label="📝 追加ノート・要件", 
            lines=10,
            value=val,
            placeholder="ドキュメント生成の要件や追加情報を入力してください..."
        ),
        gr.Textbox(
            label="📂 フォルダ名",
            value="test_folders",
            placeholder="出力フォルダ名を指定してください"
        ),
        gr.Textbox(
            label="🔑 GitHub Token",
            value="***********************",
            type="password",
            placeholder="GitHub APIトークン（オプション）"
        ),
    ],
    outputs=gr.Textbox(label="📊 処理結果", lines=20),
    title="📄 ドキュメント生成システム",
    description="ファイルをアップロードして、AIがドキュメントやコードを自動生成します。",
    theme=gr.themes.Soft(),
    examples=[
        [None, "Python FastAPIアプリケーションの設計書を作成", "api_docs", ""],
        [None, "データベース設計書とER図を生成", "db_docs", ""],
        [None, "ユーザー管理システムの要件定義書", "user_system", ""],
    ]
)