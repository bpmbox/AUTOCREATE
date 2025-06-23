#!/usr/bin/env python3
"""
🎯 ユーザー挨拶対応システム - 修正版

ユーザーからの挨拶に対する自動応答プログラム
GitHub Issue: user-greeting-hello
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ supabaseパッケージが必要です: pip install supabase")
    exit(1)

def main():
    """メイン実行 - 挨拶対応"""
    print("🎯 ユーザー挨拶対応システム")
    print("=" * 50)
    
    # Supabase初期化
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    current_time = datetime.now()
    hour = current_time.hour
    
    # 時間帯に応じた挨拶
    if 5 <= hour < 12:
        time_greeting = "おはようございます"
    elif 12 <= hour < 18:
        time_greeting = "こんにちは"
    else:
        time_greeting = "こんばんは"
    
    # 応答メッセージ生成
    response = f"""こんにちは、userさん！

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
    
    print("🎯 userさんからの挨拶を処理中...")
    
    # Supabaseに送信
    if supabase_url and supabase_key:
        try:
            supabase = create_client(supabase_url, supabase_key)
            data = {
                'ownerid': 'AI-Assistant',
                'messages': response
            }
            result = supabase.table('chat_history').insert(data).execute()
            print("✅ Supabaseに応答を送信しました")
            supabase_success = True
        except Exception as e:
            print(f"❌ Supabase送信エラー: {e}")
            supabase_success = False
    else:
        print("⚠️ Supabase設定なし - ローカル実行モード")
        supabase_success = False
    
    if not supabase_success:
        print("📝 ローカル出力:")
        print(response)
    
    print("\n📊 処理結果:")
    print("=" * 50)
    print(response)
    print("=" * 50)
    print("✨ 処理完了")
    
    # 実行結果をファイルに保存
    result_data = {
        "timestamp": current_time.isoformat(),
        "user": "user",
        "request": "こんにちわ",
        "response": response,
        "supabase_sent": supabase_success,
        "status": "completed"
    }
    
    with open("execution_result.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print("📁 実行結果をexecution_result.jsonに保存しました")

if __name__ == "__main__":
    main()
