#!/usr/bin/env python3
"""
Google Docs API テスト
ドキュメント作成・編集・読み取り機能をテスト
"""

import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from dotenv import load_dotenv
from datetime import datetime

def get_google_docs_token():
    """Google Docs API用のアクセストークンを取得"""
    print("📝 Google Docs API認証開始...")
    
    try:
        load_dotenv()
        creds_content = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT')
        
        if not creds_content:
            print("❌ Google認証情報が見つかりません")
            return None
            
        creds_dict = json.loads(creds_content)
        print(f"✅ プロジェクト: {creds_dict.get('project_id')}")
        
        # Google Docs用スコープ
        scopes = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=scopes
        )
        
        credentials.refresh(Request())
        print("✅ Google Docs用トークン取得成功!")
        
        return credentials.token
        
    except Exception as e:
        print(f"❌ 認証エラー: {e}")
        return None

def create_google_doc(access_token):
    """新しいGoogle Docを作成"""
    print("\n📄 Google Docs ドキュメント作成テスト...")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # ドキュメント作成データ
    doc_data = {
        'title': f'AUTOCREATE Google Docs テスト - {datetime.now().strftime("%Y/%m/%d %H:%M")}'
    }
    
    try:
        # Google Docs APIでドキュメント作成
        response = requests.post(
            'https://docs.googleapis.com/v1/documents',
            headers=headers,
            json=doc_data,
            timeout=15
        )
        
        if response.status_code == 200:
            doc_info = response.json()
            doc_id = doc_info.get('documentId')
            doc_title = doc_info.get('title')
            
            print(f"✅ ドキュメント作成成功!")
            print(f"   📄 タイトル: {doc_title}")
            print(f"   🆔 Document ID: {doc_id}")
            print(f"   🔗 URL: https://docs.google.com/document/d/{doc_id}/edit")
            
            return doc_id
            
        else:
            print(f"❌ 作成失敗: {response.status_code}")
            print(f"   エラー: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ ドキュメント作成エラー: {e}")
        return None

def write_to_google_doc(access_token, doc_id):
    """Google Docに内容を書き込み"""
    print(f"\n✍️ Google Docs 書き込みテスト...")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # 書き込み内容
    content = f"""🤖 AUTOCREATE Google Docs API テスト

📅 実行日時: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}

🎉 成功した機能:
✅ Google Docs API認証
✅ 新規ドキュメント作成  
✅ テキスト挿入

🌟 利用可能な操作:
📝 文書作成・編集
🎨 書式設定（太字、色、サイズ）
📊 表・画像の挿入
🔗 リンク埋め込み
👥 共有・権限設定

🚀 AUTOCREATE プロジェクト
外部連携pyautogui自動化システム完成記念！

⭐ このドキュメントはGoogle Docs APIで自動生成されました！
"""

    # 書き込みリクエスト
    requests_data = {
        'requests': [
            {
                'insertText': {
                    'location': {
                        'index': 1
                    },
                    'text': content
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            f'https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate',
            headers=headers,
            json=requests_data,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ テキスト書き込み成功!")
            print(f"   📝 {len(content)}文字を挿入")
            print(f"   🎉 Google Docsで確認可能!")
            return True
        else:
            print(f"❌ 書き込み失敗: {response.status_code}")
            print(f"   エラー: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 書き込みエラー: {e}")
        return False

def share_google_doc(access_token, doc_id):
    """Google Docを共有設定"""
    print(f"\n🔗 Google Docs 共有設定テスト...")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # 誰でも閲覧可能に設定
    permission_data = {
        'role': 'reader',
        'type': 'anyone'
    }
    
    try:
        response = requests.post(
            f'https://www.googleapis.com/drive/v3/files/{doc_id}/permissions',
            headers=headers,
            json=permission_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 共有設定成功!")
            print("   👥 誰でも閲覧可能に設定")
            print(f"   🔗 共有URL: https://docs.google.com/document/d/{doc_id}/edit?usp=sharing")
            return True
        else:
            print(f"⚠️ 共有設定: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 共有設定エラー: {e}")
        return False

def read_google_doc(access_token, doc_id):
    """Google Docの内容を読み取り"""
    print(f"\n📖 Google Docs 読み取りテスト...")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f'https://docs.googleapis.com/v1/documents/{doc_id}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            doc_data = response.json()
            title = doc_data.get('title', 'N/A')
            doc_id = doc_data.get('documentId', 'N/A')
            
            print("✅ ドキュメント読み取り成功!")
            print(f"   📄 タイトル: {title}")
            print(f"   🆔 Document ID: {doc_id}")
            
            # 内容の一部を表示
            content = doc_data.get('body', {})
            if content:
                print(f"   📝 コンテンツ構造確認: OK")
                return True
            
        else:
            print(f"❌ 読み取り失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 読み取りエラー: {e}")
        return False

def main():
    """Google Docs総合テスト実行"""
    print("📝 Google Docs API 総合テスト")
    print("=" * 50)
    
    # Step 1: 認証・トークン取得
    access_token = get_google_docs_token()
    if not access_token:
        print("❌ 認証失敗。テストを終了します。")
        return
    
    # Step 2: ドキュメント作成
    doc_id = create_google_doc(access_token)
    if not doc_id:
        print("❌ ドキュメント作成失敗。テストを終了します。")
        return
    
    # Step 3: 内容書き込み
    write_success = write_to_google_doc(access_token, doc_id)
    
    # Step 4: 共有設定
    share_success = share_google_doc(access_token, doc_id)
    
    # Step 5: 読み取りテスト
    read_success = read_google_doc(access_token, doc_id)
    
    # 結果まとめ
    print("\n" + "=" * 50)
    print("🎉 Google Docs API テスト完了!")
    
    print(f"\n📋 テスト結果:")
    print(f"  🔐 認証: ✅ 成功")
    print(f"  📄 ドキュメント作成: {'✅ 成功' if doc_id else '❌ 失敗'}")
    print(f"  ✍️ テキスト書き込み: {'✅ 成功' if write_success else '❌ 失敗'}")
    print(f"  🔗 共有設定: {'✅ 成功' if share_success else '❌ 失敗'}")
    print(f"  📖 読み取り: {'✅ 成功' if read_success else '❌ 失敗'}")
    
    if doc_id:
        print(f"\n🔗 作成されたドキュメント:")
        print(f"   URL: https://docs.google.com/document/d/{doc_id}/edit")
        print(f"   Document ID: {doc_id}")
    
    print(f"\n💡 Google Docsで可能な操作:")
    docs_features = [
        "📝 文書作成・編集・削除",
        "🎨 書式設定（フォント、色、サイズ）",
        "📊 表・リスト・画像の挿入",
        "🔗 ハイパーリンク埋め込み",
        "👥 共有・権限管理",
        "💬 コメント・提案機能",
        "📱 リアルタイム共同編集",
        "🔄 バージョン履歴管理",
        "📤 PDF・Word形式でエクスポート",
        "🔍 全文検索"
    ]
    
    for feature in docs_features:
        print(f"  {feature}")

if __name__ == "__main__":
    main()
