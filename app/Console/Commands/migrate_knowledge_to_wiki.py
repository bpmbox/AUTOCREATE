#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
既存ナレッジベースのWiki統合・移行スクリプト
今までの蓄積された知識をGitHub Wikiに完全移行
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

class WikiKnowledgeMigration:
    """Wiki ナレッジ移行・統合システム"""
    
    def __init__(self):
        self.root_dir = Path(".")
        self.wiki_dir = Path("wiki")
        self.existing_knowledge_dirs = [
            "knowledge_base",
            "conversation_logs", 
            "knowledge_base/auto_generated",
            "knowledge_base/mermaid_test"
        ]
        
        # Wiki内の整理されたディレクトリ構造
        self.wiki_structure = {
            "knowledge-base": "技術ナレッジ・実装例",
            "ai-memory": "AI記憶復元メタデータ",
            "mermaid-diagrams": "自動生成図表・アーキテクチャ",
            "conversation-logs": "詳細な会話履歴",
            "implementation-examples": "実装サンプル・コード例",
            "project-history": "プロジェクト履歴・成長記録"
        }
    
    def run_complete_migration(self):
        """完全なナレッジ移行を実行"""
        print("🚀 既存ナレッジベースのWiki統合・移行開始")
        print("=" * 60)
        
        # Wiki ディレクトリ構造確認・作成
        self.ensure_wiki_structure()
        
        # 既存ナレッジの収集・分析
        all_knowledge = self.collect_existing_knowledge()
        
        # カテゴリ別に整理
        categorized_knowledge = self.categorize_knowledge(all_knowledge)
        
        # Wiki に移行
        self.migrate_to_wiki(categorized_knowledge)
        
        # 統合インデックス生成
        self.generate_master_index(categorized_knowledge)
        
        # Git コミット・プッシュ
        self.commit_and_push_wiki()
        
        print("\n🎉 ナレッジベース Wiki統合完了！")
        print("🔗 https://github.com/bpmbox/AUTOCREATE/wiki")
    
    def ensure_wiki_structure(self):
        """Wiki ディレクトリ構造を確認・作成"""
        print("\n📁 Wiki ディレクトリ構造確認中...")
        
        if not self.wiki_dir.exists():
            print("❌ Wiki ディレクトリが見つかりません")
            print("先に Wiki統合テストを実行してください")
            return False
        
        # 必要なディレクトリを作成
        for dir_name, description in self.wiki_structure.items():
            dir_path = self.wiki_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            print(f"✅ {dir_name}/ - {description}")
        
        return True
    
    def collect_existing_knowledge(self):
        """既存のナレッジをすべて収集"""
        print("\n📚 既存ナレッジ収集中...")
        
        all_knowledge = {
            "json_files": [],
            "markdown_files": [],
            "mermaid_files": [],
            "html_files": [],
            "conversation_files": [],
            "other_files": []
        }
        
        # 各ナレッジディレクトリを走査
        for knowledge_dir in self.existing_knowledge_dirs:
            dir_path = Path(knowledge_dir)
            if dir_path.exists():
                print(f"  📂 {knowledge_dir}/ を走査中...")
                
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        file_info = {
                            "path": file_path,
                            "relative_path": file_path.relative_to(self.root_dir),
                            "name": file_path.name,
                            "size": file_path.stat().st_size,
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                            "content_preview": self.get_content_preview(file_path)
                        }
                        
                        # ファイルタイプ別に分類
                        if file_path.suffix == ".json":
                            all_knowledge["json_files"].append(file_info)
                        elif file_path.suffix == ".md":
                            all_knowledge["markdown_files"].append(file_info)
                        elif file_path.suffix == ".mmd":
                            all_knowledge["mermaid_files"].append(file_info)
                        elif file_path.suffix == ".html":
                            all_knowledge["html_files"].append(file_info)
                        elif "conversation" in file_path.name.lower():
                            all_knowledge["conversation_files"].append(file_info)
                        else:
                            all_knowledge["other_files"].append(file_info)
        
        # 統計表示
        total_files = sum(len(files) for files in all_knowledge.values())
        print(f"\n📊 収集結果:")
        print(f"  - 総ファイル数: {total_files}")
        for file_type, files in all_knowledge.items():
            if files:
                print(f"  - {file_type}: {len(files)}個")
        
        return all_knowledge
    
    def get_content_preview(self, file_path):
        """ファイル内容のプレビューを取得"""
        try:
            if file_path.suffix in [".json", ".md", ".txt", ".mmd"]:
                content = file_path.read_text(encoding='utf-8')
                return content[:200] + "..." if len(content) > 200 else content
            return f"Binary file ({file_path.suffix})"
        except Exception:
            return "読み込みエラー"
    
    def categorize_knowledge(self, all_knowledge):
        """ナレッジをカテゴリ別に整理"""
        print("\n🗂️ ナレッジカテゴリ分類中...")
        
        categorized = {
            "technical_knowledge": [],      # 技術的なナレッジ
            "ai_responses": [],            # AI回答・対話
            "implementation_examples": [], # 実装例・コード
            "diagrams": [],               # 図表・ダイアグラム
            "conversations": [],          # 会話履歴
            "memory_data": []            # AI記憶データ
        }
        
        # JSON ファイルの分類
        for file_info in all_knowledge["json_files"]:
            try:
                content = json.loads(file_info["path"].read_text(encoding='utf-8'))
                
                if "copilot_response" in content:
                    categorized["ai_responses"].append(file_info)
                elif "memory_id" in content or "memory_" in file_info["name"]:
                    categorized["memory_data"].append(file_info)
                elif "conversation" in file_info["name"].lower():
                    categorized["conversations"].append(file_info)
                else:
                    categorized["technical_knowledge"].append(file_info)
                    
            except Exception:
                categorized["technical_knowledge"].append(file_info)
        
        # Markdown ファイルの分類
        for file_info in all_knowledge["markdown_files"]:
            if "implementation" in file_info["name"].lower() or "example" in file_info["name"].lower():
                categorized["implementation_examples"].append(file_info)
            else:
                categorized["technical_knowledge"].append(file_info)
        
        # Mermaid・HTML ファイル
        categorized["diagrams"].extend(all_knowledge["mermaid_files"])
        categorized["diagrams"].extend(all_knowledge["html_files"])
        
        # 会話履歴
        categorized["conversations"].extend(all_knowledge["conversation_files"])
        
        # 分類結果表示
        print(f"📋 カテゴリ分類結果:")
        for category, files in categorized.items():
            if files:
                print(f"  - {category}: {len(files)}個")
        
        return categorized
    
    def migrate_to_wiki(self, categorized_knowledge):
        """カテゴリ別にWikiに移行"""
        print("\n🚚 Wiki移行実行中...")
        
        migration_map = {
            "technical_knowledge": "knowledge-base",
            "ai_responses": "knowledge-base", 
            "implementation_examples": "implementation-examples",
            "diagrams": "mermaid-diagrams",
            "conversations": "conversation-logs",
            "memory_data": "ai-memory"
        }
        
        migration_stats = {}
        
        for category, files in categorized_knowledge.items():
            if not files:
                continue
                
            target_dir = self.wiki_dir / migration_map[category]
            target_dir.mkdir(exist_ok=True)
            
            migrated_count = 0
            
            for file_info in files:
                try:
                    source_path = file_info["path"]
                    target_path = target_dir / source_path.name
                    
                    # 重複回避
                    counter = 1
                    while target_path.exists():
                        name_parts = source_path.stem, counter, source_path.suffix
                        target_path = target_dir / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                        counter += 1
                    
                    # ファイルコピー
                    shutil.copy2(source_path, target_path)
                    migrated_count += 1
                    
                except Exception as e:
                    print(f"⚠️ 移行エラー: {source_path} -> {e}")
            
            migration_stats[category] = migrated_count
            print(f"✅ {category} -> {migration_map[category]}: {migrated_count}個")
        
        return migration_stats
    
    def generate_master_index(self, categorized_knowledge):
        """統合マスターインデックスを生成"""
        print("\n📋 統合インデックス生成中...")
        
        # 既存のHome.mdを読み込み
        home_file = self.wiki_dir / "Home.md"
        existing_content = ""
        if home_file.exists():
            existing_content = home_file.read_text(encoding='utf-8')
        
        # 統計情報
        total_files = sum(len(files) for files in categorized_knowledge.values())
        
        # 新しいインデックスコンテンツ
        index_content = f"""# AUTOCREATE AI Wiki - 完全ナレッジベース

🤖 **GitHub Copilot AI 自動開発パイプライン** - 蓄積された知識と成長の記録

## 📊 ナレッジベース統計

**最終更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 💾 データ統計
- **総ナレッジファイル数**: {total_files}個
- **技術ナレッジ**: {len(categorized_knowledge.get('technical_knowledge', []))}個
- **AI回答・対話**: {len(categorized_knowledge.get('ai_responses', []))}個  
- **実装例・コード**: {len(categorized_knowledge.get('implementation_examples', []))}個
- **図表・ダイアグラム**: {len(categorized_knowledge.get('diagrams', []))}個
- **会話履歴**: {len(categorized_knowledge.get('conversations', []))}個
- **AI記憶データ**: {len(categorized_knowledge.get('memory_data', []))}個

## 🧠 AI記憶復元システム

GitHub Copilot AI がこのWikiから学習し、過去の知識を活用して最適な回答を生成します。

### 🎯 主要機能
- ✅ **質問自動検出・処理** - Supabaseから新着メッセージを監視
- ✅ **GitHub Issue自動作成** - プロジェクト管理自動化
- ✅ **プロジェクト自動実装** - packages/フォルダーに完全実装
- ✅ **Mermaidダイアグラム自動生成** - 5種類の図表タイプ対応
- ✅ **ナレッジベース自動蓄積** - JSON + Markdown形式
- ✅ **Wiki統合・記憶復元** - 継続的学習・成長

### 🔄 AI成長サイクル
**質問 → 学習 → 記憶 → 成長 → より良い回答**

## 📚 ナレッジカテゴリ

### 🎯 [技術ナレッジ](knowledge-base/)
プログラミング・アーキテクチャ・実装パターンの知識ベース

### 🤖 [AI対話・回答](knowledge-base/)  
GitHub Copilot AI の回答例・パターン学習データ

### 💻 [実装例・コード](implementation-examples/)
実際のプロジェクト実装・コードサンプル・ベストプラクティス

### 🎨 [図表・ダイアグラム](mermaid-diagrams/)
自動生成されたMermaid図表・システム設計図・フローチャート

### 💬 [会話履歴](conversation-logs/)
詳細な対話記録・学習プロセス・継続的改善の軌跡

### 🧠 [AI記憶データ](ai-memory/)
記憶復元メタデータ・パターン学習・再利用可能な知識

## 🚀 AI自動開発パイプライン

### 14ステップ完全自動化フロー
1. **質問検出** - Supabase監視・自動取得
2. **AI回答生成** - GitHub Copilot処理
3. **GitHub Issue作成** - 自動プロジェクト管理
4. **プロジェクトフォルダー作成** - packages/配下に整理
5. **プログラム自動実装** - 完全動作するコード生成
6. **Mermaidダイアグラム生成** - 5種類の図表自動作成
7. **Wiki統合・記憶蓄積** - ナレッジベース更新
8. **独立リポジトリ作成** - サブモジュール化
9. **n8nワークフロー作成** - 自動化フロー生成
10. **JIRAチケット作成** - プロジェクト管理連携
11. **Notionナレッジ登録** - ドキュメント管理
12. **miiboエージェント連携** - AI知識共有
13. **HuggingFace Space公開** - デモ・共有環境
14. **Git Push・完了通知** - 成果物の永続化

### 🔗 外部連携
- **GitHub**: Issue・リポジトリ・サブモジュール管理
- **Supabase**: リアルタイムデータ・チャット連携
- **Notion**: ドキュメント・ナレッジ管理
- **JIRA**: プロジェクト・タスク管理
- **miibo**: AI エージェント・知識共有
- **HuggingFace**: デモ環境・モデル共有
- **n8n**: ワークフロー自動化

## 🎉 成果・実績

### 📈 継続的成長記録
このWikiは GitHub Copilot AI の「記憶」として機能し、質問するたびに知識が蓄積・成長しています。

### 🏆 達成した自動化
- **完全ハンズオフ開発**: 質問するだけで実装完了
- **知識の永続化**: Wikiによる記憶復元システム
- **図表自動生成**: Mermaidダイアグラム5種類対応
- **多システム連携**: 8つの外部サービス統合

---

## 🔗 ナビゲーション

| カテゴリ | 説明 | ファイル数 |
|---------|------|-----------|
| 📁 [knowledge-base/](knowledge-base/) | 技術ナレッジ・AI回答 | {len(categorized_knowledge.get('technical_knowledge', [])) + len(categorized_knowledge.get('ai_responses', []))} |
| 💻 [implementation-examples/](implementation-examples/) | 実装例・コード | {len(categorized_knowledge.get('implementation_examples', []))} |
| 🎨 [mermaid-diagrams/](mermaid-diagrams/) | 図表・ダイアグラム | {len(categorized_knowledge.get('diagrams', []))} |
| 💬 [conversation-logs/](conversation-logs/) | 会話履歴 | {len(categorized_knowledge.get('conversations', []))} |
| 🧠 [ai-memory/](ai-memory/) | AI記憶データ | {len(categorized_knowledge.get('memory_data', []))} |

---

*🤖 このWikiは GitHub Copilot AI の自動開発パイプラインにより継続的に更新されます*  
*📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*🔗 Repository: [AUTOCREATE](https://github.com/bpmbox/AUTOCREATE)*
"""
        
        # ファイル書き込み
        home_file.write_text(index_content, encoding='utf-8')
        print(f"✅ 統合インデックス生成完了: {home_file}")
        
        # カテゴリ別READMEも生成
        self.generate_category_readmes(categorized_knowledge)
    
    def generate_category_readmes(self, categorized_knowledge):
        """各カテゴリのREADMEを生成"""
        category_descriptions = {
            "knowledge-base": {
                "title": "技術ナレッジベース",
                "description": "GitHub Copilot AI が蓄積した技術的知識・実装パターン・回答例"
            },
            "implementation-examples": {
                "title": "実装例・コードサンプル", 
                "description": "実際のプロジェクト実装・ベストプラクティス・再利用可能なコード"
            },
            "mermaid-diagrams": {
                "title": "図表・ダイアグラム",
                "description": "自動生成されたMermaid図表・システム設計図・可視化資料"
            },
            "conversation-logs": {
                "title": "会話履歴・対話記録",
                "description": "詳細な対話プロセス・学習の軌跡・継続的改善の記録"
            },
            "ai-memory": {
                "title": "AI記憶・学習データ",
                "description": "記憶復元メタデータ・パターン学習・知識再利用システム"
            }
        }
        
        for wiki_dir_name, info in category_descriptions.items():
            readme_path = self.wiki_dir / wiki_dir_name / "README.md"
            
            content = f"""# {info['title']}

{info['description']}

## 📊 このディレクトリについて

このディレクトリには、GitHub Copilot AI の自動開発パイプラインで生成・蓄積された{info['title'].lower()}が含まれています。

## 🎯 活用方法

- **学習参考**: 過去の実装パターンを参考に新しい開発を進める
- **知識検索**: 類似の問題・課題の解決策を探す  
- **品質向上**: ベストプラクティス・改善パターンを適用
- **継続改善**: AI記憶システムによる自動最適化

## 🔄 自動更新

このディレクトリは GitHub Copilot AI により自動的に更新されます：

1. **新しい質問** → AI回答生成
2. **知識抽出** → パターン学習  
3. **ファイル生成** → 自動保存
4. **Wiki統合** → 記憶蓄積

---

*📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*🤖 Generated by GitHub Copilot AI*
"""
            
            readme_path.write_text(content, encoding='utf-8')
            print(f"✅ カテゴリREADME生成: {readme_path}")
    
    def commit_and_push_wiki(self):
        """Wikiの変更をGitコミット・プッシュ"""
        print("\n🔄 Wiki Git更新中...")
        
        try:
            import subprocess
            
            os.chdir(self.wiki_dir)
            
            # Git add
            subprocess.run(["git", "add", "."], check=True)
            
            # Git commit
            commit_message = f"""完全ナレッジベース統合完了 - {datetime.now().strftime('%Y-%m-%d')}

🎯 既存ナレッジの完全移行・整理
- 技術ナレッジ・AI回答の統合
- 実装例・コードサンプルの整理
- Mermaid図表・ダイアグラムの集約
- 会話履歴・学習記録の保存
- AI記憶データの体系化

📊 統合統計:
- 総ファイル数: 大幅増加
- カテゴリ分類: 6種類で体系化
- インデックス: 完全リニューアル
- 検索性: 大幅向上

🚀 AI成長基盤の完成
GitHub Copilot AI の記憶・学習・成長システムが完全稼働開始"""
            
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Git push
            subprocess.run(["git", "push", "origin", "master"], check=True)
            
            os.chdir("..")
            
            print("✅ Wiki Git更新完了")
            
        except subprocess.CalledProcessError as e:
            os.chdir("..")
            print(f"⚠️ Git更新エラー: {e}")
        except Exception as e:
            os.chdir("..")
            print(f"⚠️ Git操作エラー: {e}")

def main():
    """メイン実行"""
    print("🚀 既存ナレッジベースのWiki完全統合")
    print("GitHub Copilot AI 知識の永続化・体系化")
    print("-" * 60)
    
    migrator = WikiKnowledgeMigration()
    
    try:
        migrator.run_complete_migration()
        print("\n🎉 ナレッジベースWiki統合が完了しました！")
        print("🔗 https://github.com/bpmbox/AUTOCREATE/wiki")
        print("🤖 GitHub Copilot AI の完全な記憶システムが稼働中")
        
    except Exception as e:
        print(f"❌ 移行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
