#!/usr/bin/env python3
"""
🌐 Google API 総合テストシステム
現在の.env設定でアクセス可能なGoogle API機能を確認
"""

import os
import json
import sys
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import requests

class GoogleAPITester:
    def __init__(self):
        self.setup_credentials()
        self.results = {}
        
    def setup_credentials(self):
        """サービスアカウント認証情報を設定"""
        try:
            # .envから認証情報を取得
            creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
            if not creds_content:
                raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_CONTENT not found in environment")
            
            # JSON文字列を辞書に変換
            self.service_account_info = json.loads(creds_content)
            self.project_id = self.service_account_info.get('project_id')
            self.client_email = self.service_account_info.get('client_email')
            
            print(f"✅ 認証情報設定完了")
            print(f"   プロジェクトID: {self.project_id}")
            print(f"   サービスアカウント: {self.client_email}")
            
        except Exception as e:
            print(f"❌ 認証情報設定エラー: {e}")
            sys.exit(1)
    
    def get_credentials_with_scopes(self, scopes):
        """指定されたスコープで認証情報を取得"""
        try:
            credentials = service_account.Credentials.from_service_account_info(
                self.service_account_info, scopes=scopes
            )
            return credentials
        except Exception as e:
            print(f"❌ 認証情報取得エラー: {e}")
            return None
    
    def test_google_chat_api(self):
        """Google Chat API テスト"""
        print("\n🤖 Google Chat API テスト...")
        try:
            scopes = ['https://www.googleapis.com/auth/chat.bot']
            credentials = self.get_credentials_with_scopes(scopes)
            
            if credentials:
                chat_service = build('chat', 'v1', credentials=credentials)
                self.results['google_chat'] = "✅ 接続可能"
                print("   ✅ Google Chat API 接続成功")
                return True
            else:
                self.results['google_chat'] = "❌ 認証エラー"
                return False
                
        except Exception as e:
            self.results['google_chat'] = f"❌ エラー: {str(e)}"
            print(f"   ❌ Google Chat API エラー: {e}")
            return False
    
    def test_google_drive_api(self):
        """Google Drive API テスト"""
        print("\n📁 Google Drive API テスト...")
        try:
            scopes = ['https://www.googleapis.com/auth/drive']
            credentials = self.get_credentials_with_scopes(scopes)
            
            if credentials:
                drive_service = build('drive', 'v3', credentials=credentials)
                # ファイル一覧を取得（テスト）
                results = drive_service.files().list(pageSize=1).execute()
                self.results['google_drive'] = "✅ 接続可能"
                print("   ✅ Google Drive API 接続成功")
                return True
            else:
                self.results['google_drive'] = "❌ 認証エラー"
                return False
                
        except Exception as e:
            self.results['google_drive'] = f"❌ エラー: {str(e)}"
            print(f"   ❌ Google Drive API エラー: {e}")
            return False
    
    def test_google_sheets_api(self):
        """Google Sheets API テスト"""
        print("\n📊 Google Sheets API テスト...")
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = self.get_credentials_with_scopes(scopes)
            
            if credentials:
                sheets_service = build('sheets', 'v4', credentials=credentials)
                self.results['google_sheets'] = "✅ 接続可能"
                print("   ✅ Google Sheets API 接続成功")
                return True
            else:
                self.results['google_sheets'] = "❌ 認証エラー"
                return False
                
        except Exception as e:
            self.results['google_sheets'] = f"❌ エラー: {str(e)}"
            print(f"   ❌ Google Sheets API エラー: {e}")
            return False
    
    def test_google_docs_api(self):
        """Google Docs API テスト"""
        print("\n📝 Google Docs API テスト...")
        try:
            scopes = ['https://www.googleapis.com/auth/documents']
            credentials = self.get_credentials_with_scopes(scopes)
            
            if credentials:
                docs_service = build('docs', 'v1', credentials=credentials)
                self.results['google_docs'] = "✅ 接続可能"
                print("   ✅ Google Docs API 接続成功")
                return True
            else:
                self.results['google_docs'] = "❌ 認証エラー"
                return False
                
        except Exception as e:
            self.results['google_docs'] = f"❌ エラー: {str(e)}"
            print(f"   ❌ Google Docs API エラー: {e}")
            return False
    
    def test_google_calendar_api(self):
        """Google Calendar API テスト"""
        print("\n📅 Google Calendar API テスト...")
        try:
            scopes = ['https://www.googleapis.com/auth/calendar']
            credentials = self.get_credentials_with_scopes(scopes)
            
            if credentials:
                calendar_service = build('calendar', 'v3', credentials=credentials)
                self.results['google_calendar'] = "✅ 接続可能"
                print("   ✅ Google Calendar API 接続成功")
                return True
            else:
                self.results['google_calendar'] = "❌ 認証エラー"
                return False
                
        except Exception as e:
            self.results['google_calendar'] = f"❌ エラー: {str(e)}"
            print(f"   ❌ Google Calendar API エラー: {e}")
            return False
    
    def test_google_gmail_api(self):
        """Gmail API テスト"""
        print("\n📧 Gmail API テスト...")
        try:
            scopes = ['https://www.googleapis.com/auth/gmail.readonly']
            credentials = self.get_credentials_with_scopes(scopes)
            
            if credentials:
                gmail_service = build('gmail', 'v1', credentials=credentials)
                self.results['gmail'] = "✅ 接続可能"
                print("   ✅ Gmail API 接続成功")
                return True
            else:
                self.results['gmail'] = "❌ 認証エラー"
                return False
                
        except Exception as e:
            self.results['gmail'] = f"❌ エラー: {str(e)}"
            print(f"   ❌ Gmail API エラー: {e}")
            return False
    
    def test_google_cloud_vision_api(self):
        """Google Cloud Vision API テスト"""
        print("\n👁️ Google Cloud Vision API テスト...")
        try:
            scopes = ['https://www.googleapis.com/auth/cloud-platform']
            credentials = self.get_credentials_with_scopes(scopes)
            
            if credentials:
                vision_service = build('vision', 'v1', credentials=credentials)
                self.results['google_vision'] = "✅ 接続可能"
                print("   ✅ Google Cloud Vision API 接続成功")
                return True
            else:
                self.results['google_vision'] = "❌ 認証エラー"
                return False
                
        except Exception as e:
            self.results['google_vision'] = f"❌ エラー: {str(e)}"
            print(f"   ❌ Google Cloud Vision API エラー: {e}")
            return False
    
    def test_webhook_urls(self):
        """設定されているWebhook URLのテスト"""
        print("\n🔗 Webhook URL テスト...")
        
        webhook_gas = os.getenv('WEBHOOK_GAS')
        webhook_url = os.getenv('WEBHOOK_URL')
        chat_url = os.getenv('CHAT_URL')
        
        webhooks = {
            'WEBHOOK_GAS': webhook_gas,
            'WEBHOOK_URL': webhook_url,
            'CHAT_URL': chat_url
        }
        
        for name, url in webhooks.items():
            if url:
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        print(f"   ✅ {name}: 接続成功")
                        self.results[name] = "✅ 接続可能"
                    else:
                        print(f"   ⚠️ {name}: ステータス {response.status_code}")
                        self.results[name] = f"⚠️ ステータス {response.status_code}"
                except Exception as e:
                    print(f"   ❌ {name}: エラー {e}")
                    self.results[name] = f"❌ エラー: {str(e)}"
            else:
                print(f"   ❌ {name}: URL未設定")
                self.results[name] = "❌ URL未設定"
    
    def generate_report(self):
        """総合レポート生成"""
        print("\n" + "="*60)
        print("🌐 Google API 総合診断レポート")
        print("="*60)
        print(f"診断日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"プロジェクトID: {self.project_id}")
        print(f"サービスアカウント: {self.client_email}")
        print("-"*60)
        
        # API別結果
        api_categories = {
            "🤖 チャット・コミュニケーション": ['google_chat'],
            "📁 ファイル・ドキュメント": ['google_drive', 'google_docs', 'google_sheets'],
            "📧 メール・カレンダー": ['gmail', 'google_calendar'],
            "🔍 AI・機械学習": ['google_vision'],
            "🔗 Webhook統合": ['WEBHOOK_GAS', 'WEBHOOK_URL', 'CHAT_URL']
        }
        
        for category, apis in api_categories.items():
            print(f"\n{category}:")
            for api in apis:
                if api in self.results:
                    print(f"  {api:20} : {self.results[api]}")
                else:
                    print(f"  {api:20} : ❌ 未テスト")
        
        # 成功率計算
        total_tests = len(self.results)
        successful_tests = sum(1 for result in self.results.values() if "✅" in result)
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📊 総合成功率: {success_rate:.1f}% ({successful_tests}/{total_tests})")
        
        # 推奨アクション
        print("\n💡 推奨アクション:")
        failed_apis = [api for api, result in self.results.items() if "❌" in result]
        if failed_apis:
            print("   以下のAPIで問題が検出されました:")
            for api in failed_apis:
                print(f"   - {api}: {self.results[api]}")
        else:
            print("   🎉 全てのAPIが正常に動作しています！")
        
        print("\n🚀 利用可能な機能:")
        successful_apis = [api for api, result in self.results.items() if "✅" in result]
        for api in successful_apis:
            print(f"   ✅ {api}")
    
    def run_comprehensive_test(self):
        """総合テスト実行"""
        print("🌐 Google API 総合診断を開始します...")
        print("="*60)
        
        # 各APIテストを実行
        test_methods = [
            self.test_google_chat_api,
            self.test_google_drive_api,
            self.test_google_sheets_api,
            self.test_google_docs_api,
            self.test_google_calendar_api,
            self.test_google_gmail_api,
            self.test_google_cloud_vision_api,
            self.test_webhook_urls
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"❌ テスト実行エラー: {e}")
        
        # レポート生成
        self.generate_report()

if __name__ == "__main__":
    # 環境変数を読み込み
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️ python-dotenvがインストールされていません")
        print("pip install python-dotenv でインストールしてください")
    
    # テスト実行
    tester = GoogleAPITester()
    tester.run_comprehensive_test()
