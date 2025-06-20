#!/usr/bin/env python3
"""
Google API認証情報の修正ツール
"""

import os
import json
import base64
from dotenv import load_dotenv

def fix_google_credentials():
    """Google認証情報を修正"""
    load_dotenv()
    
    # .envから認証情報を取得
    creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
    if not creds_content:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS_CONTENT が見つかりません")
        return
    
    print("🔍 現在の認証情報を確認中...")
    print(f"文字数: {len(creds_content)}")
    print(f"最初の100文字: {creds_content[:100]}")
    print(f"最後の100文字: {creds_content[-100:]}")
    
    try:
        # JSONとして解析を試行
        service_account_info = json.loads(creds_content)
        print("✅ JSON形式は正常です")
        
        # 重要なフィールドを確認
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email', 'client_id']
        for field in required_fields:
            if field in service_account_info:
                if field == 'private_key':
                    print(f"✅ {field}: 存在（長さ: {len(service_account_info[field])}）")
                else:
                    print(f"✅ {field}: {service_account_info[field]}")
            else:
                print(f"❌ {field}: 見つかりません")
        
        # private_keyの詳細確認
        private_key = service_account_info.get('private_key', '')
        if private_key:
            print(f"\n🔑 Private Key 詳細:")
            print(f"   開始: {private_key[:50]}")
            print(f"   終了: {private_key[-50:]}")
            
            # 改行文字の確認
            if '\\n' in private_key:
                print("✅ \\n 文字列が含まれています（正常）")
            if '\n' in private_key:
                print("⚠️ 実際の改行文字が含まれています")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析エラー: {e}")
        
        # エスケープ問題の可能性を確認
        if '\\' in creds_content:
            print("⚠️ エスケープ文字が検出されました")
        
        # 修正を試行
        try:
            # ダブルエスケープを修正
            fixed_content = creds_content.replace('\\\\', '\\')
            service_account_info = json.loads(fixed_content)
            print("✅ エスケープ修正後のJSON解析成功")
        except:
            print("❌ 修正後も解析できません")
    
    # テスト用の最小限の認証
    try:
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, 
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        print("✅ Google認証オブジェクト作成成功")
    except Exception as e:
        print(f"❌ Google認証オブジェクト作成エラー: {e}")

if __name__ == "__main__":
    fix_google_credentials()
