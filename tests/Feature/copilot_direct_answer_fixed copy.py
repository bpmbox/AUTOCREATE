#!/usr/bin/env python3
"""
🎯 GitHub Copilot直接回答システム

Supabaseから質問を取得 → VS Codeチャットに直接入力
OpenAI API不要、GitHub Copilotが直接回答
"""

import os
import time
import json
import pyautogui
import pyperclip
import traceback
from datetime import datetime
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

try:
    from supabase import create_client, Client
except ImportError as e:
    print(f"❌ 必要なパッケージがインストールされていません: {e}")
    print("📦 pip install supabase python-dotenv pyautogui pyperclip")
    exit(1)

class CopilotDirectAnswerSystem:
    def __init__(self):
        print("🚀 GitHub Copilot直接回答システム初期化中...")
        
        # 環境変数取得
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not all([self.supabase_url, self.supabase_key]):
            print("❌ 環境変数が設定されていません")
            return
        
        try:
            # Supabase初期化
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
            print("✅ Supabase接続成功")
        except Exception as e:
            print(f"❌ 初期化エラー: {e}")
            return
        
        # チャット座標
        self.chat_coordinates = None
        
        # PyAutoGUI設定
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2
        
        print("🎯 システム初期化完了")
    
    def infinite_auto_loop(self, interval=3):
        """無限自動ループモード（完全に手を離せる）"""
        print("🔥 無限自動ループモード開始!")
        print(f"⚡ {interval}秒間隔で永続監視")
        print("🤖 新着メッセージを完全自動で処理")
        print("📍 座標固定: (1335, 1045)")
        print("🚀 GitHub Copilotが自動回答")
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
        
        try:
            while True:  # 無限ループ
                check_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                
                # 定期的にステータス表示
                if check_count % 20 == 1:  # 20回に1回詳細表示
                    print(f"\n🔄 {current_time} - チェック #{check_count} (成功: {success_count}件)")
                else:
                    print(f"⏰ {current_time} #{check_count}", end=" ")
                
                # 最新IDより大きいメッセージのみ取得
                try:
                    result = self.supabase.table('chat_history') \
                        .select('*') \
                        .gt('id', last_id) \
                        .order('id', desc=False) \
                        .execute()
                    
                    if result.data:
                        new_messages = result.data
                        print(f"⚡ 新着 {len(new_messages)}件!")
                        
                        for msg in new_messages:
                            owner = msg.get('ownerid', '')
                            message = msg.get('messages', '')
                            msg_id = msg['id']
                            
                            # Copilot系は除外
                            if owner and (
                                owner.lower().startswith('copilot') or 
                                owner.lower().startswith('ai-assistant') or
                                owner.lower().startswith('github') or
                                'bot' in owner.lower()
                            ):
                                print(f"  🤖 Copilot系スキップ: {owner}")
                                last_id = max(last_id, msg_id)
                                continue
                            
                            # 空メッセージをスキップ
                            if not message or not message.strip():
                                print(f"  ⏭️ 空メッセージスキップ")
                                last_id = max(last_id, msg_id)
                                continue
                            
                            # ユーザーメッセージ検出
                            question_data = {
                                'id': msg_id,
                                'question': message,
                                'user': owner or 'Unknown',
                                'created': msg.get('created', '')
                            }
                            
                            print(f"\n🎯 ユーザーメッセージ検出!")
                            print(f"👤 {owner}: {message[:50]}...")
                            
                            # 完全自動でCopilotに転送
                            if self.post_question_to_chat_auto(question_data):
                                success_count += 1
                                processed_ids.add(msg_id)
                                self.mark_question_as_processed(msg_id)
                                print(f"✅ 自動転送成功! (累計: {success_count}件)")
                            else:
                                print("❌ 転送失敗")
                            
                            last_id = max(last_id, msg_id)
                            time.sleep(1)  # メッセージ間の待機
                    else:
                        print("📭")  # 新着なし
                        
                except Exception as e:
                    print(f"❌ チェックエラー: {e}")
                
                time.sleep(interval)  # 次のチェックまで待機
                
        except KeyboardInterrupt:
            print(f"\n\n⚠️ 無限自動ループを停止")
            print("="*50)
            print(f"📊 総チェック回数: {check_count}")
            print(f"🎯 自動処理成功: {success_count}件")
            print(f"🆔 最終処理ID: {last_id}")
            print("✨ お疲れ様でした!")
    
    def post_question_to_chat_auto(self, question_data):
        """質問をチャットに自動投稿（確認なし、完全自動）"""
        if not self.chat_coordinates:
            print("❌ チャット座標が未設定")
            return False
        
        try:
            question = question_data['question']
            user = question_data['user']
            
            # GitHub Copilotに分かりやすい質問形式に変換
            formatted_question = f"""📋 ユーザーからの質問\n\n質問者: {user}\n質問: {question}\n\nこの内容でGitHub Issueを作成し、専用フォルダーを作成してプログラムを実装してください。実装結果や進捗をSupabaseに送信してください。\n"""
            
            print(f"📤 Copilotチャットに質問自動投稿中...")
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
            
            # 自動送信（確認なし）
            print("🚀 自動送信中...")
            pyautogui.press('enter')
            time.sleep(2)
            print("✅ 質問送信完了")
            print("💡 GitHub Copilotが回答を生成中...")
            return True
                
        except Exception as e:
            print(f"❌ チャット投稿エラー: {e}")
            return False
    
    def mark_question_as_processed(self, question_id):
        """質問を処理済みとしてマーク"""
        try:
            # 簡単な処理済みフラグを追加
            self.supabase.table('chat_history') \
                .update({'copilot_processed': True}) \
                .eq('id', question_id) \
                .execute()
            return True
        except Exception as e:
            print(f"⚠️ 処理済みマーク失敗: {e}")
            return False

def main():
    import sys
    
    # コマンドライン引数で自動起動モードをチェック
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        print("🔥 完全自動起動モード")
        print("📍 座標固定: (1335, 1045)")
        print("⚡ 3秒間隔で永続監視開始")
        print("🤖 手を離してください - 完全自動運転中")
        print("-" * 50)
        
        system = CopilotDirectAnswerSystem()
        if hasattr(system, 'supabase') and system.supabase:
            # 座標を自動設定
            system.chat_coordinates = {"x": 1335, "y": 1045}
            print("✅ 座標自動設定完了")
            
            # 無限自動ループを即座に開始
            system.infinite_auto_loop(3)
        else:
            print("❌ システム初期化失敗")
        return
    
    print("🎯 GitHub Copilot直接回答システム")
    print("手動モードは現在利用できません")
    print("自動モードで起動してください:")
    print("python copilot_direct_answer.py --auto")

if __name__ == "__main__":
    main()
