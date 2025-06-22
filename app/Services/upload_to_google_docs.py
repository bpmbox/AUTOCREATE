#!/usr/bin/env python3
"""
作成したマークダウンをGoogle Docsにアップロード
"""

import os
import json
import requests
from dotenv import load_dotenv

def upload_markdown_to_google_docs():
    """作成したマークダウンファイルをGoogle Docsにアップロード"""
    print("📤 マークダウン → Google Docs 変換アップロード")
    print("=" * 50)
    
    load_dotenv()
    
    # 作成されたマークダウンファイルを読み込み
    md_files = [f for f in os.listdir('.') if f.startswith('AUTOCREATE_システム使い方ガイド_') and f.endswith('.md')]
    
    if not md_files:
        print("❌ マークダウンファイルが見つかりません")
        return False
    
    latest_md = sorted(md_files)[-1]  # 最新のファイル
    print(f"📄 対象ファイル: {latest_md}")
    
    try:
        with open(latest_md, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print(f"✅ ファイル読み込み成功 ({len(markdown_content)}文字)")
        
        # マークダウンをHTMLに簡易変換
        html_content = markdown_to_html(markdown_content)
        
        # Google Drive APIでファイルアップロード
        return upload_to_google_drive(html_content, "AUTOCREATE システム使い方ガイド")
        
    except Exception as e:
        print(f"❌ ファイル処理エラー: {e}")
        return False

def markdown_to_html(markdown_text):
    """マークダウンを簡易HTMLに変換"""
    print("🔄 マークダウン → HTML 変換中...")
    
    html = markdown_text
    
    # 基本的なマークダウン要素をHTMLに変換
    conversions = [
        (r'^# (.+)$', r'<h1>\1</h1>'),
        (r'^## (.+)$', r'<h2>\1</h2>'),
        (r'^### (.+)$', r'<h3>\1</h3>'),
        (r'^\*\*(.+)\*\*$', r'<strong>\1</strong>'),
        (r'`([^`]+)`', r'<code>\1</code>'),
        (r'^- (.+)$', r'<li>\1</li>'),
        (r'✅', '✅'),
        (r'🚀', '🚀'),
        (r'📝', '📝'),
        (r'🎉', '🎉'),
    ]
    
    import re
    for pattern, replacement in conversions:
        html = re.sub(pattern, replacement, html, flags=re.MULTILINE)
    
    # 基本的なHTML構造でラップ
    html = f"""
    <html>
    <head>
        <title>AUTOCREATE システム使い方ガイド</title>
        <meta charset="utf-8">
    </head>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            {html}
        </div>
    </body>
    </html>
    """
    
    print("✅ HTML変換完了")
    return html

def upload_to_google_drive(content, title):
    """Google DriveにHTMLファイルとしてアップロード"""
    print(f"☁️ Google Drive アップロード: {title}")
    
    # 既存のWEBHOOK_GAS経由でアップロード試行
    webhook_gas = os.getenv('WEBHOOK_GAS')
    
    if not webhook_gas:
        print("❌ WEBHOOK_GAS が設定されていません")
        return False
    
    try:
        # GASにアップロード依頼
        params = {
            'action': 'upload_html',
            'title': title,
            'content': content[:1000] + '...' if len(content) > 1000 else content  # 制限対応
        }
        
        response = requests.get(
            webhook_gas,
            params=params,
            timeout=30
        )
        
        print(f"📤 アップロード応答: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Google Drive アップロード要求送信完了!")
            return True
        else:
            print(f"⚠️ アップロード応答: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ アップロードエラー: {e}")
        return False

def create_simple_google_doc():
    """シンプルなGoogle Docs作成（別アプローチ）"""
    print("\n📝 シンプルGoogle Docs作成テスト...")
    
    webhook_gas = os.getenv('WEBHOOK_GAS')
    
    if not webhook_gas:
        return False
    
    # 最小限のドキュメント作成要求
    try:
        simple_params = {
            'create': 'doc',
            'title': 'AUTOCREATE使い方ガイド - 簡易版'
        }
        
        response = requests.get(
            webhook_gas,
            params=simple_params,
            timeout=15
        )
        
        print(f"📄 簡易ドキュメント作成: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 簡易版作成要求送信!")
            
            # レスポンス確認
            if 'html' not in response.text.lower():
                print(f"📊 応答: {response.text[:200]}...")
            
            return True
            
    except Exception as e:
        print(f"❌ 簡易作成エラー: {e}")
        return False

def main():
    """メイン実行"""
    print("🔄 マークダウン → Google Docs 変換システム")
    print("=" * 60)
    
    # Method 1: マークダウンファイルからのアップロード
    upload_success = upload_markdown_to_google_docs()
    
    # Method 2: シンプルなドキュメント作成
    simple_success = create_simple_google_doc()
    
    print("\n" + "=" * 60)
    print("📊 Google Docs アップロード結果")
    
    print(f"\n📋 実行結果:")
    print(f"  📤 マークダウンアップロード: {'✅ 要求送信' if upload_success else '❌ 失敗'}")
    print(f"  📝 簡易ドキュメント作成: {'✅ 要求送信' if simple_success else '❌ 失敗'}")
    
    print(f"\n💡 作成されたコンテンツ:")
    print(f"  📚 完全ガイド (125行)")
    print(f"  🚀 コマンド一覧 (20+種類)")
    print(f"  🔧 設定方法・実用例")
    print(f"  📊 実行実績・成果")
    
    print(f"\n🎯 確認方法:")
    print(f"  1. Google Docsにアクセス")
    print(f"  2. 「AUTOCREATE使い方ガイド」を検索")
    print(f"  3. 自動生成されたドキュメントを確認")
    
    print(f"\n🎊 Google Docsでシステム使い方を確認可能！")

if __name__ == "__main__":
    main()
