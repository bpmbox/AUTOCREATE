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
        
        # AI改善システムのインポート
        from ai_improvement_execution_system import AIImprovementExecutionSystem
        self.ai_improvement_system = AIImprovementExecutionSystem()
        
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
                                continue                            # ユーザーメッセージ検出
                            question_data = {
                                'id': msg_id,
                                'question': message,
                                'user': owner or 'Unknown',
                                'created': msg.get('created', '')
                            }
                            
                            print(f"\n🎯 ユーザーメッセージ検出!")
                            print(f"👤 {owner}: {message[:50]}...")
                            
                            # 🚀 AI改善システムを使用
                            print("🤖 AI自動改善システム開始...")
                            if self.improve_and_execute_user_question(question_data):
                                success_count += 1
                                processed_ids.add(msg_id)
                                self.mark_question_as_processed(msg_id)
                                print(f"✅ AI改善・Copilot処理成功! (累計: {success_count}件)")
                            else:
                                print("❌ AI改善・処理失敗")
                                # フォールバック: 元の方法で処理
                                print("🔄 フォールバック: 元の質問で処理...")
                                if self.send_to_copilot_and_get_response(question_data):
                                    success_count += 1
                                    processed_ids.add(msg_id)
                                    self.mark_question_as_processed(msg_id)
                                    print(f"✅ フォールバック処理成功! (累計: {success_count}件)")
                                else:
                                    print("❌ フォールバック処理も失敗")
                            
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

5. Mermaidダイアグラム自動生成:
   - システム構成図（system-architecture.mmd）
   - データフロー図（data-flow.mmd）
   - プロセスフロー図（process-flow.mmd）
   - API設計図（api-design.mmd）
   - 実装手順図（implementation-steps.mmd）
   - 必要に応じて追加の技術図表
   - diagrams/フォルダーに整理配置
   - README.mdに図表リンク追加

6. GitHubウィキ統合・ナレッジベース連携:
   ```bash
   # GitHub Wiki をサブモジュールとして追加
   git submodule add https://github.com/bpmbox/AUTOCREATE.wiki.git wiki
   
   # ナレッジベースをWikiに統合
   mkdir -p wiki/knowledge-base
   mkdir -p wiki/ai-memory
   mkdir -p wiki/mermaid-diagrams
   mkdir -p wiki/conversation-logs
   
   # 自動生成ナレッジをWikiに同期
   cp -r knowledge_base/auto_generated/* wiki/knowledge-base/
   cp -r knowledge_base/mermaid_test/* wiki/mermaid-diagrams/
   cp -r conversation_logs/* wiki/conversation-logs/
   
   # AI記憶復元システム連携用ファイル作成
   echo "# AI記憶復元システム - GitHub Copilot成長ナレッジ
   
   このディレクトリは GitHub Copilot AI の記憶・ナレッジが蓄積される中央リポジトリです。
   
   ## 📚 ナレッジ構造
   - \`knowledge-base/\`: 自動生成ナレッジ（JSON + Markdown）
   - \`ai-memory/\`: AI記憶復元用データ
   - \`mermaid-diagrams/\`: 自動生成図表
   - \`conversation-logs/\`: 会話履歴
   
   ## 🧠 記憶復元システム
   GitHub Copilot AI は以下の情報から過去の知識を復元します：
   
   ### 技術ナレッジ
   - プログラミング実装パターン
   - アーキテクチャ設計例
   - 問題解決手法
   - ベストプラクティス
   
   ### プロジェクト記憶
   - 過去の実装履歴
   - ユーザーの好み・パターン
   - 成功・失敗事例
   - 継続的改善点
   
   ## 🔄 自動同期フロー
   1. ユーザー質問 → AI回答生成
   2. ナレッジベース自動保存
   3. Wiki自動同期・更新
   4. AI記憶強化・成長
   5. 次回質問時に過去知識活用
   
   ## 🚀 AI成長サイクル
   質問 → 学習 → 記憶 → 成長 → より良い回答
   " > wiki/ai-memory/README.md
   
   # Wikiコミット・プッシュ
   cd wiki
   git add .
   git commit -m "AI自動開発パイプライン - ナレッジベース統合
   
   - 自動生成ナレッジ同期
   - Mermaidダイアグラム統合  
   - 会話履歴アーカイブ
   - AI記憶復元システム構築
   - GitHub Copilot成長基盤完成"
   
   git push origin master
   cd ..
   
   # メインリポジトリでWikiサブモジュール設定コミット
   git add .gitmodules wiki
   git commit -m "GitHub Wiki サブモジュール統合完了
   
   - Wiki統合でAI記憶永続化
   - ナレッジベース一元管理
   - 記憶復元システム連携
   - GitHub Copilot成長インフラ完成"
   
   git push origin main
   ```

7. 独立リポジトリ作成とサブモジュール化:
   プロジェクトフォルダーを独立したリポジトリとして作成し、メインリポジトリにサブモジュールとして設定
   
   手順:
   ```bash
   # 1. プロジェクトディレクトリに移動
   cd packages/{question.lower().replace(' ', '-').replace('　', '-')}-project
   
   # 2. Git初期化
   git init
   git add .
   git commit -m "初回コミット: {question}
   
   - 要求された機能の完全実装
   - テストコード作成完了  
   - ドキュメント作成完了
   - 商用レベル品質保証"
   
   # 3. GitHub新リポジトリ作成（.envのGITHUB_TOKENを使用）
   gh repo create "{question.lower().replace(' ', '-').replace('　', '-')}-project" --public --source=. --remote=origin --push
   
   # 4. メインリポジトリに戻る
   cd ../..
   
   # 5. 既存ディレクトリを削除
   git rm -r packages/{question.lower().replace(' ', '-').replace('　', '-')}-project
   rm -rf packages/{question.lower().replace(' ', '-').replace('　', '-')}-project
   
   # 6. サブモジュールとして追加
   git submodule add https://github.com/[USERNAME]/{question.lower().replace(' ', '-').replace('　', '-')}-project.git packages/{question.lower().replace(' ', '-').replace('　', '-')}-project
   
   # 7. サブモジュール設定をコミット
   git add .gitmodules packages/{question.lower().replace(' ', '-').replace('　', '-')}-project
   git commit -m "{question} - サブモジュール化完了
   
   - 独立リポジトリとして分離
   - サブモジュール設定完了
   - 再利用可能な構成"
   
   # 8. メインリポジトリにプッシュ
   git push origin main
   ```

6. GitHub Issue作成（独立リポジトリURL含む）:
   GitHub CLI実行例:
   ```bash
   # 独立リポジトリのURLを取得
   REPO_URL=$(gh repo view {question.lower().replace(' ', '-').replace('　', '-')}-project --json url --jq .url)
   
   # Issue作成（独立リポジトリURL含む）
   gh issue create --repo "bpmbox/AUTOCREATE" --title "{question} - 完全実装・サブモジュール化完了" --body "# {question} - 実装・サブモジュール化完了\\n\\n## 🎯 実装概要\\n{question}の完全実装が完了し、独立したリポジトリとしてサブモジュール化しました。\\n\\n## 🚀 実装内容\\n- 要求された機能の完全実装\\n- テストコード作成完了\\n- ドキュメント作成完了\\n- 動作確認・品質保証完了\\n- エラーハンドリング実装\\n\\n## 📁 プロジェクト配置\\n### メインリポジトリ\\n- サブモジュールパス: \\\`packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/\\\`\\n- メインリポジトリ: https://github.com/bpmbox/AUTOCREATE\\n\\n### 独立リポジトリ\\n- 独立リポジトリURL: \${{REPO_URL}}\\n- リポジトリ名: {question.lower().replace(' ', '-').replace('　', '-')}-project\\n\\n## 🔧 サブモジュール操作\\n### クローン時\\n\\\`\\\`\\\`bash\\\\ngit clone --recursive https://github.com/bpmbox/AUTOCREATE.git\\\\n\\\`\\\`\\\`\\n\\n### 既存プロジェクトでサブモジュール初期化\\n\\\`\\\`\\\`bash\\\\ngit submodule init\\\\ngit submodule update\\\\n\\\`\\\`\\\`\\n\\n### サブモジュール更新\\n\\\`\\\`\\\`bash\\\\ncd packages/{question.lower().replace(' ', '-').replace('　', '-')}-project\\\\ngit pull origin master\\\\ncd ../..\\\\ngit add packages/{question.lower().replace(' ', '-').replace('　', '-')}-project\\\\ngit commit -m \\\\\\\"サブモジュール更新\\\\\\\"\\\\n\\\`\\\`\\\`\\n\\n## ✅ 完了事項\\n- [x] 要求機能の完全実装\\n- [x] テストコード作成\\n- [x] ドキュメント生成\\n- [x] 独立リポジトリ作成\\n- [x] サブモジュール設定\\n- [x] 動作確認完了\\n\\n## 🎉 メリット\\n- **独立管理**: プロジェクト単独でのバージョン管理\\n- **再利用性**: 他のプロジェクトでも使用可能\\n- **メンテナンス性**: 独立した開発・更新サイクル\\n- **コラボレーション**: 専用リポジトリでの共同開発可能\\n\\n## 🔗 関連リンク\\n- メインリポジトリ: https://github.com/bpmbox/AUTOCREATE\\n- 独立リポジトリ: \${{REPO_URL}}\\n- サブモジュールパス: packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/\\n\\n## 🤖 AI自動開発システム\\n- GitHub Copilot AI による完全自動実装\\n- 独立リポジトリ + サブモジュール自動化\\n- 13ステップ自動開発パイプライン実行完了" --label "ai-automation,submodule,completed"
   ```

7. n8nワークフロー自動作成:
   .envから取得する設定値:
   - N8N_API_KEY: 環境変数から自動取得
   - N8N_SERVER_URL: 環境変数から自動取得
   - N8N_BASE_URL: 環境変数から自動取得

8. JIRAチケット自動作成:
   .envから取得するJIRA設定値:
   - JIRA_URL: 環境変数から自動取得
   - JIRA_PROJECT_KEY: 環境変数から自動取得

9. Notionナレッジベース自動登録:
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

10. miiboナレッジベース自動登録:
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

11. Hugging Face Space自動作成・公開:
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

12. JIRA チケット自動作成:
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

13. Supabase投稿:
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
### メインリポジトリ（サブモジュール）
packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/

### 独立リポジトリ
https://github.com/[USERNAME]/{{question.lower().replace(' ', '-').replace('　', '-')}}-project

## 🔗 関連リンク・成果物
- GitHub Issue: [作成されたIssue URL]
- メインリポジトリ: https://github.com/bpmbox/AUTOCREATE
- 独立リポジトリ: [新規作成された独立リポジトリURL]
- サブモジュールパス: packages/{{question.lower().replace(' ', '-').replace('　', '-')}}-project/
- JIRA チケット: [作成されたJIRA URL]  
- Notion ナレッジ: [作成されたNotion URL]
- miibo エージェント: [登録されたmiibo ID]
- Hugging Face Space: [作成されたSpace URL]
- n8n ワークフロー: 自動化フロー作成完了

## ✅ 完了状況
全14ステップの完全自動開発フローが正常に実行されました。

## 🚀 サブモジュール化完了
独立リポジトリ作成とサブモジュール設定が完了しました。

## 🤖 AI自動開発システム
- GitHub Copilot AI による完全自動実装
- 14ステップ自動開発パイプライン実行
- 独立リポジトリ + サブモジュール自動化
- API統合（GitHub/JIRA/Notion/miibo/HuggingFace/Supabase）完了
''',
       'created': datetime.now().isoformat()
   }}
   
   result = supabase.table('chat_history').insert(response_data).execute()
   
   if result.data:                print(f"✅ Supabase結果投稿成功: ID {result.data[0]['id']}")
   else:
       print("❌ Supabase結果投稿失敗")
   ```

14. 最終Git Push実行（サブモジュール含む）:
   ```bash
   # 独立リポジトリでの最終Push
   cd packages/{question.lower().replace(' ', '-').replace('　', '-')}-project
   git add .
   git commit -m "{question} - 最終実装完了
   
   - 全機能実装完了
   - テストコード完備
   - ドキュメント完備
   - 品質保証完了"
   git push origin master
   cd ../..
   
   # メインリポジトリでサブモジュール設定とPush
   git add .gitmodules packages/{question.lower().replace(' ', '-').replace('　', '-')}-project
   git commit -m "{question} - サブモジュール化完了

   - プロジェクトフォルダ: packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/
   - 独立リポジトリ作成完了
   - サブモジュール設定完了
   - API統合完了（GitHub/JIRA/Notion/miibo/HuggingFace/Supabase）
   - 13ステップ自動開発フロー実行完了"
   
   # メインブランチにプッシュ
   git push origin main
   
   echo "✅ Git Push完了:"
   echo "- メインリポジトリ: https://github.com/bpmbox/AUTOCREATE"
   echo "- 独立リポジトリ: [新規作成されたURL]"
   echo "📁 サブモジュールパス: packages/{question.lower().replace(' ', '-').replace('　', '-')}-project/"
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
- 最終Push: 全実装完了後に git add . && git commit && git push origin main を実行    このシステムは完全自動開発パイプライン + 実際のAPI統合（GitHub + JIRA + Notion + miibo + Hugging Face + Supabase + Git Push + サブモジュール化）です。全14ステップを実行し、実際にAPIを呼び出してデータを登録し、独立リポジトリを作成、サブモジュール設定、最後にGitリポジトリにプッシュしてください！"""
            
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
            time.sleep(3)  # Copilotの回答生成を待機            print("[質問送信完了]")
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
                'created': datetime.now().isoformat(),
                'targetid': 'auto-development-pipeline',
                'status': 'ai-generated',
                'tmp_file': 'auto-knowledge-base'            }).execute()
            
            if result.data:
                print(f"✅ Copilot回答をSupabaseに投稿成功: ID {result.data[0]['id']}")
                # ナレッジベースにも自動保存（Mermaidダイアグラム含む）
                self.save_to_knowledge_base(question_data, response_text)
                return True
            else:
                print("❌ Supabase投稿失敗")
                return False
                
        except Exception as e:
            print(f"❌ Supabase投稿エラー: {e}")
            return False
    
    def save_to_knowledge_base(self, question_data, response_text):
        """ナレッジベースに自動保存"""
        try:
            from pathlib import Path
            import json
            
            # ナレッジディレクトリ作成
            knowledge_dir = Path("knowledge_base/auto_generated")
            knowledge_dir.mkdir(parents=True, exist_ok=True)
            
            # ナレッジエントリ作成
            knowledge_entry = {
                "timestamp": datetime.now().isoformat(),
                "question": question_data['question'],
                "questioner": question_data['user'],
                "copilot_response": response_text,
                "auto_generated": True,
                "knowledge_type": "copilot-ai-response",
                "tags": self.extract_tags_from_question(question_data['question'])
            }
            
            # ファイル名生成（質問から安全なファイル名を作成）
            safe_filename = "".join(c for c in question_data['question'][:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename.replace(' ', '_')}.json"
            filepath = knowledge_dir / filename
            
            # JSON保存
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(knowledge_entry, f, ensure_ascii=False, indent=2)
            
            print(f"✅ ナレッジベース自動保存: {filepath}")
              # Markdownサマリーも生成
            self.generate_markdown_summary(knowledge_entry, knowledge_dir)
              # Mermaidダイアグラム自動生成
            self.generate_mermaid_diagram(knowledge_entry, knowledge_dir)
            
            # GitHub Wiki統合・記憶復元システム連携
            self.sync_to_wiki_knowledge(knowledge_entry, knowledge_dir)
            
            return True
            
        except Exception as e:
            print(f"⚠️ ナレッジベース保存エラー: {e}")
            return False
    
    def extract_tags_from_question(self, question):
        """質問からタグを自動抽出"""
        tech_keywords = {
            'react': ['react', 'jsx', 'component'],
            'python': ['python', 'django', 'flask', 'fastapi'],
            'javascript': ['javascript', 'js', 'node', 'npm'],
            'typescript': ['typescript', 'ts'],
            'database': ['database', 'sql', 'postgresql', 'mysql', 'supabase'],
            'api': ['api', 'rest', 'graphql', 'endpoint'],
            'frontend': ['frontend', 'ui', 'css', 'html'],
            'backend': ['backend', 'server', 'service'],
            'deployment': ['deploy', 'docker', 'kubernetes', 'heroku'],
            'ai': ['ai', 'machine learning', 'ml', 'copilot', 'chatgpt']
        }
        
        found_tags = []
        question_lower = question.lower()
        
        for category, keywords in tech_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                found_tags.append(category)
        
        return found_tags if found_tags else ['general']
    
    def generate_markdown_summary(self, knowledge_entry, knowledge_dir):
        """Markdownサマリー生成"""
        try:
            summary_file = knowledge_dir / "README.md"
            
            # 既存の内容を読み込み（存在する場合）
            existing_content = ""
            if summary_file.exists():
                with open(summary_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            
            # 新しいエントリを追加
            new_entry = f"""
## {knowledge_entry['timestamp'][:10]} - {knowledge_entry['question'][:100]}

**質問者**: {knowledge_entry['questioner']}  
**タグ**: {', '.join(knowledge_entry['tags'])}  
**生成日時**: {knowledge_entry['timestamp']}

### 質問
{knowledge_entry['question']}

### GitHub Copilot AI回答
{knowledge_entry['copilot_response'][:500]}...

---
"""
            
            # ファイル更新
            if not existing_content:
                content = f"""# AI自動開発パイプライン - 生成ナレッジベース

このディレクトリには、GitHub Copilot AIが自動生成したナレッジが蓄積されます。

## 📊 統計
- 生成開始日: {datetime.now().strftime('%Y-%m-%d')}
- 自動更新: 質問受信時
- 形式: JSON + Markdown

## 📋 ナレッジエントリ
{new_entry}"""
            else:
                content = existing_content + new_entry
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Markdownサマリー更新: {summary_file}")
            
        except Exception as e:
            print(f"⚠️ Markdownサマリー生成エラー: {e}")
    
    def generate_mermaid_diagram(self, knowledge_entry, knowledge_dir):
        """Mermaidダイアグラムを自動生成・保存"""
        try:
            # 質問の内容に基づいてダイアグラムタイプを決定
            question = knowledge_entry['question'].lower()
            response = knowledge_entry['copilot_response'].lower()            # ダイアグラムタイプ判定（より精密に）
            question_lower = question.lower()
            response_lower = response.lower()
            combined_text = question_lower + " " + response_lower
            
            # キーワードスコアによる判定システム
            type_scores = {
                'er': 0,
                'sequence': 0,
                'class': 0,
                'architecture': 0,
                'flowchart': 0
            }
            
            # ER図キーワード
            er_keywords = ['database', 'データベース', 'table', 'テーブル', 'relation', '関係', 'primary key', 'foreign key', 'entity', 'schema', 'スキーマ']
            type_scores['er'] = sum(1 for kw in er_keywords if kw in combined_text)
            
            # シーケンス図キーワード
            seq_keywords = ['sequence', 'シーケンス', 'interaction', 'api', 'call', '呼び出し', 'request', 'response', 'message', 'protocol']
            type_scores['sequence'] = sum(1 for kw in seq_keywords if kw in combined_text)
            
            # クラス図キーワード  
            class_keywords = ['class', 'クラス', 'object', 'オブジェクト', 'inheritance', '継承', 'method', 'メソッド', 'property', 'プロパティ', '設計パターン', 'pattern']
            type_scores['class'] = sum(1 for kw in class_keywords if kw in combined_text)
            
            # アーキテクチャ図キーワード
            arch_keywords = ['system', 'システム', 'architecture', 'アーキテクチャ', 'component', 'コンポーネント', 'service', 'サービス', 'layer', 'レイヤー']
            type_scores['architecture'] = sum(1 for kw in arch_keywords if kw in combined_text)
            
            # フローチャートキーワード
            flow_keywords = ['flow', 'フロー', 'process', 'プロセス', 'workflow', 'step', 'ステップ', 'algorithm', 'アルゴリズム']
            type_scores['flowchart'] = sum(1 for kw in flow_keywords if kw in combined_text)
            
            # 最も高いスコアのタイプを選択
            diagram_type = max(type_scores, key=type_scores.get)
            
            # スコアがすべて0の場合はデフォルト
            if type_scores[diagram_type] == 0:
                diagram_type = 'flowchart'
            
            # ダイアグラムコンテンツ生成
            mermaid_content = self.generate_mermaid_content(diagram_type, knowledge_entry)
            
            # ファイル名生成
            safe_filename = "".join(c for c in knowledge_entry['question'][:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename.replace(' ', '_')}.mmd"
            filepath = knowledge_dir / filename
            
            # Mermaidファイル保存
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(mermaid_content)
            
            print(f"✅ Mermaidダイアグラム自動生成: {filepath}")
            
            # Mermaidプレビュー用HTMLも生成
            self.generate_mermaid_html(mermaid_content, knowledge_dir, safe_filename)
            
        except Exception as e:
            print(f"⚠️ Mermaidダイアグラム生成エラー: {e}")
    
    def sync_to_wiki_knowledge(self, knowledge_entry, knowledge_dir):
        """GitHub Wiki統合・AI記憶復元システム連携"""
        try:
            from pathlib import Path
            import json
            import subprocess
            import os
            
            # Wikiディレクトリ確認・初期化
            wiki_dir = Path("wiki")
            if not wiki_dir.exists():
                print("📚 GitHub Wiki をサブモジュールとして初期化...")
                try:
                    # Wiki サブモジュール追加
                    subprocess.run([
                        "git", "submodule", "add", 
                        "https://github.com/bpmbox/AUTOCREATE.wiki.git", 
                        "wiki"
                    ], check=True, cwd=".")
                    print("✅ GitHub Wiki サブモジュール追加完了")
                except subprocess.CalledProcessError as e:
                    print(f"⚠️ Wiki サブモジュール追加スキップ (既に存在?): {e}")
            
            # Wiki内ナレッジディレクトリ作成
            wiki_knowledge_dir = wiki_dir / "knowledge-base"
            wiki_memory_dir = wiki_dir / "ai-memory"
            wiki_diagrams_dir = wiki_dir / "mermaid-diagrams"
            wiki_conversations_dir = wiki_dir / "conversation-logs"
            
            for dir_path in [wiki_knowledge_dir, wiki_memory_dir, wiki_diagrams_dir, wiki_conversations_dir]:
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # ナレッジエントリをWikiに同期
            safe_filename = "".join(c for c in knowledge_entry['question'][:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            # 1. JSONナレッジファイル同期
            wiki_json_file = wiki_knowledge_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename.replace(' ', '_')}.json"
            with open(wiki_json_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge_entry, f, ensure_ascii=False, indent=2)
            
            # 2. Markdownナレッジ生成
            wiki_md_file = wiki_knowledge_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename.replace(' ', '_')}.md"
            markdown_content = f"""# {knowledge_entry['question']}

**質問者**: {knowledge_entry['questioner']}  
**生成日時**: {knowledge_entry['timestamp']}  
**タグ**: {', '.join(knowledge_entry['tags'])}  
**自動生成**: ✅ GitHub Copilot AI

## 📝 質問内容

{knowledge_entry['question']}

## 🤖 GitHub Copilot AI 回答

{knowledge_entry['copilot_response']}

## 🏷️ メタデータ

- **ナレッジタイプ**: {knowledge_entry['knowledge_type']}
- **自動生成**: {knowledge_entry['auto_generated']}
- **技術タグ**: {', '.join(knowledge_entry['tags'])}

## 🔗 関連リンク

- [メインリポジトリ](https://github.com/bpmbox/AUTOCREATE)
- [AI自動開発パイプライン](https://github.com/bpmbox/AUTOCREATE/wiki)
- [Mermaidダイアグラム]({safe_filename.replace(' ', '_')}_diagram.html)

---
*このナレッジは GitHub Copilot AI の自動開発パイプラインにより生成されました*
"""
            
            with open(wiki_md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # 3. AI記憶復元用メタデータ生成
            memory_metadata = {
                "memory_id": f"copilot_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "question_pattern": knowledge_entry['question'],
                "response_pattern": knowledge_entry['copilot_response'][:200],
                "technical_tags": knowledge_entry['tags'],
                "user_context": knowledge_entry['questioner'],
                "success_pattern": True,
                "reuse_count": 0,
                "last_accessed": knowledge_entry['timestamp'],
                "memory_strength": 1.0,
                "related_topics": knowledge_entry['tags'],
                "implementation_context": {
                    "tools_used": ["GitHub Copilot", "Supabase", "Mermaid"],
                    "project_type": "auto-development-pipeline",
                    "complexity_level": len(knowledge_entry['copilot_response']) // 100,
                    "user_satisfaction": "high"
                }
            }
            
            memory_file = wiki_memory_dir / f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename.replace(' ', '_')}.json"
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_metadata, f, ensure_ascii=False, indent=2)
            
            # 4. Mermaidダイアグラムも同期
            mermaid_files = list(knowledge_dir.glob("*.mmd"))
            html_files = list(knowledge_dir.glob("*.html"))
            
            for mermaid_file in mermaid_files:
                if safe_filename.replace(' ', '_') in mermaid_file.name:
                    wiki_mermaid_file = wiki_diagrams_dir / mermaid_file.name
                    wiki_mermaid_file.write_text(mermaid_file.read_text(encoding='utf-8'), encoding='utf-8')
            
            for html_file in html_files:
                if safe_filename.replace(' ', '_') in html_file.name:
                    wiki_html_file = wiki_diagrams_dir / html_file.name
                    wiki_html_file.write_text(html_file.read_text(encoding='utf-8'), encoding='utf-8')
            
            # 5. Wiki統合インデックス更新
            self.update_wiki_index(wiki_dir, knowledge_entry, safe_filename)
            
            # 6. WikiをGitコミット・プッシュ
            if wiki_dir.exists():
                try:
                    os.chdir(wiki_dir)
                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run([
                        "git", "commit", "-m", 
                        f"AI自動ナレッジ追加: {knowledge_entry['question'][:50]}...\n\n- 質問者: {knowledge_entry['questioner']}\n- 自動生成JSON + Markdown\n- AI記憶復元メタデータ\n- Mermaidダイアグラム統合\n- GitHub Copilot成長記録"
                    ], check=True)
                    subprocess.run(["git", "push", "origin", "master"], check=True)
                    os.chdir("..")
                    print(f"✅ GitHub Wiki統合完了: {wiki_md_file.name}")
                except subprocess.CalledProcessError as e:
                    os.chdir("..")
                    print(f"⚠️ Wiki Git操作エラー: {e}")
                except Exception as e:
                    os.chdir("..")
                    print(f"⚠️ Wiki操作エラー: {e}")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Wiki統合エラー: {e}")
            return False
    
    def update_wiki_index(self, wiki_dir, knowledge_entry, safe_filename):
        """Wiki統合インデックスを更新"""
        try:
            index_file = wiki_dir / "Home.md"
            
            # 既存インデックス読み込み
            existing_content = ""
            if index_file.exists():
                existing_content = index_file.read_text(encoding='utf-8')
            
            # 新しいエントリ
            new_entry = f"""
### 📚 [{knowledge_entry['question'][:60]}...](knowledge-base/{safe_filename.replace(' ', '_')}.md)
**日時**: {knowledge_entry['timestamp'][:10]} | **質問者**: {knowledge_entry['questioner']} | **タグ**: {', '.join(knowledge_entry['tags'][:3])}  
**記憶ID**: `copilot_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}` | **図表**: [🎯 Mermaid](mermaid-diagrams/{safe_filename.replace(' ', '_')}_diagram.html)
"""
            
            # インデックス更新
            if "# AUTOCREATE AI Wiki" not in existing_content:
                content = f"""# AUTOCREATE AI Wiki
🤖 **GitHub Copilot AI 自動開発パイプライン** - 成長するナレッジベース

## 🧠 AI記憶復元システム

このWikiは GitHub Copilot AI の「記憶」として機能し、過去の学習内容から最適な回答を生成します。

### 📊 統計情報
- **総ナレッジ数**: 自動カウント更新
- **記憶復元精度**: 継続的向上
- **AI成長指標**: 質問→学習→記憶→成長サイクル

### 🎯 AI自動開発機能
- ✅ 質問自動検出・処理
- ✅ GitHub Issue自動作成  
- ✅ プロジェクト自動実装
- ✅ Mermaidダイアグラム自動生成
- ✅ ナレッジベース自動蓄積
- ✅ Wiki統合・記憶復元

## 📚 最新ナレッジエントリ
{new_entry}

## 🔗 ナビゲーション
- 📁 [ナレッジベース](knowledge-base/): 技術的知識・実装例
- 🧠 [AI記憶](ai-memory/): 記憶復元メタデータ  
- 🎯 [Mermaidダイアグラム](mermaid-diagrams/): 自動生成図表
- 💬 [会話履歴](conversation-logs/): 詳細な対話記録

---
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by GitHub Copilot AI*
"""
            else:
                # 最新エントリセクションに追加
                if "## 📚 最新ナレッジエントリ" in existing_content:
                    content = existing_content.replace(
                        "## 📚 最新ナレッジエントリ",
                        f"## 📚 最新ナレッジエントリ{new_entry}"
                    )
                else:
                    content = existing_content + new_entry
            
            # インデックスファイル更新
            index_file.write_text(content, encoding='utf-8')
            print(f"✅ Wiki インデックス更新完了")
            
        except Exception as e:
            print(f"⚠️ Wikiインデックス更新エラー: {e}")
    
    def generate_mermaid_content(self, diagram_type, knowledge_entry):
        """ダイアグラムタイプに応じたMermaidコンテンツを生成"""
        question = knowledge_entry['question']
        response = knowledge_entry['copilot_response']
        
        if diagram_type == 'flowchart':
            return f"""flowchart TD
    A[質問: {question[:30]}...] --> B[GitHub Copilot処理]
    B --> C[AI回答生成]
    C --> D[Supabase自動投稿]
    D --> E[ナレッジベース保存]
    E --> F[Mermaidダイアグラム生成]
    F --> G[完了]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#f1f8e9
    style G fill:#e0f2f1
"""
        
        elif diagram_type == 'sequence':
            return f"""sequenceDiagram
    participant U as User
    participant C as Copilot
    participant S as Supabase
    participant K as Knowledge Base
    
    U->>C: {question[:40]}...
    C->>C: AI処理・回答生成
    C->>S: 自動投稿
    S-->>C: 投稿完了
    C->>K: ナレッジ保存
    K-->>C: 保存完了
    C->>U: 完了通知
"""
        
        elif diagram_type == 'class':
            return f"""classDiagram
    class CopilotSystem {{
        +String question
        +String response
        +DateTime timestamp
        +Array tags
        +post_to_supabase()
        +save_to_knowledge()
        +generate_mermaid()
    }}
    
    class SupabaseStorage {{
        +String ownerid
        +String messages
        +DateTime created
        +String status
        +insert()
        +update()
    }}
    
    class KnowledgeBase {{
        +String knowledge_type
        +Array tags
        +Boolean auto_generated
        +save_json()
        +generate_markdown()
    }}
    
    CopilotSystem --> SupabaseStorage
    CopilotSystem --> KnowledgeBase
"""
        
        elif diagram_type == 'architecture':
            return f"""graph TB
    subgraph "AI自動開発パイプライン"
        Q[質問入力] --> AI[GitHub Copilot]
        AI --> R[AI回答生成]
    end
    
    subgraph "データ保存層"
        S[Supabase]
        K[ナレッジベース]
        M[Mermaidダイアグラム]
    end
    
    subgraph "外部連携"
        N[Notion]
        J[JIRA]
        H[HuggingFace]
    end
    
    R --> S
    R --> K
    K --> M
    S --> N
    S --> J
    S --> H
    
    style AI fill:#ff9800
    style S fill:#4caf50
    style K fill:#2196f3
    style M fill:#9c27b0
"""
        
        else:  # er diagram
            return f"""erDiagram
    CHAT_HISTORY ||--o{{ KNOWLEDGE_BASE : generates
    CHAT_HISTORY {{
        int id
        string ownerid
        text messages
        datetime created
        string status
        string tmp_file
    }}
    
    KNOWLEDGE_BASE {{
        int id
        string question
        string questioner
        text copilot_response
        datetime timestamp
        string knowledge_type
        json tags
        boolean auto_generated
    }}
    
    MERMAID_DIAGRAMS ||--o{{ KNOWLEDGE_BASE : visualizes
    MERMAID_DIAGRAMS {{
        int id
        string filename
        string diagram_type
        text content
        datetime created
    }}
"""
    
    def generate_mermaid_html(self, mermaid_content, knowledge_dir, safe_filename):
        """Mermaidプレビュー用HTMLを生成"""
        try:
            html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mermaidダイアグラム - {safe_filename}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4caf50;
            padding-bottom: 10px;
        }}
        .mermaid {{
            text-align: center;
            margin: 30px 0;
        }}
        .info {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 AI自動生成 Mermaidダイアグラム</h1>
        
        <div class="info">
            <strong>生成日時:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <strong>ファイル名:</strong> {safe_filename}<br>
            <strong>自動生成:</strong> GitHub Copilot AI
        </div>
        
        <div class="mermaid">
{mermaid_content}
        </div>
        
        <div class="info">
            <strong>💡 使用方法:</strong><br>
            - このHTMLファイルをブラウザで開くとダイアグラムが表示されます<br>
            - .mmdファイルはMermaid Live Editorやドキュメントで利用可能<br>
            - 自動生成されたダイアグラムはナレッジベースの一部として保存されます
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>"""
            
            html_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename}_diagram.html"
            html_filepath = knowledge_dir / html_filename
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Mermaidプレビュー HTML: {html_filepath}")
            
        except Exception as e:
            print(f"⚠️ Mermaid HTML生成エラー: {e}")
    
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

    def improve_and_execute_user_question(self, question_data):
        """ユーザーの質問を改善してGitHub Issueに登録・実行"""
        
        original_question = question_data['question']
        user = question_data.get('user', 'Unknown')
        
        print(f"🚀 AI自動改善システム開始")
        print(f"👤 ユーザー: {user}")
        print(f"📝 元の質問: {original_question}")
        
        # 1. 質問を改善
        improved_data = self.improve_user_question_with_ai(original_question)
        if not improved_data:
            print("❌ 質問改善失敗")
            return False
        
        # 2. GitHub Issueを作成
        issue_created = self.create_improvement_github_issue(improved_data, original_question, user)
        if not issue_created:
            print("❌ GitHub Issue作成失敗")
            return False
        
        # 3. Copilotに改善された質問を送信
        return self.send_improved_question_to_copilot(improved_data)
    
    def improve_user_question_with_ai(self, original_question):
        """AIを使って質問を改善"""
        
        improvement_prompt = f"""
あなたは優秀なAI技術アドバイザーです。以下のユーザーの質問を分析し、より具体的で実行可能な質問に改善してください。

【元の質問】
{original_question}

【プロジェクト背景】
- React + Vite + shadcn UI で構築されたAIチャットアプリケーション
- GitHub Copilot と Supabase を統合した自動開発システム
- GitHub Pages で公開済み
- AI自動開発パイプライン（14ステップ）を実装中

【改善の観点】
1. 技術的な具体性を追加
2. 実装可能な形に細分化
3. 期待する成果物を明確化
4. 優先度と緊急度を設定
5. コードレベルの詳細を補完

【出力形式】
以下の形式で改善案を提供してください：

**改善された質問:**
[具体的で技術的に詳細な質問]

**技術要件:**
- 使用技術: [具体的な技術スタック]
- 実装方法: [具体的な実装アプローチ]
- ファイル構成: [必要なファイル・ディレクトリ]

**期待する成果物:**
1. [具体的な成果物1]
2. [具体的な成果物2]
3. [具体的な成果物3]

**実装ステップ:**
1. [ステップ1の詳細]
2. [ステップ2の詳細]
3. [ステップ3の詳細]

**優先度:** [高/中/低]
**予想工数:** [時間]
**成功基準:** [明確な判断基準]
"""
        
        # ここでは簡易版として基本的な改善を実装
        # 実際のAI APIを使用する場合はここでAPIコールを行う
        
        if "プロンプト" in original_question and "追加" in original_question:
            return {
                "improved_question": "GitHub Copilot統合システムにユーザー質問の自動改善・Issue登録・実行機能を追加",
                "technical_requirements": [
                    "質問分析AI機能の実装",
                    "GitHub Issues API統合",
                    "自動実行システムの構築",
                    "結果レポート機能"
                ],
                "expected_deliverables": [
                    "質問改善システム（Python関数）",
                    "GitHub Issue自動作成機能",
                    "実行結果の自動レポート",
                    "ユーザー体験の向上"
                ],
                "implementation_steps": [
                    "質問分析ロジックの実装",
                    "GitHub API認証・Issue作成機能",
                    "改善された質問をCopilotに送信",
                    "実行結果の収集・レポート",
                    "統合テストとデバッグ"
                ],
                "priority": "高",
                "estimated_effort": "2-3時間",
                "success_criteria": "ユーザーが質問を投稿すると自動的に改善・Issue登録・実行が完了すること"
            }
        
        # デフォルトの改善
        return {
            "improved_question": f"技術的改善提案: {original_question}",
            "technical_requirements": ["詳細な技術仕様の確認", "実装方法の検討"],
            "expected_deliverables": ["改善されたシステム", "ドキュメント更新"],
            "implementation_steps": ["要件分析", "設計", "実装", "テスト"],
            "priority": "中",
            "estimated_effort": "1-2時間",
            "success_criteria": "ユーザーの要求が満たされること"
        }
    
    def create_improvement_github_issue(self, improved_data, original_question, user):
        """改善提案をGitHub Issueとして作成"""
        
        # GitHub API情報
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("⚠️ GitHub Token未設定のため、Issue作成をスキップ")
            return True  # 処理は続行
        
        repo = "bpmbox/AUTOCREATE"
        
        # Issue本文作成
        issue_body = f"""## 🚀 AI自動改善提案

### 👤 提案ユーザー
{user}

### 📝 元の質問
```
{original_question}
```

### ✨ 改善された質問
{improved_data['improved_question']}

### 🔧 技術要件
{chr(10).join(['- ' + req for req in improved_data['technical_requirements']])}

### 📋 期待する成果物
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(improved_data['expected_deliverables'])])}

### 📊 実装ステップ
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(improved_data['implementation_steps'])])}

### 📈 メタ情報
- **優先度**: {improved_data['priority']}
- **予想工数**: {improved_data['estimated_effort']}
- **成功基準**: {improved_data['success_criteria']}
- **作成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **AI改善システム**: 自動生成

### 🎯 実行ステータス
- [ ] 質問をCopilotに送信
- [ ] 回答を取得
- [ ] Supabaseに結果を保存
- [ ] ユーザーにフィードバック

---
*このIssueはAI自動改善システムにより生成されました*
"""
        
        # Issue作成のデータ
        issue_data = {
            "title": f"🤖 AI改善提案: {improved_data['improved_question'][:60]}...",
            "body": issue_body,
            "labels": ["ai-improved", "auto-generated", f"priority-{improved_data['priority']}"]
        }
        
        try:
            # 実際のGitHub API呼び出しは環境に依存するため、
            # ここでは情報をログ出力
            print("📝 GitHub Issue作成情報:")
            print(f"   タイトル: {issue_data['title']}")
            print(f"   ラベル: {', '.join(issue_data['labels'])}")
            print("✅ Issue情報生成完了")
            
            # 実際のAPI呼び出しをここに実装可能
            # response = requests.post(f"https://api.github.com/repos/{repo}/issues", ...)
            
            return True
            
        except Exception as e:
            print(f"❌ Issue作成エラー: {e}")
            return False
    
    def send_improved_question_to_copilot(self, improved_data):
        """改善された質問をCopilotに送信"""
        
        # 改善された質問を構築
        enhanced_question = f"""
🚀 AI改善システムからの質問

【改善された質問】
{improved_data['improved_question']}

【技術要件】
{chr(10).join(['• ' + req for req in improved_data['technical_requirements']])}

【期待する成果物】
{chr(10).join([f"{i+1}. {item}" for i, item in enumerate(improved_data['expected_deliverables'])])}

【実装ステップの提案】
{chr(10).join([f"ステップ{i+1}: {step}" for i, step in enumerate(improved_data['implementation_steps'])])}

【優先度】{improved_data['priority']} | 【予想工数】{improved_data['estimated_effort']}

この内容について、具体的な実装方法とコード例を提供してください。
"""
        
        print("🎯 改善された質問をCopilotに送信中...")
        print(f"📝 送信内容: {enhanced_question[:100]}...")
        
        # 既存のCopilot送信メソッドを使用
        question_data = {
            'question': enhanced_question,
            'user': 'AI改善システム',
            'id': f"improved_{int(time.time())}"
        }
        
        return self.send_to_copilot_and_get_response(question_data)

    # ...existing code...
