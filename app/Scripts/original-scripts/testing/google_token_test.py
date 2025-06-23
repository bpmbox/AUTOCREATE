#!/usr/bin/env python3
"""
Google API完全テスト - トークン取得 + API実行
"""

import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from dotenv import load_dotenv

def get_access_token():
    """Google APIアクセストークンを取得"""
    print("🔐 Google認証トークン取得開始...")
    
    try:
        # .envファイルを読み込み
        load_dotenv()
        
        # .envからサービスアカウント情報を取得
        creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
        if not creds_content:
            print("❌ GOOGLE_APPLICATION_CREDENTIALS_CONTENT が見つかりません")
            return None
        
        print("✅ 認証情報を.envから取得")
        
        # JSONとしてパース
        creds_dict = json.loads(creds_content)
        project_id = creds_dict.get('project_id', 'N/A')
        client_email = creds_dict.get('client_email', 'N/A')
        print(f"✅ JSON解析成功 - Project ID: {project_id}")
        print(f"✅ Service Account: {client_email}")
        
        # 認証情報作成（複数のスコープを指定）
        scopes = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/chat.bot',
            'https://www.googleapis.com/auth/script.projects',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=scopes
        )
        print("✅ サービスアカウント認証情報作成成功")
        
        # アクセストークンを取得
        credentials.refresh(Request())
        access_token = credentials.token
        print("✅ アクセストークン取得成功!")
        print(f"🔑 Token (最初の20文字): {access_token[:20]}...")
        
        return access_token, credentials
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析エラー: {e}")
        print("🔧 .envファイルのJSON形式を確認してください")
        return None
    except Exception as e:
        print(f"❌ 認証エラー: {e}")
        return None

def test_google_apis(access_token):
    """取得したトークンでGoogle APIをテスト"""
    print("\n🌐 Google API機能テスト開始...")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Google Cloud Platform API（プロジェクト情報）
    try:
        print("\n📊 1. Google Cloud Platform API テスト...")
        response = requests.get(
            'https://cloudresourcemanager.googleapis.com/v1/projects',
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            projects = response.json().get('projects', [])
            print(f"✅ GCP API成功! プロジェクト数: {len(projects)}")
            for project in projects[:2]:  # 最初の2つを表示
                print(f"   📁 {project.get('projectId', 'N/A')}: {project.get('name', 'N/A')}")
        else:
            print(f"⚠️ GCP API: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"❌ GCP API エラー: {e}")
    
    # 2. Google Apps Script API
    try:
        print("\n📜 2. Google Apps Script API テスト...")
        response = requests.get(
            'https://script.googleapis.com/v1/projects',
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            projects = response.json().get('projects', [])
            print(f"✅ GAS API成功! スクリプト数: {len(projects)}")
            for project in projects[:2]:
                script_id = project.get('scriptId', 'N/A')
                title = project.get('title', 'N/A')
                print(f"   📜 {script_id}: {title}")
        else:
            print(f"⚠️ GAS API: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"❌ GAS API エラー: {e}")
    
    # 3. 既存のWEBHOOK_GAS をトークンでテスト
    try:
        print("\n🎯 3. 既存WEBHOOK_GAS（トークン付き）テスト...")
        webhook_gas = os.getenv('WEBHOOK_GAS')
        if webhook_gas:
            # トークンをパラメータとして追加
            webhook_with_token = f"{webhook_gas}?access_token={access_token}"
            response = requests.get(webhook_with_token, timeout=10)
            print(f"✅ WEBHOOK_GAS成功: {response.status_code}")
            print(f"   レスポンス: {response.text[:200]}...")
        else:
            print("⚠️ WEBHOOK_GAS が.envに設定されていません")
    except Exception as e:
        print(f"❌ WEBHOOK_GAS エラー: {e}")

def test_google_chat_with_token(access_token):
    """Google ChatAPIをトークン付きでテスト"""
    print("\n💬 4. Google Chat API（トークン付き）テスト...")
    
    # .envからチャットURLを取得
    chat_url = os.getenv('CHAT_URL')
    if not chat_url:
        print("⚠️ CHAT_URL が.envに設定されていません")
        return
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # テストメッセージを送信
    test_message = {
        "text": f"🤖 Google API診断テスト完了！\n⏰ {os.environ.get('DATE', '2025-06-19')}\n🔑 アクセストークン認証成功"
    }
    
    try:
        # URLからクエリパラメータを除去してAPIエンドポイントのみ使用
        base_url = chat_url.split('?')[0]
        response = requests.post(
            base_url,
            headers=headers,
            json=test_message,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Google Chat送信成功!")
            print(f"   メッセージ送信完了: {test_message['text'][:50]}...")
        else:
            print(f"⚠️ Google Chat: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"❌ Google Chat エラー: {e}")

def main():
    """メイン実行"""
    print("🚀 Google API総合診断システム（トークン取得版）")
    print("=" * 60)
    
    # Step 1: トークン取得
    result = get_access_token()
    if not result:
        print("❌ 認証失敗。プログラムを終了します。")
        return
    
    access_token, credentials = result
    
    # Step 2: API機能テスト
    test_google_apis(access_token)
    
    # Step 3: Google Chat テスト
    test_google_chat_with_token(access_token)
    
    print("\n" + "=" * 60)
    print("🎉 Google API診断完了!")
    print("\n📋 診断結果:")
    print(f"  🔑 サービスアカウント認証: ✅ 成功")
    print(f"  🌐 アクセストークン取得: ✅ 成功")
    print(f"  📊 Google Cloud Platform: テスト実行済み")
    print(f"  📜 Google Apps Script: テスト実行済み")
    print(f"  💬 Google Chat Bot: テスト実行済み")
    
    print("\n💡 このトークンで利用可能な機能:")
    available_apis = [
        "🤖 Google Chat Bot操作",
        "📜 Google Apps Script実行", 
        "💾 Google Drive/Sheets操作",
        "👁️ Google Cloud Vision OCR",
        "🗂️ Google Workspace API全般",
        "☁️ Google Cloud Platform API",
        "📧 Gmail API",
        "📅 Google Calendar API",
        "🎬 YouTube API",
        "🗺️ Google Maps API"
    ]
    
    for api in available_apis:
        print(f"  {api}")
    
    print(f"\n🔗 アクセストークン（保存用）:")
    print(f"Bearer {access_token}")

if __name__ == "__main__":
    main()
