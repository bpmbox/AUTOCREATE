"""
高度なテスト実行エンジン - Test Runner Module

テストの発見、実行、結果収集を行うメインエンジン
並列実行、フィルタリング、レポート生成をサポート
"""

import asyncio
import concurrent.futures
import time
import threading
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
import json
import logging
from dataclasses import dataclass, field
from enum import Enum

class TestStatus(Enum):
    """テスト実行ステータス"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

@dataclass
class TestResult:
    """テスト結果データクラス"""
    test_name: str
    status: TestStatus
    duration: float
    message: str = ""
    traceback: str = ""
    assertions: int = 0
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

class TestRunner:
    """
    高度なテスト実行エンジン
    
    Features:
    - 並列テスト実行
    - リアルタイム進捗表示
    - フィルタリング・選択実行
    - 結果収集・レポート生成
    - パフォーマンス測定
    """
    
    def __init__(self, 
                 max_workers: int = 4,
                 timeout: float = 300.0,
                 output_dir: str = "reports"):
        """
        テストランナー初期化
        
        Args:
            max_workers: 並列実行する最大ワーカー数
            timeout: テスト全体のタイムアウト（秒）
            output_dir: レポート出力ディレクトリ
        """
        self.max_workers = max_workers
        self.timeout = timeout
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 実行状態管理
        self.tests: List[Callable] = []
        self.results: List[TestResult] = []
        self.running_tests: Dict[str, threading.Thread] = {}
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
        # ログ設定
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # 統計情報
        self.stats = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def discover_tests(self, test_dir: str = "tests", pattern: str = "test_*.py") -> List[str]:
        """
        テストファイルを自動発見
        
        Args:
            test_dir: テストディレクトリ
            pattern: ファイルパターン
            
        Returns:
            発見されたテストファイルのリスト
        """
        test_path = Path(test_dir)
        if not test_path.exists():
            self.logger.warning(f"テストディレクトリが存在しません: {test_dir}")
            return []
        
        test_files = []
        for file_path in test_path.rglob(pattern):
            if file_path.is_file():
                test_files.append(str(file_path))
        
        self.logger.info(f"発見されたテストファイル: {len(test_files)}個")
        return sorted(test_files)
    
    def add_test(self, test_func: Callable, name: Optional[str] = None):
        """
        テスト関数を追加
        
        Args:
            test_func: テスト関数
            name: テスト名（省略時は関数名を使用）
        """
        if name is None:
            name = getattr(test_func, '__name__', str(test_func))
        
        # テスト関数に名前を設定
        test_func._test_name = name
        self.tests.append(test_func)
        self.logger.debug(f"テスト追加: {name}")
    
    def run_single_test(self, test_func: Callable) -> TestResult:
        """
        単一テストの実行
        
        Args:
            test_func: 実行するテスト関数
            
        Returns:
            テスト結果
        """
        test_name = getattr(test_func, '_test_name', str(test_func))
        start_time = time.time()
        
        try:
            self.logger.info(f"テスト実行開始: {test_name}")
            
            # テスト実行
            result = test_func()
            duration = time.time() - start_time
            
            # 成功判定
            if result is None or result is True:
                status = TestStatus.PASSED
                message = "テスト成功"
            else:
                status = TestStatus.FAILED
                message = f"テスト失敗: {result}"
            
            self.logger.info(f"テスト完了: {test_name} ({duration:.3f}s)")
            
        except AssertionError as e:
            duration = time.time() - start_time
            status = TestStatus.FAILED
            message = f"アサーション失敗: {str(e)}"
            traceback = str(e)
            self.logger.error(f"テスト失敗: {test_name} - {message}")
            
        except Exception as e:
            duration = time.time() - start_time
            status = TestStatus.ERROR
            message = f"実行エラー: {str(e)}"
            traceback = str(e)
            self.logger.error(f"テストエラー: {test_name} - {message}")
        
        return TestResult(
            test_name=test_name,
            status=status,
            duration=duration,
            message=message,
            traceback=getattr(locals(), 'traceback', ''),
            timestamp=start_time
        )
    
    def run_tests_parallel(self) -> List[TestResult]:
        """
        テストを並列実行
        
        Returns:
            全テスト結果のリスト
        """
        if not self.tests:
            self.logger.warning("実行するテストがありません")
            return []
        
        self.start_time = time.time()
        self.logger.info(f"並列テスト実行開始: {len(self.tests)}個のテスト")
        
        results = []
        
        # ThreadPoolExecutorで並列実行
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 全テストを並列で開始
            future_to_test = {
                executor.submit(self.run_single_test, test): test 
                for test in self.tests
            }
            
            # 結果を順次収集
            for future in concurrent.futures.as_completed(future_to_test, timeout=self.timeout):
                test = future_to_test[future]
                try:
                    result = future.result()
                    results.append(result)
                    self._update_stats(result)
                    
                except Exception as e:
                    test_name = getattr(test, '_test_name', str(test))
                    error_result = TestResult(
                        test_name=test_name,
                        status=TestStatus.ERROR,
                        duration=0.0,
                        message=f"並列実行エラー: {str(e)}",
                        traceback=str(e)
                    )
                    results.append(error_result)
                    self._update_stats(error_result)
        
        self.end_time = time.time()
        self.results = results
        
        self.logger.info(f"並列テスト実行完了: {len(results)}個の結果")
        return results
    
    def run_tests_sequential(self) -> List[TestResult]:
        """
        テストを順次実行
        
        Returns:
            全テスト結果のリスト
        """
        if not self.tests:
            self.logger.warning("実行するテストがありません")
            return []
        
        self.start_time = time.time()
        self.logger.info(f"順次テスト実行開始: {len(self.tests)}個のテスト")
        
        results = []
        
        for i, test in enumerate(self.tests, 1):
            self.logger.info(f"進捗: {i}/{len(self.tests)}")
            
            result = self.run_single_test(test)
            results.append(result)
            self._update_stats(result)
        
        self.end_time = time.time()
        self.results = results
        
        self.logger.info(f"順次テスト実行完了: {len(results)}個の結果")
        return results
    
    def _update_stats(self, result: TestResult):
        """統計情報更新"""
        self.stats['total'] += 1
        
        if result.status == TestStatus.PASSED:
            self.stats['passed'] += 1
        elif result.status == TestStatus.FAILED:
            self.stats['failed'] += 1
        elif result.status == TestStatus.SKIPPED:
            self.stats['skipped'] += 1
        elif result.status == TestStatus.ERROR:
            self.stats['errors'] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """
        実行サマリーを取得
        
        Returns:
            実行結果のサマリー情報
        """
        total_duration = 0.0
        if self.start_time and self.end_time:
            total_duration = self.end_time - self.start_time
        
        return {
            'timestamp': time.time(),
            'total_duration': total_duration,
            'total_tests': len(self.results),
            'statistics': self.stats.copy(),
            'success_rate': (self.stats['passed'] / max(self.stats['total'], 1)) * 100,
            'fastest_test': min((r.duration for r in self.results), default=0.0),
            'slowest_test': max((r.duration for r in self.results), default=0.0),
            'average_duration': sum(r.duration for r in self.results) / max(len(self.results), 1)
        }
    
    def generate_json_report(self, filename: str = "test_results.json"):
        """
        JSON形式でレポート生成
        
        Args:
            filename: 出力ファイル名
        """
        report_data = {
            'summary': self.get_summary(),
            'results': [
                {
                    'test_name': r.test_name,
                    'status': r.status.value,
                    'duration': r.duration,
                    'message': r.message,
                    'traceback': r.traceback,
                    'assertions': r.assertions,
                    'timestamp': r.timestamp,
                    'metadata': r.metadata
                }
                for r in self.results
            ]
        }
        
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"JSONレポート生成: {output_path}")
        return output_path
    
    def print_summary(self):
        """実行サマリーをコンソールに出力"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("🧪 テスト実行サマリー")
        print("="*60)
        print(f"📊 総テスト数: {summary['total_tests']}")
        print(f"✅ 成功: {self.stats['passed']}")
        print(f"❌ 失敗: {self.stats['failed']}")
        print(f"⚠️  エラー: {self.stats['errors']}")
        print(f"⏭️  スキップ: {self.stats['skipped']}")
        print(f"🎯 成功率: {summary['success_rate']:.1f}%")
        print(f"⏱️  総実行時間: {summary['total_duration']:.3f}秒")
        print(f"📈 平均実行時間: {summary['average_duration']:.3f}秒")
        print(f"🚀 最速テスト: {summary['fastest_test']:.3f}秒")
        print(f"🐌 最遅テスト: {summary['slowest_test']:.3f}秒")
        print("="*60)
        
        # 失敗したテストの詳細表示
        failed_tests = [r for r in self.results if r.status in [TestStatus.FAILED, TestStatus.ERROR]]
        if failed_tests:
            print("\n❌ 失敗したテスト:")
            for result in failed_tests:
                print(f"  • {result.test_name}: {result.message}")
        
        print()

# 使用例とデモ
if __name__ == "__main__":
    
    def sample_test_1():
        """サンプルテスト1: 成功"""
        assert 1 + 1 == 2
        return True
    
    def sample_test_2():
        """サンプルテスト2: 失敗"""
        assert 1 + 1 == 3  # 意図的な失敗
    
    def sample_test_3():
        """サンプルテスト3: エラー"""
        raise ValueError("テストエラーのデモ")
    
    def sample_test_4():
        """サンプルテスト4: 時間のかかるテスト"""
        import time
        time.sleep(0.5)  # 0.5秒待機
        assert True
    
    # テストランナーの使用例
    runner = TestRunner(max_workers=2)
    
    # テスト追加
    runner.add_test(sample_test_1, "基本的な計算テスト")
    runner.add_test(sample_test_2, "失敗デモテスト")
    runner.add_test(sample_test_3, "エラーデモテスト")
    runner.add_test(sample_test_4, "時間のかかるテスト")
    
    # 並列実行
    print("🚀 並列テスト実行中...")
    results = runner.run_tests_parallel()
    
    # 結果表示
    runner.print_summary()
    
    # JSONレポート生成
    report_path = runner.generate_json_report()
    print(f"📄 詳細レポート: {report_path}")
