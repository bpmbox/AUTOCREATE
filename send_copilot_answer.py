#!/usr/bin/env python3
"""
GitHub Copilot回答送信テスト
"""

import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def send_copilot_answer():
    print("🎯 GitHub Copilot回答送信システム")
    print("=" * 50)
    
    try:
        from supabase import create_client
        
        # 環境変数取得
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ 環境変数が設定されていません")
            return False
        
        print("✅ 環境変数確認OK")
        
        # Supabase接続
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Supabase接続成功")
        
        # GitHub Copilotからの回答
        copilot_response = f"""📋 ユーザー質問への回答

質問: test
質問者: user

🤖 GitHub Copilot回答:

こんにちは！テストメッセージを受信しました。

✅ システム動作確認:
- Supabaseからの質問取得: 正常
- VS Codeチャットへの自動投稿: 正常  
- GitHub Copilotによる回答生成: 正常
- Supabaseへの回答送信: 実行中

システムが正常に動作しています！何か他にご質問があれば、お気軽にお聞かせください。

---
🕒 回答時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🤖 回答者: GitHub Copilot Assistant"""
        
        # 回答データ
        answer_data = {
            'messages': copilot_response,
            'ownerid': 'github-copilot',
            'created': datetime.now().isoformat(),
            'isread': False,
            'targetid': 'user-test-question',
            'status': 'copilot_response'
        }
        
        print("📤 GitHub Copilotの回答をSupabaseに送信中...")
        result = supabase.table('chat_history').insert(answer_data).execute()
        
        if result.data:
            record_id = result.data[0]['id']
            print(f"✅ 回答送信成功! ID: {record_id}")
            print("📊 送信データ:")
            print(f"   📝 Owner: {answer_data['ownerid']}")
            print(f"   🏷️  Status: {answer_data['status']}")
            print(f"   🎯 Target: {answer_data['targetid']}")
            print(f"   📅 Created: {answer_data['created']}")
            print(f"   💬 Message Length: {len(copilot_response)} chars")
            return True
        else:
            print("❌ 回答送信失敗")
            return False
            
    except ImportError as e:
        print(f"❌ パッケージエラー: {e}")
        print("💡 pip install supabase python-dotenv")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = send_copilot_answer()
    if success:
        print("\n🎉 GitHub Copilotの回答送信完了!")
        print("📱 Supabaseのchat_historyテーブルで確認してください")
    else:
        print("\n❌ 回答送信に失敗しました")
