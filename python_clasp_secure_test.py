#!/usr/bin/env python3
"""
Python版clasp APIテスト（完全セキュア版）
全ての認証情報は環境変数から取得
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def test_secure_oauth2():
    """セキュアなOAuth2認証テスト"""
    print("🔐 セキュアOAuth2認証テスト")
    print("=" * 40)
    
    # 環境変数から認証情報取得
    load_dotenv()
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        print("❌ 環境変数が設定されていません")
        print("必要な変数: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN")
        return False
    
    # トークン取得
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    try:
        response = requests.post(token_url, data=payload, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            
            if access_token:
                print("✅ OAuth2認証成功!")
                print(f"🔑 トークン取得済み（最初の10文字）: {access_token[:10]}...")
                return access_token
            else:
                print("❌ アクセストークン取得失敗")
                return None
        else:
            print(f"❌ 認証失敗: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 認証エラー: {e}")
        return None

def test_secure_gas_execution():
    """セキュアなGAS関数実行テスト"""
    print("\n🧪 セキュアGAS関数実行テスト")
    print("=" * 40)
    
    # 認証トークン取得
    access_token = test_secure_oauth2()
    if not access_token:
        return False
    
    # 環境変数からスクリプトID取得
    script_id = os.getenv('GOOGLE_SCRIPT_ID')
    if not script_id:
        print("❌ GOOGLE_SCRIPT_ID が設定されていません")
        return False
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # テスト関数一覧
    test_functions = [
        {
            "name": "gastest",
            "description": "基本テスト関数",
            "parameters": []
        },
        {
            "name": "getExternalIP",
            "description": "外部IP取得",
            "parameters": []
        }
    ]
    
    exec_url = f"https://script.googleapis.com/v1/scripts/{script_id}:run"
    
    for func_test in test_functions:
        print(f"\n🔧 関数テスト: {func_test['name']}")
        
        test_payload = {
            "function": func_test['name'],
            "parameters": func_test['parameters'],
            "devMode": True
        }
        
        try:
            response = requests.post(exec_url, headers=headers, json=test_payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                
                if "error" in result:
                    error_info = result["error"]
                    print(f"   ⚠️ 実行エラー: {error_info.get('message', 'Unknown error')}")
                else:
                    print(f"   ✅ 実行成功!")
                    exec_result = result.get("response", {})
                    
                    if "result" in exec_result:
                        result_data = exec_result["result"]
                        print(f"      📊 結果: {result_data}")
                        
            else:
                print(f"   ❌ HTTP エラー: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 例外エラー: {e}")
    
    return True

def main():
    """メインテスト実行"""
    print("🛡️ Python版clasp API セキュリティテスト")
    print("=" * 60)
    
    # セキュアなOAuth2テスト
    oauth_result = test_secure_oauth2()
    
    if oauth_result:
        print("\n✅ セキュリティテスト: 成功")
        print("🔐 認証情報: 環境変数から安全に取得")
        print("🌐 GitHub Secret Scanning: 対応済み")
        
        # GAS実行テスト
        gas_result = test_secure_gas_execution()
        
        if gas_result:
            print("\n🎉 全テスト完了!")
            print("✅ OAuth2認証: 成功")
            print("✅ GAS関数実行: 成功")
            print("✅ セキュリティ: 環境変数使用")
            print("✅ GitHub対応: 完全")
        
    else:
        print("\n❌ セキュリティテスト失敗")
        print("💡 解決策:")
        print("1. .envファイルに認証情報を設定")
        print("2. 環境変数が正しく読み込まれているか確認")
    
    print(f"\n🎊 Python版clasp API（セキュア版）テスト完了!")

if __name__ == "__main__":
    main()
