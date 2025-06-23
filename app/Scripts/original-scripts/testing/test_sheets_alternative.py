#!/usr/bin/env python3
"""
Google Sheets版でシステムガイド作成テスト
（Docsが使えない場合の代替）
"""

import os
import requests
from dotenv import load_dotenv

def create_sheets_guide():
    """Google SheetsでAUTOCREATEガイド作成"""
    print("📊 Google Sheets版 システムガイド作成")
    print("=" * 50)
    
    load_dotenv()
    webhook_gas = os.getenv('WEBHOOK_GAS')
    
    if not webhook_gas:
        print("❌ WEBHOOK_GAS未設定")
        return False
    
    # Sheetsでのガイド作成パラメータ
    sheets_params = {
        'api': 'sheets',
        'action': 'create_guide',
        'title': 'AUTOCREATE システム使い方ガイド - Sheets版',
        'type': 'spreadsheet'
    }
    
    try:
        print("📤 Google Sheets作成リクエスト送信中...")
        response = requests.get(webhook_gas, params=sheets_params, timeout=15)
        
        print(f"✅ Sheets応答: {response.status_code}")
        
        if response.status_code == 200:
            # エラーチェック
            if 'エラー' in response.text or 'Error' in response.text:
                print("⚠️ Sheetsもスコープエラーの可能性")
                return False
            else:
                print("🎊 Google Sheets版作成要求成功！")
                return True
        else:
            print(f"❌ Sheets作成失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Sheetsテストエラー: {e}")
        return False

if __name__ == "__main__":
    create_sheets_guide()
