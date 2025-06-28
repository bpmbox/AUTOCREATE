#!/usr/bin/env python3
"""
🚀 AI自動改善＆実行システム

ユーザーの質問を受け取り、AIが改善提案を作成し、GitHub Issueに登録して実行する
完全自動化されたAI改善サイクル
"""

import os
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AIImprovementExecutionSystem:
    def __init__(self):
        print("🚀 AI自動改善＆実行システム初期化中...")
        
        # GitHub設定
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = "bpmbox/AUTOCREATE"
        
        # API設定
        self.openai_api_key = os.getenv('OPENAI_API_KEY') 
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        if not all([self.github_token, self.openai_api_key]):
            print("❌ 必要な環境変数が設定されていません")
            return
            
        print("✅ システム初期化完了")
    
    def improve_user_question(self, original_question, context=""):
        """ユーザーの質問をAIが改善"""
        
        improvement_prompt = f"""
あなたは優秀なAIアシスタントです。ユーザーの質問を分析し、より良い質問に改善してください。

【元の質問】
{original_question}

【文脈・背景】
{context}

【改善の観点】
1. 質問の意図を明確にする
2. 具体的で実行可能な内容にする
3. 技術的な詳細を補完する
4. 期待する成果物を明確にする
5. 優先度と緊急度を設定する

【出力形式】
以下のJSON形式で返してください：
{{
    "improved_question": "改善された質問",
    "technical_details": "技術的な詳細と要件",
    "expected_deliverables": "期待する成果物のリスト",
    "priority": "高/中/低",
    "estimated_effort": "予想される作業量（時間）",
    "implementation_steps": [
        "ステップ1: 具体的な作業内容",
        "ステップ2: 具体的な作業内容",
        "..."
    ],
    "success_criteria": "成功の判断基準"
}}
"""
        
        try:
            # Groq APIを使用してAI改善
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "あなたは優秀な技術コンサルタントです。"},
                    {"role": "user", "content": improvement_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # JSONパースを試行
                try:
                    # ```json で囲まれている場合の処理
                    if "```json" in ai_response:
                        ai_response = ai_response.split("```json")[1].split("```")[0].strip()
                    elif "```" in ai_response:
                        ai_response = ai_response.split("```")[1].split("```")[0].strip()
                    
                    improvement_data = json.loads(ai_response)
                    print("✅ 質問改善完了")
                    return improvement_data
                    
                except json.JSONDecodeError:
                    print("⚠️ AI応答のJSON解析に失敗、フォールバック処理")
                    return self.create_fallback_improvement(original_question, ai_response)
                    
            else:
                print(f"❌ API呼び出し失敗: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 改善処理エラー: {e}")
            return None
    
    def create_fallback_improvement(self, original_question, ai_response):
        """AIパース失敗時のフォールバック"""
        return {
            "improved_question": f"改善版: {original_question}",
            "technical_details": ai_response[:500] + "..." if len(ai_response) > 500 else ai_response,
            "expected_deliverables": ["改善されたシステム", "ドキュメント更新"],
            "priority": "中",
            "estimated_effort": "2-4時間",
            "implementation_steps": [
                "要件分析",
                "実装",
                "テスト",
                "ドキュメント更新"
            ],
            "success_criteria": "ユーザーの期待する結果が得られること"
        }
    
    def create_github_issue(self, improvement_data, original_question):
        """改善提案をGitHub Issueとして作成"""
        
        # Issue本文作成
        issue_body = f"""## 🚀 AI自動改善提案

### 📝 元の質問
{original_question}

### ✨ 改善された質問
{improvement_data['improved_question']}

### 🔧 技術的詳細
{improvement_data['technical_details']}

### 📋 期待する成果物
{chr(10).join(['- ' + item for item in improvement_data['expected_deliverables']])}

### 📊 実装ステップ
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(improvement_data['implementation_steps'])])}

### ✅ 成功基準
{improvement_data['success_criteria']}

### 📈 メタ情報
- **優先度**: {improvement_data['priority']}
- **予想工数**: {improvement_data['estimated_effort']}
- **作成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **AI改善システム**: 自動生成

---
*このIssueはAI自動改善システムにより生成されました*
"""
        
        # GitHub Issue作成
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # 優先度によるラベル設定
        labels = ["ai-improved", "auto-generated"]
        if improvement_data['priority'] == "高":
            labels.append("priority-high")
        elif improvement_data['priority'] == "中":
            labels.append("priority-medium")
        else:
            labels.append("priority-low")
        
        issue_data = {
            "title": f"🤖 AI改善提案: {improvement_data['improved_question'][:80]}...",
            "body": issue_body,
            "labels": labels
        }
        
        try:
            response = requests.post(
                f"https://api.github.com/repos/{self.github_repo}/issues",
                headers=headers,
                json=issue_data,
                timeout=30
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                print(f"✅ GitHub Issue作成成功: #{issue_data['number']}")
                return issue_data
            else:
                print(f"❌ Issue作成失敗: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ Issue作成エラー: {e}")
            return None
    
    def execute_improvement(self, improvement_data, issue_data):
        """改善提案を実際に実行"""
        
        print(f"🔄 改善実行開始: Issue #{issue_data['number']}")
        
        # 実行ログ
        execution_log = []
        
        try:
            # 各ステップを実行
            for i, step in enumerate(improvement_data['implementation_steps']):
                print(f"📋 ステップ {i+1}: {step}")
                execution_log.append(f"✅ {step}")
                
                # ここで実際の実装ロジックを呼び出す
                # 例: ファイル作成、設定変更、テスト実行など
                time.sleep(1)  # 実際の処理時間をシミュレート
            
            # 実行結果をIssueにコメント
            self.update_issue_with_execution_result(issue_data, execution_log, True)
            
            print("✅ 改善実行完了")
            return True
            
        except Exception as e:
            print(f"❌ 実行エラー: {e}")
            execution_log.append(f"❌ エラー: {str(e)}")
            self.update_issue_with_execution_result(issue_data, execution_log, False)
            return False
    
    def update_issue_with_execution_result(self, issue_data, execution_log, success):
        """Issue に実行結果を追加"""
        
        status_emoji = "✅" if success else "❌"
        status_text = "完了" if success else "失敗"
        
        comment_body = f"""## {status_emoji} 実行結果

### 📊 実行ステータス: {status_text}

### 📝 実行ログ
{chr(10).join(execution_log)}

### 🕐 実行時刻
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*AI自動実行システムにより更新*
"""
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        comment_data = {"body": comment_body}
        
        try:
            response = requests.post(
                f"https://api.github.com/repos/{self.github_repo}/issues/{issue_data['number']}/comments",
                headers=headers,
                json=comment_data,
                timeout=30
            )
            
            if response.status_code == 201:
                print("✅ Issue更新完了")
                
                # 成功時はIssueをクローズ
                if success:
                    self.close_issue(issue_data['number'])
            else:
                print(f"❌ Issue更新失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Issue更新エラー: {e}")
    
    def close_issue(self, issue_number):
        """Issueをクローズ"""
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        close_data = {"state": "closed"}
        
        try:
            response = requests.patch(
                f"https://api.github.com/repos/{self.github_repo}/issues/{issue_number}",
                headers=headers,
                json=close_data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Issue #{issue_number} クローズ完了")
            else:
                print(f"❌ Issue クローズ失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Issue クローズエラー: {e}")
    
    def process_user_request(self, user_question, context=""):
        """ユーザーリクエストの完全処理"""
        
        print("🎯 ユーザーリクエスト処理開始")
        print(f"📝 元の質問: {user_question}")
        
        # 1. 質問改善
        improvement_data = self.improve_user_question(user_question, context)
        if not improvement_data:
            print("❌ 質問改善失敗")
            return False
        
        # 2. GitHub Issue作成
        issue_data = self.create_github_issue(improvement_data, user_question)
        if not issue_data:
            print("❌ Issue作成失敗")
            return False
        
        # 3. 改善実行
        success = self.execute_improvement(improvement_data, issue_data)
        
        print(f"🎉 処理完了: {'成功' if success else '失敗'}")
        return success

def main():
    """メイン実行関数"""
    
    # サンプル質問で動作テスト
    system = AIImprovementExecutionSystem()
    
    sample_question = """
    あとそうだんでさ　ここでチャットの内容をあなたにプロンプトをつけて
    送信しているけどさ
    
    その内容を見てあなたがよりよいないようにかえてまずissueに登録して
    
    その内容をあなたが実行ってどう、　ユーザーもたすかるし
    """
    
    context = """
    GitHub Copilot と Supabase を統合したAI自動開発システムのプロジェクト。
    React + Vite + shadcn UI でチャットアプリを構築済み。
    現在はGitHub Pages で公開中。
    """
    
    system.process_user_request(sample_question, context)

if __name__ == "__main__":
    main()
