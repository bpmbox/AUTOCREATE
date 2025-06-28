#!/usr/bin/env python3
"""
🧪 FastAPI AI自動化システム 拡張テストスイート
=============================================

より詳細で包括的なテストを実行
"""

import requests
import json
import time
import threading
from datetime import datetime
from pprint import pprint

# サーバーのベースURL
BASE_URL = "http://localhost:7862"

class FastAPITestSuite:
    def __init__(self):
        self.passed_tests = 0
        self.total_tests = 0
        self.test_results = []
        
    def run_test(self, test_name, test_func):
        """個別テストを実行"""
        self.total_tests += 1
        print(f"\n🧪 テスト {self.total_tests}: {test_name}")
        print("=" * 50)
        
        start_time = time.time()
        try:
            success = test_func()
            execution_time = time.time() - start_time
            
            if success:
                print(f"✅ {test_name}: 成功 ({execution_time:.2f}秒)")
                self.passed_tests += 1
                status = "SUCCESS"
            else:
                print(f"❌ {test_name}: 失敗 ({execution_time:.2f}秒)")
                status = "FAILED"
                
            self.test_results.append({
                "name": test_name,
                "status": status,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"💥 {test_name}: 例外発生 - {e} ({execution_time:.2f}秒)")
            self.test_results.append({
                "name": test_name,
                "status": "ERROR",
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            })
        
        time.sleep(0.5)  # テスト間の待機

    def test_basic_connectivity(self):
        """基本接続テスト"""
        try:
            response = requests.get(f"{BASE_URL}/automation/health", timeout=10)
            print(f"📡 接続テスト: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 接続エラー: {e}")
            return False

    def test_system_status_detailed(self):
        """詳細システム状態テスト"""
        try:
            response = requests.get(f"{BASE_URL}/automation/status")
            result = response.json()
            
            print(f"📊 システム状態:")
            print(f"   - ステータス: {result.get('status')}")
            print(f"   - GitHub CLI: {result.get('github_cli_available')}")
            print(f"   - Supabase: {result.get('supabase_connected')}")
            
            env_vars = result.get('environment_variables', {})
            print(f"   - 環境変数:")
            for key, value in env_vars.items():
                print(f"     • {key}: {'✅' if value else '❌'}")
            
            return response.status_code == 200 and result.get('status') == 'healthy'
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False

    def test_multiple_mermaid_generations(self):
        """複数のMermaid図生成テスト"""
        test_prompts = [
            "Pythonでウェブスクレイピングシステムを作成",
            "ReactとNode.jsでECサイトを構築",
            "機械学習を使った画像分類システム",
            "DockerとKubernetesでマイクロサービス"
        ]
        
        success_count = 0
        for i, prompt in enumerate(test_prompts, 1):
            try:
                data = {
                    "content": prompt,
                    "diagram_type": "flowchart"
                }
                response = requests.post(f"{BASE_URL}/automation/mermaid/generate", json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    success_count += 1
                    print(f"   📈 テスト {i}: 成功 - {len(result.get('mermaid_content', ''))} 文字")
                else:
                    print(f"   ❌ テスト {i}: 失敗 - {response.status_code}")
                
                time.sleep(1)  # 各リクエスト間の待機
                
            except Exception as e:
                print(f"   💥 テスト {i}: エラー - {e}")
        
        print(f"📊 結果: {success_count}/{len(test_prompts)} 成功")
        return success_count == len(test_prompts)

    def test_automation_run_variations(self):
        """自動化実行のバリエーションテスト"""
        test_cases = [
            {
                "name": "基本実行",
                "data": {
                    "message": "Hello Worldプログラムを作成",
                    "create_issue": False,
                    "generate_mermaid": True,
                    "offline_mode": True
                }
            },
            {
                "name": "Mermaid無効",
                "data": {
                    "message": "シンプルなウェブページを作成",
                    "create_issue": False,
                    "generate_mermaid": False,
                    "offline_mode": True
                }
            },
            {
                "name": "長い質問",
                "data": {
                    "message": "大規模なマイクロサービスアーキテクチャを使用したeコマースプラットフォームを構築し、ユーザー認証、商品管理、注文処理、支払い統合を含む完全なソリューションを作成してください",
                    "create_issue": False,
                    "generate_mermaid": True,
                    "offline_mode": True
                }
            }
        ]
        
        success_count = 0
        for test_case in test_cases:
            try:
                response = requests.post(f"{BASE_URL}/automation/run", json=test_case["data"])
                if response.status_code == 200:
                    result = response.json()
                    success_count += 1
                    print(f"   ✅ {test_case['name']}: 成功")
                    print(f"      処理時間: {result.get('processing_time', 'N/A')}秒")
                else:
                    print(f"   ❌ {test_case['name']}: 失敗 - {response.status_code}")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"   💥 {test_case['name']}: エラー - {e}")
        
        return success_count == len(test_cases)

    def test_background_service_interaction(self):
        """バックグラウンドサービス連携テスト"""
        try:
            # 状態確認
            status_response = requests.get(f"{BASE_URL}/background/status")
            if status_response.status_code != 200:
                return False
                
            status = status_response.json()
            print(f"📊 バックグラウンドサービス状態:")
            print(f"   - 実行中: {status.get('is_running')}")
            print(f"   - スレッド生存: {status.get('thread_alive')}")
            print(f"   - 間隔: {status.get('loop_interval')}秒")
            print(f"   - 最終チェック: {status.get('last_check')}")
            
            # 複数回状態チェック
            print(f"🔄 連続状態チェック:")
            for i in range(3):
                response = requests.get(f"{BASE_URL}/background/status")
                if response.status_code == 200:
                    print(f"   チェック {i+1}: ✅")
                else:
                    print(f"   チェック {i+1}: ❌")
                    return False
                time.sleep(2)
            
            return True
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False

    def test_api_documentation_completeness(self):
        """API ドキュメント完全性テスト"""
        try:
            # OpenAPI JSON 取得
            response = requests.get(f"{BASE_URL}/openapi.json")
            if response.status_code != 200:
                return False
                
            openapi_spec = response.json()
            paths = openapi_spec.get('paths', {})
            
            print(f"📖 API ドキュメント分析:")
            print(f"   - 総エンドポイント数: {len(paths)}")
            
            # エンドポイント分析
            method_counts = {}
            for path, methods in paths.items():
                for method in methods.keys():
                    method_counts[method.upper()] = method_counts.get(method.upper(), 0) + 1
            
            print(f"   - HTTPメソッド分布:")
            for method, count in method_counts.items():
                print(f"     • {method}: {count}個")
            
            # 必須エンドポイントの確認
            required_endpoints = [
                "/automation/status",
                "/automation/health",
                "/automation/run",
                "/automation/mermaid/generate",
                "/background/status"
            ]
            
            missing_endpoints = []
            for endpoint in required_endpoints:
                if endpoint not in paths:
                    missing_endpoints.append(endpoint)
            
            if missing_endpoints:
                print(f"   ❌ 不足エンドポイント: {missing_endpoints}")
                return False
            else:
                print(f"   ✅ 全必須エンドポイント確認済み")
            
            return True
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False

    def test_performance_stress(self):
        """パフォーマンス・ストレステスト"""
        print(f"🚀 パフォーマンステスト開始...")
        
        def make_request():
            try:
                response = requests.get(f"{BASE_URL}/automation/health", timeout=5)
                return response.status_code == 200
            except:
                return False
        
        # 並行リクエストテスト
        threads = []
        results = []
        start_time = time.time()
        
        for i in range(10):  # 10並行リクエスト
            thread = threading.Thread(target=lambda: results.append(make_request()))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        success_count = sum(results)
        total_time = end_time - start_time
        
        print(f"📊 並行リクエスト結果:")
        print(f"   - 成功: {success_count}/10")
        print(f"   - 総時間: {total_time:.2f}秒")
        print(f"   - 平均レスポンス時間: {total_time/10:.3f}秒")
        
        return success_count >= 8  # 80%以上成功で合格

    def test_error_handling(self):
        """エラーハンドリングテスト"""
        error_tests = [
            {
                "name": "不正なJSON",
                "url": f"{BASE_URL}/automation/run",
                "data": "invalid_json",
                "expected_status": 422
            },
            {
                "name": "必須フィールド欠如",
                "url": f"{BASE_URL}/automation/mermaid/generate",
                "data": {"diagram_type": "flowchart"},  # contentフィールドなし
                "expected_status": 422
            },
            {
                "name": "存在しないエンドポイント",
                "url": f"{BASE_URL}/nonexistent/endpoint",
                "data": {},
                "expected_status": 404
            }
        ]
        
        success_count = 0
        for test in error_tests:
            try:
                if isinstance(test["data"], str):
                    response = requests.post(test["url"], data=test["data"])
                else:
                    response = requests.post(test["url"], json=test["data"])
                
                if response.status_code == test["expected_status"]:
                    print(f"   ✅ {test['name']}: 期待通りのエラー ({response.status_code})")
                    success_count += 1
                else:
                    print(f"   ❌ {test['name']}: 予期しないステータス ({response.status_code})")
                    
            except Exception as e:
                print(f"   💥 {test['name']}: 例外 - {e}")
        
        return success_count == len(error_tests)

    def generate_test_report(self):
        """テスト結果レポート生成"""
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎯 FastAPI AI自動化システム 拡張テスト レポート")
        print("=" * 60)
        print(f"📊 テスト結果: {self.passed_tests}/{self.total_tests} 成功")
        print(f"📈 成功率: {success_rate:.1f}%")
        print(f"⏱️  実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📋 詳細結果:")
        for i, result in enumerate(self.test_results, 1):
            status_emoji = "✅" if result["status"] == "SUCCESS" else "❌" if result["status"] == "FAILED" else "💥"
            print(f"   {i:2d}. {status_emoji} {result['name']} ({result['execution_time']:.2f}s)")
        
        # 推奨アクション
        print(f"\n🎯 評価:")
        if success_rate >= 90:
            print("🎉 優秀！システムは非常に安定して動作しています")
        elif success_rate >= 70:
            print("✅ 良好！一部改善の余地がありますが、全体的に良好です")
        elif success_rate >= 50:
            print("⚠️  注意！複数の問題があります。改善が必要です")
        else:
            print("🚨 重要！多数の問題があります。システムの見直しが必要です")
        
        print(f"\n🔗 システム情報:")
        print(f"   - サーバー: {BASE_URL}")
        print(f"   - Swagger UI: {BASE_URL}/docs")
        print(f"   - システム状態: {BASE_URL}/automation/status")

    def run_all_tests(self):
        """全テストを実行"""
        print("🚀 FastAPI AI自動化システム 拡張テストスイート開始")
        print(f"⏰ 開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # テスト実行
        self.run_test("基本接続テスト", self.test_basic_connectivity)
        self.run_test("詳細システム状態テスト", self.test_system_status_detailed)
        self.run_test("複数Mermaid図生成テスト", self.test_multiple_mermaid_generations)
        self.run_test("自動化実行バリエーションテスト", self.test_automation_run_variations)
        self.run_test("バックグラウンドサービス連携テスト", self.test_background_service_interaction)
        self.run_test("APIドキュメント完全性テスト", self.test_api_documentation_completeness)
        self.run_test("パフォーマンス・ストレステスト", self.test_performance_stress)
        self.run_test("エラーハンドリングテスト", self.test_error_handling)
        
        # レポート生成
        self.generate_test_report()

if __name__ == "__main__":
    test_suite = FastAPITestSuite()
    test_suite.run_all_tests()
