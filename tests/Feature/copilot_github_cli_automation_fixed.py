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
import sys
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip
from supabase import create_client

# 設定
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

class GitHubCopilotAutomation:
    def __init__(self):
        # Supabase設定
        url = "https://tnojlywkucnzgakwrgep.supabase.co"
        key = "ENV_SUPABASE_KEY_PLACEHOLDER"
        self.supabase = create_client(url, key)
        
        # チャット座標管理
        self.coordinates_file = "chat_coordinates.json"
        self.chat_coordinates = self.load_coordinates()
        
        print("🤖 GitHub Copilot完全自動化システム (サブモジュール分離型) 起動")
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
            print("🎨 Mermaid図付きIssue作成")
            print("📦 サブモジュール分離型開発")
            print("🚀 9ステップ完全自動化実行中...")
            
            return True
                
        except Exception as e:
            print(f"❌ チャット送信エラー: {e}")
            return False

    def infinite_auto_loop(self, interval=3):
        """無限自動ループモード（完全に手を離せる）+ ホットリロード"""
        print("🔥 無限自動ループモード開始!")
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
                    # 新着メッセージを確認
                    result = self.supabase.table('chat_history') \
                        .select('*') \
                        .gt('id', last_id) \
                        .order('id', desc=False) \
                        .execute()
                    
                    if result.data:
                        for message in result.data:
                            message_id = message['id']
                            
                            if (message_id not in processed_ids and 
                                message.get('ownerid') != 'GitHub-Copilot-AI' and
                                message.get('messages', '').strip()):
                                
                                print(f"\n🚀 新着メッセージ検出! ID: {message_id}")
                                print(f"👤 ユーザー: {message.get('ownerid', 'unknown')}")
                                print(f"📝 質問: {message.get('messages', '')[:100]}...")
                                
                                # 自動実行
                                if self.send_to_copilot_and_get_response(message):
                                    processed_ids.add(message_id)
                                    last_id = max(last_id, message_id)
                                    success_count += 1
                                    print(f"✅ 自動処理完了! 成功数: {success_count}")
                                    print(f"🎨 Mermaid図生成・保存完了")
                                    print(f"📦 サブモジュール分離型フロー送信完了")
                                else:
                                    print(f"⚠️ 自動処理失敗")
                                    processed_ids.add(message_id)
                                    last_id = max(last_id, message_id)
                    
                    # ステータス表示（10回おき）
                    if check_count % 10 == 0:
                        print(f"🔍 監視継続中... チェック回数: {check_count}, 成功処理数: {success_count}, 現在時刻: {datetime.now().strftime('%H:%M:%S')}")
                
                except Exception as e:
                    print(f"⚠️ メッセージ監視エラー: {e}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n🛑 無限ループ停止")
            print(f"📊 最終統計: チェック回数={check_count}, 成功処理数={success_count}")
            print("👋 システム終了")

if __name__ == "__main__":
    print("🤖 GitHub Copilot自動化システム (サブモジュール分離型) - 開始")
    print("🎨 動的Mermaid図生成対応")
    print("📦 サブモジュール完全分離開発対応")
    
    automation = GitHubCopilotAutomation()
    
    print("\n🚀 選択肢:")
    print("1. 無限自動ループ開始")
    print("2. テスト実行")
    print("3. 終了")
    
    choice = input("選択してください (1-3): ")
    
    if choice == "1":
        automation.infinite_auto_loop()
    elif choice == "2":
        # テスト質問でMermaid図生成をテスト
        test_question = "Pythonでデータベース管理システムを作成してください"
        print(f"\n🧪 テスト実行: {test_question}")
        
        # 動的Mermaid図を生成・保存
        mermaid_diagram = automation.generate_dynamic_mermaid_diagram(test_question)
        mermaid_file = automation.save_mermaid_to_file(mermaid_diagram, "test_auto_dev_flow.mermaid")
        
        print(f"✅ テスト完了 - Mermaid図ファイル: {mermaid_file}")
        print("📊 Mermaid図の内容:")
        print(mermaid_diagram[:500] + "..." if len(mermaid_diagram) > 500 else mermaid_diagram)
    else:
        print("👋 終了しました")
