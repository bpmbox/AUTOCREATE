#!/usr/bin/env python3
"""
🚀 GitHub Copilot完全自動化システム (GitHub CLI対応版)
Supabase監視 → VS Code Chat → GitHub Copilot → Issue作成 → 実装 → 完了報告

機能:
- Supabaseのchat_historyを監視
- 新しい質問をVS Code Chatに投稿
- GitHub CopilotにGitHub CLI含む詳細なプロンプトを送信
- 完全自動開発フローを実行
- ホットリロード対応
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip
from supabase import create_client

# 設定
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

class GitHubCopilotAutomation:
    def __init__(self):
        # Supabase設定
        url = "https://tnojlywkucnzgakwrgep.supabase.co"
        key = "ENV_SUPABASE_KEY_PLACEHOLDER"
        self.supabase = create_client(url, key)
        
        # チャット座標管理
        self.coordinates_file = "chat_coordinates.json"
        self.chat_coordinates = self.load_coordinates()
        
        print("🤖 GitHub Copilot完全自動化システム (GitHub CLI対応版) 起動")
        print("📊 Supabase接続完了")
        print("⚡ ホットリロード対応")

    def load_coordinates(self):
        """保存されたチャット座標を読み込み"""
        try:
            if os.path.exists(self.coordinates_file):
                with open(self.coordinates_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ 座標ファイル読み込みエラー: {e}")
        return None

    def infinite_auto_loop(self, interval=3):
        """無限自動ループモード（完全に手を離せる）+ ホットリロード"""
        print("🔥 無限自動ループモード開始!")
        print(f"⚡ {interval}秒間隔で永続監視")
        print("🤖 新着メッセージを完全自動で処理")
        print("📍 座標固定: (1335, 1045)")
        print("🚀 GitHub Copilotが自動回答")
        print("🔄 ホットリロード: ファイル変更時自動再起動")
        print("="*50)
        
        # 座標を固定設定
        if not self.chat_coordinates:
            self.chat_coordinates = {'x': 1335, 'y': 1045, 'timestamp': datetime.now().isoformat()}
            print("✅ 座標を固定設定しました")
        
        processed_ids = set()
        last_id = 0
        check_count = 0
        success_count = 0
        
        # 現在の最新IDを取得
        try:
            result = self.supabase.table('chat_history') \
                .select('id') \
                .order('id', desc=True) \
                .limit(1) \
                .execute()
            if result.data:
                last_id = result.data[0]['id']
                print(f"📊 監視開始ID: {last_id}")
        except Exception as e:
            print(f"⚠️ 初期化エラー: {e}")
        
        print("\n🎯 無限ループ開始 - Ctrl+C で停止")
        print("="*50)
        
        # ホットリロード用のファイル監視設定
        current_file = Path(__file__)
        last_modified = current_file.stat().st_mtime
        
        try:
            while True:  # 無限ループ
                # ホットリロード監視
                try:
                    current_modified = current_file.stat().st_mtime
                    if current_modified > last_modified:
                        print("\n🔄 ファイル変更検出 - 自動再起動中...")
                        print("="*50)
                        
                        # Pythonプロセスを再起動
                        import subprocess
                        subprocess.Popen([sys.executable] + sys.argv)
                        sys.exit(0)  # 現在のプロセスを終了
                        
                except Exception as e:
                    print(f"⚠️ ホットリロード監視エラー: {e}")
                
                check_count += 1
                
                # 新しいメッセージをチェック
                try:
                    result = self.supabase.table('chat_history') \
                        .select('*') \
                        .gt('id', last_id) \
                        .order('id', desc=False) \
                        .execute()
                    
                    if result.data:
                        for message in result.data:
                            if (message['id'] not in processed_ids and 
                                message.get('ownerid') != 'GitHub-Copilot-AI' and
                                message.get('messages', '').strip()):
                                
                                print(f"\n🚨 新着メッセージ検出! ID: {message['id']}")
                                print(f"👤 ユーザー: {message.get('ownerid', 'unknown')}")
                                print(f"💬 内容: {message.get('messages', '')[:100]}...")
                                
                                # Copilotに送信
                                if self.send_to_copilot_and_get_response(message):
                                    success_count += 1
                                    print(f"✅ 自動処理完了 #{success_count}")
                                else:
                                    print("❌ 処理失敗")
                                
                                processed_ids.add(message['id'])
                                last_id = max(last_id, message['id'])
                                
                                print(f"📊 処理済み最新ID: {last_id}")
                                print("="*30)
                                
                except Exception as e:
                    print(f"❌ メッセージ取得エラー: {e}")
                
                # 5分ごとに統計表示
                if check_count % 100 == 0:
                    print(f"\n📊 統計 - チェック回数: {check_count}, 成功処理: {success_count}, 最新ID: {last_id}")
                    print("💤 監視継続中...")
                
                time.sleep(interval)  # 次のチェックまで待機
                
        except KeyboardInterrupt:
            print(f"\n\n⚠️ 無限自動ループを停止")
            print("="*50)
            print(f"📊 総チェック回数: {check_count}")
            print(f"🎯 自動処理成功: {success_count}件")
            print(f"🆔 最終処理ID: {last_id}")
            print("✨ お疲れ様でした!")
    
    def send_to_copilot_and_get_response(self, question_data):
        """VS CodeチャットでCopilotに質問を送信し、回答をSupabaseに投稿"""
        if not self.chat_coordinates:
            print("❌ チャット座標が未設定")
            return False
        
        try:
            question = question_data['question'] if 'question' in question_data else question_data['messages']
            user = question_data.get('ownerid', 'unknown')
            
            # GitHub Copilotに分かりやすい質問形式に変換（GitHub CLI対応版）
            formatted_question = f"""📋 ユーザーからの質問

質問者: {user}
質問: {question}

🚀 完全自動開発フロー実行をお願いします：

1️⃣ **詳細な回答生成**: この質問に対して実用的で具体的な回答を作成

2️⃣ **GitHub Issue作成**: 
   📋 GitHub CLIコマンド実行:
   gh issue create --repo "bpmbox/AUTOCREATE" --title "🎯 {question} - 実装要求" --body "実装詳細" --label "ai-automation"
   
   - リポジトリ: bpmbox/AUTOCREATE (必須)
   - ラベル: ai-automation (必須)
   - 文字コード対応: $env:PYTHONUTF8=1 を設定

3️⃣ **プロジェクトフォルダー作成**:
   - フォルダー名: {question.lower().replace(' ', '-').replace('　', '-')}-project
   - 必要なファイル構成を自動生成
   - README.md、実装ファイル、設定ファイル等

4️⃣ **プログラム自動実装**:
   - 要求された機能を完全実装
   - テストコード作成
   - ドキュメント生成
   - 完全動作確認

5️⃣ **GitHub Issue完了報告**:
   📋 完了時のGitHub CLIコマンド:
   gh issue create --repo "bpmbox/AUTOCREATE" --title "✅ {question} - 完全実装完了" --body "実装結果詳細" --label "ai-automation"
   
   - 実装完了報告のIssue作成
   - 成果物の詳細説明
   - リポジトリURL報告

6️⃣ **Supabase投稿**: 
   - ownerid: 'GitHub-Copilot-AI'
   - messages: 回答内容 + GitHub Issue URL + 実装結果詳細
   - created: 現在時刻

🔥 重要なガイド:
- GitHub CLI認証: gh auth status で確認
- 文字化け対策: UTF-8設定必須
- ラベル: "ai-automation" 必須使用
- リポジトリ: bpmbox/AUTOCREATE 固定

🤖 このシステムは完全自動開発パイプラインです。全ステップを実行してください！"""
            
            print(f"📤 Copilotチャットに質問送信中...")
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
            
            print("📝 質問入力完了")
            
            # 自動送信
            print("🚀 Copilotに送信中...")
            pyautogui.press('enter')
            time.sleep(3)  # Copilotの回答生成を待機
            
            print("✅ 質問送信完了")
            print("💡 GitHub Copilotが完全自動開発フローを実行中...")
            print("🚀 Issue作成 → フォルダー生成 → プログラム実装 → 完了報告 → Supabase投稿")
            print("🔥 GitHub Copilot様へ: 6ステップ全てを実行してください！")
            
            return True
                
        except Exception as e:
            print(f"❌ チャット送信エラー: {e}")
            return False

if __name__ == "__main__":
    automation = GitHubCopilotAutomation()
    
    print("🚀 選択肢:")
    print("1. 無限自動ループ開始")
    print("2. 終了")
    
    choice = input("選択してください (1-2): ")
    
    if choice == "1":
        automation.infinite_auto_loop()
    else:
        print("👋 終了しました")
