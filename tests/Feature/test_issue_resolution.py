#!/usr/bin/env python3
"""
Issue解決機能テスト用スクリプト
"""

import sys
import os

# メインスクリプトのパスを追加
sys.path.append(os.path.dirname(__file__))

from copilot_github_cli_automation import GitHubCopilotAutomation

def test_issue_resolution():
    """Issue解決機能のテスト"""
    print("🧪 Issue解決機能テスト開始")
    print("="*50)
    
    # 自動化システム初期化
    automation = GitHubCopilotAutomation(offline_mode=False)
    
    # 1. Issue一覧表示テスト
    print("\n1️⃣ Issue一覧表示テスト")
    selected_issue = automation.list_and_select_issues()
    
    if selected_issue:
        print(f"✅ Issue選択成功: #{selected_issue['number']} - {selected_issue['title']}")
        
        # 2. Issue詳細取得テスト
        print("\n2️⃣ Issue詳細取得テスト")
        issue_details = automation.get_issue_details(selected_issue['number'])
        
        if issue_details:
            print("✅ Issue詳細取得成功")
            print(f"📖 詳細内容（最初の200文字）:")
            print(issue_details[:200] + "..." if len(issue_details) > 200 else issue_details)
            
            # 3. 確認
            proceed = input("\n実際にチャットに送信しますか？ (y/N): ").lower()
            
            if proceed == 'y':
                # 4. チャット送信テスト
                print("\n3️⃣ チャット送信テスト")
                success = automation.send_issue_to_chat_for_resolution(selected_issue)
                
                if success:
                    print("✅ チャット送信成功！")
                    print("🤖 GitHub Copilotが自動解決を開始します")
                    
                    # 5. 監視オプション
                    monitor = input("\n解決監視を開始しますか？ (Y/n): ").lower()
                    if monitor != 'n':
                        automation.monitor_issue_resolution(selected_issue['number'])
                else:
                    print("❌ チャット送信失敗")
            else:
                print("💡 チャット送信をスキップしました")
        else:
            print("❌ Issue詳細取得失敗")
    else:
        print("❌ Issue選択失敗またはキャンセル")
    
    print("\n🏁 テスト完了")

if __name__ == "__main__":
    test_issue_resolution()
