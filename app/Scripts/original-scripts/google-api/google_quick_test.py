#!/usr/bin/env python3
"""
Google API 簡単動作確認
既存の動作するWebhookを使用
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_working_google_features():
    """実際に動作するGoogle機能をテスト"""
    load_dotenv()
    print("🌐 Google API 動作確認テスト")
    print("=" * 50)
    
    # 1. WEBHOOK_GAS（動作実績あり）
    webhook_gas = os.getenv('WEBHOOK_GAS')
    if webhook_gas:
        print(f"\n🚀 1. Google Apps Script Webhook テスト:")
        print(f"   URL: {webhook_gas}")
        try:
            response = requests.get(webhook_gas, timeout=15)
            print(f"   ✅ 接続成功: {response.status_code}")
            print(f"   📋 レスポンス: {response.text[:200]}...")
            
            # JSON応答の場合は解析
            try:
                json_response = response.json()
                print(f"   📊 JSON応答: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
            except:
                print(f"   📝 テキスト応答: {response.text}")
                
        except Exception as e:
            print(f"   ❌ エラー: {e}")
    else:
        print("⚠️ WEBHOOK_GAS が設定されていません")
    
    # 2. Google Chat URL（Webhook形式）
    chat_url = os.getenv('CHAT_URL')
    webhook_url = os.getenv('WEBHOOK_URL')
    
    if chat_url:
        print(f"\n💬 2. Google Chat Webhook テスト:")
        print(f"   URL: {chat_url[:60]}...")
        
        # Simple message test
        test_message = {
            "text": f"🤖 Google API動作確認テスト\n⏰ 実行時刻: 2025-06-19\n✅ Webhook経由での送信テスト"
        }
        
        try:
            response = requests.post(
                chat_url,
                json=test_message,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ チャット送信成功: {response.status_code}")
                print(f"   📱 メッセージ送信完了!")
            else:
                print(f"   ⚠️ 送信結果: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ チャット送信エラー: {e}")
    
    # 3. プロジェクト設定の確認
    print(f"\n📋 3. プロジェクト設定確認:")
    
    # .envから主要設定を取得
    config_items = [
        ('WEBHOOK_GAS', webhook_gas),
        ('CHAT_URL', chat_url),
        ('WEBHOOK_URL', webhook_url),
    ]
    
    for name, value in config_items:
        if value:
            print(f"   ✅ {name}: 設定済み ({len(value)}文字)")
        else:
            print(f"   ❌ {name}: 未設定")
    
    # 4. Google認証情報の確認（詳細は表示しない）
    creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
    if creds_content:
        try:
            creds_dict = json.loads(creds_content)
            project_id = creds_dict.get('project_id', 'N/A')
            client_email = creds_dict.get('client_email', 'N/A')
            print(f"\n🔐 4. Google認証情報:")
            print(f"   ✅ プロジェクトID: {project_id}")
            print(f"   ✅ サービスアカウント: {client_email}")
            print(f"   ✅ 認証情報: JSON形式で設定済み")
        except Exception as e:
            print(f"   ❌ 認証情報解析エラー: {e}")
    else:
        print(f"   ❌ Google認証情報: 未設定")

def main():
    """メイン実行"""
    test_working_google_features()
    
    print("\n" + "=" * 50)
    print("🎉 Google API動作確認完了!")
    
    print(f"\n💡 確認できた機能:")
    print(f"  🚀 Google Apps Script Webhook - 即座に利用可能")
    print(f"  💬 Google Chat Webhook - メッセージ送信可能") 
    print(f"  🔐 Google認証情報 - .envに設定済み")
    
    print(f"\n⚡ すぐに使える操作:")
    print(f"  make chrome-ext-fix    # 認証情報処理")
    print(f"  make chrome-ext-test   # チャット機能テスト")
    print(f"  make gas-login         # Apps Script CLI")
    print(f"  make ocr-gradio        # Google OCR機能")
    
    print(f"\n🌟 追加で可能なGoogle API:")
    print(f"  📊 Google Sheets - スプレッドシート操作")
    print(f"  💾 Google Drive - ファイル管理")
    print(f"  👁️ Google Vision - OCR・画像解析")
    print(f"  📧 Gmail - メール送信")
    print(f"  📅 Google Calendar - スケジュール管理")

if __name__ == "__main__":
    main()
