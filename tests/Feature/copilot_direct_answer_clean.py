#!/usr/bin/env python3
"""
[TARGET] GitHub Copilot直接回答システム（完全版）

Supabaseから質問を取得 → VS Codeチャットに送信 → Copilotの回答をSupabaseに投稿
VS Codeチャット経由でCopilotとつながり、回答をSupabaseに自動登録
"""

import os
import sys
import time
import json
import hashlib
import pyautogui
import pyperclip
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# 設定読み込み
load_dotenv()

def install_requirements():
    """必要な依存関係を確認/インストール"""
    try:
        import supabase
        import dotenv  
        import pyautogui
        import pyperclip
        return True
    except ImportError as e:
        print(f"[WARNING] インポートエラー: {e}")
        print("pip install supabase python-dotenv pyautogui pyperclip")
        return False

class CopilotDirectAnswer:
    def __init__(self):
        print("[INIT] GitHub Copilot-Supabase統合システム初期化中...")
        
        # Supabase接続設定
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            print("[ERROR] SUPABASE_URLまたはSUPABASE_KEYが.envファイルに設定されていません")
            exit(1)
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.chat_coordinates_file = 'chat_coordinates.json'
        self.file_hash = None  # ホットリロード用
        
        # VS Code チャット座標を読み込み
        self.chat_coordinates = self.load_chat_coordinates()
        
        # マウス位置固定（座標がない場合のデフォルト）
        if not self.chat_coordinates:
            self.chat_coordinates = {'x': 1335, 'y': 1045}
            self.save_chat_coordinates()
        
        # PyAutoGUI安全設定
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        print("[SUCCESS] システム初期化完了")
    
    def get_file_hash(self):
        """現在のファイルのハッシュを取得（ホットリロード用）"""
        try:
            with open(__file__, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def check_for_reload(self):
        """ファイル変更をチェックしてホットリロード"""
        current_hash = self.get_file_hash()
        if self.file_hash and current_hash != self.file_hash:
            if current_hash:  # ファイルが存在する場合のみ
                print("\n[HOT-RELOAD] ファイル変更検出! ホットリロード実行中...")
                print("[RESTART] プログラムを再起動します...")
                os.execv(sys.executable, ['python'] + sys.argv)
        self.file_hash = current_hash
    
    def load_chat_coordinates(self):
        """チャット座標設定を読み込み"""
        try:
            with open(self.chat_coordinates_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def save_chat_coordinates(self):
        """チャット座標設定を保存"""
        with open(self.chat_coordinates_file, 'w') as f:
            json.dump(self.chat_coordinates, f)
    
    def run_infinite_auto_mode(self, interval=5):
        """完全自動無限ループモード"""
        print("[INFINITE-MODE] 無限自動ループモード開始!")
        print("=" * 50)
        print("[AUTO-PROCESS] 新着メッセージを完全自動で処理")
        print("[COORDINATES] 座標固定: (1335, 1045)")
        print("[COPILOT] GitHub Copilotが自動回答")
        print("[HOT-RELOAD] ホットリロード: ファイル変更時自動再起動")
        print("=" * 50)
        
        # 初期ファイルハッシュ記録
        self.file_hash = self.get_file_hash()
        
        # 最新IDを取得
        try:
            result = self.supabase.table('chat_history').select('id').order('id', desc=True).limit(1).execute()
            if result.data:
                last_id = result.data[0]['id']
            else:
                last_id = 0
                
            if last_id > 0:
                print(f"[MONITOR] 監視開始ID: {last_id}")
            
        except Exception as e:
            print(f"[ERROR] 初期ID取得エラー: {e}")
            last_id = 0
        
        print("\n[LOOP-START] 無限ループ開始 - Ctrl+C で停止")
        print("-" * 50)
        
        check_count = 0
        success_count = 0
        
        try:
            while True:
                # ホットリロードチェック
                current_hash = self.get_file_hash()
                if self.file_hash and current_hash != self.file_hash:
                    if current_hash:  # ファイルが存在する場合のみ
                        print("\n[HOT-RELOAD] ファイル変更検出! ホットリロード実行中...")
                        print("[RESTART] プログラムを再起動します...")
                        import sys
                        os.execv(sys.executable, ['python'] + sys.argv)
                
                check_count += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                
                # 進行状況を表示
                if check_count % 10 == 1:  # 10回に1回詳細表示
                    print(f"\n[CHECK] {current_time} - チェック #{check_count} (成功: {success_count}件)")
                else:
                    print(".", end="", flush=True)  # ドット表示
                
                try:
                    # 新しいメッセージをチェック
                    result = self.supabase.table('chat_history').select('*').gt('id', last_id).order('id', desc=False).execute()
                    
                    if result.data:
                        for message_data in result.data:
                            message_id = message_data['id']
                            message = message_data.get('messages', '').strip()
                            owner = message_data.get('ownerid', '').strip()
                            
                            # 処理済みチェック
                            if message_data.get('processed', False):
                                continue
                            
                            # AI/Bot系のメッセージはスキップ
                            if any(keyword in owner.lower() for keyword in ['bot', 'ai', 'copilot', 'assistant', 'github']):
                                print(f"  [SKIP-AI] Copilot系スキップ: {owner}")
                                # 処理済みフラグ設定
                                self.supabase.table('chat_history').update({
                                    'processed': True,
                                    'processed_at': datetime.now().isoformat()
                                }).eq('id', message_id).execute()
                                continue
                            
                            # 空のメッセージはスキップ
                            if not message or len(message.strip()) < 3:
                                # 処理済みフラグ設定
                                self.supabase.table('chat_history').update({
                                    'processed': True,
                                    'processed_at': datetime.now().isoformat()
                                }).eq('id', message_id).execute()
                                continue
                            
                            # 有効なユーザーメッセージを処理
                            print(f"\n[NEW-MESSAGE] ユーザーメッセージ検出!")
                            print(f"[USER] {owner}: {message[:50]}...")
                            
                            # Copilotに送信して処理
                            question_data = {
                                'id': message_id,
                                'question': message,
                                'user': owner
                            }
                            
                            if self.send_to_copilot_and_get_response(question_data):
                                success_count += 1
                                last_id = message_id
                            
                            time.sleep(2)  # 連続処理の間隔
                    else:
                        print("[NO-NEW]")  # 新着なし
                        
                except Exception as e:                    print(f"\n[ERROR] チェック中エラー: {e}")
                
                time.sleep(interval)  # 次のチェックまで待機
                
        except KeyboardInterrupt:
            print(f"\n\n[STOP] 無限自動ループを停止")
            print("="*50)
            print(f"[STATS] 総チェック回数: {check_count}")
            print(f"[SUCCESS] 自動処理成功: {success_count}件")
            print(f"[LAST-ID] 最終処理ID: {last_id}")
            print("[DONE] お疲れ様でした!")
    
    def send_to_copilot_and_get_response(self, question_data):
        """VS CodeチャットでCopilotに質問を送信し、回答をSupabaseに投稿"""
        if not self.chat_coordinates:
            print("[ERROR] チャット座標が未設定")
            return False
        
        try:
            question = question_data['question']
            user = question_data['user']
              # GitHub Copilotに分かりやすい質問形式に変換
            formatted_question = f"""🎯 ユーザーからの質問

👤 質問者: {user}
💬 質問: {question}

🚀 [完全自動開発フロー実行をお願いします]

1️⃣ **詳細な回答生成**: この質問に対して実用的で具体的な回答を作成

2️⃣ **GitHub Issue作成**: 
   📋 GitHub CLIコマンド例:
   ```bash
   gh issue create --repo "bpmbox/AUTOCREATE" \\
     --title "🎯 {question} - 実装要求" \\
     --body "# 📝 {question}の実装\\n\\n## 🎯 要件\\n- {question}に関する実装\\n\\n## ⚙️ 仕様\\n- 詳細な技術仕様\\n\\n## 📋 実装計画\\n- ステップバイステップの実装手順\\n\\n## 📁 プロジェクトフォルダー\\n- フォルダー: `{question.lower().replace(' ', '-').replace('　', '-')}-project`" \\
     --label "ai-automation"
   ```
   - 🏷️ タイトル: 🎯「{question}」の実装
   - 📝 説明: 要件、仕様、実装計画を詳細記載
   - 🏷️ ラベル: ai-automation (重要: このラベルを必ず使用)

3️⃣ **プロジェクトフォルダー作成**:
   - 📁 フォルダー名: `{question.lower().replace(' ', '-').replace('　', '-')}-project`
   - 🗂️ 必要なファイル構成を自動生成
   - 📖 README.md、実装ファイル、設定ファイル等

4️⃣ **プログラム自動実装**:
   - ⚡ 要求された機能を完全実装
   - 🧪 ユニットテスト・統合テスト作成
   - 🔍 テストデータベース設定（Supabase Test DB）
   - 📚 ドキュメント生成
   - ✅ 完全動作確認・テスト実行

5️⃣ **GitHub Issue更新とリポジトリ作成**:
   📋 GitHub CLI実行例:
   ```bash
   # Issue作成（メインリポジトリに統合報告）
   gh issue create --repo "bpmbox/AUTOCREATE" \\
     --title "✅ {question} - 完全実装完了" \\
     --body "# 🎉 実装完了報告\\n\\n## 📁 プロジェクトフォルダー\\n- 📂 フォルダー: `{question.lower().replace(' ', '-').replace('　', '-')}-project`\\n- 🔗 パス: [プロジェクトフォルダー](https://github.com/bpmbox/AUTOCREATE/tree/main/{question.lower().replace(' ', '-').replace('　', '-')}-project)\\n\\n## 🚀 実装詳細\\n- 実装内容とリポジトリリンク\\n- テスト結果\\n- 使用方法" \\
     --label "ai-automation"
   ```
   - ✅ 実装完了報告のIssue作成
   - 🔗 プロジェクトフォルダーのリンク追加
   - 📊 成果物の詳細説明

6️⃣ **Supabase投稿**: 
   - 🤖 ownerid: 'GitHub-Copilot-AI'
   - 💬 messages: 回答内容 + GitHub Issue URL + プロジェクトフォルダーリンク + 実装結果詳細
   - ⏰ created: 現在時刻

🔥 **重要な実行ガイド**:
- 🔐 GitHub CLI認証確認: gh auth status
- 📦 リポジトリ: bpmbox/AUTOCREATE にIssue作成
- 🏷️ ラベル: "ai-automation" 必須使用
- 📝 文字コード: UTF-8設定で実行
- 💻 PowerShell例: $env:PYTHONUTF8=1; gh issue create...
- 📁 フォルダーリンク: プロジェクトへのリンクを必ず含める

🤖 このシステムは完全自動開発パイプラインです。全ステップを実行してください！"""
            
            print(f"[SEND-TO-COPILOT] Copilotチャットに質問送信中...")
            print(f"質問: {question}")
            
            x, y = self.chat_coordinates['x'], self.chat_coordinates['y']
            
            # チャット欄クリック
            for i in range(3):
                pyautogui.click(x, y)
                time.sleep(0.3)
            
            # 内容クリア
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.3)
            
            # クリップボード経由で入力
            pyperclip.copy(formatted_question)
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.5)
            
            print("[INPUT-COMPLETE] 質問入力完了")
            # 自動送信
            print("[SENDING] Copilotに送信中...")
            pyautogui.press('enter')
            time.sleep(3)  # Copilotの回答生成を待機
            print("[SENT] 質問送信完了")
            print("GitHub Copilotが完全自動開発フローを実行中...")
            
            # Supabaseに処理済みとしてマーク
            self.supabase.table('chat_history').update({
                'processed': True,
                'processed_at': datetime.now().isoformat(),
                'copilot_sent': True
            }).eq('id', question_data['id']).execute()
            
            print("[MARKED] 処理済みマーク完了")
            return True
            
        except Exception as e:
            print(f"[ERROR] Copilot送信エラー: {e}")
            return False

def main():
    """メイン実行関数"""
    if not install_requirements():
        print("[EXIT] 必要な依存関係をインストールしてから再実行してください")
        return
    
    try:
        copilot_system = CopilotDirectAnswer()
        copilot_system.run_infinite_auto_mode(interval=3)  # 3秒間隔
    except KeyboardInterrupt:
        print("\n[INTERRUPT] プログラムを終了します")
    except Exception as e:
        print(f"[FATAL-ERROR] 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
