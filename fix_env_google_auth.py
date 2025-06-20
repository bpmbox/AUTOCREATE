#!/usr/bin/env python3
"""
.envファイルのGoogle認証情報を修正
"""

import os
import json
import re

def fix_env_file():
    """env ファイルのGoogle認証情報を修正"""
    env_path = '.env'
    
    # .envファイルを読み込み
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 .envファイルのGoogle認証情報を修正中...")
    
    # GOOGLE_APPLICATION_CREDENTIALS_CONTENTセクションを見つける
    pattern = r"GOOGLE_APPLICATION_CREDENTIALS_CONTENT='([^']+)'"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS_CONTENT が見つかりません")
        return
    
    json_content = match.group(1)
    
    try:
        # JSONをパース
        service_account_info = json.loads(json_content)
        
        # private_keyの改行文字を\\nに変換
        if 'private_key' in service_account_info:
            original_key = service_account_info['private_key']
            # 実際の改行文字を\\nに変換
            fixed_key = original_key.replace('\n', '\\n')
            service_account_info['private_key'] = fixed_key
            
            print(f"✅ Private key修正完了")
            print(f"   元の長さ: {len(original_key)}")
            print(f"   修正後長さ: {len(fixed_key)}")
        
        # 修正されたJSONを文字列に変換
        fixed_json = json.dumps(service_account_info, separators=(',', ':'))
        
        # .envファイル内容を更新
        new_content = re.sub(
            pattern,
            f"GOOGLE_APPLICATION_CREDENTIALS_CONTENT='{fixed_json}'",
            content,
            flags=re.DOTALL
        )
        
        # バックアップを作成
        with open(f'{env_path}.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 修正されたファイルを保存
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ .envファイル修正完了")
        print(f"   バックアップファイル: {env_path}.backup")
        
        # 修正を検証
        verify_fix()
        
    except Exception as e:
        print(f"❌ 修正エラー: {e}")

def verify_fix():
    """修正の検証"""
    print("\n🔍 修正の検証中...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
    if creds_content:
        try:
            service_account_info = json.loads(creds_content)
            private_key = service_account_info.get('private_key', '')
            
            if '\\n' in private_key and '\n' not in private_key:
                print("✅ Private key形式は正常です")
                
                # Google認証テスト
                try:
                    from google.oauth2 import service_account
                    credentials = service_account.Credentials.from_service_account_info(
                        service_account_info, 
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    print("✅ Google認証オブジェクト作成成功！")
                    return True
                except Exception as e:
                    print(f"❌ Google認証テストエラー: {e}")
                    return False
            else:
                print("❌ Private key形式に問題があります")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析エラー: {e}")
            return False
    else:
        print("❌ 認証情報が見つかりません")
        return False

if __name__ == "__main__":
    fix_env_file()
