#!/usr/bin/env python3
"""
🧪 自動化システムテスト - FastAPI自動作成システムの専用テスト
==============================================================

新しく作成したautomation_api.pyのエンドポイントをテストします
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8001"

def test_automation_api():
    """自動化APIの統合テスト"""
    print("🧪 自動化API統合テストを開始...")
    print("=" * 60)
    
    test_results = []
    
    # 1. ルートエンドポイントテスト
    print("📋 1. ルートエンドポイント (/) のテスト")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ ルートエンドポイント: OK")
            print(f"   メッセージ: {data.get('message', 'N/A')}")
            print(f"   機能数: {len(data.get('features', []))}")
            test_results.append(("root", True))
        else:
            print(f"❌ ルートエンドポイント: {response.status_code}")
            test_results.append(("root", False))
    except Exception as e:
        print(f"❌ ルートエンドポイント接続エラー: {e}")
        test_results.append(("root", False))
    
    # 2. ステータスエンドポイントテスト
    print("\n📋 2. ステータスエンドポイント (/api/status) のテスト")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ ステータスエンドポイント: OK")
            print(f"   サービス: {data.get('service', 'N/A')}")
            print(f"   バージョン: {data.get('version', 'N/A')}")
            test_results.append(("status", True))
        else:
            print(f"❌ ステータスエンドポイント: {response.status_code}")
            test_results.append(("status", False))
    except Exception as e:
        print(f"❌ ステータスエンドポイント接続エラー: {e}")
        test_results.append(("status", False))
    
    # 3. ヘルスチェックテスト
    print("\n📋 3. ヘルスチェック (/health) のテスト")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ ヘルスチェック: OK")
            print(f"   ステータス: {data.get('status', 'N/A')}")
            checks = data.get('checks', {})
            for check_name, check_result in checks.items():
                status = "✅" if check_result else "❌"
                print(f"   {status} {check_name}")
            test_results.append(("health", True))
        else:
            print(f"❌ ヘルスチェック: {response.status_code}")
            test_results.append(("health", False))
    except Exception as e:
        print(f"❌ ヘルスチェック接続エラー: {e}")
        test_results.append(("health", False))
    
    # 4. Copilot状態確認テスト
    print("\n📋 4. Copilot自動化システム (/automation/copilot) のテスト")
    try:
        response = requests.get(f"{BASE_URL}/automation/copilot")
        if response.status_code == 200:
            data = response.json()
            print("✅ Copilot状態確認: OK")
            print(f"   ステータス: {data.get('status', 'N/A')}")
            print(f"   オフラインモード: {data.get('offline_mode', 'N/A')}")
            print(f"   座標読み込み: {data.get('coordinates_loaded', 'N/A')}")
            features = data.get('features', [])
            print(f"   利用可能機能: {len(features)}個")
            test_results.append(("copilot", True))
        else:
            print(f"❌ Copilot状態確認: {response.status_code}")
            test_results.append(("copilot", False))
    except Exception as e:
        print(f"❌ Copilot状態確認接続エラー: {e}")
        test_results.append(("copilot", False))
    
    # 5. 自動化トリガーテスト（基本）
    print("\n📋 5. 自動化トリガー (/automation/trigger) の基本テスト")
    try:
        test_data = {
            "message": "FastAPI自動化システムのテストプロジェクトを作成してください",
            "user": "test_user",
            "project_type": "fastapi",
            "auto_create": False
        }
        
        response = requests.post(f"{BASE_URL}/automation/trigger", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ 自動化トリガー（基本）: OK")
            print(f"   ステータス: {data.get('status', 'N/A')}")
            print(f"   メッセージ: {data.get('message', 'N/A')}")
            print(f"   自動化ID: {data.get('automation_id', 'N/A')}")
            test_results.append(("trigger_basic", True))
        else:
            print(f"❌ 自動化トリガー（基本）: {response.status_code}")
            test_results.append(("trigger_basic", False))
    except Exception as e:
        print(f"❌ 自動化トリガー（基本）接続エラー: {e}")
        test_results.append(("trigger_basic", False))
    
    # 6. 自動化トリガーテスト（自動作成）
    print("\n📋 6. 自動化トリガー (/automation/trigger) の自動作成テスト")
    try:
        test_data = {
            "message": "Vue.jsでダッシュボード画面を作成してください",
            "user": "test_user",
            "project_type": "vue",
            "auto_create": True
        }
        
        response = requests.post(f"{BASE_URL}/automation/trigger", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ 自動化トリガー（自動作成）: OK")
            print(f"   ステータス: {data.get('status', 'N/A')}")
            print(f"   プロジェクト名: {data.get('project_name', 'N/A')}")
            print(f"   Mermaidファイル: {data.get('mermaid_file', 'N/A')}")
            test_results.append(("trigger_autocreate", True))
        else:
            print(f"❌ 自動化トリガー（自動作成）: {response.status_code}")
            test_results.append(("trigger_autocreate", False))
    except Exception as e:
        print(f"❌ 自動化トリガー（自動作成）接続エラー: {e}")
        test_results.append(("trigger_autocreate", False))
    
    # 7. 統合テストエンドポイント
    print("\n📋 7. 統合テスト (/automation/test) のテスト")
    try:
        response = requests.post(f"{BASE_URL}/automation/test")
        if response.status_code == 200:
            data = response.json()
            print("✅ 統合テスト: OK")
            summary = data.get('test_summary', {})
            print(f"   成功率: {summary.get('success_rate', 'N/A')}")
            print(f"   成功/総数: {summary.get('passed', 0)}/{summary.get('total', 0)}")
            
            results = data.get('test_results', {})
            for test_name, result in results.items():
                if isinstance(result, dict) and 'status' in result:
                    status = "✅" if result['status'] == 'ok' else "❌"
                    print(f"   {status} {test_name}: {result['status']}")
            
            test_results.append(("integration", True))
        else:
            print(f"❌ 統合テスト: {response.status_code}")
            test_results.append(("integration", False))
    except Exception as e:
        print(f"❌ 統合テスト接続エラー: {e}")
        test_results.append(("integration", False))
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 テスト結果サマリー")
    print("=" * 60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"✅ 成功: {passed}/{total} テスト")
    print(f"📈 成功率: {success_rate:.1f}%")
    
    print("\n📋 詳細結果:")
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    if success_rate >= 80:
        print("\n🎉 自動化システムは正常に動作しています！")
    elif success_rate >= 50:
        print("\n⚠️ 一部の機能に問題がありますが、基本動作は確認できました。")
    else:
        print("\n❌ 重要な問題が検出されました。システムの確認が必要です。")
    
    return success_rate >= 80

if __name__ == "__main__":
    print("🚀 FastAPI自動化システムテスト開始")
    print(f"🌐 テスト対象: {BASE_URL}")
    print(f"⏰ 開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # サーバーの起動を少し待つ
    print("⏳ サーバーの準備を待機中...")
    time.sleep(2)
    
    success = test_automation_api()
    exit(0 if success else 1)
