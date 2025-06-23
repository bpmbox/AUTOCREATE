#!/usr/bin/env python3
"""
🎯 GitHub Copilot直接回答システム（完全版）

Supabaseから質問を取得 → VS Codeチャットに送信 → Copilotの回答をSupabaseに投稿
VS Codeチャット経由でCopilotとつながり、回答をSupabaseに自動登録
"""

import os
import time
import json
import pyautogui
import pyperclip
import traceback
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# 環境変数読み込み
load_dotenv()

try:
    from supabase import create_client, Client
except ImportError as e:
    print(f"❌ 必要なパッケージがインストールされていません: {e}")
    print("📦 pip install supabase python-dotenv pyautogui pyperclip")
    exit(1)

class CopilotSupabaseIntegrationSystem:
    def __init__(self):
        print("🚀 GitHub Copilot-Supabase統合システム初期化中...")
        
        # 環境変数取得
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not all([self.supabase_url, self.supabase_key]):
            print("❌ 環境変数が設定されていません")
            return
        
        try:
            # Supabase初期化
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
            print("✅ Supabase接続成功")
        except Exception as e:
            print(f"❌ 初期化エラー: {e}")
            return
        
        # チャット座標
        self.chat_coordinates = None
        
        # PyAutoGUI設定
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2
        
        print("🎯 システム初期化完了")
    
    def check_file_changes(self):
        """ファイルの変更を監視してホットリロード"""
        current_file = Path(__file__)
        last_modified = current_file.stat().st_mtime
        
        while True:
            try:
                current_modified = current_file.stat().st_mtime
                if current_modified > last_modified:
                    print("\n🔥 ファイル変更検出! ホットリロード実行中...")
                    print("🔄 プログラムを再起動します...")
                    time.sleep(1)
                      # 現在のプロセスを新しいプロセスで置き換え
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                
                time.sleep(2)  # 2秒間隔でチェック
            except Exception as e:
                print(f"⚠️ ファイル監視エラー: {e}")
                time.sleep(5)
    
    def infinite_auto_loop(self, interval=3):
        """無限自動ループモード（完全に手を離せる）+ ホットリロード"""
        print("🔥 無限自動ループモード開始!")
        print(f"⚡ {interval}秒間隔で永続監視")
        print("🤖 新着メッセージを完全自動で処理")
        print("📍 座標固定: (1335, 1045)")
        print("🚀 GitHub Copilotが自動回答")
        print("🔄 ホットリロード: ファイル変更時自動再起動")
        print("="*50)
        
        # 座標を固定設定
        if not self.chat_coordinates:
            self.chat_coordinates = {'x': 1335, 'y': 1045, 'timestamp': datetime.now().isoformat()}
            print("✅ 座標を固定設定しました")
        
        processed_ids = set()
        last_id = 0
        check_count = 0
        success_count = 0
          # 現在の最新IDを取得
        try:
            result = self.supabase.table('chat_history') \
                .select('id') \
                .order('id', desc=True) \
                .limit(1) \
                .execute()
            if result.data:
                last_id = result.data[0]['id']
                print(f"📊 監視開始ID: {last_id}")
        except Exception as e:
            print(f"⚠️ 初期化エラー: {e}")
        
        print("\n🎯 無限ループ開始 - Ctrl+C で停止")
        print("="*50)
        
        # ホットリロード用のファイル監視設定
        current_file = Path(__file__)
        last_modified = current_file.stat().st_mtime
        
        try:
            while True:  # 無限ループ
                # ファイル変更チェック（ホットリロード）
                try:
                    current_modified = current_file.stat().st_mtime
                    if current_modified > last_modified:
                        print("\n🔥 ファイル変更検出! ホットリロード実行中...")
                        print("🔄 プログラムを再起動します...")
                        time.sleep(1)
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                except Exception as e:
                    print(f"⚠️ ホットリロードエラー: {e}")
                
                check_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                
                # 定期的にステータス表示
                if check_count % 20 == 1:  # 20回に1回詳細表示
                    print(f"\n🔄 {current_time} - チェック #{check_count} (成功: {success_count}件)")
                else:
                    print(f"⏰ {current_time} #{check_count}", end=" ")
                
                # 最新IDより大きいメッセージのみ取得
                try:
                    result = self.supabase.table('chat_history') \
                        .select('*') \
                        .gt('id', last_id) \
                        .order('id', desc=False) \
                        .execute()
                    
                    if result.data:
                        new_messages = result.data
                        print(f"⚡ 新着 {len(new_messages)}件!")
                        
                        for msg in new_messages:
                            owner = msg.get('ownerid', '')
                            message = msg.get('messages', '')
                            msg_id = msg['id']
                            
                            # Copilot系は除外
                            if owner and (
                                owner.lower().startswith('copilot') or 
                                owner.lower().startswith('ai-assistant') or
                                owner.lower().startswith('github') or
                                'bot' in owner.lower()
                            ):
                                print(f"  🤖 Copilot系スキップ: {owner}")
                                last_id = max(last_id, msg_id)
                                continue
                            
                            # 空メッセージをスキップ
                            if not message or not message.strip():
                                print(f"  ⏭️ 空メッセージスキップ")
                                last_id = max(last_id, msg_id)
                                continue
                              # ユーザーメッセージ検出
                            question_data = {
                                'id': msg_id,
                                'question': message,
                                'user': owner or 'Unknown',
                                'created': msg.get('created', '')
                            }
                            
                            print(f"\n🎯 ユーザーメッセージ検出!")
                            print(f"👤 {owner}: {message[:50]}...")
                              # VS CodeチャットでCopilotに質問 → 回答をSupabaseに投稿
                            if self.send_to_copilot_and_get_response(question_data):
                                success_count += 1
                                processed_ids.add(msg_id)
                                self.mark_question_as_processed(msg_id)
                                print(f"✅ Copilot質問送信成功! (累計: {success_count}件)")
                            else:
                                print("❌ 送信失敗")
                            
                            last_id = max(last_id, msg_id)
                            time.sleep(1)  # メッセージ間の待機
                    else:
                        print("📭")  # 新着なし
                        
                except Exception as e:
                    print(f"❌ チェックエラー: {e}")
                
                time.sleep(interval)  # 次のチェックまで待機
                
        except KeyboardInterrupt:
            print(f"\n\n⚠️ 無限自動ループを停止")
            print("="*50)
            print(f"📊 総チェック回数: {check_count}")
            print(f"🎯 自動処理成功: {success_count}件")
            print(f"🆔 最終処理ID: {last_id}")
            print("✨ お疲れ様でした!")
    
    def send_to_copilot_and_get_response(self, question_data):
        """VS CodeチャットでCopilotに質問を送信し、回答をSupabaseに投稿"""
        if not self.chat_coordinates:
            print("❌ チャット座標が未設定")
            return False
        
        try:
            question = question_data['question']
            user = question_data['user']            # GitHub Copilotに分かりやすい質問形式に変換
            formatted_question = f"""ユーザーからの質問

質問者: {user}
質問: {question}

[完全自動開発フロー実行をお願いします]

1. 詳細な回答生成: この質問に対して実用的で具体的な回答を作成

2. GitHub Issue作成:   GitHub設定値（.envから取得）:
   - GITHUB_TOKEN: 環境変数から自動取得
   
   GitHub CLIコマンド例:
   gh issue create --repo "bpmbox/AUTOCREATE" --title "{question} - 実装要求" --body "# {question}の実装\\n\\n## 要件\\n- {question}に関する実装\\n\\n## 仕様\\n- 詳細な技術仕様\\n\\n## 実装計画\\n- ステップバイステップの実装手順\\n\\n## Gitフォルダーパス\\n\`packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/\`\\n\\n## リポジトリ\\nhttps://github.com/bpmbox/AUTOCREATE" --label "ai-automation"
   - タイトル: 「{question}」の実装
   - 説明: 要件、仕様、実装計画、Gitフォルダーパス、リポジトリURL詳細記載
   - ラベル: ai-automation (重要: このラベルを必ず使用)

3. プロジェクトフォルダー作成:
   - フォルダー名: `packages/{question.lower().replace(' ', '-').replace('　', '-')}-project`
   - 必要なファイル構成を自動生成
   - README.md、実装ファイル、設定ファイル等
   - packagesフォルダー以下に整理して配置

4. プログラム自動実装:
   - 要求された機能を完全実装
   - テストコード作成
   - ドキュメント生成
   - 完全動作確認

5. GitHub Issue更新とリポジトリ作成:
   GitHub CLI実行例:
   # Issue更新（実装完了報告とGitパス含む）
   gh issue create --repo "bpmbox/AUTOCREATE" --title "{question} - 完全実装完了" --body "# {question} - 実装完了\\n\\n## 実装内容\\n- 全機能実装完了\\n- テストコード作成完了\\n- ドキュメント作成完了\\n\\n## Gitフォルダーパス\\n\`packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/\`\\n\\n## リポジトリURL\\nhttps://github.com/bpmbox/AUTOCREATE\\n\\n## 実装詳細\\n実装ファイル一覧と機能詳細をここに記載" --label "ai-automation,completed"
   
   # 新リポジトリ作成（必要に応じて）
   gh repo create "project-name" --public
   git push origin main   - 実装完了報告のIssue作成（Gitパス含む）
   - 新しいリポジトリURL報告
   - 成果物の詳細説明

6. n8nワークフロー自動作成:
   .envから取得する設定値:
   - N8N_API_KEY: 環境変数から自動取得
   - N8N_SERVER_URL: 環境変数から自動取得
   - N8N_BASE_URL: 環境変数から自動取得

7. JIRAチケット自動作成:
   .envから取得するJIRA設定値:
   - JIRA_URL: 環境変数から自動取得
   - JIRA_PROJECT_KEY: 環境変数から自動取得

8. Notionナレッジベース自動登録:
   .envから取得するNotion設定値:
   - NOTION_TOKEN: 環境変数から自動取得
   - NOTION_DATABASE_ID: 環境変数から自動取得
   
   実際のNotion API実行コード:
   ```python
   import requests
   import json
   
   notion_token = "{os.getenv('NOTION_TOKEN')}"
   database_id = "{os.getenv('NOTION_DATABASE_ID')}"
   
   if not notion_token or not database_id:
       print("❌ Notion環境変数が設定されていません")
       print("必要な環境変数: NOTION_TOKEN, NOTION_DATABASE_ID")
       return
   
   headers = {{
       "Authorization": f"Bearer {{notion_token}}",
       "Content-Type": "application/json",
       "Notion-Version": "2022-06-28"
   }}
   
   data = {{
       "parent": {{"database_id": database_id}},
       "properties": {{
           "Name": {{
               "title": [{{
                   "text": {{"content": "{question}"}}
               }}]
           }},           "Category": {{
               "select": {{"name": "AI自動開発"}}
           }},
           "Status": {{
               "select": {{"name": "完了"}}
           }},
           "Tags": {{
               "multi_select": [
                   {{"name": "ai-automation"}},
                   {{"name": "auto-implementation"}},
                   {{"name": "copilot-generated"}}
               ]
           }}
       }},
       "children": [{{
           "object": "block",
           "type": "paragraph",
           "paragraph": {{
               "rich_text": [{{
                   "type": "text",
                   "text": {{"content": f"{{'{question}'}} の実装が完了しました。packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project に配置されています。"}}
               }}]
           }}
       }}]
   }}
   
   response = requests.post(
       "https://api.notion.com/v1/pages",
       headers=headers,
       json=data
   )
   
   if response.status_code == 200:
       notion_page_url = response.json().get("url", "")
       print(f"✅ Notion ページ作成成功: {{notion_page_url}}")
   else:
       print(f"❌ Notion ページ作成失敗: {{response.text}}")
   ```

9. miiboナレッジベース自動登録:
   .envから取得するmiibo設定値:
   - MIIBO_API_KEY: 環境変数から自動取得
   - MIIBO_AGENT_ID: 環境変数から自動取得
   
   実際のmiibo API実行コード:
   ```python
   import requests
   import json
   
   miibo_api_key = "{os.getenv('MIIBO_API_KEY')}"
   miibo_agent_id = "{os.getenv('MIIBO_AGENT_ID')}"
   
   if not miibo_api_key or not miibo_agent_id:
       print("❌ miibo環境変数が設定されていません")
       print("必要な環境変数: MIIBO_API_KEY, MIIBO_AGENT_ID")
       return
   
   headers = {{
       "Authorization": f"Bearer {{miibo_api_key}}",
       "Content-Type": "application/json"
   }}
     knowledge_data = {{
       "title": "{question}",
       "content": f"{{'{question}'}} の実装が完了しました。\\n\\n実装内容:\\n- 要求された機能の完全実装\\n- テストコード作成\\n- ドキュメント生成\\n- 動作確認完了\\n\\nプロジェクトパス: packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project",
       "category": "auto-development",
       "tags": ["ai-automation", "auto-implementation", "copilot-generated"],
       "agent_id": miibo_agent_id
   }}
   
   response = requests.post(
       f"https://api.miibo.com/v1/agents/{{miibo_agent_id}}/knowledge",
       headers=headers,
       json=knowledge_data
   )
   
   if response.status_code == 200:
       miibo_knowledge_id = response.json().get("id", "")
       print(f"✅ miibo ナレッジ登録成功: ID {{miibo_knowledge_id}}")
   else:
       print(f"❌ miibo ナレッジ登録失敗: {{response.text}}")
   ```

10. Hugging Face Space自動作成・公開:
   .envから取得するHugging Face設定値:
   - HF_TOKEN: 環境変数から自動取得作成するHugging Face Space例:
   - Space名: `{question.lower().replace(' ', '-').replace('　', '-')}-app`
   - フレームワーク: Gradio (自動選択)
   - 可視性: Public (完全公開)
   - 必要ファイル: app.py, requirements.txt, README.md, .env.example
   - ローカルプロジェクト: packages/{question.lower().replace(' ', '-').replace('　', '-')}-project フォルダーから自動生成
   
   実際のHugging Face Spaces API実行コード:
   ```python
   import requests
   import json
   import os
   from huggingface_hub import HfApi, create_repo
   
   hf_token = "{os.getenv('HF_TOKEN')}"
   
   if not hf_token:
       print("❌ Hugging Face環境変数が設定されていません")
       print("必要な環境変数: HF_TOKEN")
       return
   space_name = "{question.lower().replace(' ', '-').replace('　', '-')}-app"
   
   # HF APIクライアント初期化
   api = HfApi(token=hf_token)
   
   try:
       # Space作成
       repo_id = f"{{api.whoami()['name']}}/{{space_name}}"
       
       create_repo(
           repo_id=repo_id,
           repo_type="space",
           space_sdk="gradio",
           private=False,
           token=hf_token
       )
       
       # app.pyファイルアップロード
       app_py_path = f"packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/app.py"
       if os.path.exists(app_py_path):
           api.upload_file(
               path_or_fileobj=app_py_path,
               path_in_repo="app.py",
               repo_id=repo_id,
               repo_type="space",
               token=hf_token
           )
       
       # requirements.txtアップロード
       req_path = f"packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/requirements.txt"
       if os.path.exists(req_path):
           api.upload_file(
               path_or_fileobj=req_path,
               path_in_repo="requirements.txt",
               repo_id=repo_id,
               repo_type="space",
               token=hf_token
           )
       
       # README.mdアップロード  
       readme_path = f"packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/README_HF.md"
       if os.path.exists(readme_path):
           api.upload_file(
               path_or_fileobj=readme_path,
               path_in_repo="README.md",
               repo_id=repo_id,
               repo_type="space",
               token=hf_token
           )
       
       space_url = f"https://huggingface.co/spaces/{{repo_id}}"
       print(f"✅ Hugging Face Space作成成功: {{space_url}}")
       
   except Exception as e:
       print(f"❌ Hugging Face Space作成失敗: {{str(e)}}")
   ```
   
   Hugging Face Space作成手順:
   1. Space作成 (Gradio SDK使用)
   2. app.pyファイル自動生成・アップロード
   3. requirements.txt作成・アップロード
   4. README.md作成・アップロード
   5. 公開URL取得・確認

11. JIRA チケット自動作成:
   .envから取得するJIRA設定値:
   - JIRA_URL: 環境変数から自動取得（デフォルト: https://bpmboxes-team-oyd7xvuu.atlassian.net）
   - JIRA_PROJECT_KEY: 環境変数から自動取得（デフォルト: OPS）
   - JIRA_USER: 環境変数から自動取得
   - JIRA_API_TOKEN: 環境変数から自動取得
   
   実際のJIRA API実行コード:
   ```python
   import requests
   import json
   import base64
   
   jira_url = "{os.getenv('JIRA_URL', 'https://bpmboxes-team-oyd7xvuu.atlassian.net')}"
   jira_user = "{os.getenv('JIRA_USER', 'your-email@domain.com')}"
   jira_token = "{os.getenv('JIRA_API_TOKEN', 'your-api-token')}"
   project_key = "{os.getenv('JIRA_PROJECT_KEY', 'OPS')}"
   
   # Basic認証
   credentials = base64.b64encode(f"{{jira_user}}:{{jira_token}}".encode()).decode()
   
   headers = {{
       "Authorization": f"Basic {{credentials}}",
       "Content-Type": "application/json"
   }}
     issue_data = {{
       "fields": {{
           "project": {{"key": project_key}},
           "summary": f"{question} - 実装完了",
           "description": f"{{'{question}'}} の実装が完了しました。\\n\\n## 実装内容\\n- 要求された機能の完全実装\\n- テストコード作成完了\\n- ドキュメント作成完了\\n- 動作確認完了\\n\\n## プロジェクト配置\\npackages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/\\n\\n## 実装方式\\n- AI自動開発パイプライン使用\\n- 13ステップ完全自動化\\n- GitHub Copilot AI実装",
           "issuetype": {{"name": "Task"}},
           "priority": {{"name": "High"}},
           "labels": ["ai-automation", "auto-implementation", "copilot-generated"]
       }}
   }}
   
   response = requests.post(
       f"{{jira_url}}/rest/api/3/issue",
       headers=headers,
       json=issue_data
   )
   
   if response.status_code == 201:
       issue_key = response.json().get("key", "")
       issue_url = f"{{jira_url}}/browse/{{issue_key}}"
       print(f"✅ JIRA チケット作成成功: {{issue_url}}")
   else:
       print(f"❌ JIRA チケット作成失敗: {{response.text}}")
   ```

12. Supabase投稿:
   - ownerid: 'GitHub-Copilot-AI'
   - messages: 回答内容 + GitHub Issue URL + リポジトリURL + n8nワークフローURL + JIRAチケットURL + NotionページURL + miiboナレッジURL + HuggingFace SpaceURL + 実装結果詳細
   - created: 現在時刻
     実際のSupabase API実行コード:
   ```python
   from supabase import create_client, Client
   from datetime import datetime
   
   supabase_url = "{os.getenv('SUPABASE_URL')}"
   supabase_key = "{os.getenv('SUPABASE_KEY')}"
   
   if not supabase_url or not supabase_key:
       print("❌ Supabase環境変数が設定されていません")
       print("必要な環境変数: SUPABASE_URL, SUPABASE_KEY")
       return
   
   supabase: Client = create_client(supabase_url, supabase_key)     response_data = {{
       'ownerid': 'GitHub-Copilot-AI',
       'messages': f'''{{'{question}'}} の完全実装が完了しました！
       
## 🎯 実装概要
ユーザーからの要求「{{'{question}'}}」に対して、AI自動開発パイプラインにより完全実装を実行しました。

## 🚀 実装内容
- 要求された機能の完全実装
- 包括的なテストコード作成
- 詳細なドキュメント生成
- 動作確認・品質保証完了
- エラーハンドリング実装

## 📁 プロジェクト配置
packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/

## 🔗 関連リンク・成果物
- GitHub Issue: [作成されたIssue URL]
- GitHub リポジトリ: https://github.com/bpmbox/AUTOCREATE
- プロジェクトパス: packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/
- JIRA チケット: [作成されたJIRA URL]  
- Notion ナレッジ: [作成されたNotion URL]
- miibo エージェント: [登録されたmiibo ID]
- Hugging Face Space: [作成されたSpace URL]
- n8n ワークフロー: 自動化フロー作成完了

## ✅ 完了状況
全13ステップの完全自動開発フローが正常に実行されました。

## 🚀 最終Git Push実行
変更をメインブランチにプッシュしています...

## 🤖 AI自動開発システム
- GitHub Copilot AI による完全自動実装
- 13ステップ自動開発パイプライン実行
- API統合（GitHub/JIRA/Notion/miibo/HuggingFace/Supabase）完了
''',
       'created': datetime.now().isoformat()
   }}
   
   result = supabase.table('chat_history').insert(response_data).execute()
   
   if result.data:
       print(f"✅ Supabase結果投稿成功: ID {{result.data[0]['id']}}")
   else:
       print("❌ Supabase結果投稿失敗")
   ```

13. 最終Git Push実行:
   ```bash
   # Gitステータス確認
   git status
   
   # 全変更をステージング
   git add .
   
   # コミット（質問内容を含む）
   git commit -m "{question} - 完全実装完了

   - プロジェクトフォルダ: packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/
   - 全ファイル実装完了
   - API統合完了（GitHub/JIRA/Notion/miibo/HuggingFace/Supabase）
   - 12ステップ自動開発フロー実行完了"
   
   # メインブランチにプッシュ
   git push origin main
   
   echo "✅ Git Push完了: https://github.com/bpmbox/AUTOCREATE"
   echo "📁 プロジェクトパス: packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/"
   ```

重要な実行ガイド:
- GitHub CLI認証確認: gh auth status
- リポジトリ: bpmbox/AUTOCREATE にIssue作成
- ラベル: "ai-automation" 必須使用
- 文字コード: UTF-8設定で実行
- PowerShell例: $env:PYTHONUTF8=1; gh issue create...
- 必須パッケージインストール: pip install requests huggingface_hub supabase python-dotenv
- 実際のAPI実行: 上記のPythonコードを全て実行してください
- エラーハンドリング: API失敗時は詳細なエラーメッセージを表示
- 成功確認: 各APIの成功メッセージとURLを表示
- Gitフォルダーパス: packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/ を必ずIssueに記載
- 最終Push: 全実装完了後に git add . && git commit && git push origin main を実行

このシステムは完全自動開発パイプライン + 実際のAPI統合（GitHub + JIRA + Notion + miibo + Hugging Face + Supabase + Git Push）です。全13ステップを実行し、実際にAPIを呼び出してデータを登録し、最後にGitリポジトリにプッシュしてください！"""
            
            print(f"📤 Copilotチャットに質問送信中...")
            print(f"質問: {question}")
            
            x, y = self.chat_coordinates['x'], self.chat_coordinates['y']
            
            # チャット欄クリック
            for i in range(3):
                pyautogui.click(x, y)
                time.sleep(0.3)
            
            # 内容クリア
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.3)
            
            # クリップボード経由で入力
            pyperclip.copy(formatted_question)
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.5)
            
            print("[質問入力完了]")
            # 自動送信
            print("[Copilotに送信中...]")
            pyautogui.press('enter')
            time.sleep(3)  # Copilotの回答生成を待機
            print("[質問送信完了]")
            print("GitHub Copilotが完全自動開発フローを実行中...")
            print("🚀 Issue作成 → フォルダー生成 → プログラム実装 → リポジトリ登録 → Supabase投稿")
            print("🔥 GitHub Copilot様へ: 6ステップ全てを実行してください！")
            
            return True
                
        except Exception as e:
            print(f"❌ チャット送信エラー: {e}")
            return False
    
    def post_copilot_response_to_supabase(self, question_data, response_text):
        """Copilotの回答をSupabaseに投稿"""
        try:
            # AI/Copilotの回答をSupabaseに投稿
            result = self.supabase.table('chat_history').insert({
                'ownerid': 'GitHub-Copilot-AI',
                'messages': response_text,
                'created': datetime.now().isoformat()
            }).execute()
            
            if result.data:
                print(f"✅ Copilot回答をSupabaseに投稿成功: ID {result.data[0]['id']}")
                return True
            else:
                print("❌ Supabase投稿失敗")
                return False
                
        except Exception as e:
            print(f"❌ Supabase投稿エラー: {e}")
            return False
    
    def mark_question_as_processed(self, question_id):
        """質問を処理済みとしてマーク"""
        try:
            # 簡単な処理済みフラグを追加
            self.supabase.table('chat_history') \
                .update({'copilot_processed': True}) \
                .eq('id', question_id) \
                .execute()
            return True
        except Exception as e:
            print(f"⚠️ 処理済みマーク失敗: {e}")
            return False

def main():
    import sys
    
    # コマンドライン引数で自動起動モードをチェック
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        print("🔥 完全自動起動モード")
        print("📍 座標固定: (1335, 1045)")
        print("⚡ 3秒間隔で永続監視開始")
        print("🤖 手を離してください - 完全自動運転中")
        print("-" * 50)
        
        system = CopilotSupabaseIntegrationSystem()
        if hasattr(system, 'supabase') and system.supabase:
            # 座標を自動設定
            system.chat_coordinates = {"x": 1335, "y": 1045}
            print("✅ 座標自動設定完了")            
            # 無限自動ループを即座に開始
            system.infinite_auto_loop(3)
        else:
            print("❌ システム初期化失敗")
        return
    
    print("🎯 GitHub Copilot-Supabase統合システム")
    print("VS Codeチャット経由でCopilotと連携し、回答をSupabaseに自動投稿")
    print("自動モードで起動してください:")
    print("python copilot_direct_answer_fixed.py --auto")

if __name__ == "__main__":
    main()
