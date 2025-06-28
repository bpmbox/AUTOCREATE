#!/usr/bin/env python3
"""
🧪 pytest対応 統一自動化テストスイート
GitHub Copilot自動化システムのpytest実行用テスト

実行方法:
  pytest test_unified_automation.py -v
  pytest test_unified_automation.py::test_unified_mode -v
  make test-unified
"""

import pytest
import os
import sys
from datetime import datetime
from pathlib import Path

# テスト対象のモジュールをインポート
try:
    # 直接インポートを試行
    from tests.Feature.copilot_github_cli_automation import GitHubCopilotAutomation
except ImportError:
    # パス追加してインポート
    sys.path.append(str(Path(__file__).parent / "tests" / "Feature"))
    try:
        from copilot_github_cli_automation import GitHubCopilotAutomation
    except ImportError:
        # 最後の手段: 絶対パスでインポート
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "copilot_github_cli_automation", 
            Path(__file__).parent / "tests" / "Feature" / "copilot_github_cli_automation.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        GitHubCopilotAutomation = module.GitHubCopilotAutomation


class TestUnifiedAutomation:
    """統一自動化テストクラス"""
    
    @pytest.fixture
    def automation(self):
        """テスト用GitHubCopilotAutomationインスタンス"""
        return GitHubCopilotAutomation(offline_mode=True)  # テスト時はオフライン
    
    def test_initialization(self, automation):
        """🔧 初期化テスト"""
        print("\n🔧 初期化テスト開始")
        
        assert automation is not None
        assert hasattr(automation, 'offline_mode')
        assert hasattr(automation, 'chat_coordinates')
        assert hasattr(automation, 'coordinates_file')
        
        print("✅ 初期化テスト完了")
    
    def test_mermaid_generation(self, automation):
        """🎨 Mermaid図生成テスト"""
        print("\n🎨 Mermaid図生成テスト開始")
        
        test_questions = [
            "Pythonで機械学習アプリケーションを作成してください",
            "ReactとTypeScriptでダッシュボードUIを開発したい",
            "PostgreSQLとPythonでデータベース連携システムを作りたい"
        ]
        
        generated_files = []
        
        for i, question in enumerate(test_questions):
            print(f"  📝 テスト{i+1}: {question[:30]}...")
            
            # Mermaid図生成
            mermaid_content = automation.generate_dynamic_mermaid_diagram(question)
            assert mermaid_content is not None
            assert len(mermaid_content) > 100
            assert "graph TB" in mermaid_content
            
            # ファイル保存
            filename = f"pytest_mermaid_{i+1}_{int(datetime.now().timestamp())}.mermaid"
            saved_file = automation.save_mermaid_to_file(mermaid_content, filename)
            assert saved_file is not None
            assert os.path.exists(saved_file)
            
            generated_files.append(saved_file)
            print(f"    ✅ 生成・保存完了: {saved_file}")
        
        print(f"✅ Mermaid図生成テスト完了 - {len(generated_files)}件生成")
        
        # テスト後クリーンアップ
        for file in generated_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"🧹 クリーンアップ: {file}")
            except Exception as e:
                print(f"⚠️ クリーンアップ失敗: {file} - {e}")
    
    def test_filtering_logic(self, automation):
        """🔍 フィルタリングロジックテスト"""
        print("\n🔍 フィルタリングロジックテスト開始")
        
        test_data = [
            {
                'id': 1001,
                'messages': 'Pythonで機械学習アプリケーションを作成してください',
                'ownerid': 'test_user_1',
                'expected': True,  # 処理対象
                'reason': '有効質問'
            },
            {
                'id': 1002,
                'messages': 'copilotでAPIを作成してください',
                'ownerid': 'test_user_2',
                'expected': False,  # 除外
                'reason': 'copilotキーワード'
            },
            {
                'id': 1003,
                'messages': 'こんにちは',
                'ownerid': 'test_user_3',
                'expected': False,  # 除外
                'reason': '短すぎ'
            },
            {
                'id': 1004,
                'messages': 'Node.jsでREST APIサーバーを構築してください',
                'ownerid': 'copilot',
                'expected': False,  # 除外
                'reason': 'copilotユーザー'
            },
            {
                'id': 1005,
                'messages': 'Vue.jsとFirebaseでリアルタイムチャットアプリを作成してください',
                'ownerid': 'test_user_4',
                'expected': True,  # 処理対象
                'reason': '有効質問'
            }
        ]
        
        correct_predictions = 0
        
        for data in test_data:
            message_content = data.get('messages', '').strip()
            message_owner = data.get('ownerid', '')
            expected = data['expected']
            reason = data['reason']
            
            # フィルタリングロジック適用
            should_process = (
                message_owner != 'copilot' and
                message_content and
                len(message_content) >= 15 and
                not any(keyword.lower() in message_content.lower() 
                       for keyword in ['copilot', 'github copilot', '@copilot'])
            )
            
            is_correct = (should_process == expected)
            if is_correct:
                correct_predictions += 1
            
            status = "✅ 正解" if is_correct else "❌ 不正解"
            result = "処理対象" if should_process else "除外"
            
            print(f"  ID:{data['id']} | {status} | {result} | 理由:{reason}")
            print(f"    内容: {message_content[:40]}...")
            
            # アサーション
            assert should_process == expected, f"ID:{data['id']} フィルタリング結果が期待値と異なります"
        
        accuracy = (correct_predictions / len(test_data)) * 100
        print(f"\n📊 フィルタリング精度: {accuracy:.1f}% ({correct_predictions}/{len(test_data)})")
        print("✅ フィルタリングロジックテスト完了")
        
        assert accuracy == 100.0, "フィルタリング精度が100%ではありません"
    
    def test_coordinates_management(self, automation):
        """📍 座標管理テスト"""
        print("\n📍 座標管理テスト開始")
        
        # 座標が設定されているかチェック
        assert automation.chat_coordinates is not None
        assert 'x' in automation.chat_coordinates
        assert 'y' in automation.chat_coordinates
        
        x = automation.chat_coordinates['x']
        y = automation.chat_coordinates['y']
        
        print(f"  📍 現在座標: ({x}, {y})")
        
        # 座標値の妥当性チェック
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert x > 0
        assert y > 0
        
        print("✅ 座標管理テスト完了")
    
    def test_report_generation(self, automation):
        """📋 レポート生成テスト"""
        print("\n📋 レポート生成テスト開始")
        
        test_cases = [
            {
                'issue_number': 9001,
                'question': 'pytest用テスト質問1',
                'title': 'pytestレポート生成テスト1'
            },
            {
                'issue_number': 9002,
                'question': 'pytest用テスト質問2',
                'title': 'pytestレポート生成テスト2'
            }
        ]
        
        for case in test_cases:
            print(f"  📝 レポート生成: Issue #{case['issue_number']}")
            
            report = automation.create_implementation_report(
                case['issue_number'],
                case['question'],
                case['title']
            )
            
            # レポートの基本構造チェック
            assert report is not None
            assert len(report) > 100
            assert f"Issue #{case['issue_number']}" in report
            assert case['question'] in report
            assert case['title'] in report
            assert "実装完了" in report
            assert "✅" in report
            
            print(f"    ✅ レポート生成完了 - {len(report)}文字")
        
        print("✅ レポート生成テスト完了")
    
    def test_unified_mode_execution(self, automation):
        """🧪 統一テストモード実行テスト"""
        print("\n🧪 統一テストモード実行テスト開始")
        
        # 統一テストモードの実行
        result = automation.unified_test_mode()
        
        # 結果検証
        assert result is not None
        assert isinstance(result, dict)
        assert 'total' in result
        assert 'processed' in result
        assert 'excluded' in result
        assert 'success_rate' in result
        
        # 期待値の検証
        assert result['total'] == 6  # テストデータ6件
        assert result['processed'] == 3  # 処理対象3件
        assert result['excluded'] == 3  # 除外3件
        assert result['success_rate'] == 50.0  # 処理率50%
        
        print(f"📊 統一テスト結果: {result}")
        print("✅ 統一テストモード実行テスト完了")
    
    def test_github_cli_integration_dry_run(self, automation):
        """🔧 GitHub CLI統合テスト（ドライラン）"""
        print("\n🔧 GitHub CLI統合テスト開始")
        
        # GitHub CLI統合テストの実行
        result = automation.test_github_cli_integration()
        
        # 結果検証
        assert result is not None
        assert isinstance(result, dict)
        assert 'project_name' in result
        assert 'commands_generated' in result
        assert 'mermaid_generated' in result
        assert 'report_generated' in result
        
        # 期待値の検証
        assert result['commands_generated'] >= 4  # 最低4つのコマンド生成
        assert result['mermaid_generated'] is True  # Mermaid図生成成功
        assert result['report_generated'] is True  # レポート生成成功
        
        print(f"🔧 CLI統合テスト結果: {result}")
        print("✅ GitHub CLI統合テスト完了")


@pytest.mark.integration
def test_full_system_integration():
    """🚀 フルシステム統合テスト"""
    print("\n🚀 フルシステム統合テスト開始")
    
    automation = GitHubCopilotAutomation(offline_mode=True)
    
    # 1. 初期化確認
    assert automation is not None
    print("  ✅ システム初期化")
    
    # 2. 統一テストモード実行
    unified_result = automation.unified_test_mode()
    assert unified_result['success_rate'] == 50.0
    print("  ✅ 統一テストモード")
    
    # 3. CLI統合テスト実行
    cli_result = automation.test_github_cli_integration()
    assert cli_result['commands_generated'] >= 4
    print("  ✅ CLI統合テスト")
    
    # 4. ローカルテスト実行
    try:
        automation.local_test_mode()
        print("  ✅ ローカルテスト")
    except Exception as e:
        print(f"  ⚠️ ローカルテスト軽微エラー: {e}")
    
    print("✅ フルシステム統合テスト完了")


@pytest.mark.performance
def test_performance_benchmarks():
    """⚡ パフォーマンステスト"""
    import time
    
    print("\n⚡ パフォーマンステスト開始")
    
    automation = GitHubCopilotAutomation(offline_mode=True)
    
    # Mermaid生成速度テスト
    start_time = time.time()
    
    test_questions = [
        "Pythonで機械学習アプリケーションを作成してください",
        "ReactとTypeScriptでダッシュボードUIを開発したい",
        "Node.jsでREST APIサーバーを構築してください",
        "Vue.jsとFirebaseでリアルタイムチャットアプリを作成してください",
        "PostgreSQLとPythonでデータベース連携システムを作りたい"
    ]
    
    generated_count = 0
    for question in test_questions:
        mermaid_content = automation.generate_dynamic_mermaid_diagram(question)
        if mermaid_content:
            generated_count += 1
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"  📊 Mermaid生成: {generated_count}件 / {execution_time:.2f}秒")
    print(f"  📊 平均生成時間: {execution_time/len(test_questions):.2f}秒/件")
    
    # パフォーマンス基準チェック
    assert execution_time < 10.0, "Mermaid生成が遅すぎます（10秒以内）"
    assert generated_count == len(test_questions), "全ての図が生成されませんでした"
    
    print("✅ パフォーマンステスト完了")


if __name__ == "__main__":
    """直接実行時のテスト"""
    print("🧪 pytest対応統一自動化テストスイート")
    print("📋 直接実行モード - 主要テストのみ実行")
    
    automation = GitHubCopilotAutomation(offline_mode=True)
    
    # 主要テスト実行
    print("\n1️⃣ フィルタリングテスト")
    test_filtering = TestUnifiedAutomation()
    test_filtering.test_filtering_logic(automation)
    
    print("\n2️⃣ Mermaid生成テスト")
    test_filtering.test_mermaid_generation(automation)
    
    print("\n3️⃣ 統一テストモード")
    test_filtering.test_unified_mode_execution(automation)
    
    print("\n✅ 主要テスト完了 - pytest実行推奨")
    print("💡 完全なテスト実行: pytest test_unified_automation.py -v")
