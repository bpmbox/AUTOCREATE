#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaidダイアグラム自動生成機能のテストスクリプト
GitHub Copilot AI自動開発パイプラインのナレッジベース可視化
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

class MermaidGenerationTester:
    """Mermaidダイアグラム自動生成のテストクラス"""
    
    def __init__(self):
        self.system = CopilotSupabaseIntegrationSystem()
        self.test_questions = [
            {
                "question": "React+Viteでチャットアプリを作成してください",
                "user": "test-user",
                "expected_type": "flowchart"
            },
            {
                "question": "データベース設計を教えて - ユーザーテーブルと投稿テーブルの関係",
                "user": "test-user", 
                "expected_type": "er"
            },
            {
                "question": "API呼び出しのシーケンスを説明してください",
                "user": "test-user",
                "expected_type": "sequence"
            },
            {
                "question": "システムアーキテクチャの全体設計について",
                "user": "test-user",
                "expected_type": "architecture"
            },
            {
                "question": "オブジェクト指向のクラス設計パターン",
                "user": "test-user", 
                "expected_type": "class"
            }
        ]
    
    def run_all_tests(self):
        """全てのMermaidダイアグラム生成テストを実行"""
        print("🎯 Mermaidダイアグラム自動生成テスト開始")
        print("=" * 60)
        
        # テスト用ナレッジディレクトリ作成
        knowledge_dir = Path("knowledge_base/mermaid_test")
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        for i, test_case in enumerate(self.test_questions, 1):
            print(f"\n📊 テスト {i}/{len(self.test_questions)}")
            print(f"質問: {test_case['question']}")
            print(f"期待ダイアグラムタイプ: {test_case['expected_type']}")
            
            # テストナレッジエントリ作成
            knowledge_entry = {
                "timestamp": datetime.now().isoformat(),
                "question": test_case['question'],
                "questioner": test_case['user'],
                "copilot_response": f"AI回答: {test_case['question']}に対する詳細な実装ガイドを提供します。フローチャート、ER図、シーケンス図などを含む包括的な回答。",
                "auto_generated": True,
                "knowledge_type": "copilot-ai-response",
                "tags": ["test", "mermaid", test_case['expected_type']]
            }
            
            try:
                # Mermaidダイアグラム生成テスト
                self.system.generate_mermaid_diagram(knowledge_entry, knowledge_dir)
                results.append({"test": i, "status": "SUCCESS", "type": test_case['expected_type']})
                print(f"✅ ダイアグラム生成成功")
                
            except Exception as e:
                results.append({"test": i, "status": "FAILED", "error": str(e)})
                print(f"❌ ダイアグラム生成失敗: {e}")
        
        # テスト結果サマリー
        self.print_test_summary(results, knowledge_dir)
        
        return results
    
    def print_test_summary(self, results, knowledge_dir):
        """テスト結果のサマリーを表示"""
        print("\n" + "=" * 60)
        print("📋 Mermaidダイアグラム生成テスト結果")
        print("=" * 60)
        
        success_count = len([r for r in results if r['status'] == 'SUCCESS'])
        total_count = len(results)
        
        print(f"成功: {success_count}/{total_count}")
        print(f"成功率: {(success_count/total_count)*100:.1f}%")
        
        # 生成されたファイルをリスト
        generated_files = list(knowledge_dir.glob("*.mmd")) + list(knowledge_dir.glob("*.html"))
        print(f"\n📁 生成されたファイル数: {len(generated_files)}")
        
        for file_path in generated_files:
            file_size = file_path.stat().st_size
            print(f"  - {file_path.name} ({file_size:,} bytes)")
        
        # ダイアグラムタイプ別統計
        diagram_types = {}
        for result in results:
            if result['status'] == 'SUCCESS':
                dtype = result.get('type', 'unknown')
                diagram_types[dtype] = diagram_types.get(dtype, 0) + 1
        
        if diagram_types:
            print(f"\n📊 生成されたダイアグラムタイプ:")
            for dtype, count in diagram_types.items():
                print(f"  - {dtype}: {count}個")
        
        # エラー詳細
        failed_tests = [r for r in results if r['status'] == 'FAILED']
        if failed_tests:
            print(f"\n❌ 失敗したテスト:")
            for fail in failed_tests:
                print(f"  - テスト{fail['test']}: {fail.get('error', 'Unknown error')}")
        
        print(f"\n💾 生成ファイル保存場所: {knowledge_dir.absolute()}")
        
        # HTML プレビューファイルの案内
        html_files = list(knowledge_dir.glob("*.html"))
        if html_files:
            print(f"\n🌐 HTMLプレビュー:")
            for html_file in html_files:
                print(f"  - ブラウザで開く: {html_file.absolute()}")

def main():
    """メイン実行関数"""
    print("🎯 Mermaidダイアグラム自動生成機能テスト")
    print("GitHub Copilot AI自動開発パイプライン - ナレッジ可視化")
    print("-" * 60)
    
    tester = MermaidGenerationTester()
    
    try:
        results = tester.run_all_tests()
        
        # 追加テスト: 実際のファイル存在確認
        print("\n🔍 生成ファイル検証中...")
        knowledge_dir = Path("knowledge_base/mermaid_test")
        
        mmd_files = list(knowledge_dir.glob("*.mmd"))
        html_files = list(knowledge_dir.glob("*.html"))
        
        print(f"✅ .mmdファイル: {len(mmd_files)}個")
        print(f"✅ .htmlファイル: {len(html_files)}個")
        
        # サンプルファイルの内容チェック
        if mmd_files:
            sample_mmd = mmd_files[0]
            with open(sample_mmd, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"\n📄 サンプル.mmdファイル ({sample_mmd.name}):")
                print("```mermaid")
                print(content[:200] + "..." if len(content) > 200 else content)
                print("```")
        
        print(f"\n🎉 Mermaidダイアグラム自動生成テスト完了！")
        print(f"総合成功率: {len([r for r in results if r['status'] == 'SUCCESS'])/len(results)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
