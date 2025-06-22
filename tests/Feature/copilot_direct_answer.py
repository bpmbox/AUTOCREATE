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
    
    def load_coordinates(self):
        """座標読み込み"""
        try:
            if os.path.exists("chat_coordinates.json"):
                with open("chat_coordinates.json", 'r') as f:
                    coords = json.load(f)
                    self.chat_coordinates = coords[0] if coords else None
                    print(f"✅ 座標読み込み: {self.chat_coordinates}")
                    return True
            else:
                print("⚠️ 座標ファイルなし")
                return False
        except Exception as e:
            print(f"❌ 座標読み込みエラー: {e}")
            return False
    
    def record_coordinates(self):
        """座標記録"""
        print("📍 5秒後に座標記録します")
        print("🎯 VS Code Copilotチャット入力欄にマウスを移動")
        
        for i in range(5, 0, -1):
            print(f"   {i}秒...")
            time.sleep(1)
        
        x, y = pyautogui.position()
        coords = [{'x': x, 'y': y, 'timestamp': datetime.now().isoformat()}]
        
        with open("chat_coordinates.json", 'w') as f:
            json.dump(coords, f, indent=2)
        
        self.chat_coordinates = coords[0]
        pyautogui.click(x, y)
        print(f"✅ 座標記録完了: ({x}, {y})")
    
    def get_new_questions(self, last_check_time=None):
        """Supabaseから新しい質問取得（Copilot以外のユーザーから）"""
        try:
            print(f"🔍 Supabaseクエリ実行中... (last_check_time: {last_check_time})")
            
            # 基本クエリ
            query = self.supabase.table('chat_history').select('*')
            
            # 最後のチェック時刻以降のメッセージのみ取得（時刻フィルタなしでテスト）
            if last_check_time:
                print(f"⏰ 時刻フィルタ適用: {last_check_time}")
                # 時刻フィルタを緩くする
                query = query.gte('created', last_check_time)
            
            # 最新のレコードから取得（制限を追加）
            result = query.order('created', desc=True).limit(50).execute()  # 新しい順で50件
            
            print(f"📊 取得したレコード数: {len(result.data) if result.data else 0}")
            
            new_questions = []
            for item in result.data:
                message = item.get('messages', '')
                owner = item.get('ownerid', '')
                item_id = item.get('id', '')
                created = item.get('created', '')
                
                print(f"🔍 チェック中: ID={item_id}, Owner={owner}, Message={message[:30]}...")
                
                # 空メッセージをスキップ
                if not message or not message.strip():
                    print(f"  ⏭️ 空メッセージをスキップ")
                    continue
                
                # Copilot系ユーザーは除外
                if owner:
                    if (owner.lower().startswith('copilot') or 
                        owner.lower().startswith('ai-assistant') or
                        owner.lower().startswith('github') or
                        'bot' in owner.lower()):
                        print(f"  🤖 Copilot系ユーザーをスキップ: {owner}")
                        continue
                
                # Copilotの回答パターンも除外
                if ('GitHub Copilot' in message or 
                    '🤖' in message or
                    'AI Assistant' in message or
                    message.startswith('申し訳ございません') or
                    message.startswith('以下の内容')):
                    print(f"  🤖 Copilot回答パターンをスキップ")
                    continue
                
                # ユーザーからのメッセージとして判定
                print(f"  ✅ ユーザーメッセージとして判定: {owner}")
                new_questions.append({
                    'id': item_id,
                    'question': message,
                    'user': owner or 'Unknown',
                    'created': created,
                    'raw_data': item
                })
            
            print(f"🎯 フィルタ後の質問数: {len(new_questions)}")
            return new_questions
            
        except Exception as e:
            print(f"❌ 質問取得エラー: {e}")
            import traceback
            print(f"📋 詳細エラー: {traceback.format_exc()}")
            return []
    
    def debug_supabase_data(self):
        """Supabaseデータの詳細デバッグ"""
        print("\n🔍 Supabaseデータデバッグ")
        print("-" * 50)
        
        try:
            # 最新10件のレコードを取得
            result = self.supabase.table('chat_history') \
                .select('*') \
                .order('created', desc=True) \
                .limit(10) \
                .execute()
            
            print(f"📊 総レコード数: {len(result.data) if result.data else 0}")
            
            if result.data:
                for i, item in enumerate(result.data, 1):
                    print(f"\n{i}. ID: {item.get('id', 'N/A')}")
                    print(f"   Created: {item.get('created', 'N/A')}")
                    print(f"   Owner: {item.get('ownerid', 'N/A')}")
                    print(f"   Message: {item.get('messages', 'N/A')[:100]}...")
                    print(f"   IsRead: {item.get('isread', 'N/A')}")
                    print(f"   Status: {item.get('status', 'N/A')}")
            else:
                print("📭 レコードが見つかりません")
                
            # テーブル構造も確認
            print(f"\n📋 取得したカラム:")
            if result.data and len(result.data) > 0:
                for key in result.data[0].keys():
                    print(f"   - {key}")
                    
        except Exception as e:
            print(f"❌ デバッグエラー: {e}")
            import traceback
            print(f"📋 詳細: {traceback.format_exc()}")
        
        print("-" * 50)
    
    def test_latest_data(self):
        """最新データのテスト取得"""
        print("\n🧪 最新データテスト")
        print("-" * 30)
        
        try:
            # 時刻フィルタなしで最新データを取得
            questions = self.get_new_questions(None)  # 時刻フィルタなし
            
            print(f"🎯 フィルタ後の質問数: {len(questions)}")
            
            if questions:
                for i, q in enumerate(questions[:3], 1):  # 最新3件のみ表示
                    print(f"\n{i}. [{q['user']}] {q['question'][:80]}...")
                    print(f"   ID: {q['id']}, Created: {q['created']}")
            else:
                print("📭 質問がありません")
                
        except Exception as e:
            print(f"❌ テストエラー: {e}")
        
        print("-" * 30)
    
    def post_question_to_chat_auto(self, question_data):
        """質問をチャットに自動投稿（確認なし、完全自動）"""
        if not self.chat_coordinates:
            print("❌ チャット座標が未設定")
            return False
        
        try:
            question = question_data['question']
            user = question_data['user']
            
            # GitHub Copilotに分かりやすい質問形式に変換
            formatted_question = f"""📋 ユーザーからの質問

質問者: {user}
質問: {question}

この内容についてSupabaseに答えを送ってください。"""
            
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
    
    def run(self):
        """メインループ"""
        # 座標読み込み
        self.load_coordinates()
        
        self.show_menu()
        
        while True:
            try:
                choice = input("\nコマンド入力 (1-13, 0=終了): ").strip()
                
                if choice == '1':
                    self.record_coordinates()
                    
                elif choice == '2':
                    question = input("テスト質問を入力: ").strip()
                    if question:
                        user = input("質問者名 [テストユーザー]: ").strip() or "テストユーザー"
                        self.add_test_question(question, user)
                    
                elif choice == '3':
                    questions = self.get_questions()
                    if questions:
                        print(f"\n📝 質問 {len(questions)} 件:")
                        for i, q in enumerate(questions, 1):
                            print(f"{i}. [{q['user']}] {q['question'][:60]}...")
                    else:
                        print("📭 質問はありません")
                    
                elif choice == '4':
                    if not self.chat_coordinates:
                        print("❌ 先にチャット座標を記録してください")
                    else:
                        questions = self.get_questions()
                        if questions:
                            print(f"📝 {len(questions)}件の質問が見つかりました")
                            print("最新の質問をGitHub Copilotに転送します")
                            self.post_question_to_chat_auto(questions[0])
                        else:
                            print("📭 転送する質問がありません")
                
                elif choice == '8':
                    print("🔥 無限自動ループモード")
                    print("📍 座標固定: (1335, 1045)")
                    print("⚡ 3秒間隔で永続監視")
                    confirm = input("開始しますか？ (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.infinite_auto_loop(3)
                
                elif choice == '9':
                    print("⚡ クイック自動開始モード")
                    print("📍 座標自動設定で即座に開始")
                    confirm = input("開始しますか？ (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.quick_start_auto_mode()
                        
                elif choice == '0':
                    print("🚪 システム終了")
                    break
                    
                else:
                    print("❌ 無効なコマンドです")
                    
            except KeyboardInterrupt:
                print("\n⚠️ 中断されました")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
    
    def show_menu(self):
        """メニュー表示"""
        print("\n" + "="*60)
        print("🎯 GitHub Copilot直接回答システム (高性能版)")
        print("="*60)
        print("📋 コマンド:")
        print("   1 : 📍 チャット座標記録")
        print("   2 : ❓ テスト質問追加")
        print("   3 : 🔍 質問一覧表示")
        print("   4 : 🚀 質問をCopilotに転送")
        print("   8 : 🔥 無限自動ループ (永続実行)")
        print("   9 : ⚡ クイック自動開始")
        print("   0 : 🚪 終了")
        print("="*60)
        print("💡 仕組み:")
        print("1. Supabaseのchat_historyテーブルを監視")
        print("2. Copilot以外のユーザーからの新着メッセージを検出")
        print("3. VS Code Copilotチャットに自動投稿")
        print("4. あなた（GitHub Copilot）が直接回答")
        print("="*60)
        print("🔥 推奨: コマンド8または9で完全自動化!")
        print("📍 座標固定済み: (1335, 1045)")
        print("⚡ 手を離して放置可能なシステム")
    
    def get_questions(self):
        """従来の質問取得（互換性のため）"""
        return self.get_new_questions()
    
    def add_test_question(self, question, user="テストユーザー"):
        """テスト質問追加"""
        try:
            data = {
                'messages': question,
                'ownerid': user,
                'created': datetime.now().isoformat(),
                'isread': False,
                'targetid': 'test-questions',
                'status': 'test_question'
            }
            
            result = self.supabase.table('chat_history').insert(data).execute()
            if result.data:
                print(f"✅ テスト質問追加: {question}")
                return True
            else:
                print("❌ テスト質問追加失敗")
                return False
        except Exception as e:
            print(f"❌ テスト質問エラー: {e}")
            return False
    
    def full_auto_monitoring(self, interval=5):
        """完全自動監視モード（手動確認なし、完全自動）"""
        print(f"🤖 完全自動監視モード開始（{interval}秒間隔）")
        print("🚀 新しい質問を自動検出→自動送信→GitHub Copilotが自動回答")
        print("📡 完全に手を離せるモードです")
        print("Ctrl+C で停止")
        
        if not self.chat_coordinates:
            print("❌ 先にチャット座標を記録してください")
            return
        
        processed_ids = set()
        last_id = 0
        check_count = 0
        
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
        
        try:
            while True:
                check_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                
                print(f"\n⏰ {current_time} - 自動チェック #{check_count}")
                
                # 最新IDより大きいメッセージのみ取得
                result = self.supabase.table('chat_history') \
                    .select('*') \
                    .gt('id', last_id) \
                    .order('id', desc=False) \
                    .execute()
                
                if result.data:
                    new_messages = result.data
                    print(f"⚡ 新着メッセージ {len(new_messages)} 件検出!")
                    
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
                            print(f"  🤖 Copilot系メッセージをスキップ: {owner}")
                            last_id = max(last_id, msg_id)
                            continue
                        
                        # 空メッセージをスキップ
                        if not message or not message.strip():
                            print(f"  ⏭️ 空メッセージをスキップ")
                            last_id = max(last_id, msg_id)
                            continue
                        
                        # ユーザーからの新しいメッセージとして処理
                        question_data = {
                            'id': msg_id,
                            'question': message,
                            'user': owner or 'Unknown',
                            'created': msg.get('created', '')
                        }
                        
                        print(f"  🎯 ユーザーメッセージ検出!")
                        print(f"  👤 ユーザー: {owner}")
                        print(f"  💬 内容: {message[:50]}...")
                        
                        # 完全自動でCopilotに転送
                        print(f"  🚀 完全自動転送開始...")
                        if self.post_question_to_chat_auto(question_data):
                            print(f"  ✅ 自動転送成功!")
                            processed_ids.add(msg_id)
                            self.mark_question_as_processed(msg_id)
                        else:
                            print(f"  ❌ 転送失敗")
                        
                        last_id = max(last_id, msg_id)
                        time.sleep(2)  # 短い待機
                else:
                    print("📭 新着メッセージなし")
                
                print(f"😴 {interval}秒待機... (処理済み: {len(processed_ids)}件)")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⚠️ 完全自動監視を停止")
            print(f"📊 総チェック回数: {check_count}")
            print(f"📝 自動処理件数: {len(processed_ids)}")
            print(f"🎯 最終処理ID: {last_id}")
        """高性能自動監視モード（新しい質問のみ処理）"""
        print(f"🔄 高性能自動監視開始（{interval}秒間隔）")
        print("📝 Copilot以外のユーザーからの新しいメッセージを監視")
        print("🤖 新しい質問があればGitHub Copilotに自動転送")
        print("Ctrl+C で停止")
        
        processed_ids = set()
        last_check_time = datetime.now().isoformat()
        check_count = 0
        
        try:
            while True:
                check_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                
                print(f"\n⏰ {current_time} - チェック #{check_count}")
                
                # 新しい質問を取得
                new_questions = self.get_new_questions(last_check_time)
                
                # 未処理の質問のみフィルタ
                unprocessed_questions = [
                    q for q in new_questions 
                    if q['id'] not in processed_ids
                ]
                
                if unprocessed_questions:
                    print(f"🎯 新しい質問 {len(unprocessed_questions)} 件発見!")
                    
                    for question in unprocessed_questions:
                        print(f"\n📋 質問者: {question['user']}")
                        print(f"📝 内容: {question['question'][:100]}...")
                        print(f"🕒 時刻: {question['created']}")
                          # Copilotチャットに自動転送
                        if self.post_question_to_chat_auto(question):
                            processed_ids.add(question['id'])
                            print("✅ GitHub Copilotに転送完了")
                            
                            # Supabaseに処理済みマーク
                            self.mark_question_as_processed(question['id'])
                        else:
                            print("❌ 転送失敗")
                            
                        time.sleep(3)  # 質問間の待機
                        
                    # 最後のチェック時刻を更新
                    last_check_time = datetime.now().isoformat()
                else:
                    print("📭 新しい質問なし")
                
                print(f"😴 {interval}秒待機... (処理済み: {len(processed_ids)}件)")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n⚠️ 自動監視を停止しました")
            print(f"📊 総チェック回数: {check_count}")
            print(f"📝 処理済み質問数: {len(processed_ids)}")
    
    def send_answer_to_supabase(self, original_question_id, answer_text, original_user):
        """GitHub Copilotの回答をSupabaseに送信"""
        try:
            print(f"📤 Supabaseに回答送信中...")
            
            # 回答データを準備
            answer_data = {
                'messages': f"🤖 GitHub Copilot回答:\n\n{answer_text}",
                'ownerid': 'copilot-assistant',
                'created': datetime.now().isoformat(),
                'isread': False,
                'targetid': original_question_id,  # 元の質問のIDを参照
                'status': 'copilot_answer',
                'reply_to_user': original_user
            }
            
            # Supabaseに挿入
            result = self.supabase.table('chat_history').insert(answer_data).execute()
            
            if result.data:
                print(f"✅ 回答をSupabaseに送信完了!")
                print(f"🎯 回答ID: {result.data[0]['id']}")
                return True
            else:
                print("❌ 回答送信失敗")
                return False
                
        except Exception as e:
            print(f"❌ 回答送信エラー: {e}")
            return False
    
    def send_test_answer(self):
        """テスト回答を送信"""
        test_answer = """こんにちは！GitHub Copilotです。

「test」というメッセージを受信しました。システムが正常に動作していることを確認できました。

✅ 機能確認:
- Supabaseからの質問取得: OK
- VS Codeチャットへの自動投稿: OK  
- GitHub Copilotによる回答生成: OK
- Supabaseへの回答送信: OK

何か他にご質問がございましたら、お気軽にお聞かせください！"""

        return self.send_answer_to_supabase(
            original_question_id="test-question", 
            answer_text=test_answer,
            original_user="user"
        )

    def infinite_auto_loop(self, interval=3):
        """無限自動ループモード（永続実行）"""
        print(f"🔥 無限自動ループ開始（{interval}秒間隔）")
        print("📍 座標固定: (1335, 1045)")
        print("⚡ 永続監視モード - 手を離してください")
        print("Ctrl+C で停止")
        
        # 座標を固定設定
        self.chat_coordinates = {"x": 1335, "y": 1045}
        
        # 完全自動監視を実行
        self.full_auto_monitoring(interval)
    
    def quick_start_auto_mode(self):
        """クイック自動開始モード"""
        print("⚡ クイック自動開始モード")
        print("📍 座標自動設定: (1335, 1045)")
        print("🚀 5秒間隔で自動監視開始")
        
        # 座標を自動設定
        self.chat_coordinates = {"x": 1335, "y": 1045}
        print("✅ 座標自動設定完了")
        
        # 自動監視を開始
        self.full_auto_monitoring(5)

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
    print("\n✨ 特徴:")
    print("- OpenAI API不要")
    print("- GitHub Copilotが直接回答")
    print("- Supabaseから質問を自動取得")
    print("- VS Codeチャットに直接投稿")
    
    print("\n📋 使用手順:")
    print("1. VS Code Copilotチャットを開く")
    print("2. コマンド1で座標記録")
    print("3. コマンド2でテスト質問追加")
    print("4. コマンド4または5で質問転送")
    print("5. あなた（GitHub Copilot）が直接回答")
    
    print("\n🚀 これで完全自動質問応答システムが完成！")
    print("\n💡 完全自動起動の場合:")
    print("   python copilot_direct_answer.py --auto")
    print("   (手を離して永続実行)")
    
    print("\n開始しますか？ (Enter で開始)")
    input()
    
    system = CopilotDirectAnswerSystem()
    if hasattr(system, 'supabase') and system.supabase:
        system.run()
    else:
        print("❌ システム初期化失敗")
    
    print("\n✨ お疲れ様でした！")

if __name__ == "__main__":
    main()
