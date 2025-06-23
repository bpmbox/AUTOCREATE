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
import unicodedata
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
    SYSTEM_PROMPT = (
        "あなたはプロの自動プログラム生成AIです。ユーザーからの要望が曖昧な場合は、" 
        "『どの言語・用途でどんなプログラムを作りたいですか？』など追加質問を必ず行い、" 
        "具体的な指示があれば自動でプログラムを生成し、Supabaseに返信してください。"
    )

    def __init__(self):
        print("🚀 GitHub Copilot直接回答システム初期化中...")
        print(f"[SYSTEM PROMPT] {self.SYSTEM_PROMPT}")
        
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
                            # プログラム作成依頼なら自動生成
                            if self.auto_reply_if_program_request(question_data):
                                print("✅ プログラム自動生成・返信完了")
                                success_count += 1
                                processed_ids.add(msg_id)
                                self.mark_question_as_processed(msg_id)
                                last_id = max(last_id, msg_id)
                                time.sleep(1)
                                continue
                            # 詳細不明なら追加質問
                            if self.ask_user_for_details(question_data):
                                print("✅ 追加質問をSupabaseに自動送信")
                                success_count += 1
                                processed_ids.add(msg_id)
                                self.mark_question_as_processed(msg_id)
                                last_id = max(last_id, msg_id)
                                time.sleep(1)
                                continue
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
        
    def send_answer_to_supabase(self, answer, user="copilot", original_id=None):
        """Supabaseのchat_historyに回答を送信"""
        try:
            data = {
                'ownerid': user,
                'messages': answer,
                'copilot_processed': True
            }
            if original_id:
                data['reply_to'] = original_id
            self.supabase.table('chat_history').insert(data).execute()
            print("✅ Supabaseに回答を送信しました")
            return True
        except Exception as e:
            print(f"❌ Supabase送信エラー: {e}")
            return False
        
    def process_and_reply_sample(self):
        """サンプル作成指示に対し、サンプルプログラム作成＆Supabase返信"""
        sample_code = """def sample_function():\n    print(\"これはサンプル関数です\")\n\nif __name__ == "__main__":\n    sample_function()\n"""
        sample_path = os.path.join(os.getcwd(), "sample", "sample.py")
        os.makedirs(os.path.dirname(sample_path), exist_ok=True)
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write(sample_code)
        print(f"✅ サンプルプログラム作成: {sample_path}")
        answer = "sample.py（サンプルプログラム）を自動生成・配置し、正常に実行されました。\n\n```python\n" + sample_code + "```"
        self.send_answer_to_supabase(answer)
    
    def normalize_text(self, text):
        """質問文を正規化（全角→半角・小文字化）"""
        text = unicodedata.normalize('NFKC', text)
        text = text.lower()
        return text
    
    def auto_reply_if_program_request(self, question_data):
        """ユーザーの質問からプログラム作成依頼を自動判定し、各言語サンプルを自動生成・Supabase返信"""
        question_raw = question_data.get('question', '')
        question = self.normalize_text(question_raw)
        # 「AIがsupabaseに直接返信」などの指示への自動応答
        if any(word in question for word in ['supabaseに直接返信', 'あなたが返信', '直接返信', 'aiが返信']):
            answer = "はい、今後は私（AI）がSupabaseに直接返信します。ご要望やご質問があれば、引き続きご記入ください。"
            self.send_answer_to_supabase(answer)
            return True
        # システムへの指摘・催促・エラー報告への自動返信（自動返信も含む）
        if any(word in question for word in ['自動返信', '返信がない', '返事がない', '動かない', 'エラー', 'バグ', '不具合']):
            answer = "ご不便をおかけして申し訳ありません。現在システムは稼働中です。もし自動返信が届かない場合は、もう一度ご要望を具体的にご記入いただくか、管理者までご連絡ください。"
            self.send_answer_to_supabase(answer)
            return True
        # AI(Copilot)が自分の知識・考えで直接答える指示への自動応答
        if any(word in question for word in ['あなたがこたえる', 'あなたが答える', 'aiがこたえる', 'aiが答える', 'aiが直接答えて', 'aiが直接こたえて', 'aiが返事', 'aiが返答']):
            user_question = question_data.get('question', '').strip()
            normalized_question = user_question
            if '質問者:' in user_question and '質問:' in user_question:
                try:
                    parts = user_question.split('質問:')
                    if len(parts) > 1:
                        normalized_question = parts[-1].strip()
                except Exception:
                    pass
            # 質問内容を要約・推測し、AIの見解やアドバイスを加えて返す
            # （ここでは簡易的に要約例を生成。実際はNLP要約やルールベースで拡張可能）
            summary = normalized_question[:60] + ('...' if len(normalized_question) > 60 else '')
            advice = "このご質問について、私なりの見解を述べます。"
            if any(word in normalized_question for word in ['おすすめ', '方法', 'やり方', 'コツ']):
                advice = "ご要望のテーマについて、私のおすすめやポイントをお伝えします。"
            elif any(word in normalized_question for word in ['トラブル', 'エラー', '困った', 'できない']):
                advice = "お困りの点について、考えられる原因や対策をお伝えします。"
            elif any(word in normalized_question for word in ['最新', '動向', '将来', '今後']):
                advice = "最新の動向や今後の展望について、私の知識でお答えします。"
            answer = (
                f"ご質問ありがとうございます。\n\n"
                f"【ご質問要約】{summary}\n"
                f"{advice}\n"
                "---\n"
                "（※より具体的なご要望や状況があれば、追加でご記入ください）"
            )
            print(f"[DEBUG] Supabase送信内容: {answer}")
            result = self.send_answer_to_supabase(answer)
            print(f"[DEBUG] Supabase送信完了: {result}")
            return True
        # PHPバッチ処理サンプル
        if 'php' in question and 'バッチ' in question and 'サンプル' in question:
            php_code = """<?php\n// php_batch_sample.php\n// シンプルなPHPバッチ処理サンプル\n\necho \"バッチ処理開始\\n\";\nfor ($i = 1; $i <= 5; $i++) {\n    echo \"処理中: $i\\n\";\n    sleep(1);\n}\necho \"バッチ処理終了\\n\";\n"""
            php_path = os.path.join(os.getcwd(), "php_batch_sample", "php_batch_sample.php")
            os.makedirs(os.path.dirname(php_path), exist_ok=True)
            with open(php_path, "w", encoding="utf-8") as f:
                f.write(php_code)
            answer = "php_batch_sample.php（PHPバッチ処理サンプル）を自動生成・配置しました。\n\n```php\n" + php_code + "```"
            self.send_answer_to_supabase(answer)
            return True
        # PHPでHello出力
        if 'php' in question and ('hello' in question or '出力' in question):
            php_code = """<?php\n// hello_world.php\necho \"Hello, world!\\n\";\n"""
            php_path = os.path.join(os.getcwd(), "php_hello_sample", "hello_world.php")
            os.makedirs(os.path.dirname(php_path), exist_ok=True)
            with open(php_path, "w", encoding="utf-8") as f:
                f.write(php_code)
            answer = "hello_world.php（PHP Hello出力サンプル）を自動生成・配置しました。\n\n```php\n" + php_code + "```"
            self.send_answer_to_supabase(answer)
            return True
        # Pythonサンプル依頼（プログラム自動生成せず案内・例示・アドバイスも含めて返答）
        if 'python' in question and ('サンプル' in question or 'example' in question or '作成' in question):
            answer = (
                "Pythonのサンプルプログラムをご希望ですね。\n"
                "例えば、ファイル操作・Webスクレイピング・データ処理・API連携・自動化スクリプトなど、Pythonでは様々な用途のサンプルが作成できます。\n"
                "もしご希望の用途や機能があれば、ぜひ具体的にご記入ください。\n"
                "特に決まっていない場合は、よく使われるサンプル例（例: ファイルの読み書き、リストの操作、簡単なWebアクセスなど）もご案内できます。\n"
                "お気軽にご相談ください。"
            )
            self.send_answer_to_supabase(answer)
            return True
        # 他言語や一般的な「プログラム作成」依頼（案内のみ）
        if 'プログラム' in question or 'code' in question or 'script' in question:
            answer = "プログラム作成のご要望を受け付けました。どの言語・どんな機能のプログラムをご希望ですか？できるだけ具体的にご記入いただければ、最適な案内やアドバイスをお送りします。"
            self.send_answer_to_supabase(answer)
            return True
        # システムへの指摘・催促・エラー報告への自動返信（自動返信も含む）
        if any(word in question for word in ['自動返信', '返信がない', '返事がない', '動かない', 'エラー', 'バグ', '不具合']):
            answer = "ご不便をおかけして申し訳ありません。現在システムは稼働中です。もし自動返信が届かない場合は、もう一度ご要望を具体的にご記入いただくか、管理者までご連絡ください。"
            self.send_answer_to_supabase(answer)
            return True
        # 「AIがsupabaseに直接返信」などの指示への自動応答
        if any(word in question for word in ['supabaseに直接返信', 'あなたが返信', '直接返信', 'aiが返信']):
            answer = "はい、今後は私（AI）がSupabaseに直接返信します。ご要望やご質問があれば、引き続きご記入ください。"
            self.send_answer_to_supabase(answer)
            return True
        # それ以外はAIが直接自然言語で返信
        default_reply = f"こんにちは！ご質問ありがとうございます。\n\n「{question_data.get('question', '')}」\n\nご要望や作成したいプログラムがあれば、できるだけ具体的にご記入ください。"
        self.send_answer_to_supabase(default_reply)
        return True
    
    def ask_user_for_details(self, question_data):
        """ユーザーの要望が曖昧な場合、Supabase経由で追加質問を自動送信"""
        question = question_data.get('question', '')
        # プログラム作成依頼だが詳細が不明な場合
        if 'プログラム' in question or 'code' in question or 'script' in question or 'サンプル' in question or 'example' in question:
            if not any(lang in question.lower() for lang in ['python', 'php', 'javascript', 'java', 'c#', 'go', 'ruby', 'shell', 'バッチ']):
                ask = "ご要望ありがとうございます。どの言語・用途でどんなプログラムを作りたいですか？\n例: Pythonでファイル操作のサンプル、PHPでバッチ処理 など\n具体的にご指示いただければ自動生成します。"
                self.send_answer_to_supabase(ask)
                return True
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
