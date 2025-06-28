#!/usr/bin/env python3
"""
🚀 GitHub Copilot完全自動化システム (GitHub CLI対応版) - サブモジュール分離型
Supabase監視 → VS Code Chat → GitHub Copilot → Issue作成 → 実装 → 完了報告

機能:
- Supabaseのchat_historyを監視
- 新しい質問をVS Code Chatに投稿
- GitHub CopilotにGitHub CLI含む詳細なプロンプトを送信
- 動的Mermaid図生成・可視化
- 新リポジトリ作成→サブモジュール追加→完全分離開発
- ホットリロード対応
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

import pyautogui
import pyperclip
from supabase import create_client

# .envファイルを読み込み
load_dotenv()

# 設定
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

class GitHubCopilotAutomation:
    def __init__(self, offline_mode=False):
        # .envファイルから設定を読み込み
        print("🔧 .envファイルから設定を読み込み中...")
        
        # 環境変数取得
        supabase_url = os.getenv('SUPABASE_URL', 'https://tnojlywkucnzgakwrgep.supabase.co')
        supabase_key = os.getenv('SUPABASE_KEY', 'ENV_SUPABASE_KEY_PLACEHOLDER')
        github_token = os.getenv('GITHUB_TOKEN', '')
        self.debug_mode = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
        
        # デバッグ情報表示
        if self.debug_mode:
            print(f"📋 Supabase URL: {supabase_url}")
            print(f"📋 Supabase Key: {supabase_key[:10]}..." if len(supabase_key) > 10 else f"📋 Supabase Key: {supabase_key}")
            print(f"📋 GitHub Token: {'設定済み' if github_token else '未設定'}")
        
        # オフラインモード設定
        self.offline_mode = offline_mode or os.getenv('OFFLINE_MODE', 'False').lower() == 'true'
        
        if not self.offline_mode:
            try:
                self.supabase = create_client(supabase_url, supabase_key)
                print("📊 Supabase接続完了")
            except Exception as e:
                print(f"⚠️ Supabase接続エラー: {e}")
                if supabase_key == 'ENV_SUPABASE_KEY_PLACEHOLDER':
                    print("💡 .envファイルでSUPABASE_KEYを設定してください")
                print("🔄 オフラインモードに切り替えます")
                self.offline_mode = True
                self.supabase = None
        else:
            self.supabase = None
            print("🔧 オフラインモードで起動")
        
        # チャット座標管理（.envから取得）
        self.coordinates_file = "chat_coordinates.json"
        self.chat_coordinates = self.load_coordinates()
        
        # .envから座標を取得（ファイルがない場合）
        if not self.chat_coordinates:
            default_x = int(os.getenv('CHAT_COORDINATE_X', '1335'))
            default_y = int(os.getenv('CHAT_COORDINATE_Y', '1045'))
            self.chat_coordinates = {
                'x': default_x, 
                'y': default_y, 
                'timestamp': datetime.now().isoformat()
            }
            print(f"✅ .envから座標を設定: ({default_x}, {default_y})")
        
        print("🤖 GitHub Copilot完全自動化システム (サブモジュール分離型) 起動")
        if not self.offline_mode:
            print("📊 Supabase接続完了")
        print("🎨 動的Mermaid図生成対応")
        print("📦 サブモジュール分離開発対応")
        print("⚡ ホットリロード対応")

    def load_coordinates(self):
        """保存されたチャット座標を読み込み"""
        try:
            if os.path.exists(self.coordinates_file):
                with open(self.coordinates_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ 座標ファイル読み込みエラー: {e}")
        return None

    def generate_dynamic_mermaid_diagram(self, question):
        """質問に応じた動的Mermaid図を生成"""
        
        # プロジェクト名を生成
        project_name = question.lower().replace(' ', '-').replace('　', '-').replace('?', '').replace('？', '')[:30]
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        # 基本フロー図
        base_flow = f"""graph TB
    START[🚀 {question[:20]}... 開発開始] --> SAVE[1️⃣ 作業保存・Push]
    SAVE --> NEWREPO[2️⃣ 新リポジトリ作成]
    NEWREPO --> SUBMOD[📦 サブモジュール追加]
    SUBMOD --> BRANCH[🌿 featureブランチ作成]
    BRANCH --> ANSWER[3️⃣ 詳細回答生成]
    ANSWER --> ISSUE[4️⃣ GitHub Issue作成]
    ISSUE --> FOLDER[5️⃣ プロジェクトフォルダ作成]
    FOLDER --> IMPLEMENT[6️⃣ プログラム実装]
    IMPLEMENT --> TEST[🧪 テスト実行]
    TEST --> COMMIT[7️⃣ Git操作・コミット]
    COMMIT --> REPORT[8️⃣ 完了報告Issue]
    REPORT --> SUPABASE[9️⃣ Supabase投稿]
    SUPABASE --> END[✅ 完了]
    
    SAVE --> S1[git add .]
    SAVE --> S2[git commit]
    SAVE --> S3[git push]
    
    NEWREPO --> N1[.envトークン使用]
    NEWREPO --> N2[gh repo create]
    NEWREPO --> N3[--private --clone]
    
    SUBMOD --> SM1[git submodule add]
    SUBMOD --> SM2[projects/{project_name}]
    SUBMOD --> SM3[メイン汚染回避]
    
    BRANCH --> B1[feature/implementation]
    BRANCH --> B2[{timestamp}]
    BRANCH --> B3[分離環境]
    
    IMPLEMENT --> I1[ソースコード]
    IMPLEMENT --> I2[テスト]
    IMPLEMENT --> I3[ドキュメント]
    
    TEST --> T1[単体テスト]
    TEST --> T2[統合テスト]
    TEST --> T3[動作確認]
    
    COMMIT --> C1[サブモジュール内]
    COMMIT --> C2[メイン参照更新]
    COMMIT --> C3[完全分離管理]
    
    style START fill:#e3f2fd
    style SAVE fill:#fff3e0
    style NEWREPO fill:#f3e5f5
    style SUBMOD fill:#e8f5e8
    style BRANCH fill:#fff8e1
    style IMPLEMENT fill:#e8f5e8
    style TEST fill:#fff3e0
    style END fill:#f1f8e9
    style N1 fill:#ffebee
    style SM1 fill:#e8f5e8
    style C1 fill:#e3f2fd"""
        
        # 質問のタイプに応じて特化部分を追加
        specialized_part = ""
        if any(keyword in question.lower() for keyword in ['api', 'rest', 'graphql']):
            specialized_part = """
    IMPLEMENT --> API1[API設計]
    IMPLEMENT --> API2[エンドポイント]
    IMPLEMENT --> API3[認証・認可]
    
    style API1 fill:#e1f5fe
    style API2 fill:#e1f5fe
    style API3 fill:#e1f5fe"""
        elif any(keyword in question.lower() for keyword in ['ui', 'frontend', 'react', 'vue']):
            specialized_part = """
    IMPLEMENT --> UI1[コンポーネント設計]
    IMPLEMENT --> UI2[状態管理]
    IMPLEMENT --> UI3[レスポンシブ対応]
    
    style UI1 fill:#f3e5f5
    style UI2 fill:#f3e5f5
    style UI3 fill:#f3e5f5"""
        elif any(keyword in question.lower() for keyword in ['database', 'db', 'sql']):
            specialized_part = """
    IMPLEMENT --> DB1[テーブル設計]
    IMPLEMENT --> DB2[マイグレーション]
    IMPLEMENT --> DB3[インデックス最適化]
    
    style DB1 fill:#fff8e1
    style DB2 fill:#fff8e1
    style DB3 fill:#fff8e1"""
        
        return base_flow + specialized_part
    
    def save_mermaid_to_file(self, mermaid_code, filename=None):
        """Mermaid図をファイルに保存"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"auto_dev_flow_{timestamp}.mermaid"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)
            print(f"📁 Mermaid図をファイルに保存: {filename}")
            return filename
        except Exception as e:
            print(f"⚠️ Mermaidファイル保存エラー: {e}")
            return None

    def send_to_copilot_and_get_response(self, question_data):
        """VS CodeチャットでCopilotに質問を送信し、回答をSupabaseに投稿"""
        if not self.chat_coordinates:
            print("❌ チャット座標が未設定")
            return False
        
        try:
            question = question_data['question'] if 'question' in question_data else question_data['messages']
            user = question_data.get('ownerid', 'unknown')
            
            # 動的Mermaid図を生成
            dynamic_mermaid = self.generate_dynamic_mermaid_diagram(question)
            mermaid_file = self.save_mermaid_to_file(dynamic_mermaid)
            
            # プロジェクト名を生成
            project_name = question.lower().replace(' ', '-').replace('　', '-').replace('?', '').replace('？', '')[:30]
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            
            # GitHub Copilotに分かりやすい質問形式に変換（サブモジュール分離型 + 動的Mermaid図付き）
            formatted_question = f"""📋 ユーザーからの質問

質問者: {user}
質問: {question}

🎨 **自動生成フロー図（Mermaid）**:
```mermaid
{dynamic_mermaid}
```

🚀 **GitHub Copilot完全自動開発フロー実行をお願いします**：

1️⃣ **現在の作業保存とpush**: 
   📋 実行前に現在の作業を安全に保存:
   ```bash
   git add .
   git commit -m "🔄 自動開発実行前の作業保存 - {question}"
   git push
   ```

2️⃣ **新しいリポジトリ・サブモジュール作成**: 
   📋 完全分離された開発環境を準備:
   
   **新リポジトリ作成** (.envのGitHubトークン使用):
   ```bash
   gh repo create "bpmbox/{project_name}-project" --private --clone
   ```
   
   **サブモジュールとして追加** (メインリポジトリを汚さない):
   ```bash
   git submodule add https://github.com/bpmbox/{project_name}-project.git projects/{project_name}-project
   git submodule update --init --recursive
   ```
   
   **作業ブランチ作成**:
   ```bash
   cd projects/{project_name}-project
   git checkout -b "feature/implementation-{timestamp}"
   ```

3️⃣ **詳細な回答生成**: この質問に対して実用的で具体的な回答を作成

4️⃣ **GitHub Issue作成**: 
   📋 GitHub CLIコマンド実行（動的Mermaid図付き）:
   
   ```bash
   gh issue create --repo "bpmbox/AUTOCREATE" --title "🎯 {question} - 実装要求" --body "
## 📊 実装フロー

\\`\\`\\`mermaid
{dynamic_mermaid}
\\`\\`\\`

## 🎯 実装詳細
**質問**: {question}
**リポジトリ**: bpmbox/{project_name}-project
**ブランチ**: feature/implementation-{timestamp}
**サブモジュールパス**: projects/{project_name}-project
**実行時刻**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Mermaidファイル**: {mermaid_file}
" --label "ai-automation,implementation"
   ```

5️⃣ **プロジェクトフォルダー作成**:
   - プロジェクトパス: projects/{project_name}-project/
   - 必要なファイル構成を自動生成
   - README.md、実装ファイル、設定ファイル等
   - サブモジュール内での完全な開発環境

6️⃣ **プログラム自動実装**:
   - 要求された機能を完全実装
   - テストコード作成
   - ドキュメント生成
   - 完全動作確認

7️⃣ **Git操作とコミット**:
   📋 サブモジュール内でのGit操作:
   ```bash
   cd projects/{project_name}-project
   git add .
   git commit -m "🎯 {question} - 完全実装完了"
   git push origin feature/implementation-{timestamp}
   ```
   
   📋 メインリポジトリでのサブモジュール更新:
   ```bash
   cd ../..
   git add projects/{project_name}-project
   git commit -m "📦 サブモジュール追加: {question} プロジェクト"
   git push
   ```

8️⃣ **GitHub Issue完了報告**:
   📋 完了時のGitHub CLIコマンド（結果Mermaid図付き）:
   ```bash
   gh issue create --repo "bpmbox/AUTOCREATE" --title "✅ {question} - 完全実装完了" --body "
## 🎉 実装完了レポート

\\`\\`\\`mermaid
graph LR
    START[🚀 開始] --> IMPL[⚙️ 実装]
    IMPL --> TEST[✅ テスト]
    TEST --> DOC[📚 ドキュメント]
    DOC --> COMPLETE[🎯 完了]
    
    style START fill:#e3f2fd
    style COMPLETE fill:#e8f5e8
\\`\\`\\`

**実装結果**:
- リポジトリ: https://github.com/bpmbox/{project_name}-project
- ブランチ: feature/implementation-{timestamp}
- サブモジュールパス: projects/{project_name}-project
- 完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Mermaidファイル: {mermaid_file}
" --label "ai-automation,completed"
   ```

9️⃣ **Supabase投稿**: 
   - ownerid: 'GitHub-Copilot-AI'
   - messages: 回答内容 + GitHub Issue URL + 実装結果詳細 + リポジトリURL + サブモジュールパス
   - created: 現在時刻

🔥 **重要なガイド**:
- 🚨 実行前push: 必ず現在の作業を保存してから開始
- 🏗️ 新リポジトリ作成: .envのGitHubトークンを使用
- 📦 サブモジュール管理: メインリポジトリを汚さない分離構造
- 🌿 ブランチ戦略: feature/implementation-{timestamp}
- 📊 Mermaid可視化: Issue内でフローを視覚的に表示
- 📁 ファイル保存: {mermaid_file} として図を保存
- GitHub CLI認証: gh auth status で確認
- 文字化け対策: UTF-8設定必須
- ラベル: "ai-automation" 必須使用
- リポジトリ: bpmbox/AUTOCREATE 固定（レポート用）

🤖 **このシステムは完全自動開発パイプライン（サブモジュール分離型）です。全9ステップを実行してください！**"""
            
            print(f"📤 Copilotチャットに質問送信中...")
            print(f"質問: {question}")
            print(f"🎨 動的Mermaid図: {mermaid_file}")
            print(f"📦 プロジェクト名: {project_name}-project")
            
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
            
            print("📝 質問入力完了")
            
            # 自動送信
            print("🚀 Copilotに送信中...")
            pyautogui.press('enter')
            time.sleep(3)  # Copilotの回答生成を待機
            
            print("✅ 質問送信完了")
            print("💡 GitHub Copilotが完全自動開発フローを実行中...")
            print("🎨 Mermaid図付きIssue作成 → GitHub Copilotが実行")
            print("📦 サブモジュール分離型開発 → GitHub Copilotが実行")
            print("🚀 9ステップ完全自動化 → GitHub Copilotが実行")
            print("\n� 次はGitHub Copilotがプロンプト内の指示に従って:")
            print("  1️⃣ GitHub Issue作成")
            print("  2️⃣ 新リポジトリ作成")
            print("  3️⃣ サブモジュール追加")
            print("  4️⃣ 実装・テスト・コミット")
            print("  5️⃣ 完了報告Issue作成")
            print("  6️⃣ Supabase投稿")
            
            return True
                
        except Exception as e:
            print(f"❌ チャット送信エラー: {e}")
            return False

    def infinite_auto_loop(self, interval=3):
        """無限自動ループモード（完全に手を離せる）+ ホットリロード"""
        if self.offline_mode:
            print("❌ オンラインモードでは無限自動ループは利用できません")
            print("� オンライン環境で実行してください")
            return False
            
        print("�🔥 無限自動ループモード開始!")
        print(f"⚡ {interval}秒間隔で永続監視")
        print("🤖 新着メッセージを完全自動で処理")
        print("📍 座標固定: (1335, 1045)")
        print("🚀 GitHub Copilotが自動回答")
        print("🎨 動的Mermaid図生成")
        print("📦 サブモジュール分離開発")
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
            if self.supabase:
                result = self.supabase.table('chat_history') \
                    .select('id') \
                    .order('id', desc=True) \
                    .limit(1) \
                    .execute()
                if result.data:
                    last_id = result.data[0]['id']
                    print(f"📊 監視開始ID: {last_id}")
                    processed_ids.add(last_id)  # 初期IDは処理済みとして追加
                else:
                    last_id = 0
                    print("📊 初期データなし - ID 0から開始")
            else:
                print("⚠️ Supabase接続がありません")
                return False
        except Exception as e:
            print(f"⚠️ 初期化エラー: {e}")
            print("🔄 ネットワーク問題により停止します")
            return False
        
        print("\n🎯 無限ループ開始 - Ctrl+C で停止")
        print("="*50)
        
        # ホットリロード用のファイル監視設定
        current_file = Path(__file__)
        last_modified = current_file.stat().st_mtime
        
        try:
            while True:  # 無限ループ
                # ホットリロード監視
                try:
                    current_modified = current_file.stat().st_mtime
                    if current_modified > last_modified:
                        print("\n🔄 ファイル変更検出 - 自動再起動中...")
                        print("🔄 新しいバージョンでシステム再起動します")
                        os.execv(sys.executable, ['python'] + sys.argv)
                        return
                    last_modified = current_modified
                except Exception as e:
                    print(f"⚠️ ホットリロード監視エラー: {e}")
                
                check_count += 1
                
                try:
                    # 新着メッセージを確認（最新のもの優先で取得）
                    result = self.supabase.table('chat_history') \
                        .select('*') \
                        .gt('id', last_id) \
                        .order('id', desc=True) \
                        .limit(10) \
                        .execute()
                    
                    if result.data:
                        # 新しいメッセージを古い順に処理（IDの昇順）
                        messages_to_process = sorted(result.data, key=lambda x: x['id'])
                        
                        for message in messages_to_process:
                            message_id = message['id']
                            message_content = message.get('messages', '').strip()
                            message_owner = message.get('ownerid', '')
                            
                            # 処理条件をチェック
                            should_process = (
                                message_id not in processed_ids and 
                                message_owner not in ['GitHub-Copilot-AI', 'ai-assistant', 'GitHub-Copilot-AI-System'] and
                                message_content and
                                len(message_content) > 5  # 最低5文字以上
                            )
                            
                            if should_process:
                                print(f"\n🚀 新着メッセージ検出! ID: {message_id}")
                                print(f"👤 ユーザー: {message_owner}")
                                print(f"📝 質問: {message_content[:100]}...")
                                print(f"� 作成時刻: {message.get('created', 'unknown')}")
                                
                                # 🚀 一気に実行フロー: チャット → Issue作成 → 他AI実行待ち
                                issue_url = self.create_comprehensive_issue_immediately(message)
                                
                                if issue_url:
                                    processed_ids.add(message_id)
                                    last_id = max(last_id, message_id)
                                    success_count += 1
                                    print(f"✅ 一気実行完了! 成功数: {success_count}")
                                    print(f"� Issue作成: {issue_url}")
                                    print(f"🤖 他のAIが実行可能な状態になりました")
                                    
                                    # 処理完了をSupabaseに記録
                                    try:
                                        self.supabase.table('chat_history').insert({
                                            'ownerid': 'GitHub-Copilot-AI-System',
                                            'messages': f"🎯 一気実行完了: Issue作成済み {issue_url} - {message_content[:50]}...",
                                            'created': datetime.now().isoformat()
                                        }).execute()
                                    except Exception as log_error:
                                        print(f"📝 ログ記録エラー: {log_error}")
                                        
                                else:
                                    print(f"⚠️ 自動処理失敗")
                                    processed_ids.add(message_id)
                                    last_id = max(last_id, message_id)
                            else:
                                # 処理をスキップした理由を記録
                                if message_id in processed_ids:
                                    reason = "処理済み"
                                elif message_owner in ['GitHub-Copilot-AI', 'ai-assistant', 'GitHub-Copilot-AI-System']:
                                    reason = f"AIメッセージ({message_owner})"
                                elif not message_content or len(message_content) <= 5:
                                    reason = "内容が短すぎる"
                                else:
                                    reason = "その他"
                                
                                print(f"⏭️ ID:{message_id} スキップ - {reason}")
                                processed_ids.add(message_id)
                                last_id = max(last_id, message_id)
                    
                    # ステータス表示（10回おき）
                    if check_count % 10 == 0:
                        print(f"🔍 監視継続中... チェック回数: {check_count}, 成功処理数: {success_count}, 現在時刻: {datetime.now().strftime('%H:%M:%S')}")
                        print(f"📊 現在の last_id: {last_id}, 処理済みID数: {len(processed_ids)}")
                        
                        # デバッグ: 最新の5件を表示
                        if self.debug_mode and check_count % 50 == 0:  # 50回おきに詳細表示
                            try:
                                debug_result = self.supabase.table('chat_history') \
                                    .select('id, ownerid, messages, created') \
                                    .order('id', desc=True) \
                                    .limit(5) \
                                    .execute()
                                
                                print("🔍 デバッグ: 最新5件のメッセージ:")
                                for debug_msg in debug_result.data:
                                    status = "処理済み" if debug_msg['id'] in processed_ids else "未処理"
                                    print(f"  ID:{debug_msg['id']} | {debug_msg.get('ownerid', 'unknown')[:15]} | {status} | {debug_msg.get('messages', '')[:30]}...")
                            except Exception as debug_error:
                                print(f"🔍 デバッグ表示エラー: {debug_error}")
                
                except Exception as e:
                    print(f"⚠️ メッセージ監視エラー: {e}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n🛑 無限ループ停止")
            print(f"📊 最終統計: チェック回数={check_count}, 成功処理数={success_count}")
            print("👋 システム終了")

    def local_test_mode(self):
        """ローカルテストモード - ネットワーク接続不要"""
        print("🧪 ローカルテストモード開始")
        print("📋 Supabase接続なしでテスト実行")
        print("="*50)
        
        # テスト用の質問データ
        test_questions = [
            "ReactとPythonでリアルタイムチャットシステムを作成してください",
            "PostgreSQLを使ったタスク管理APIを開発してください", 
            "Vue.jsでダッシュボード画面を作成してください",
            "機械学習を使った画像認識システムを作ってください",
            "Dockerを使ったマイクロサービス環境を構築してください"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 テスト {i}: {question}")
            
            # 動的Mermaid図を生成
            mermaid_diagram = self.generate_dynamic_mermaid_diagram(question)
            
            # ファイルに保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"local_test_{i}_{timestamp}.mermaid"
            saved_file = self.save_mermaid_to_file(mermaid_diagram, filename)
            
            # プロンプト生成テスト
            test_data = {
                'messages': question,
                'ownerid': 'test_user'
            }
            
            # プロンプト生成（送信はしない）
            prompt = self.generate_enhanced_prompt(test_data, test_mode=True)
            
            print(f"✅ テスト {i} 完了")
            print(f"📁 Mermaidファイル: {saved_file}")
            print(f"📋 プロンプト長: {len(prompt)} 文字")
            print(f"🎯 プロジェクト名: {question.lower().replace(' ', '-').replace('　', '-')[:30]}-project")
            print("-" * 30)
        
        print(f"\n🎉 全{len(test_questions)}件のローカルテスト完了!")
        
        # 生成されたファイル一覧を表示
        mermaid_files = [f for f in os.listdir('.') if f.startswith('local_test_') and f.endswith('.mermaid')]
        print("📁 生成されたファイル:")
        for file in sorted(mermaid_files):
            print(f"  - {file}")
        
        return True
    
    def generate_enhanced_prompt(self, question_data, test_mode=False):
        """拡張プロンプト生成（テストモード対応）"""
        question = question_data['question'] if 'question' in question_data else question_data['messages']
        user = question_data.get('ownerid', 'unknown')
        
        # 動的Mermaid図を生成
        dynamic_mermaid = self.generate_dynamic_mermaid_diagram(question)
        
        if not test_mode:
            mermaid_file = self.save_mermaid_to_file(dynamic_mermaid)
        else:
            mermaid_file = "test_mode_diagram.mermaid"
        
        # プロジェクト名を生成
        project_name = question.lower().replace(' ', '-').replace('　', '-').replace('?', '').replace('？', '')[:30]
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        enhanced_prompt = f"""📋 ユーザーからの質問

質問者: {user}
質問: {question}

🎨 **自動生成フロー図（Mermaid）**:
```mermaid
{dynamic_mermaid}
```

🚀 **GitHub Copilot完全自動開発フロー実行をお願いします**：

1️⃣ **現在の作業保存とpush**: 
   📋 実行前に現在の作業を安全に保存:
   ```bash
   git add .
   git commit -m "🔄 自動開発実行前の作業保存 - {question}"
   git push
   ```

2️⃣ **新しいリポジトリ・サブモジュール作成**: 
   📋 完全分離された開発環境を準備:
   
   **新リポジトリ作成** (.envのGitHubトークン使用):
   ```bash
   gh repo create "bpmbox/{project_name}-project" --private --clone
   ```
   
   **サブモジュールとして追加** (メインリポジトリを汚さない):
   ```bash
   git submodule add https://github.com/bpmbox/{project_name}-project.git projects/{project_name}-project
   git submodule update --init --recursive
   ```
   
   **作業ブランチ作成**:
   ```bash
   cd projects/{project_name}-project
   git checkout -b "feature/implementation-{timestamp}"
   ```

3️⃣ **詳細な回答生成**: この質問に対して実用的で具体的な回答を作成

4️⃣ **GitHub Issue作成**: 
   📋 GitHub CLIコマンド実行（動的Mermaid図付き）:
   
   ```bash
   gh issue create --repo "bpmbox/AUTOCREATE" --title "🎯 {question} - 実装要求" --body "
## 📊 実装フロー

\\`\\`\\`mermaid
{dynamic_mermaid}
\\`\\`\\`

## 🎯 実装詳細
**質問**: {question}
**リポジトリ**: bpmbox/{project_name}-project
**ブランチ**: feature/implementation-{timestamp}
**サブモジュールパス**: projects/{project_name}-project
**実行時刻**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Mermaidファイル**: {mermaid_file}
" --label "ai-automation,implementation"
   ```

5️⃣ **プロジェクトフォルダー作成**:
   - プロジェクトパス: projects/{project_name}-project/
   - 必要なファイル構成を自動生成
   - README.md、実装ファイル、設定ファイル等
   - サブモジュール内での完全な開発環境

6️⃣ **プログラム自動実装**:
   - 要求された機能を完全実装
   - テストコード作成
   - ドキュメント生成
   - 完全動作確認

7️⃣ **Git操作とコミット**:
   📋 サブモジュール内でのGit操作:
   ```bash
   cd projects/{project_name}-project
   git add .
   git commit -m "🎯 {question} - 完全実装完了"
   git push origin feature/implementation-{timestamp}
   ```
   
   📋 メインリポジトリでのサブモジュール更新:
   ```bash
   cd ../..
   git add projects/{project_name}-project
   git commit -m "📦 サブモジュール追加: {question} プロジェクト"
   git push
   ```

8️⃣ **GitHub Issue完了報告**:
   📋 完了時のGitHub CLIコマンド（結果Mermaid図付き）:
   ```bash
   gh issue create --repo "bpmbox/AUTOCREATE" --title "✅ {question} - 完全実装完了" --body "
## 🎉 実装完了レポート

\\`\\`\\`mermaid
graph LR
    START[🚀 開始] --> IMPL[⚙️ 実装]
    IMPL --> TEST[✅ テスト]
    TEST --> DOC[📚 ドキュメント]
    DOC --> COMPLETE[🎯 完了]
    
    style START fill:#e3f2fd
    style COMPLETE fill:#e8f5e8
\\`\\`\\`

**実装結果**:
- リポジトリ: https://github.com/bpmbox/{project_name}-project
- ブランチ: feature/implementation-{timestamp}
- サブモジュールパス: projects/{project_name}-project
- 完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Mermaidファイル: {mermaid_file}
" --label "ai-automation,completed"
   ```

9️⃣ **Supabase投稿**: 
   - ownerid: 'GitHub-Copilot-AI'
   - messages: 回答内容 + GitHub Issue URL + 実装結果詳細 + リポジトリURL + サブモジュールパス
   - created: 現在時刻

🔥 **重要なガイド**:
- 🚨 実行前push: 必ず現在の作業を保存してから開始
- 🏗️ 新リポジトリ作成: .envのGitHubトークンを使用
- 📦 サブモジュール管理: メインリポジトリを汚さない分離構造
- 🌿 ブランチ戦略: feature/implementation-{timestamp}
- 📊 Mermaid可視化: Issue内でフローを視覚的に表示
- 📁 ファイル保存: {mermaid_file} として図を保存
- GitHub CLI認証: gh auth status で確認
- 文字化け対策: UTF-8設定必須
- ラベル: "ai-automation" 必須使用
- リポジトリ: bpmbox/AUTOCREATE 固定（レポート用）

🤖 **このシステムは完全自動開発パイプライン（サブモジュール分離型）です。全9ステップを実行してください！**"""
        
        return enhanced_prompt

    def test_github_cli_integration(self):
        """GitHub CLI統合テスト"""
        print("🔧 GitHub CLI統合テスト開始")
        
        # GitHub CLI の認証状態確認
        try:
            result = os.system("gh auth status")
            if result == 0:
                print("✅ GitHub CLI認証済み")
            else:
                print("⚠️ GitHub CLI未認証 - gh auth login を実行してください")
        except Exception as e:
            print(f"❌ GitHub CLI確認エラー: {e}")
        
        # Git設定確認
        try:
            result = os.system("git config --global user.name")
            if result == 0:
                print("✅ Git設定済み")
            else:
                print("⚠️ Git設定未完了")
        except Exception as e:
            print(f"❌ Git確認エラー: {e}")
        
        return True

    def setup_github_environment(self):
        """GitHub環境のセットアップ"""
        github_token = os.getenv('GITHUB_TOKEN', '')
        
        if github_token and github_token != 'your_github_token_here':
            # GitHub CLIにトークンを設定
            try:
                os.environ['GITHUB_TOKEN'] = github_token
                print("✅ GitHub Token環境変数設定完了")
                return True
            except Exception as e:
                print(f"⚠️ GitHub Token設定エラー: {e}")
                return False
        else:
            print("⚠️ GitHub Tokenが設定されていません")
            print("💡 .envファイルでGITHUB_TOKENを設定してください")
            return False

    def create_new_repository(self, project_name):
        """新しいリポジトリを作成（.envのGitHubトークン使用）"""
        if not self.setup_github_environment():
            print("❌ GitHub環境設定が必要です")
            return False
            
        github_username = os.getenv('GITHUB_USERNAME', 'bpmbox')
        repo_name = f"{project_name}-project"
        
        print(f"🏗️ 新リポジトリ作成開始: {github_username}/{repo_name}")
        
        try:
            # GitHub CLIでリポジトリ作成
            import subprocess
            
            cmd = [
                'gh', 'repo', 'create', 
                f"{github_username}/{repo_name}", 
                '--private', 
                '--clone'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ リポジトリ作成成功: https://github.com/{github_username}/{repo_name}")
                return True
            else:
                print(f"❌ リポジトリ作成失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ リポジトリ作成エラー: {e}")
            return False

    def add_as_submodule(self, project_name):
        """プロジェクトをサブモジュールとして追加"""
        github_username = os.getenv('GITHUB_USERNAME', 'bpmbox')
        repo_name = f"{project_name}-project"
        repo_url = f"https://github.com/{github_username}/{repo_name}.git"
        submodule_path = f"projects/{repo_name}"
        
        print(f"📦 サブモジュール追加開始: {submodule_path}")
        
        try:
            import subprocess
            
            # プロジェクトディレクトリを作成
            os.makedirs("projects", exist_ok=True)
            
            # サブモジュール追加コマンド
            cmd = ['git', 'submodule', 'add', repo_url, submodule_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ サブモジュール追加成功: {submodule_path}")
                
                # サブモジュール初期化・更新
                subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'])
                print("✅ サブモジュール初期化完了")
                return True
            else:
                print(f"❌ サブモジュール追加失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ サブモジュール追加エラー: {e}")
            return False

    def check_latest_messages(self, limit=10):
        """最新のメッセージを確認（デバッグ用）"""
        if self.offline_mode:
            print("❌ オンラインモードでは利用できません")
            return False
            
        try:
            result = self.supabase.table('chat_history') \
                .select('*') \
                .order('id', desc=True) \
                .limit(limit) \
                .execute()
            
            print(f"📊 最新{limit}件のメッセージ:")
            print("="*80)
            
            for i, message in enumerate(result.data, 1):
                print(f"{i:2d}. ID:{message['id']:4d} | {message.get('ownerid', 'unknown')[:20]:20s} | {message.get('created', 'unknown')[:19]}")
                print(f"    📝 {message.get('messages', '')[:100]}...")
                print("-" * 80)
                
            return True
            
        except Exception as e:
            print(f"❌ 最新メッセージ確認エラー: {e}")
            return False

    def create_comprehensive_issue_immediately(self, message):
        """一気実行: ユーザー質問 → 即座にGitHub Issue作成 → 他AI実行待ち"""
        try:
            question = message.get('messages', '').strip()
            user = message.get('ownerid', 'unknown')
            
            if not question:
                print("❌ 質問内容が空です")
                return None
            
            print(f"🚀 一気実行開始: {question}")
            
            # 1️⃣ まず現在の作業を保存 (Push)
            push_success = self.safe_git_push(question)
            if not push_success:
                print("⚠️ Git Push失敗 - 続行します")
            
            # 2️⃣ Mermaid図生成
            dynamic_mermaid = self.generate_dynamic_mermaid_diagram(question)
            mermaid_file = self.save_mermaid_to_file(dynamic_mermaid)
            
            # 3️⃣ プロジェクト名生成
            project_name = question.lower().replace(' ', '-').replace('　', '-').replace('?', '').replace('？', '')[:30]
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            
            # 4️⃣ GitHub Issue作成 (他のAIが読みやすい形式)
            issue_url = self.create_readable_github_issue(
                question, user, mermaid_file, project_name, timestamp, dynamic_mermaid
            )
            
            if issue_url:
                print(f"✅ 一気実行完了!")
                print(f"📋 Issue URL: {issue_url}")
                print(f"🤖 他のAIがこのIssueを読み込み実行可能")
                return issue_url
            else:
                print("❌ Issue作成失敗")
                return None
                
        except Exception as e:
            print(f"❌ 一気実行エラー: {e}")
            return None

    def safe_git_push(self, question):
        """安全なGit Push実行"""
        try:
            import subprocess
            
            print("📤 Git Push実行中...")
            
            # 1. git add .
            add_result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True, timeout=30)
            if add_result.returncode != 0:
                print(f"⚠️ git add 失敗: {add_result.stderr}")
                return False
            
            # 2. git commit
            commit_msg = f"🔄 自動開発実行前の作業保存 - {question[:50]}"
            commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True, timeout=30)
            if commit_result.returncode != 0:
                print(f"💡 コミット対象なし（変更なし）")
            
            # 3. git push
            push_result = subprocess.run(['git', 'push'], capture_output=True, text=True, timeout=60)
            if push_result.returncode == 0:
                print("✅ Git Push完了")
                return True
            else:
                print(f"⚠️ git push 失敗: {push_result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Git Push エラー: {e}")
            return False

    def create_readable_github_issue(self, question, user, mermaid_file, project_name, timestamp, dynamic_mermaid):
        """他のAIが読みやすいGitHub Issue作成"""
        try:
            import subprocess
            import tempfile
            
            print("📋 他AI向けGitHub Issue作成中...")
            
            # 他のAIが読みやすい詳細なIssue本文
            issue_body = f"""# 🎯 実装要求: {question}

## 📊 自動生成実装フロー図
```mermaid
{dynamic_mermaid}
```

## 🎯 実装仕様
- **ユーザー質問**: {question}
- **質問者**: {user}
- **プロジェクト名**: {project_name}-project
- **対象リポジトリ**: bpmbox/{project_name}-project
- **作業ブランチ**: feature/implementation-{timestamp}
- **サブモジュールパス**: projects/{project_name}-project
- **Mermaidファイル**: {mermaid_file}

## 🚀 実行手順 (他AI・開発者向け)

### 1️⃣ 環境準備
```bash
# 新リポジトリ作成
gh repo create "bpmbox/{project_name}-project" --private --clone

# サブモジュール追加
git submodule add https://github.com/bpmbox/{project_name}-project.git projects/{project_name}-project
git submodule update --init --recursive

# 作業ブランチ作成
cd projects/{project_name}-project
git checkout -b "feature/implementation-{timestamp}"
```

### 2️⃣ 実装要件
- **要求内容**: {question}
- **完全実装**: ソースコード、テスト、ドキュメント
- **動作確認**: 実行可能な状態で完成
- **コード品質**: ベストプラクティス準拠

### 3️⃣ 完了条件
- [ ] 機能実装完了
- [ ] テストコード作成
- [ ] README.md作成
- [ ] 動作確認完了
- [ ] Git コミット・プッシュ

## 📝 自動化システム情報
- **実行時刻**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **システム**: GitHub Copilot完全自動化
- **処理ID**: MSG-{timestamp}

## 🤖 他AI実行ガイド
このIssueを読み込み、上記の要件に従って実装を開始してください。
完了後は完了報告Issueを自動作成してください。"""

            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
                f.write(issue_body)
                temp_file = f.name

            try:
                # GitHub CLI でIssue作成
                cmd = [
                    'gh', 'issue', 'create',
                    '--repo', 'bpmbox/AUTOCREATE',
                    '--title', f'🎯 {question} - AI実装要求',
                    '--body-file', temp_file,
                    '--label', 'ai-automation,implementation,ready-for-ai'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    issue_url = result.stdout.strip()
                    print(f"✅ 他AI向けIssue作成完了: {issue_url}")
                    return issue_url
                else:
                    print(f"❌ Issue作成失敗: {result.stderr}")
                    return None
                    
            finally:
                # 一時ファイル削除
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Issue作成エラー: {e}")
            return None

if __name__ == "__main__":
    print("🤖 GitHub Copilot自動化システム (一気実行対応版) - 開始")
    print("🎨 動的Mermaid図生成対応")
    print("📦 サブモジュール完全分離開発対応")
    print("🚀 一気実行: チャット → Push → Issue作成 → 他AI実行待ち")
    
    # ネットワーク接続テスト
    try:
        import requests
        requests.get("https://www.google.com", timeout=5)
        online_mode = True
        print("🌐 オンラインモード")
    except:
        online_mode = False
        print("🔧 オフラインモード（ネットワーク接続なし）")
    
    automation = GitHubCopilotAutomation(offline_mode=not online_mode)
    
    print("\n🚀 選択肢:")
    print("1. 無限自動ループ開始（一気実行モード）")
    print("2. ローカルテスト実行（オフラインOK）")
    print("3. GitHub CLI統合テスト")
    print("4. 単発Mermaid図生成テスト")
    print("5. 最新メッセージ確認（デバッグ用）")
    print("6. 単発Push+Issue作成テスト")
    print("7. 終了")
    
    choice = input("選択してください (1-7): ")
    
    if choice == "1":
        if automation.offline_mode:
            print("❌ オンラインモードが必要です")
        else:
            print("🚀 一気実行モード: チャット検出 → 自動Push → Issue作成 → 他AI実行待ち")
            automation.infinite_auto_loop()
    elif choice == "2":
        automation.local_test_mode()
    elif choice == "3":
        automation.test_github_cli_integration()
    elif choice == "4":
        # 単発テスト
        test_question = input("テスト質問を入力してください: ") or "Pythonでデータベース管理システムを作成してください"
        print(f"\n🧪 単発テスト実行: {test_question}")
        
        # 動的Mermaid図を生成・保存
        mermaid_diagram = automation.generate_dynamic_mermaid_diagram(test_question)
        mermaid_file = automation.save_mermaid_to_file(mermaid_diagram, "single_test_auto_dev_flow.mermaid")
        
        print(f"✅ テスト完了 - Mermaid図ファイル: {mermaid_file}")
        print("📊 Mermaid図の内容:")
        print(mermaid_diagram[:500] + "..." if len(mermaid_diagram) > 500 else mermaid_diagram)
    elif choice == "5":
        # 最新メッセージ確認
        automation.check_latest_messages()
    elif choice == "6":
        # 単発Push+Issue作成テスト
        test_question = input("テスト質問を入力してください: ") or "単発テスト実行"
        test_message = {
            'messages': test_question,
            'ownerid': 'test_user',
            'created': datetime.now().isoformat()
        }
        
        print(f"\n🧪 単発Push+Issue作成テスト: {test_question}")
        issue_url = automation.create_comprehensive_issue_immediately(test_message)
        
        if issue_url:
            print(f"✅ テスト成功!")
            print(f"📋 作成されたIssue: {issue_url}")
        else:
            print("❌ テスト失敗")
    elif choice == "7":
        print("👋 終了しました")
    else:
        print("❌ 無効な選択です")