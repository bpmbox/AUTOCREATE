"""
パフォーマンステスト機能 - Performance Tester Module

実行時間測定、メモリ使用量監視、負荷テスト、ボトルネック検出を行う
高度なパフォーマンステストフレームワーク
"""

import time
import psutil
import threading
import concurrent.futures
import memory_profiler
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from contextlib import contextmanager
import matplotlib.pyplot as plt
import json
from pathlib import Path
import statistics

@dataclass
class PerformanceMetrics:
    """パフォーマンス測定結果"""
    test_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    peak_memory: float
    iterations: int
    throughput: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

class PerformanceTester:
    """
    高度なパフォーマンステストフレームワーク
    
    Features:
    - 実行時間測定
    - メモリ使用量監視
    - CPU使用率測定
    - 負荷テスト (Load Testing)
    - ストレステスト (Stress Testing)
    - 結果の可視化・レポート生成
    """
    
    def __init__(self, output_dir: str = "reports/performance"):
        """
        パフォーマンステスター初期化
        
        Args:
            output_dir: レポート出力ディレクトリ
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 測定結果保存
        self.metrics: List[PerformanceMetrics] = []
        self.active_measurements: Dict[str, Dict] = {}
          # システム情報取得
        import platform
        self.system_info = {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'platform': platform.system(),
        }
    
    @contextmanager
    def measure_performance(self, test_name: str, iterations: int = 1):
        """
        パフォーマンス測定コンテキストマネージャー
        
        Args:
            test_name: テスト名
            iterations: 繰り返し回数
        """
        # 測定開始
        start_time = time.time()
        start_memory = psutil.virtual_memory().used
        process = psutil.Process()
        
        # CPU使用率測定用のベースライン
        cpu_before = process.cpu_percent()
        
        measurement_data = {
            'start_time': start_time,
            'start_memory': start_memory,
            'peak_memory': start_memory,
            'cpu_samples': []
        }
        
        self.active_measurements[test_name] = measurement_data
        
        # バックグラウンドでの監視開始
        monitor_thread = threading.Thread(
            target=self._monitor_resources, 
            args=(test_name,), 
            daemon=True
        )
        monitor_thread.start()
        
        try:
            yield self
        finally:
            # 測定終了
            end_time = time.time()
            end_memory = psutil.virtual_memory().used
            cpu_after = process.cpu_percent()
            
            # 結果計算
            execution_time = end_time - start_time
            memory_usage = end_memory - start_memory
            cpu_usage = cpu_after - cpu_before
            peak_memory = measurement_data['peak_memory'] - start_memory
            throughput = iterations / execution_time if execution_time > 0 else 0
            
            # メトリクス保存
            metrics = PerformanceMetrics(
                test_name=test_name,
                execution_time=execution_time,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage,
                peak_memory=peak_memory,
                iterations=iterations,
                throughput=throughput
            )
            
            self.metrics.append(metrics)
            
            # アクティブ測定から削除
            self.active_measurements.pop(test_name, None)
    
    def _monitor_resources(self, test_name: str):
        """
        リソース使用量をバックグラウンドで監視
        
        Args:
            test_name: 監視対象のテスト名
        """
        measurement = self.active_measurements.get(test_name)
        if not measurement:
            return
        
        while test_name in self.active_measurements:
            try:
                current_memory = psutil.virtual_memory().used
                measurement['peak_memory'] = max(
                    measurement['peak_memory'], 
                    current_memory
                )
                
                # CPU使用率サンプル取得
                cpu_percent = psutil.cpu_percent(interval=0.1)
                measurement['cpu_samples'].append(cpu_percent)
                
                time.sleep(0.1)  # 100ms間隔で監視
                
            except Exception:
                break  # エラー時は監視終了
    
    def benchmark_function(self, 
                          func: Callable, 
                          iterations: int = 100,
                          warmup: int = 10,
                          test_name: Optional[str] = None) -> PerformanceMetrics:
        """
        関数のベンチマークテスト
        
        Args:
            func: ベンチマーク対象の関数
            iterations: 実行回数
            warmup: ウォームアップ回数
            test_name: テスト名
            
        Returns:
            パフォーマンス測定結果
        """
        if test_name is None:
            test_name = getattr(func, '__name__', 'benchmark_test')
        
        # ウォームアップ実行
        for _ in range(warmup):
            func()
        
        # 本測定
        with self.measure_performance(test_name, iterations):
            for _ in range(iterations):
                func()
        
        return self.metrics[-1]
    
    def load_test(self, 
                  func: Callable, 
                  concurrent_users: int = 10,
                  duration: float = 30.0,
                  ramp_up: float = 5.0,
                  test_name: Optional[str] = None) -> Dict[str, Any]:
        """
        負荷テスト実行
        
        Args:
            func: テスト対象の関数
            concurrent_users: 同時実行ユーザー数
            duration: テスト実行時間（秒）
            ramp_up: ランプアップ時間（秒）
            test_name: テスト名
            
        Returns:
            負荷テスト結果
        """
        if test_name is None:
            test_name = f"load_test_{getattr(func, '__name__', 'function')}"
        
        results = {
            'test_name': test_name,
            'concurrent_users': concurrent_users,
            'duration': duration,
            'start_time': time.time(),
            'executions': [],
            'errors': [],
            'statistics': {}
        }
        
        def user_simulation():
            """単一ユーザーのシミュレーション"""
            user_results = []
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    start = time.time()
                    func()
                    execution_time = time.time() - start
                    user_results.append({
                        'timestamp': start,
                        'duration': execution_time,
                        'success': True
                    })
                except Exception as e:
                    user_results.append({
                        'timestamp': time.time(),
                        'duration': 0,
                        'success': False,
                        'error': str(e)
                    })
                
                # 少し待機（リアルなユーザー動作をシミュレート）
                time.sleep(0.01)
            
            return user_results
        
        # 並列実行でユーザーをシミュレート
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # ランプアップ期間で段階的にユーザー追加
            futures = []
            for i in range(concurrent_users):
                if i > 0:
                    time.sleep(ramp_up / concurrent_users)
                
                future = executor.submit(user_simulation)
                futures.append(future)
            
            # 全ユーザーの結果を収集
            for future in concurrent.futures.as_completed(futures):
                try:
                    user_results = future.result()
                    results['executions'].extend(user_results)
                except Exception as e:
                    results['errors'].append(str(e))
        
        # 統計計算
        successful_executions = [e for e in results['executions'] if e['success']]
        if successful_executions:
            durations = [e['duration'] for e in successful_executions]
            results['statistics'] = {
                'total_executions': len(results['executions']),
                'successful_executions': len(successful_executions),
                'failed_executions': len(results['executions']) - len(successful_executions),
                'success_rate': len(successful_executions) / len(results['executions']) * 100,
                'average_response_time': statistics.mean(durations),
                'median_response_time': statistics.median(durations),
                'min_response_time': min(durations),
                'max_response_time': max(durations),
                'throughput': len(successful_executions) / duration,
                'total_duration': time.time() - results['start_time']
            }
        
        return results
    
    def stress_test(self, 
                   func: Callable,
                   max_users: int = 100,
                   step_size: int = 10,
                   step_duration: float = 30.0,
                   test_name: Optional[str] = None) -> Dict[str, Any]:
        """
        ストレステスト実行
        
        Args:
            func: テスト対象の関数
            max_users: 最大ユーザー数
            step_size: ステップごとのユーザー増加数
            step_duration: 各ステップの実行時間
            test_name: テスト名
            
        Returns:
            ストレステスト結果
        """
        if test_name is None:
            test_name = f"stress_test_{getattr(func, '__name__', 'function')}"
        
        stress_results = {
            'test_name': test_name,
            'max_users': max_users,
            'step_size': step_size,
            'step_duration': step_duration,
            'steps': [],
            'breaking_point': None
        }
        
        # 段階的にユーザー数を増加
        for users in range(step_size, max_users + 1, step_size):
            print(f"ストレステスト実行中: {users}ユーザー")
            
            # 負荷テスト実行
            load_result = self.load_test(
                func=func,
                concurrent_users=users,
                duration=step_duration,
                ramp_up=step_duration * 0.2,  # 20%をランプアップに使用
                test_name=f"{test_name}_step_{users}"
            )
            
            step_result = {
                'users': users,
                'statistics': load_result['statistics'],
                'system_load': {
                    'cpu_percent': psutil.cpu_percent(),
                    'memory_percent': psutil.virtual_memory().percent,
                    'load_average': getattr(psutil, 'getloadavg', lambda: [0, 0, 0])()
                }
            }
            
            stress_results['steps'].append(step_result)
            
            # 破綻点の検出
            stats = load_result['statistics']
            if (stats['success_rate'] < 95 or  # 成功率95%未満
                stats['average_response_time'] > 5.0 or  # 平均応答時間5秒超
                psutil.cpu_percent() > 90):  # CPU使用率90%超
                
                stress_results['breaking_point'] = {
                    'users': users,
                    'reason': 'パフォーマンス劣化検出',
                    'metrics': step_result
                }
                print(f"破綻点検出: {users}ユーザーでパフォーマンス劣化")
                break
        
        return stress_results
    
    def generate_performance_report(self, filename: str = "performance_report.json"):
        """
        パフォーマンスレポート生成
        
        Args:
            filename: 出力ファイル名
        """
        report_data = {
            'timestamp': time.time(),
            'system_info': self.system_info,
            'test_summary': {
                'total_tests': len(self.metrics),
                'total_execution_time': sum(m.execution_time for m in self.metrics),
                'average_execution_time': statistics.mean([m.execution_time for m in self.metrics]) if self.metrics else 0,
                'peak_memory_usage': max([m.peak_memory for m in self.metrics]) if self.metrics else 0,
                'average_throughput': statistics.mean([m.throughput for m in self.metrics]) if self.metrics else 0
            },
            'metrics': [
                {
                    'test_name': m.test_name,
                    'execution_time': m.execution_time,
                    'memory_usage': m.memory_usage,
                    'cpu_usage': m.cpu_usage,
                    'peak_memory': m.peak_memory,
                    'iterations': m.iterations,
                    'throughput': m.throughput,
                    'timestamp': m.timestamp,
                    'metadata': m.metadata
                }
                for m in self.metrics
            ]
        }
        
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 パフォーマンスレポート生成: {output_path}")
        return output_path
    
    def visualize_performance(self, save_plots: bool = True):
        """
        パフォーマンス結果の可視化
        
        Args:
            save_plots: グラフを保存するかどうか
        """
        if not self.metrics:
            print("可視化するデータがありません")
            return
        
        # 実行時間の可視化
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('パフォーマンステスト結果', fontsize=16)
        
        # 実行時間
        test_names = [m.test_name for m in self.metrics]
        execution_times = [m.execution_time for m in self.metrics]
        
        axes[0, 0].bar(test_names, execution_times)
        axes[0, 0].set_title('実行時間 (秒)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # メモリ使用量
        memory_usage = [m.memory_usage / (1024 * 1024) for m in self.metrics]  # MB変換
        axes[0, 1].bar(test_names, memory_usage)
        axes[0, 1].set_title('メモリ使用量 (MB)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # スループット
        throughput = [m.throughput for m in self.metrics]
        axes[1, 0].bar(test_names, throughput)
        axes[1, 0].set_title('スループット (ops/sec)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 実行時間分布
        axes[1, 1].hist(execution_times, bins=10, alpha=0.7)
        axes[1, 1].set_title('実行時間分布')
        axes[1, 1].set_xlabel('実行時間 (秒)')
        axes[1, 1].set_ylabel('頻度')
        
        plt.tight_layout()
        
        if save_plots:
            plot_path = self.output_dir / "performance_charts.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            print(f"📈 パフォーマンスグラフ保存: {plot_path}")
        
        plt.show()
    
    def print_summary(self):
        """パフォーマンステスト結果サマリー表示"""
        if not self.metrics:
            print("表示するパフォーマンスデータがありません")
            return
        
        print("\n" + "="*70)
        print("🚀 パフォーマンステスト結果サマリー")
        print("="*70)
        
        for metric in self.metrics:
            print(f"\n📊 テスト: {metric.test_name}")
            print(f"   ⏱️  実行時間: {metric.execution_time:.4f}秒")
            print(f"   💾 メモリ使用量: {metric.memory_usage / (1024*1024):.2f}MB")
            print(f"   🖥️  CPU使用率: {metric.cpu_usage:.2f}%")
            print(f"   📈 スループット: {metric.throughput:.2f} ops/sec")
            print(f"   🔄 繰り返し回数: {metric.iterations}")
        
        # 統計情報
        if len(self.metrics) > 1:
            execution_times = [m.execution_time for m in self.metrics]
            memory_usages = [m.memory_usage for m in self.metrics]
            throughputs = [m.throughput for m in self.metrics]
            
            print(f"\n📈 統計情報:")
            print(f"   平均実行時間: {statistics.mean(execution_times):.4f}秒")
            print(f"   最速テスト: {min(execution_times):.4f}秒")
            print(f"   最遅テスト: {max(execution_times):.4f}秒")
            print(f"   平均メモリ使用量: {statistics.mean(memory_usages) / (1024*1024):.2f}MB")
            print(f"   平均スループット: {statistics.mean(throughputs):.2f} ops/sec")
        
        print("="*70)

# 使用例とデモ
if __name__ == "__main__":
    
    def sample_cpu_intensive():
        """CPU集約的な処理のサンプル"""
        result = 0
        for i in range(100000):
            result += i ** 2
        return result
    
    def sample_memory_intensive():
        """メモリ集約的な処理のサンプル"""
        data = []
        for i in range(10000):
            data.append([j for j in range(100)])
        return len(data)
    
    def sample_io_operation():
        """I/O操作のサンプル"""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            for i in range(1000):
                f.write(f"行{i}: テストデータ\n")
            temp_path = f.name
        
        # ファイル読み込み
        with open(temp_path, 'r') as f:
            lines = f.readlines()
        
        # ファイル削除
        os.unlink(temp_path)
        return len(lines)
    
    # パフォーマンステスターの使用例
    tester = PerformanceTester()
    
    # 各テストのベンチマーク
    print("🧪 ベンチマークテスト実行中...")
    
    tester.benchmark_function(sample_cpu_intensive, iterations=50, test_name="CPU集約処理")
    tester.benchmark_function(sample_memory_intensive, iterations=20, test_name="メモリ集約処理")
    tester.benchmark_function(sample_io_operation, iterations=30, test_name="I/O操作")
    
    # 結果表示
    tester.print_summary()
    
    # レポート生成
    tester.generate_performance_report()
    
    # 可視化
    tester.visualize_performance()
    
    # 負荷テストのデモ
    print("\n🔥 負荷テスト実行中...")
    load_result = tester.load_test(
        func=sample_cpu_intensive,
        concurrent_users=5,
        duration=10.0,
        test_name="CPU負荷テスト"
    )
    
    print(f"負荷テスト結果:")
    print(f"  総実行数: {load_result['statistics']['total_executions']}")
    print(f"  成功率: {load_result['statistics']['success_rate']:.1f}%")
    print(f"  平均応答時間: {load_result['statistics']['average_response_time']:.4f}秒")
    print(f"  スループット: {load_result['statistics']['throughput']:.2f} ops/sec")
