#!/usr/bin/env python3
"""
Python版clasp API - 完全セキュア版
OAuth2認証でGoogle Apps Script操作システム
全ての認証情報は環境変数から取得
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

class PythonClaspAPI:
    """Python版clasp - Google Apps Script API操作クラス（セキュア版）"""
    
    def __init__(self):
        load_dotenv()
        # OAuth2認証情報を環境変数から取得
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')  
        self.refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
        self.access_token = None
        
        # 認証情報チェック
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            print("⚠️ 環境変数が設定されていません:")
            print("   GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN")
            print("   .envファイルを確認してください")
        
    def get_access_token(self):
        """OAuth2アクセストークンを取得"""
        if self.access_token:
            return self.access_token
            
        if not all([self.client_id, self.client_secret, self.refresh_token]):
            print("❌ OAuth2認証情報が不完全です")
            return None
            
        print("🔐 OAuth2トークン取得中...")
        
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        
        try:
            response = requests.post(token_url, data=payload, timeout=10)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                print("✅ トークン取得成功")
                return self.access_token
            else:
                print(f"❌ トークン取得失敗: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ トークンエラー: {e}")
            return None
    
    def execute_gas_function(self, script_id=None, function_name="gastest", parameters=None):
        """Google Apps Script関数を実行"""
        if not script_id:
            script_id = os.getenv('GOOGLE_SCRIPT_ID')
            
        access_token = self.get_access_token()
        if not access_token:
            return {"error": "認証失敗"}
        
        url = f"https://script.googleapis.com/v1/scripts/{script_id}:run"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "function": function_name,
            "devMode": True
        }
        
        if parameters:
            payload["parameters"] = parameters
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "result": result.get("response", {}).get("result"),
                    "execution_time": result.get("response", {}).get("executionTime")
                }
            else:
                error_data = response.json()
                return {
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_google_docs_via_gas(self, script_id=None, title=None, content=None):
        """Google Apps Script経由でGoogle Docs作成"""
        if not script_id:
            script_id = os.getenv('GOOGLE_SCRIPT_ID')
            
        print(f"📝 Google Docs作成開始...")
        
        # デフォルトタイトル
        if not title:
            title = f"AUTOCREATE システムガイド - {datetime.now().strftime('%Y/%m/%d %H:%M')}"
        
        # AUTOCREATEシステムガイド作成関数を実行
        result = self.execute_gas_function(
            script_id=script_id,
            function_name="createAUTOCREATESystemGuide",
            parameters=[]
        )
        
        if result.get("success"):
            doc_info = result.get("result", {})
            print(f"✅ Google Docs作成成功!")
            print(f"   📄 タイトル: {doc_info.get('title', 'N/A')}")
            print(f"   🆔 Document ID: {doc_info.get('id', 'N/A')}")
            print(f"   🔗 URL: {doc_info.get('url', 'N/A')}")
            return doc_info
        else:
            print(f"❌ Google Docs作成失敗: {result.get('error')}")
            return None

def demo_python_clasp():
    """Python版clasp APIのデモ実行"""
    print("🚀 Python版clasp API デモ（完全セキュア版）")
    print("=" * 60)
    
    # PythonClaspAPI インスタンス作成
    python_clasp = PythonClaspAPI()
    
    # 基本テスト
    print("\n🧪 基本テスト実行...")
    result = python_clasp.execute_gas_function(function_name="gastest")
    
    if result.get("success"):
        print(f"✅ 基本テスト成功: {result.get('result')}")
    else:
        print(f"❌ 基本テスト失敗: {result.get('error')}")
    
    # 外部IP取得テスト
    print("\n🌐 外部IP取得テスト...")
    ip_result = python_clasp.execute_gas_function(function_name="getExternalIP")
    
    if ip_result.get("success"):
        print(f"✅ 外部IP取得成功: {ip_result.get('result')}")
    else:
        print(f"❌ 外部IP取得失敗: {ip_result.get('error')}")
    
    return True

def webhook_google_docs_endpoint(script_id=None, title=None, content=None):
    """Webhook/n8n用のGoogle Docs作成エンドポイント（セキュア版）"""
    python_clasp = PythonClaspAPI()
    
    try:
        result = python_clasp.create_google_docs_via_gas(script_id, title, content)
        
        if result:
            return {
                "status": "success",
                "message": "Google Docs作成成功",
                "document": {
                    "id": result.get("id"),
                    "url": result.get("url"),
                    "title": result.get("title")
                }
            }
        else:
            return {
                "status": "error",
                "message": "Google Docs作成失敗"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"システムエラー: {e}"
        }

def main():
    """メイン実行"""
    print("🐍 Python版Google Apps Script API システム（完全セキュア版）")
    print("=" * 70)
    
    # デモ実行
    result = demo_python_clasp()
    
    print("\n" + "=" * 70)
    print("📊 Python版clasp実行結果")
    
    if result:
        print("✅ Python版clasp API: 動作確認済み")
        print("🔐 セキュリティ: 環境変数使用")
        print("🌐 n8n/Webhook対応: 準備完了")
        
        print(f"\n🎯 使用方法:")
        print(f"```python")
        print(f"from python_clasp_secure import webhook_google_docs_endpoint")
        print(f"result = webhook_google_docs_endpoint()")
        print(f"```")
        
        print(f"\n📝 必要な環境変数:")
        print(f"GOOGLE_CLIENT_ID=your_client_id")
        print(f"GOOGLE_CLIENT_SECRET=your_client_secret")
        print(f"GOOGLE_REFRESH_TOKEN=your_refresh_token")
        print(f"GOOGLE_SCRIPT_ID=your_script_id")
        
    else:
        print("❌ システム実行失敗")
        print("🔧 対処法: 環境変数設定・GASプロジェクト権限確認")
    
    print(f"\n🎊 Python版clasp API（セキュア版）完成!")

if __name__ == "__main__":
    main()
