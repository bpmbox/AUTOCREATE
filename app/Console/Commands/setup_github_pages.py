#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Pages自動設定スクリプト
AUTOCREATE AI自動開発パイプライン
"""

import requests
import json
import os
from datetime import datetime

def setup_github_pages():
    """
    GitHub Pages設定を自動で有効化
    """
    print("🚀 GitHub Pages自動設定開始")
    print("=" * 50)
    
    # GitHub設定
    repo_owner = "bpmbox"
    repo_name = "AUTOCREATE"
    
    # GitHub Personal Access Tokenを環境変数から取得
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN環境変数が設定されていません")
        print("GitHub Settings > Developer settings > Personal access tokens")
        print("で'repo'権限を持つトークンを作成し、環境変数に設定してください")
        return False
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    # GitHub Pages設定
    pages_config = {
        "source": {
            "branch": "main",
            "path": "/docs"
        }
    }
    
    try:
        # GitHub Pages設定API呼び出し
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pages"
        
        print(f"📡 GitHub Pages設定中...")
        print(f"🔗 Repository: {repo_owner}/{repo_name}")
        print(f"📁 Source: main branch /docs folder")
        
        response = requests.post(url, headers=headers, json=pages_config)
        
        if response.status_code == 201:
            print("✅ GitHub Pages設定完了！")
            result = response.json()
            pages_url = result.get('html_url', f"https://{repo_owner}.github.io/{repo_name}/")
            print(f"🌐 公開URL: {pages_url}")
            print(f"💬 チャットアプリ: {pages_url}chat/")
            print()
            print("📝 設定が反映されるまで数分かかる場合があります")
            return True
            
        elif response.status_code == 409:
            print("✅ GitHub Pagesは既に設定済みです")
            
            # 現在の設定を取得
            get_response = requests.get(url, headers=headers)
            if get_response.status_code == 200:
                current_config = get_response.json()
                pages_url = current_config.get('html_url', f"https://{repo_owner}.github.io/{repo_name}/")
                print(f"🌐 公開URL: {pages_url}")
                print(f"💬 チャットアプリ: {pages_url}chat/")
                
                # 設定を更新
                print("🔄 設定を更新中...")
                put_response = requests.put(url, headers=headers, json=pages_config)
                if put_response.status_code == 200:
                    print("✅ GitHub Pages設定更新完了！")
                else:
                    print(f"⚠️ 設定更新に失敗: {put_response.status_code}")
                    print(put_response.text)
            return True
            
        else:
            print(f"❌ GitHub Pages設定に失敗: {response.status_code}")
            print(f"レスポンス: {response.text}")
            
            if response.status_code == 422:
                print("💡 ヒント: リポジトリがpublicであることを確認してください")
            elif response.status_code == 401:
                print("💡 ヒント: GITHUB_TOKENの権限を確認してください ('repo' scope必要)")
                
            return False
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        return False

def verify_pages_deployment():
    """
    GitHub Pages デプロイメント状況を確認
    """
    print("\n🔍 GitHub Pages デプロイメント確認中...")
    
    repo_owner = "bpmbox"
    repo_name = "AUTOCREATE"
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("❌ 確認にはGITHUB_TOKENが必要です")
        return
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Pages デプロイメント状況取得
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pages"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            pages_info = response.json()
            print("📊 GitHub Pages 状況:")
            print(f"   🌐 URL: {pages_info.get('html_url', 'N/A')}")
            print(f"   📁 Source: {pages_info.get('source', {}).get('branch', 'N/A')} / {pages_info.get('source', {}).get('path', 'N/A')}")
            print(f"   📈 Status: {pages_info.get('status', 'N/A')}")
            
            if pages_info.get('status') == 'built':
                print("✅ デプロイメント完了 - サイトアクセス可能")
            else:
                print("🔄 デプロイメント進行中...")
                
        else:
            print(f"❌ デプロイメント状況取得失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 確認エラー: {str(e)}")

def manual_setup_instructions():
    """
    手動設定手順を表示
    """
    print("\n📋 手動設定手順 (GITHUB_TOKENが無い場合):")
    print("=" * 50)
    print("1. https://github.com/bpmbox/AUTOCREATE にアクセス")
    print("2. Settings タブをクリック")
    print("3. 左メニューから Pages をクリック")
    print("4. Source を 'Deploy from a branch' に設定")
    print("5. Branch を 'main' に設定")
    print("6. Folder を '/docs' に設定")  
    print("7. Save ボタンをクリック")
    print()
    print("設定後のURL:")
    print("🌐 メインページ: https://bpmbox.github.io/AUTOCREATE/")
    print("💬 チャットアプリ: https://bpmbox.github.io/AUTOCREATE/chat/")

if __name__ == "__main__":
    print("🤖 AUTOCREATE GitHub Pages自動設定")
    print(f"📅 実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # GitHub Pages設定実行
    success = setup_github_pages()
    
    if success:
        # デプロイメント確認
        verify_pages_deployment()
        
        print("\n🎉 GitHub Pages設定完了！")
        print("📱 数分後にReact+Vite+shadcn UIチャットアプリが利用可能になります")
    else:
        # 手動設定手順を表示
        manual_setup_instructions()
