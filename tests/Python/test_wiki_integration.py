#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Wiki統合・AI記憶復元システムのテストスクリプト
GitHub Copilot AI の成長・記憶蓄積機能テスト
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent))

# 必要なモジュールをインポート
try:
    from tests.Feature.copilot_direct_answer_fixed import CopilotSupabaseIntegrationSystem
except ImportError:
    print("❌ copilot_direct_answer_fixed.pyのインポートに失敗しました")
    sys.exit(1)

class WikiIntegrationTester:
    """Wiki統合・AI記憶復元システムのテストクラス"""
    
    def __init__(self):
        self.system = CopilotSupabaseIntegrationSystem()
        self.test_knowledge_entries = [
            {
                "question": "React+TypeScriptでチャットアプリの状態管理",
                "user": "test-developer",
                "response": "React+TypeScriptでのチャットアプリ状態管理には、Context API + useReducer の組み合わせが効果的です。メッセージ状態、ユーザー状態、UI状態を分離して管理し、型安全性を確保することで保守性の高いアプリケーションを構築できます。"
            },
            {
                "question": "Supabase Real-time機能でのデータ同期パターン",
                "user": "test-developer",
                "response": "Supabase Real-timeを使用したデータ同期では、楽観的アップデート + リアルタイム同期の組み合わせが重要です。ローカル状態を即座に更新し、サーバーからの変更を subscription で監視することで、responsive なUXを実現できます。"
            },
            {
                "question": "Mermaidダイアグラムによるシステム設計の可視化手法",
                "user": "test-architect", 
                "response": "Mermaidダイアグラムでは、フローチャート・シーケンス図・ER図・クラス図を適切に使い分けることが重要です。システムの複雑性に応じて段階的に詳細化し、ステークホルダーとのコミュニケーションツールとして活用します。"
            }
        ]
    
    def run_wiki_integration_test(self):
        """Wiki統合機能の包括的テスト"""
        print("🚀 GitHub Wiki統合・AI記憶復元システムテスト開始")
        print("=" * 70)
        
        # テスト用ナレッジディレクトリ作成
        knowledge_dir = Path("knowledge_base/wiki_test")
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        total_tests = len(self.test_knowledge_entries)
        
        for i, test_data in enumerate(self.test_knowledge_entries, 1):
            print(f"\n📚 Wiki統合テスト {i}/{total_tests}")
            print(f"質問: {test_data['question']}")
            print(f"ユーザー: {test_data['user']}")
            
            # ナレッジエントリ作成
            knowledge_entry = {
                "timestamp": datetime.now().isoformat(),
                "question": test_data['question'],
                "questioner": test_data['user'],
                "copilot_response": test_data['response'],
                "auto_generated": True,
                "knowledge_type": "copilot-ai-response",
                "tags": self.system.extract_tags_from_question(test_data['question'])
            }
            
            try:
                # Wiki統合テスト実行
                print("🔄 Wiki統合処理中...")
                success = self.system.sync_to_wiki_knowledge(knowledge_entry, knowledge_dir)
                
                if success:
                    print("✅ Wiki統合成功")
                    success_count += 1
                    
                    # 生成ファイル確認
                    self.verify_wiki_files(knowledge_entry)
                else:
                    print("❌ Wiki統合失敗")
                    
            except Exception as e:
                print(f"❌ Wiki統合エラー: {e}")
        
        # テスト結果サマリー
        self.print_wiki_test_summary(success_count, total_tests)
        
        return success_count == total_tests
    
    def verify_wiki_files(self, knowledge_entry):
        """Wiki統合で生成されたファイルを検証"""
        wiki_dir = Path("wiki")
        
        if not wiki_dir.exists():
            print("⚠️ Wikiディレクトリが見つかりません")
            return False
        
        # 各ディレクトリの存在確認
        required_dirs = [
            "knowledge-base",
            "ai-memory", 
            "mermaid-diagrams",
            "conversation-logs"
        ]
        
        for dir_name in required_dirs:
            dir_path = wiki_dir / dir_name
            if dir_path.exists():
                print(f"  ✅ {dir_name}/ ディレクトリ存在確認")
                
                # ファイル数確認
                files = list(dir_path.glob("*"))
                print(f"    📁 {len(files)}個のファイル")
            else:
                print(f"  ❌ {dir_name}/ ディレクトリ未作成")
        
        # Home.mdの存在確認
        home_file = wiki_dir / "Home.md"
        if home_file.exists():
            print("  ✅ Home.md インデックスファイル更新済み")
            
            # 内容確認
            content = home_file.read_text(encoding='utf-8')
            if knowledge_entry['question'][:30] in content:
                print("  ✅ 新しいナレッジエントリがインデックスに追加済み")
            else:
                print("  ⚠️ インデックスに新エントリが見つかりません")
        else:
            print("  ❌ Home.md インデックスファイル未作成")
        
        return True
    
    def print_wiki_test_summary(self, success_count, total_tests):
        """Wiki統合テスト結果のサマリー表示"""
        print("\n" + "=" * 70)
        print("📊 GitHub Wiki統合テスト結果")
        print("=" * 70)
        
        success_rate = (success_count / total_tests) * 100
        print(f"成功: {success_count}/{total_tests}")
        print(f"成功率: {success_rate:.1f}%")
        
        # Wiki構造確認
        wiki_dir = Path("wiki")
        if wiki_dir.exists():
            print(f"\n📁 Wiki構造:")
            self.print_directory_tree(wiki_dir, prefix="  ")
            
            # 統計情報
            all_files = list(wiki_dir.rglob("*"))
            file_count = len([f for f in all_files if f.is_file()])
            dir_count = len([f for f in all_files if f.is_dir()])
            
            print(f"\n📈 Wiki統計:")
            print(f"  - 総ファイル数: {file_count}")
            print(f"  - ディレクトリ数: {dir_count}")
            
            # ファイルタイプ別統計
            extensions = {}
            for file_path in all_files:
                if file_path.is_file():
                    ext = file_path.suffix or 'no_extension'
                    extensions[ext] = extensions.get(ext, 0) + 1
            
            if extensions:
                print(f"  - ファイル形式:")
                for ext, count in extensions.items():
                    print(f"    {ext}: {count}個")
        else:
            print("⚠️ Wikiディレクトリが作成されていません")
        
        # AI記憶復元システム統計
        memory_dir = wiki_dir / "ai-memory"
        if memory_dir.exists():
            memory_files = list(memory_dir.glob("*.json"))
            print(f"\n🧠 AI記憶復元システム:")
            print(f"  - 記憶エントリ数: {len(memory_files)}")
            print(f"  - 記憶強度平均: 継続計測中")
            print(f"  - 再利用回数: 0回 (新規記憶)")
        
        print(f"\n🎉 Wiki統合システム構築完了！")
        print(f"GitHub Copilot AI の成長・記憶基盤が整いました。")
        print(f"🔗 Wiki URL: https://github.com/bpmbox/AUTOCREATE/wiki")
    
    def print_directory_tree(self, directory, prefix=""):
        """ディレクトリツリーを表示"""
        try:
            items = sorted(directory.iterdir())
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and len(list(item.iterdir())) > 0:
                    extension = "    " if is_last else "│   "
                    self.print_directory_tree(item, prefix + extension)
                    
        except PermissionError:
            print(f"{prefix}└── [アクセス権限なし]")

def main():
    """メイン実行関数"""
    print("🚀 GitHub Wiki統合・AI記憶復元システムテスト")
    print("GitHub Copilot AI 成長基盤構築テスト")
    print("-" * 70)
    
    tester = WikiIntegrationTester()
    
    try:
        # Wiki統合テスト実行
        success = tester.run_wiki_integration_test()
        
        if success:
            print("\n🎉 全ての Wiki統合テストが成功しました！")
            print("🤖 GitHub Copilot AI の記憶・成長システムが稼働開始")
            print("📚 今後の質問でAIがこの知識を活用します")
        else:
            print("\n⚠️ 一部のテストが失敗しました")
            print("🔧 システムを調整して再実行してください")
            
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
