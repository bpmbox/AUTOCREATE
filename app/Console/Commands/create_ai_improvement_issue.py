#!/usr/bin/env python3
"""
GitHub Issue作成スクリプト - AI改善提案システム
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def create_ai_improvement_issue():
    """AI自動質問改善システムのIssueを作成"""
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN環境変数が設定されていません")
        return False
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    issue_body = """## 🚀 AI自動質問改善＆実行システム

### 💡 提案概要
ユーザーからの質問を受け取り、AIが自動的に改善してから実行するシステムの実装

### 🎯 解決したい課題
- ユーザーの質問が曖昧で実行しにくい場合がある
- 質問の意図を汲み取って最適化したい
- 改善プロセスを自動化して効率を上げたい
- 実行まで一貫してAIが担当することでユーザー負担を軽減

### 🔧 実装すべき機能

#### 1. 質問受信・分析システム
- [ ] チャット内容の自動取得
- [ ] 自然言語による質問意図の解析
- [ ] 技術的要件の抽出と補完

#### 2. AI改善エンジン
- [ ] 質問内容の明確化
- [ ] 具体的なアクションプランの生成
- [ ] 優先度と工数の見積もり
- [ ] 成功基準の定義

#### 3. GitHub Issues自動管理
- [ ] 改善された内容でのIssue自動作成
- [ ] 適切なラベル付けとマイルストーン設定
- [ ] 実行ステータスの追跡

#### 4. 自動実行システム
- [ ] Issue内容に基づく自動タスク実行
- [ ] ファイル作成・編集の自動化
- [ ] テスト実行とデプロイ
- [ ] 実行結果のフィードバック

### 📋 実装ステップ

1. **要件分析・設計** (2時間)
   - 既存システムとの統合ポイント特定
   - AI改善ロジックの詳細設計
   - データフローの定義

2. **コア機能実装** (4時間)
   - 質問分析エンジンの実装
   - GitHub API統合
   - 自動実行フレームワーク構築

3. **統合・テスト** (2時間)
   - 既存のCopilot-Supabaseシステムとの連携
   - エンドツーエンドテスト
   - エラーハンドリングの実装

4. **運用・改善** (継続)
   - 実際の使用による精度向上
   - フィードバックループの最適化
   - システム拡張

### ✅ 成功基準
- [ ] ユーザーの曖昧な質問を90%以上正確に理解できる
- [ ] 改善された質問が実行可能な形になっている
- [ ] Issue作成から実行完了まで5分以内で処理
- [ ] ユーザー満足度の向上（手動作業の削減）

### 🔗 関連システム
- `copilot_direct_answer_fixed.py` - 既存のCopilot統合システム
- `ai_improvement_execution_system.py` - 新規実装システム
- Supabase - データ永続化
- GitHub Actions - 自動実行環境

### 📈 期待効果
- **効率化**: 質問→実行の時間短縮
- **品質向上**: AI による質問の最適化
- **自動化**: 人的作業の削減
- **学習**: 継続的な改善サイクル

### 🚀 実装優先度: 高
**推定工数: 8時間**
**緊急度: 中**

---
**作成者**: AI自動改善システム  
**作成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**関連**: AI/自動化/GitHub統合
"""
    
    issue_data = {
        "title": "🤖 AI自動質問改善＆実行システムの実装",
        "body": issue_body,
        "labels": [
            "enhancement",
            "ai-improvement", 
            "automation",
            "priority-high",
            "github-integration"
        ]
    }
    
    try:
        response = requests.post(
            "https://api.github.com/repos/bpmbox/AUTOCREATE/issues",
            headers=headers,
            json=issue_data,
            timeout=30
        )
        
        if response.status_code == 201:
            issue_data = response.json()
            print(f"✅ GitHub Issue作成成功!")
            print(f"📋 Issue #{issue_data['number']}: {issue_data['title']}")
            print(f"🔗 URL: {issue_data['html_url']}")
            return issue_data
        else:
            print(f"❌ Issue作成失敗: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Issue作成エラー: {e}")
        return None

if __name__ == "__main__":
    print("🎯 AI改善提案のGitHub Issue作成中...")
    result = create_ai_improvement_issue()
    
    if result:
        print("\n🎉 提案が正常にIssueとして登録されました！")
        print("次のステップ: 実装開始")
    else:
        print("\n❌ Issue作成に失敗しました")
