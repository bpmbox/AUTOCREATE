#!/usr/bin/env python3
"""
Supabaseに回答を送信するスクリプト
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

# 環境変数読み込み
load_dotenv()

def send_answer_to_supabase():
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not all([supabase_url, supabase_key]):
            print("❌ 環境変数が設定されていません")
            return False
        
        supabase = create_client(supabase_url, supabase_key)
        
        # GitHub Copilotからの詳細回答
        answer = """🤖 GitHub Copilotからの回答

質問「別のシステムからそうしん」について詳しく回答いたします：

## 📡 外部システム連携の実装方法

### 1. **API連携による送信**
```python
# REST API経由での送信例
import requests
import json

def send_to_external_system(data):
    url = "https://your-api-endpoint.com/api/data"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_TOKEN'
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

### 2. **Supabaseからの送信**
```python
# Supabaseから外部システムへの送信
from supabase import create_client

def supabase_to_external():
    supabase = create_client(url, key)
    
    # データ取得
    result = supabase.table('source_table').select('*').execute()
    
    # 外部システムに送信
    for record in result.data:
        send_to_external_system(record)
```

### 3. **Webhook設定**
- Supabaseの Database Webhooks機能を使用
- リアルタイムでデータ変更を通知
- 自動トリガーによる連携

### 4. **定期バッチ処理**
```python
# 定期実行スクリプト
import schedule
import time

def sync_data():
    # データ同期処理
    print("データ同期実行中...")

schedule.every(10).minutes.do(sync_data)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## 🔧 実装時の注意点

1. **認証・セキュリティ**
   - API キーの適切な管理
   - HTTPS通信の使用
   - レート制限の考慮

2. **エラーハンドリング**
   - リトライ機能の実装
   - ログ記録
   - 失敗時の通知

3. **データ整合性**
   - トランザクション処理
   - 重複チェック
   - バックアップ機能

ご質問の「別のシステムから送信」について、具体的にどのようなシステム間連携をお考えでしょうか？詳細をお聞かせいただければ、より具体的な実装方法をご提案いたします！

🚀 お役に立てれば幸いです！"""

        # Supabaseに回答を投稿
        result = supabase.table('chat_history').insert({
            'ownerid': 'GitHub Copilot Assistant',
            'messages': answer,
            'created': datetime.now().isoformat()
        }).execute()
        
        print('✅ Supabaseに回答を送信しました！')
        if result.data:
            print(f'📊 投稿ID: {result.data[0]["id"]}')
        print('🎯 回答内容を送信完了')
        
        return True
        
    except Exception as e:
        print(f'❌ エラー: {e}')
        return False

if __name__ == "__main__":
    send_answer_to_supabase()
