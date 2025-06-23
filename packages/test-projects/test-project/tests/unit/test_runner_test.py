"""
テストランナーのユニットテスト

test_runner.py の動作を検証するテストケース
並列実行、順次実行、エラーハンドリング、レポート生成をテスト
"""

import unittest
import time
import threading
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json
from pathlib import Path

# テスト対象のモジュールをインポート
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.test_runner import TestRunner, TestResult, TestStatus

class TestTestRunner(unittest.TestCase):
    """TestRunnerクラスのテストケース"""
    
    def setUp(self):
        """各テストメソッド実行前の準備"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        self.runner = TestRunner(max_workers=2, output_dir=self.temp_dir)
    
    def tearDown(self):
        """各テストメソッド実行後のクリーンアップ"""
        # 一時ディレクトリを削除
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_runner_initialization(self):
        """TestRunnerの初期化テスト"""
        # 基本的な初期化確認
        self.assertEqual(self.runner.max_workers, 2)
        self.assertEqual(self.runner.timeout, 300.0)
        self.assertEqual(len(self.runner.tests), 0)
        self.assertEqual(len(self.runner.results), 0)
        
        # 出力ディレクトリの確認
        self.assertTrue(Path(self.temp_dir).exists())
    
    def test_add_test(self):
        """テスト追加機能のテスト"""
        def sample_test():
            return True
        
        # テスト追加
        self.runner.add_test(sample_test, "サンプルテスト")
        
        # 追加確認
        self.assertEqual(len(self.runner.tests), 1)
        self.assertEqual(self.runner.tests[0]._test_name, "サンプルテスト")
        
        # 名前なしで追加
        def another_test():
            return True
        
        self.runner.add_test(another_test)
        self.assertEqual(len(self.runner.tests), 2)
        self.assertEqual(self.runner.tests[1]._test_name, "another_test")
    
    def test_run_single_test_success(self):
        """単一テスト実行（成功）のテスト"""
        def passing_test():
            return True
        
        passing_test._test_name = "成功テスト"
        
        # テスト実行
        result = self.runner.run_single_test(passing_test)
        
        # 結果確認
        self.assertEqual(result.test_name, "成功テスト")
        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertGreater(result.duration, 0)
        self.assertEqual(result.message, "テスト成功")
    
    def test_run_single_test_failure(self):
        """単一テスト実行（失敗）のテスト"""
        def failing_test():
            assert False, "意図的な失敗"
        
        failing_test._test_name = "失敗テスト"
        
        # テスト実行
        result = self.runner.run_single_test(failing_test)
        
        # 結果確認
        self.assertEqual(result.test_name, "失敗テスト")
        self.assertEqual(result.status, TestStatus.FAILED)
        self.assertIn("意図的な失敗", result.message)
    
    def test_run_single_test_error(self):
        """単一テスト実行（エラー）のテスト"""
        def error_test():
            raise ValueError("テストエラー")
        
        error_test._test_name = "エラーテスト"
        
        # テスト実行
        result = self.runner.run_single_test(error_test)
        
        # 結果確認
        self.assertEqual(result.test_name, "エラーテスト")
        self.assertEqual(result.status, TestStatus.ERROR)
        self.assertIn("テストエラー", result.message)
    
    def test_run_tests_sequential(self):
        """順次テスト実行のテスト"""
        def test1():
            return True
        
        def test2():
            time.sleep(0.1)  # 少し時間をかける
            return True
        
        def test3():
            assert False, "テスト失敗"
        
        # テスト追加
        self.runner.add_test(test1, "テスト1")
        self.runner.add_test(test2, "テスト2")
        self.runner.add_test(test3, "テスト3")
        
        # 順次実行
        results = self.runner.run_tests_sequential()
        
        # 結果確認
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].status, TestStatus.PASSED)
        self.assertEqual(results[1].status, TestStatus.PASSED)
        self.assertEqual(results[2].status, TestStatus.FAILED)
        
        # 統計確認
        self.assertEqual(self.runner.stats['total'], 3)
        self.assertEqual(self.runner.stats['passed'], 2)
        self.assertEqual(self.runner.stats['failed'], 1)
    
    def test_run_tests_parallel(self):
        """並列テスト実行のテスト"""
        def fast_test():
            return True
        
        def slow_test():
            time.sleep(0.2)
            return True
        
        # テスト追加
        self.runner.add_test(fast_test, "高速テスト")
        self.runner.add_test(slow_test, "低速テスト")
        
        # 並列実行
        start_time = time.time()
        results = self.runner.run_tests_parallel()
        total_time = time.time() - start_time
        
        # 結果確認
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.status == TestStatus.PASSED for r in results))
        
        # 並列実行により実行時間が短縮されることを確認
        # (順次実行なら0.2秒以上、並列なら0.2秒程度)
        self.assertLess(total_time, 0.3)
    
    def test_get_summary(self):
        """サマリー取得のテスト"""
        def test1():
            return True
        
        def test2():
            time.sleep(0.1)
            assert False
        
        # テスト追加・実行
        self.runner.add_test(test1, "テスト1")
        self.runner.add_test(test2, "テスト2")
        self.runner.run_tests_sequential()
        
        # サマリー取得
        summary = self.runner.get_summary()
        
        # サマリー内容確認
        self.assertEqual(summary['total_tests'], 2)
        self.assertEqual(summary['statistics']['passed'], 1)
        self.assertEqual(summary['statistics']['failed'], 1)
        self.assertGreater(summary['success_rate'], 0)
        self.assertGreater(summary['total_duration'], 0)
    
    def test_generate_json_report(self):
        """JSONレポート生成のテスト"""
        def sample_test():
            return True
        
        # テスト追加・実行
        self.runner.add_test(sample_test, "JSONレポートテスト")
        self.runner.run_tests_sequential()
        
        # JSONレポート生成
        report_path = self.runner.generate_json_report("test_report.json")
        
        # ファイル存在確認
        self.assertTrue(report_path.exists())
        
        # JSON内容確認
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        self.assertIn('summary', report_data)
        self.assertIn('results', report_data)
        self.assertEqual(len(report_data['results']), 1)
        self.assertEqual(report_data['results'][0]['test_name'], "JSONレポートテスト")
    
    def test_discover_tests(self):
        """テスト発見機能のテスト"""
        # 一時的なテストディレクトリとファイルを作成
        test_dir = Path(self.temp_dir) / "test_discovery"
        test_dir.mkdir()
        
        # テストファイル作成
        (test_dir / "test_example1.py").write_text("# テストファイル1")
        (test_dir / "test_example2.py").write_text("# テストファイル2")
        (test_dir / "not_a_test.py").write_text("# テストファイルではない")
        
        # テスト発見実行
        test_files = self.runner.discover_tests(str(test_dir))
        
        # 結果確認
        self.assertEqual(len(test_files), 2)
        self.assertTrue(any("test_example1.py" in f for f in test_files))
        self.assertTrue(any("test_example2.py" in f for f in test_files))
        self.assertFalse(any("not_a_test.py" in f for f in test_files))
    
    def test_stats_update(self):
        """統計更新のテスト"""
        # 初期状態確認
        self.assertEqual(self.runner.stats['total'], 0)
        
        # 成功結果で更新
        success_result = TestResult("テスト", TestStatus.PASSED, 0.1)
        self.runner._update_stats(success_result)
        
        self.assertEqual(self.runner.stats['total'], 1)
        self.assertEqual(self.runner.stats['passed'], 1)
        
        # 失敗結果で更新
        failure_result = TestResult("テスト", TestStatus.FAILED, 0.1)
        self.runner._update_stats(failure_result)
        
        self.assertEqual(self.runner.stats['total'], 2)
        self.assertEqual(self.runner.stats['failed'], 1)
    
    def test_timeout_handling(self):
        """タイムアウト処理のテスト"""
        def long_running_test():
            time.sleep(2)  # 2秒間処理
            return True
        
        # 短いタイムアウトで実行
        short_timeout_runner = TestRunner(max_workers=1, timeout=1.0)
        short_timeout_runner.add_test(long_running_test, "長時間テスト")
        
        # タイムアウトが発生することを確認
        start_time = time.time()
        try:
            results = short_timeout_runner.run_tests_parallel()
            # タイムアウトにより例外が発生する可能性がある
        except Exception:
            pass  # タイムアウト例外は正常
        
        elapsed_time = time.time() - start_time
        self.assertLess(elapsed_time, 1.5)  # タイムアウト時間より少し長い程度
    
    @patch('builtins.print')
    def test_print_summary(self, mock_print):
        """サマリー出力のテスト"""
        def test1(): return True
        def test2(): assert False
        
        # テスト実行
        self.runner.add_test(test1, "成功テスト")
        self.runner.add_test(test2, "失敗テスト")
        self.runner.run_tests_sequential()
        
        # サマリー出力
        self.runner.print_summary()
        
        # print関数が呼ばれたことを確認
        self.assertTrue(mock_print.called)
        
        # 出力内容の一部確認
        call_args = [str(call) for call in mock_print.call_args_list]
        summary_output = '\n'.join(call_args)
        
        self.assertIn('テスト実行サマリー', summary_output)
        self.assertIn('総テスト数: 2', summary_output)
        self.assertIn('成功: 1', summary_output)
        self.assertIn('失敗: 1', summary_output)

class TestTestResult(unittest.TestCase):
    """TestResultクラスのテストケース"""
    
    def test_test_result_creation(self):
        """TestResult作成のテスト"""
        result = TestResult(
            test_name="サンプルテスト",
            status=TestStatus.PASSED,
            duration=0.123,
            message="成功メッセージ"
        )
        
        self.assertEqual(result.test_name, "サンプルテスト")
        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertEqual(result.duration, 0.123)
        self.assertEqual(result.message, "成功メッセージ")
        self.assertGreater(result.timestamp, 0)
    
    def test_test_result_defaults(self):
        """TestResultのデフォルト値テスト"""
        result = TestResult("テスト", TestStatus.FAILED, 1.0)
        
        self.assertEqual(result.message, "")
        self.assertEqual(result.traceback, "")
        self.assertEqual(result.assertions, 0)
        self.assertEqual(result.metadata, {})

class TestTestStatus(unittest.TestCase):
    """TestStatusクラスのテストケース"""
    
    def test_status_values(self):
        """ステータス値のテスト"""
        self.assertEqual(TestStatus.PENDING.value, "pending")
        self.assertEqual(TestStatus.RUNNING.value, "running")
        self.assertEqual(TestStatus.PASSED.value, "passed")
        self.assertEqual(TestStatus.FAILED.value, "failed")
        self.assertEqual(TestStatus.SKIPPED.value, "skipped")
        self.assertEqual(TestStatus.ERROR.value, "error")

class IntegrationTest(unittest.TestCase):
    """統合テスト"""
    
    def setUp(self):
        """テスト準備"""
        self.temp_dir = tempfile.mkdtemp()
        self.runner = TestRunner(output_dir=self.temp_dir)
    
    def tearDown(self):
        """テスト後処理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_full_workflow(self):
        """完全なワークフローのテスト"""
        # 様々なテストパターンを定義
        def success_test_1():
            """成功テスト1"""
            assert 1 + 1 == 2
            return True
        
        def success_test_2():
            """成功テスト2"""
            time.sleep(0.05)  # 少し時間をかける
            assert "hello".upper() == "HELLO"
            return True
        
        def failure_test():
            """失敗テスト"""
            assert 1 + 1 == 3, "計算が間違っています"
        
        def error_test():
            """エラーテスト"""
            raise RuntimeError("予期しないエラー")
        
        # テスト追加
        self.runner.add_test(success_test_1, "基本計算テスト")
        self.runner.add_test(success_test_2, "文字列操作テスト")
        self.runner.add_test(failure_test, "計算失敗テスト")
        self.runner.add_test(error_test, "ランタイムエラーテスト")
        
        # 並列実行
        results = self.runner.run_tests_parallel()
        
        # 結果検証
        self.assertEqual(len(results), 4)
        
        # 成功テストの確認
        success_results = [r for r in results if r.status == TestStatus.PASSED]
        self.assertEqual(len(success_results), 2)
        
        # 失敗テストの確認
        failed_results = [r for r in results if r.status == TestStatus.FAILED]
        self.assertEqual(len(failed_results), 1)
        self.assertIn("計算が間違っています", failed_results[0].message)
        
        # エラーテストの確認
        error_results = [r for r in results if r.status == TestStatus.ERROR]
        self.assertEqual(len(error_results), 1)
        self.assertIn("予期しないエラー", error_results[0].message)
        
        # 統計確認
        self.assertEqual(self.runner.stats['total'], 4)
        self.assertEqual(self.runner.stats['passed'], 2)
        self.assertEqual(self.runner.stats['failed'], 1)
        self.assertEqual(self.runner.stats['errors'], 1)
        
        # サマリー取得
        summary = self.runner.get_summary()
        self.assertEqual(summary['total_tests'], 4)
        self.assertEqual(summary['success_rate'], 50.0)  # 2/4 = 50%
        
        # JSONレポート生成
        report_path = self.runner.generate_json_report()
        self.assertTrue(report_path.exists())
        
        # レポート内容確認
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        self.assertEqual(len(report_data['results']), 4)
        self.assertEqual(report_data['summary']['total_tests'], 4)

if __name__ == '__main__':
    # テスト実行設定
    unittest.main(verbosity=2, buffer=True)
