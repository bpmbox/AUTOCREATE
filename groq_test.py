import requests
import os
import json
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def test_groq_api():
    """Groq APIのテスト"""
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not groq_api_key:
        print('❌ GROQ_API_KEY が環境変数に設定されていません')
        return False

    print('🔍 Groq API キーをテスト中...')
    
    try:
        response = requests.post('https://api.groq.com/openai/v1/chat/completions', 
            headers={
                'Authorization': f'Bearer {groq_api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-70b-versatile',
                'messages': [
                    {
                        'role': 'user',
                        'content': 'こんにちは！簡単なテストメッセージです。Python版です。'
                    }
                ],
                'max_tokens': 100,
                'temperature': 0.7
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print('✅ Groq API テスト成功!')
            print('📤 送信メッセージ: こんにちは！簡単なテストメッセージです。Python版です。')
            print('📥 受信レスポンス:', data['choices'][0]['message']['content'])
            print('🔢 使用トークン数:', data['usage']['total_tokens'])
            print('⚡ モデル:', data['model'])
            return True
        else:
            print(f'❌ Groq API テスト失敗: {response.status_code}')
            print('エラーメッセージ:', response.text)
            return False
            
    except Exception as e:
        print(f'❌ Groq API テスト中にエラーが発生: {e}')
        return False

def list_groq_models():
    """利用可能なGroqモデル一覧を取得"""
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not groq_api_key:
        print('❌ GROQ_API_KEY が環境変数に設定されていません')
        return

    try:
        response = requests.get('https://api.groq.com/openai/v1/models',
            headers={
                'Authorization': f'Bearer {groq_api_key}',
                'Content-Type': 'application/json'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print('📋 利用可能なGroqモデル一覧:')
            for i, model in enumerate(data['data'], 1):
                print(f'{i}. {model["id"]}')
        else:
            print(f'❌ モデル一覧取得失敗: {response.status_code}')
            print('エラーメッセージ:', response.text)
            
    except Exception as e:
        print(f'❌ モデル一覧取得中にエラーが発生: {e}')

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'test':
            test_groq_api()
        elif command == 'models':
            list_groq_models()
        elif command == 'both':
            test_groq_api()
            print('\n' + '='*50 + '\n')
            list_groq_models()
        else:
            print('使用方法:')
            print('  python groq_test.py test    - API接続テスト')
            print('  python groq_test.py models  - 利用可能モデル一覧')
            print('  python groq_test.py both    - 両方実行')
    else:
        print('使用方法:')
        print('  python groq_test.py test    - API接続テスト')
        print('  python groq_test.py models  - 利用可能モデル一覧')
        print('  python groq_test.py both    - 両方実行')
