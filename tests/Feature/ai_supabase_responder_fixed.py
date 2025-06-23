#!/usr/bin/env python3
"""
🎯 AI自動返信システム（修正版）

Supabaseから質問を取得 → AIが直接返信をSupabaseに送信
スキーマエラー対応版
"""

import os
import time
import json
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
    print("📦 pip install supabase python-dotenv")
    exit(1)

class AISupabaseResponder:
    def __init__(self):
        print("🚀 AI自動返信システム初期化中...")
        
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
        
        print("🎯 システム初期化完了")
    
    def infinite_auto_loop(self, interval=5):
        """無限自動ループモード（修正版）"""
        print("🔥 AI自動返信モード開始!")
        print(f"⚡ {interval}秒間隔で永続監視")
        print("🤖 新着質問にAIが直接返信")
        print("💬 Supabase経由で自動応答")
        print("🔧 スキーマエラー対応版")
        print("="*50)
        
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
                            
                            # AI系・Bot系は除外
                            if owner and (
                                owner.lower().startswith('ai') or 
                                owner.lower().startswith('bot') or
                                owner.lower().startswith('copilot') or
                                owner.lower().startswith('assistant') or
                                'ai' in owner.lower() or
                                'bot' in owner.lower()
                            ):
                                print(f"  🤖 AI/Bot系スキップ: {owner}")
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
                            
                            print(f"\n🎯 ユーザー質問検出!")
                            print(f"👤 {owner}: {message[:50]}...")
                            
                            # AIが直接返信
                            if self.generate_ai_reply_and_send(question_data):
                                success_count += 1
                                processed_ids.add(msg_id)
                                print(f"✅ AI自動返信成功! (累計: {success_count}件)")
                            else:
                                print("❌ AI返信失敗")
                            
                            last_id = max(last_id, msg_id)
                            time.sleep(2)  # メッセージ間の待機
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
    
    def generate_ai_reply_and_send(self, question_data):
        """質問に対してAIが返信を生成しSupabaseに送信"""
        try:
            question = question_data['question']
            user = question_data['user']
            
            print(f"🤖 AI返信生成中...")
            print(f"質問: {question}")
            
            # AI返信を生成
            ai_reply = self.generate_ai_response(question, user)
            
            # Supabaseに返信を送信（スキーマに合わせて最小限のフィールドのみ）
            if self.send_reply_to_supabase(ai_reply, user):
                print("✅ AI返信をSupabaseに送信完了")
                return True
            else:
                print("❌ Supabase送信失敗")
                return False
                
        except Exception as e:
            print(f"❌ AI返信生成エラー: {e}")
            traceback.print_exc()
            return False
    
    def generate_ai_response(self, question, user):
        """質問に対するAI返信を生成"""
        question_normalized = self.normalize_text(question)
        current_time = datetime.now()
        hour = current_time.hour
        
        # 時間帯に応じた挨拶
        if 5 <= hour < 12:
            time_greeting = "おはようございます"
        elif 12 <= hour < 18:
            time_greeting = "こんにちは"
        else:
            time_greeting = "こんばんは"
        
        # 挨拶への対応
        if any(word in question_normalized for word in ['こんにちは', 'こんにちわ', 'hello', 'hi', 'はじめまして']):
            return f"""こんにちは、{user}さん！

{time_greeting}！AI自動応答システムです。

🎯 **システム情報**
- 現在時刻: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
- 対応言語: 日本語・英語
- 稼働状況: 正常動作中

💡 **対応可能な内容**
- プログラム作成（Python、PHP、JavaScript等）
- 技術的な質問・相談
- システム開発のアドバイス
- 自動化スクリプト作成
- データ処理・API連携

🚀 **ご利用方法**
具体的なご要望やご質問をお聞かせください。
例：
- "Pythonでファイル処理のプログラムを作って"
- "PHPでデータベース接続のサンプルが欲しい"
- "JavaScriptでAPI呼び出しの方法を教えて"

何かお手伝いできることがあれば、お気軽にお声がけください！"""
        
        # プログラム作成依頼の場合
        if any(word in question_normalized for word in ['プログラム', 'program', 'code', 'script', 'サンプル', 'example']):
            if 'python' in question_normalized:
                return self.generate_python_response(question)
            elif 'php' in question_normalized:
                return self.generate_php_response(question)
            elif 'javascript' in question_normalized or 'js' in question_normalized:
                return self.generate_javascript_response(question)
            else:
                return f"""こんにちは{user}さん！

プログラム作成のご要望ですね。
どの言語でどのような機能のプログラムをご希望ですか？

**対応可能な言語：**
- Python: データ処理、自動化スクリプト
- PHP: Web開発、API作成  
- JavaScript: フロントエンド、Node.js
- その他の言語もご相談ください

具体的にお聞かせください！"""
        
        # テスト関連
        if any(word in question_normalized for word in ['テスト', 'test', '動作確認']):
            return f"""テストありがとうございます、{user}さん！

AI自動返信システムは正常に動作しています。

**現在の機能：**
✅ 質問の自動検出
✅ AI返信の自動生成  
✅ Supabaseへの自動送信
✅ バックグラウンド実行
✅ スキーマエラー対応

他にご質問やご要望があれば、お気軽にお聞かせください。"""
        
        # エラー・問題報告
        if any(word in question_normalized for word in ['エラー', 'error', '動かない', '問題', 'バグ', 'bug']):
            return f"""お困りのようですね、{user}さん。

問題の詳細を教えていただけますか？

**確認事項：**
- どのような操作をした時に発生しましたか？
- エラーメッセージはありましたか？
- 使用している環境（OS、ブラウザ等）

詳細をお聞かせいただければ、解決策をご提案いたします。"""
        
        # デフォルト返信
        return f"""こんにちは、{user}さん！

ご質問ありがとうございます。

「{question}」

について、もう少し詳しく教えていただけますか？

具体的なご要望や状況をお聞かせいただければ、より適切な回答やサポートをご提供できます。

お気軽にご相談ください！"""
    
    def generate_python_response(self, question):
        """Python関連の返信を生成"""
        return """Pythonのサンプルプログラムをご紹介します。

```python
# ファイル読み込みの基本例
def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"ファイル読み込み成功: {filename}")
        return content
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filename}")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None

# 使用例
content = read_file("sample.txt")
if content:
    print(content)
```

**対応可能な分野：**
- ファイル操作（読み書き、CSV、JSON）
- API連携（REST API、認証）
- データ処理（pandas、numpy）
- Web開発（Flask、Django）
- 自動化スクリプト

具体的な用途があれば教えてください！"""
    
    def generate_php_response(self, question):
        """PHP関連の返信を生成"""
        return """PHPのサンプルプログラムをご用意いたします。

```php
<?php
// 基本的なPHPサンプル
function hello_world($name = "World") {
    return "Hello, " . $name . "!";
}

// データベース接続例（PDO）
function connect_database() {
    try {
        $pdo = new PDO('mysql:host=localhost;dbname=test', $username, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        return $pdo;
    } catch(PDOException $e) {
        echo "接続エラー: " . $e->getMessage();
        return null;
    }
}

echo hello_world("PHP User");
?>
```

**対応可能な内容：**
- Web開発（フォーム処理、セッション管理）
- データベース操作（MySQL、PostgreSQL）
- API開発（REST API、JSON処理）
- ファイル操作
- バッチ処理

具体的なご要望をお聞かせください！"""
    
    def generate_javascript_response(self, question):
        """JavaScript関連の返信を生成"""
        return """JavaScriptのサンプルをご紹介します。

```javascript
// 基本的なJavaScript関数
function greetUser(name = "User") {
    return `Hello, ${name}!`;
}

// 非同期処理の例
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

console.log(greetUser("JavaScript Developer"));
```

**対応分野：**
- フロントエンド開発（DOM操作、イベント処理）
- Node.js（サーバーサイド開発）
- API連携（fetch、axios）
- 非同期処理（Promise、async/await）

どのような機能を実装したいですか？"""
    
    def normalize_text(self, text):
        """テキストを正規化"""
        if not text:
            return ""
        text = unicodedata.normalize('NFKC', text)
        return text.lower()
    
    def send_reply_to_supabase(self, reply, original_user):
        """返信をSupabaseに送信（最小限のフィールドのみ）"""
        try:
            # 基本的なフィールドのみ使用
            data = {
                'ownerid': 'AI-Assistant',
                'messages': reply
            }
            
            result = self.supabase.table('chat_history').insert(data).execute()
            return True
            
        except Exception as e:
            print(f"❌ Supabase送信エラー: {e}")
            traceback.print_exc()
            return False

def main():
    import sys
    
    # バックグラウンド自動実行モード
    if len(sys.argv) > 1 and sys.argv[1] == '--background':
        print("🔥 バックグラウンド自動実行モード（修正版）")
        print("🤖 AI自動返信システム起動中...")
        print("🔧 スキーマエラー対応版")
        print("-" * 50)
        
        system = AISupabaseResponder()
        if hasattr(system, 'supabase') and system.supabase:
            print("✅ システム初期化完了")
            
            # 無限自動ループを即座に開始
            system.infinite_auto_loop(5)  # 5秒間隔
        else:
            print("❌ システム初期化失敗")
        return
    
    print("🎯 AI自動返信システム（修正版）")
    print("バックグラウンドで起動してください:")
    print("python ai_supabase_responder_fixed.py --background")

if __name__ == "__main__":
    main()
