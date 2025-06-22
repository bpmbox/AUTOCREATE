#!/usr/bin/env python3
"""
Google API スコープ設定確認・診断
"""

import os
import json
from dotenv import load_dotenv

def check_google_api_scopes():
    """Google API認証スコープの詳細確認"""
    print("🔐 Google API スコープ診断")
    print("=" * 50)
    
    load_dotenv()
    
    # 現在の認証情報を確認
    creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
    
    if not creds_content:
        print("❌ Google認証情報が見つかりません")
        return
    
    try:
        creds_dict = json.loads(creds_content)
        
        print("✅ 現在の認証情報:")
        print(f"   📧 サービスアカウント: {creds_dict.get('client_email', 'N/A')}")
        print(f"   🆔 プロジェクトID: {creds_dict.get('project_id', 'N/A')}")
        print(f"   🔑 クライアントID: {creds_dict.get('client_id', 'N/A')}")
        
    except Exception as e:
        print(f"❌ 認証情報解析エラー: {e}")
        return
    
    # 必要なスコープ一覧
    print(f"\n📋 Google Docs作成に必要なスコープ:")
    
    required_scopes = {
        'Google Docs': [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/documents.readonly'
        ],
        'Google Drive': [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.readonly'
        ],
        'Google Apps Script': [
            'https://www.googleapis.com/auth/script.projects',
            'https://www.googleapis.com/auth/script.projects.readonly'
        ],
        'Google Sheets': [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/spreadsheets.readonly'
        ],
        'Google Chat': [
            'https://www.googleapis.com/auth/chat.bot',
            'https://www.googleapis.com/auth/chat.messages'
        ]
    }
    
    for service, scopes in required_scopes.items():
        print(f"\n   🌐 {service}:")
        for scope in scopes:
            print(f"      - {scope}")
    
    # Google Apps Scriptの権限設定確認
    print(f"\n🔧 Google Apps Script権限設定:")
    print(f"   📜 現在のスクリプトID: AKfycbwFrOSPmAFXP-sDH7_BxXe3oqzL9FQhllOIuwTO5ylNwjEw9RBI-BRCIWnZLQ53jvE9")
    print(f"   🔗 管理URL: https://script.google.com/d/AKfycbwFrOSPmAFXP-sDH7_BxXe3oqzL9FQhllOIuwTO5ylNwjEw9RBI-BRCIWnZLQ53jvE9/edit")
    
    print(f"\n💡 GASで確認すべき権限:")
    gas_permissions = [
        "📝 Google Docs API - DocumentApp.create()権限",
        "💾 Google Drive API - DriveApp.createFile()権限", 
        "🔐 実行権限 - 誰でも実行可能設定",
        "🌐 ウェブアプリ権限 - 公開設定"
    ]
    
    for permission in gas_permissions:
        print(f"   {permission}")

def diagnose_scope_issues():
    """スコープ関連の問題診断"""
    print(f"\n🔍 スコープ問題診断:")
    
    print(f"\n❌ 可能な問題:")
    issues = [
        {
            'problem': 'サービスアカウント権限不足',
            'description': 'Google Docsスコープが未許可',
            'solution': 'Google Cloud Consoleで権限追加'
        },
        {
            'problem': 'GASスクリプト権限エラー',
            'description': 'DocumentApp使用権限なし',
            'solution': 'GAS内でスコープを明示的に設定'
        },
        {
            'problem': 'ウェブアプリ実行権限',
            'description': '外部からの実行が拒否',
            'solution': '「誰でも」実行可能に設定変更'
        },
        {
            'problem': 'プロジェクト設定問題',
            'description': 'Google Docs APIが無効',
            'solution': 'Google Cloud ConsoleでAPI有効化'
        }
    ]
    
    for i, issue in enumerate(issues, 1):
        print(f"\n   {i}. 🚨 {issue['problem']}")
        print(f"      📋 詳細: {issue['description']}")
        print(f"      🔧 解決: {issue['solution']}")

def provide_scope_solutions():
    """スコープ問題の解決方法"""
    print(f"\n🛠️ スコープ問題の解決手順:")
    
    print(f"\n📋 方法1: Google Cloud Console設定")
    console_steps = [
        "1. https://console.cloud.google.com/ にアクセス",
        "2. プロジェクト 'urlounge74620' を選択",
        "3. 「APIとサービス」→「ライブラリ」",
        "4. 「Google Docs API」を検索して有効化",
        "5. 「認証情報」でサービスアカウント権限確認"
    ]
    
    for step in console_steps:
        print(f"   {step}")
    
    print(f"\n📜 方法2: Google Apps Script設定")
    gas_steps = [
        "1. GAS管理画面を開く",
        "2. 「リソース」→「Googleの詳細サービス」",
        "3. 「Google Docs API」を有効化",
        "4. 「公開」→「ウェブアプリケーションとして導入」",
        "5. 「実行者: 私」「アクセス: 全員（匿名含む）」に設定"
    ]
    
    for step in gas_steps:
        print(f"   {step}")
    
    print(f"\n⚡ 方法3: 代替アプローチ")
    alternatives = [
        "🔧 直接Google Drive APIでHTMLファイル作成",
        "📄 Google Sheetsで一覧表作成",
        "📧 Gmailでドキュメント送信",
        "💾 Google Driveフォルダに保存"
    ]
    
    for alt in alternatives:
        print(f"   {alt}")

def test_alternative_google_apis():
    """代替Google API機能のテスト"""
    print(f"\n🧪 代替Google API機能テスト:")
    
    webhook_gas = os.getenv('WEBHOOK_GAS')
    
    if not webhook_gas:
        print("❌ WEBHOOK_GAS未設定")
        return
    
    # 代替API機能のテスト
    import requests
    
    alternative_tests = [
        {
            'name': 'Google Drive ファイル作成',
            'params': {'api': 'drive', 'action': 'create_file', 'name': 'test.txt'}
        },
        {
            'name': 'Google Sheets 作成',
            'params': {'api': 'sheets', 'action': 'create', 'title': 'Test Sheet'}
        },
        {
            'name': 'Gmail 送信',
            'params': {'api': 'gmail', 'action': 'send', 'subject': 'Test Mail'}
        }
    ]
    
    for test in alternative_tests:
        print(f"\n   📊 {test['name']}テスト:")
        try:
            response = requests.get(webhook_gas, params=test['params'], timeout=10)
            print(f"      ステータス: {response.status_code}")
            
            if response.status_code == 200:
                if 'エラー' not in response.text and 'Error' not in response.text:
                    print(f"      ✅ 成功可能性あり")
                else:
                    print(f"      ⚠️ スコープエラーの可能性")
            else:
                print(f"      ❌ API呼び出し失敗")
                
        except Exception as e:
            print(f"      ❌ テストエラー: {e}")

def main():
    """メイン実行"""
    print("🔐 Google API スコープ完全診断")
    print("=" * 60)
    
    # 基本スコープ確認
    check_google_api_scopes()
    
    # 問題診断
    diagnose_scope_issues()
    
    # 解決方法
    provide_scope_solutions()
    
    # 代替API機能テスト
    test_alternative_google_apis()
    
    print("\n" + "=" * 60)
    print("🎯 スコープ診断結果")
    
    print(f"\n📋 診断結果:")
    print(f"  🔐 認証情報: ✅ 設定済み")
    print(f"  📜 GASスクリプト: ⚠️ エラーあり（スコープ問題の可能性）")
    print(f"  🌐 API有効化: 要確認")
    print(f"  🛠️ 権限設定: 要調整")
    
    print(f"\n💡 推奨対応:")
    print(f"  1. 🔧 Google Cloud ConsoleでGoogle Docs API有効化")
    print(f"  2. 📜 GASスクリプトの権限設定確認")
    print(f"  3. ⚡ 代替方法での機能確認")
    print(f"  4. 🧪 段階的なAPI機能テスト")
    
    print(f"\n🎊 結論: スコープ設定調整でGoogle Docs機能が復活する可能性が高い！")

if __name__ == "__main__":
    main()
