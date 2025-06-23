"""
🧪 単体テスト

テストフレームワークの単体テスト実装
"""

import pytest
import unittest
from src.core.test_framework import TestFramework, PerformanceTest

class TestTestFramework(unittest.TestCase):
    """TestFrameworkクラスのテスト"""
    
    def setUp(self):
        """テスト前準備"""
        self.framework = TestFramework()
    
    def test_framework_initialization(self):
        """フレームワーク初期化テスト"""
        self.assertIsInstance(self.framework, TestFramework)
        self.assertEqual(self.framework.results, [])
        self.assertIsNone(self.framework.start_time)
    
    def test_run_test_suite(self):
        """テストスイート実行テスト"""
        results = self.framework.run_test_suite(['unit'])
        
        self.assertIn('timestamp', results)
        self.assertIn('results', results)
        self.assertIn('duration', results)
        self.assertEqual(results['status'], 'SUCCESS')
    
    def test_specific_test_execution(self):
        """特定テスト実行テスト"""
        result = self.framework._run_specific_tests('unit')
        
        self.assertEqual(result['test_type'], 'unit')
        self.assertTrue(result['passed'])
        self.assertGreater(result['total_tests'], 0)
    
    def test_report_generation(self):
        """レポート生成テスト"""
        results = self.framework.run_test_suite(['unit'])
        report_path = self.framework.generate_report(results, 'test_output.json')
        
        self.assertIsInstance(report_path, str)
        self.assertTrue(report_path.endswith('.json'))

class TestPerformanceTest(unittest.TestCase):
    """PerformanceTestクラスのテスト"""
    
    def test_execution_time_measurement(self):
        """実行時間測定テスト"""
        def sample_function():
            return sum(range(1000))
        
        result = PerformanceTest.measure_execution_time(sample_function)
        
        self.assertIn('result', result)
        self.assertIn('execution_time', result)
        self.assertIn('timestamp', result)
        self.assertGreater(result['execution_time'], 0)
    
    def test_load_test(self):
        """負荷テストテスト"""
        def sample_function():
            return 42
        
        result = PerformanceTest.load_test(sample_function, iterations=10)
        
        self.assertEqual(result['iterations'], 10)
        self.assertIn('average_time', result)
        self.assertIn('min_time', result)
        self.assertIn('max_time', result)

@pytest.mark.parametrize("test_type", ["unit", "integration", "e2e"])
def test_different_test_types(test_type):
    """異なるテストタイプのパラメータ化テスト"""
    framework = TestFramework()
    result = framework._run_specific_tests(test_type)
    
    assert result['test_type'] == test_type
    assert result['passed'] is True
    assert result['total_tests'] > 0

def test_full_integration():
    """統合テスト"""
    framework = TestFramework()
    results = framework.run_test_suite()
    report_path = framework.generate_report(results)
    
    assert results['status'] == 'SUCCESS'
    assert 'unit' in results['results']
    assert 'integration' in results['results']
    assert 'e2e' in results['results']

if __name__ == "__main__":
    unittest.main()
