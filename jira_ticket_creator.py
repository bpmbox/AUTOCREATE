import os
import requests
import json
from datetime import datetime
import base64

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class JiraTicketCreator:
    def __init__(self):
        self.jira_url = os.getenv('JIRA_URL', 'https://your-domain.atlassian.net')
        self.username = os.getenv('JIRA_USERNAME')
        self.api_token = os.getenv('JIRA_API_TOKEN')
        self.project_key = os.getenv('JIRA_PROJECT_KEY', 'AUTOCREATE')
        self.board_id = os.getenv('JIRA_BOARD_ID', '1')
        
        if self.username and self.api_token:
            # Basic Auth for JIRA Cloud
            auth_string = f"{self.username}:{self.api_token}"
            self.auth_header = base64.b64encode(auth_string.encode()).decode()
        else:
            self.auth_header = None
    
    def create_development_ticket(self, title, description, priority="Medium", issue_type="Task"):
        """開発タスクのJIRAチケット作成"""
        
        if not self.auth_header:
            print("❌ JIRA認証情報が設定されていません")
            return None
        
        # JIRA Issue作成データ
        issue_data = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "name": issue_type
                },
                "priority": {
                    "name": priority
                },
                "labels": ["autocreate", "automation", "notion-integration"],
                "components": [
                    {
                        "name": "Automation"
                    }
                ]
            }
        }
        
        headers = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json"
        }
        
        try:
            url = f"{self.jira_url}/rest/api/2/issue"
            response = requests.post(url, headers=headers, json=issue_data)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ JIRAチケット作成成功！")
                print(f"   チケット番号: {result['key']}")
                print(f"   URL: {self.jira_url}/browse/{result['key']}")
                return result
            else:
                print(f"❌ JIRAチケット作成失敗: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            return None
    
    def create_autocreate_tickets(self):
        """AUTOCREATE プロジェクト用の包括的チケット作成"""
        
        print("🎯 AUTOCREATE JIRA チケット作成システム")
        print("=" * 50)
        
        tickets = [
            {
                "title": "🎯 AUTOCREATE Notion統合システム実装",
                "description": """## 概要
AUTOCREATE システムとNotion APIの完全統合実装

## 実装内容
- Python/Node.js デュアル実装
- Chrome拡張機能連携
- リッチコンテンツページ自動作成
- エラーハンドリング・診断システム

## 成果物
- notion_page_creator.js
- notion_knowledge_manager.py  
- Chrome Extension統合
- Makefileコマンド

## 完了条件
- [ ] API接続確認
- [ ] ページ作成機能動作確認
- [ ] エラーハンドリング動作確認
- [ ] ドキュメント完備

## 優先度: High
## 見積工数: 5日
## 担当者: AUTOCREATE Team""",
                "priority": "High",
                "issue_type": "Story"
            },
            {
                "title": "🌐 Chrome拡張機能 XPath設定管理",
                "description": """## 概要
Chrome拡張機能でのXPath設定管理システム実装

## 実装内容
- XPath設定UI (xpath-config-manager.html)
- 設定保存・読み込み機能
- テスト・検証機能
- エラー処理

## 技術スタック
- Chrome Extension Manifest V3
- HTML/CSS/JavaScript
- Chrome Storage API

## 完了条件
- [ ] 設定UI動作確認
- [ ] 設定保存・読み込み確認
- [ ] XPathテスト機能確認
- [ ] Chrome Store準備

## 優先度: High
## 見積工数: 3日""",
                "priority": "High", 
                "issue_type": "Task"
            },
            {
                "title": "📚 ナレッジベース自動生成システム",
                "description": """## 概要
業務向け・開発向けナレッジベースの自動生成システム

## 実装内容
- 業務向けNotionページ自動作成
- 開発向けGitHub Issue自動作成
- テンプレート管理システム
- 一括展開機能

## 成果物
- notion_business_knowledge.js
- create_developer_issue.py
- resource-first-deploy コマンド

## ビジネス価値
- 資料作成時間 99.4%削減
- 品質統一・標準化
- アクセス性向上

## 完了条件
- [ ] 業務ナレッジ自動作成
- [ ] 開発仕様書自動作成
- [ ] 統合展開機能
- [ ] 品質検証

## 優先度: Medium
## 見積工数: 2日""",
                "priority": "Medium",
                "issue_type": "Epic"
            },
            {
                "title": "🔧 Makefileコマンド統合システム",
                "description": """## 概要
全機能を統合するMakefileコマンドシステム構築

## 実装内容
- notion-* コマンド群
- chrome-ext-* コマンド群  
- jira-* コマンド群
- 診断・テストコマンド
- ヘルプ・ガイドシステム

## 完了条件
- [ ] コマンド体系統一
- [ ] エラーハンドリング統一
- [ ] ヘルプシステム完備
- [ ] 使用説明書作成

## 優先度: Medium
## 見積工数: 1日""",
                "priority": "Medium",
                "issue_type": "Task"
            },
            {
                "title": "🚀 Triple Deploy 統合システム",
                "description": """## 概要
Notion + GitHub + JIRA の統合展開システム

## 実装内容
- 一括リソース作成
- 相互連携設定
- 統合テスト
- 品質保証

## ビジネス価値
- 展開時間 95%削減
- 人的エラー削除
- 一貫性保証
- チーム生産性向上

## 完了条件
- [ ] triple-deploy コマンド動作
- [ ] 全サービス連携確認
- [ ] エラー回復機能
- [ ] ドキュメント完備

## 優先度: High
## 見積工数: 3日""",
                "priority": "High",
                "issue_type": "Epic"
            },
            {
                "title": "🛡️ JIRA統合セキュリティ・認証",
                "description": """## 概要
JIRA API統合における認証とセキュリティ実装

## 実装内容
- Basic認証実装
- API Token管理
- 権限管理
- セキュリティベストプラクティス

## セキュリティ要件
- API Token暗号化保存
- 最小権限の原則
- ログ記録・監査
- エラー情報秘匿

## 完了条件
- [ ] 認証機能動作確認
- [ ] セキュリティテスト完了
- [ ] アクセス制御確認
- [ ] 脆弱性診断

## 優先度: High
## 見積工数: 2日""",
                "priority": "High",
                "issue_type": "Task"
            },
            {
                "title": "📊 AUTOCREATE プロジェクト管理ダッシュボード",
                "description": """## 概要
JIRA内でのAUTOCREATEプロジェクト進捗管理ダッシュボード作成

## 実装内容
- カンバンボード設定
- バーンダウンチャート
- 進捗レポート自動生成
- アラート・通知設定

## 管理機能
- スプリント管理
- リソース配分可視化
- 品質メトリクス
- リスク管理

## 完了条件
- [ ] ダッシュボード作成
- [ ] メトリクス設定
- [ ] 自動レポート機能
- [ ] チーム共有設定

## 優先度: Medium
## 見積工数: 1日""",
                "priority": "Medium",
                "issue_type": "Task"
            },
            {
                "title": "🔄 CI/CD JIRA統合パイプライン",
                "description": """## 概要
GitHubアクション - JIRA統合の自動化パイプライン

## 実装内容
- PR作成時のJIRAチケット自動更新
- ビルド・デプロイ状況のJIRA反映
- コードレビュー - JIRAコメント連携
- リリース時のチケット自動クローズ

## 技術スタック
- GitHub Actions
- JIRA REST API
- Webhook連携
- 状態管理

## 完了条件
- [ ] GitHub-JIRA連携確認
- [ ] 自動更新機能動作
- [ ] 状態同期確認
- [ ] 通知機能確認

## 優先度: Low
## 見積工数: 2日""",
                "priority": "Low",
                "issue_type": "Task"
            }
        ]
        
        print(f"📋 {len(tickets)}個のチケットを作成します...")
        print()
        
        created_tickets = []
        for i, ticket in enumerate(tickets, 1):
            print(f"[{i}/{len(tickets)}] {ticket['title']}")
            result = self.create_development_ticket(
                title=ticket['title'],
                description=ticket['description'],
                priority=ticket['priority'],
                issue_type=ticket['issue_type']
            )
            if result:
                created_tickets.append(result)
            print()
        
        print("=" * 50)
        print("📊 JIRA チケット作成結果")
        print(f"✅ 作成成功: {len(created_tickets)}個")
        print(f"❌ 作成失敗: {len(tickets) - len(created_tickets)}個")
        
        if created_tickets:
            print()
            print("🎯 作成されたチケット:")
            for ticket in created_tickets:
                print(f"   • {ticket['key']}: {self.jira_url}/browse/{ticket['key']}")
        
        return created_tickets
    
    def create_business_process_tickets(self):
        """ビジネスプロセス改善用のJIRAチケット作成"""
        
        business_tickets = [
            {
                "title": "📋 業務プロセス自動化戦略",
                "description": """## 概要
AUTOCREATE による業務プロセス自動化の戦略策定

## 対象業務
- 資料作成プロセス
- 情報共有・ナレッジ管理
- プロジェクト管理
- 品質管理

## 期待効果
- 作業時間 95%削減
- 品質向上・標準化
- コスト削減
- 従業員満足度向上

## アクションプラン
- [ ] 現状分析
- [ ] 自動化対象特定
- [ ] 優先順位付け
- [ ] ROI計算

## 完了条件
- [ ] 戦略文書作成
- [ ] ステークホルダー承認
- [ ] 実行計画策定
- [ ] KPI設定

## 優先度: High
## 見積工数: 3日""",
                "priority": "High",
                "issue_type": "Epic"
            },
            {
                "title": "🎯 ROI測定・効果検証システム",
                "description": """## 概要
AUTOCREATE 導入効果の定量的測定システム

## 測定指標
- 作業時間削減率
- 品質向上度
- コスト削減額
- ユーザー満足度

## 実装内容
- 使用状況ログ収集
- 効果測定ダッシュボード
- レポート自動生成
- 改善提案システム

## 完了条件
- [ ] 測定システム構築
- [ ] ダッシュボード作成
- [ ] レポート機能
- [ ] 継続改善プロセス

## 優先度: Medium
## 見積工数: 2日""",
                "priority": "Medium",
                "issue_type": "Task"
            }
        ]
        
        return self._create_tickets_batch(business_tickets, "ビジネスプロセス")
    
    def _create_tickets_batch(self, tickets, category_name):
        """チケット一括作成の共通処理"""
        
        print(f"🎯 {category_name} JIRAチケット作成")
        print("=" * 50)
        print(f"📋 {len(tickets)}個のチケットを作成します...")
        print()
        
        created_tickets = []
        for i, ticket in enumerate(tickets, 1):
            print(f"[{i}/{len(tickets)}] {ticket['title']}")
            result = self.create_development_ticket(
                title=ticket['title'],
                description=ticket['description'],
                priority=ticket['priority'],
                issue_type=ticket['issue_type']
            )
            if result:
                created_tickets.append(result)
            print()
        
        print("=" * 50)
        print(f"📊 {category_name} チケット作成結果")
        print(f"✅ 作成成功: {len(created_tickets)}個")
        print(f"❌ 作成失敗: {len(tickets) - len(created_tickets)}個")
        
        if created_tickets:
            print()
            print("🎯 作成されたチケット:")
            for ticket in created_tickets:
                print(f"   • {ticket['key']}: {self.jira_url}/browse/{ticket['key']}")
        
        return created_tickets

    def test_jira_connection(self):
        """JIRA API接続テスト"""
        
        if not self.auth_header:
            print("❌ JIRA認証情報が設定されていません")
            return False
        
        headers = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json"
        }
        
        try:
            # 自分のユーザー情報を取得してテスト
            url = f"{self.jira_url}/rest/api/2/myself"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                user_info = response.json()
                print("✅ JIRA API接続成功！")
                print(f"   👤 ユーザー: {user_info.get('displayName', 'Unknown')}")
                print(f"   📧 メール: {user_info.get('emailAddress', 'Unknown')}")
                return True
            else:
                print(f"❌ JIRA API接続失敗: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 接続エラー: {e}")
            return False


def main():
    """メイン実行関数"""
    creator = JiraTicketCreator()
    
    if not creator.auth_header:
        print("❌ JIRA認証情報が設定されていません")
        print("📝 .envファイルで以下を設定してください:")
        print("   JIRA_URL=https://your-domain.atlassian.net")
        print("   JIRA_USERNAME=your-email@domain.com")
        print("   JIRA_API_TOKEN=your_jira_api_token_here")
        return
    
    print("🎯 AUTOCREATE JIRA統合システム")
    print("=" * 50)
    print("1. 開発チケット作成")
    print("2. ビジネスプロセスチケット作成")
    print("3. 全チケット作成")
    print("4. 接続テスト")
    print()
    
    choice = input("選択してください (1/2/3/4): ").strip()
    
    if choice == "1":
        creator.create_autocreate_tickets()
    elif choice == "2":
        creator.create_business_process_tickets()
    elif choice == "3":
        creator.create_autocreate_tickets()
        print("\n" + "=" * 50 + "\n")
        creator.create_business_process_tickets()
    elif choice == "4":
        creator.test_jira_connection()
    else:
        print("❌ 無効な選択です")


if __name__ == "__main__":
    main()
