"""
🧠 OpenInterpreter統合 - Gradioインターフェース
AI搭載のコード実行・分析機能

Laravel風アーキテクチャ: app/Http/Controllers/Gradio/gra_09_openinterpreter/
"""

import gradio as gr
import subprocess
import sys
import os
import json
from typing import List, Tuple, Optional

class OpenInterpreterService:
    """OpenInterpreter統合サービス"""
    
    def __init__(self):
        self.conversation_history = []
        self.is_interpreter_available = self.check_interpreter_availability()
    
    def check_interpreter_availability(self) -> bool:
        """OpenInterpreterの利用可能性をチェック"""
        try:
            result = subprocess.run([sys.executable, "-c", "import interpreter"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except Exception as e:
            print(f"OpenInterpreter check failed: {e}")
            return False
    
    def install_interpreter(self) -> str:
        """OpenInterpreterをインストール"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "open-interpreter"], 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.is_interpreter_available = True
                return "✅ OpenInterpreter installed successfully!"
            else:
                return f"❌ Installation failed: {result.stderr}"
        except Exception as e:
            return f"❌ Installation error: {str(e)}"
    
    def execute_with_interpreter(self, user_input: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        """OpenInterpreterでコード実行・分析"""
        
        if not self.is_interpreter_available:
            error_msg = """
❌ OpenInterpreterが利用できません。

🔧 解決方法:
1. 下の「Install OpenInterpreter」ボタンをクリック
2. インストール完了後、再度お試しください

📚 OpenInterpreterについて:
- AI搭載のコード実行・分析ツール
- Python、JavaScript、Shell等のコード実行
- データ分析、ファイル操作、システム管理等が可能
"""
            history.append((user_input, error_msg))
            return error_msg, history
        
        try:
            # シンプルなインタープリター実行
            result = subprocess.run([
                sys.executable, "-c", 
                f"import interpreter; interpreter.chat('{user_input}')"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                response = f"🧠 OpenInterpreter実行結果:\n\n{result.stdout}"
                if result.stderr:
                    response += f"\n\n⚠️ 警告:\n{result.stderr}"
            else:
                response = f"❌ 実行エラー:\n{result.stderr}"
            
            history.append((user_input, response))
            return response, history
            
        except subprocess.TimeoutExpired:
            error_msg = "⏱️ タイムアウト: 実行時間が60秒を超えました"
            history.append((user_input, error_msg))
            return error_msg, history
            
        except Exception as e:
            error_msg = f"❌ 予期しないエラー: {str(e)}"
            history.append((user_input, error_msg))
            return error_msg, history
    
    def get_system_info(self) -> str:
        """システム情報を取得"""
        info = []
        info.append(f"🐍 Python: {sys.version}")
        info.append(f"📁 Working Directory: {os.getcwd()}")
        info.append(f"🧠 OpenInterpreter: {'✅ Available' if self.is_interpreter_available else '❌ Not Available'}")
        
        # 利用可能なライブラリをチェック
        libraries = ['numpy', 'pandas', 'matplotlib', 'requests', 'beautifulsoup4']
        available_libs = []
        for lib in libraries:
            try:
                __import__(lib)
                available_libs.append(f"✅ {lib}")
            except ImportError:
                available_libs.append(f"❌ {lib}")
        
        info.append("\n📚 利用可能なライブラリ:")
        info.extend(available_libs)
        
        return "\n".join(info)

# サービスインスタンス
interpreter_service = OpenInterpreterService()

def chat_with_interpreter(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
    """OpenInterpreterとのチャット"""
    return interpreter_service.execute_with_interpreter(message, history)

def install_interpreter_action() -> str:
    """OpenInterpreterインストール処理"""
    return interpreter_service.install_interpreter()

def get_system_info_action() -> str:
    """システム情報取得"""
    return interpreter_service.get_system_info()

def create_sample_code() -> str:
    """サンプルコード生成"""
    return """
# 🧠 OpenInterpreter サンプルコード

# データ分析例
import pandas as pd
data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
df = pd.DataFrame(data)
print(df)

# ファイル操作例  
with open('sample.txt', 'w') as f:
    f.write('Hello OpenInterpreter!')

# 数学計算例
import math
result = math.sqrt(16) + math.pi
print(f"計算結果: {result}")
"""

# Gradioインターフェース作成
with gr.Blocks(title="🧠 OpenInterpreter統合", theme=gr.themes.Soft()) as gradio_interface:
    
    gr.Markdown("""
    # 🧠 OpenInterpreter統合 - AI Code Execution
    
    **AI搭載のコード実行・分析プラットフォーム**
    
    ## 🚀 機能
    - **🤖 AI Code Assistant**: 自然言語でコード生成・実行
    - **📊 Data Analysis**: データ分析・可視化  
    - **📁 File Operations**: ファイル操作・管理
    - **⚡ Real-time Execution**: リアルタイムコード実行
    
    ## 💡 使用例
    - "CSVファイルを読み込んでグラフを作成して"
    - "現在のディレクトリのファイル一覧を表示"
    - "簡単な機械学習モデルを作成して"
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            # チャットインターフェース
            chatbot = gr.Chatbot(
                label="🧠 OpenInterpreter Chat",
                height=400,
                avatar_images=["🧑‍💻", "🧠"]
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="メッセージ", 
                    placeholder="自然言語またはコードを入力してください...",
                    lines=3,
                    scale=4
                )
                send_btn = gr.Button("送信 🚀", variant="primary")
            
            # サンプルコード表示
            with gr.Accordion("📝 サンプルコード", open=False):
                sample_code = gr.Code(
                    value=create_sample_code(),
                    language="python",
                    label="Python Sample Code"
                )
        
        with gr.Column(scale=1):
            # システム情報・コントロール
            gr.Markdown("### 🔧 System Control")
            
            install_btn = gr.Button("Install OpenInterpreter 📦", variant="secondary")
            system_info_btn = gr.Button("System Info 📊", variant="secondary")
            
            system_output = gr.Textbox(
                label="System Output",
                interactive=False,
                lines=10
            )
    
    # イベントハンドラー
    def respond(message, history):
        if message.strip():
            bot_message, new_history = chat_with_interpreter(message, history)
            return "", new_history
        return message, history
    
    # チャット機能
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    
    # システム機能
    install_btn.click(install_interpreter_action, outputs=system_output)
    system_info_btn.click(get_system_info_action, outputs=system_output)
    
    # 初期システム情報表示
    gradio_interface.load(get_system_info_action, outputs=system_output)

# Gradioインターフェースをエクスポート
if __name__ == "__main__":
    # スタンドアロン実行時
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7866,
        share=False
    )
