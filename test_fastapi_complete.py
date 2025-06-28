#!/usr/bin/env python3
"""
🧪 FastAPI自動化システム テストスクリプト
==================================

FastAPIエンドポイントの基本テスト
"""

import requests
import json
import time
from pprint import pprint

# サーバーのベースURL
BASE_URL = "http://localhost:7862"

def test_automation_status():
    """自動化システムの状態確認テスト"""
    print("🔍 自動化システム状態確認テスト")
    try:
        response = requests.get(f"{BASE_URL}/automation/status")
        print(f"📊 ステータスコード: {response.status_code}")
        print(f"📋 レスポンス:")
        pprint(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_health_check():
    """ヘルスチェックテスト"""
    print("\n💊 ヘルスチェックテスト")
    try:
        response = requests.get(f"{BASE_URL}/automation/health")
        print(f"📊 ステータスコード: {response.status_code}")
        print(f"📋 レスポンス:")
        pprint(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_mermaid_generation():
    """Mermaid図生成テスト"""
    print("\n🎨 Mermaid図生成テスト")
    try:
        data = {
            "content": "FastAPIでリアルタイムチャットシステムを作成してください",
            "diagram_type": "flowchart"
        }
        response = requests.post(f"{BASE_URL}/automation/mermaid/generate", json=data)
        print(f"📊 ステータスコード: {response.status_code}")
        print(f"📋 レスポンス:")
        result = response.json()
        pprint(result)
        
        # Mermaid図の内容を確認
        if "mermaid_content" in result:
            print(f"\n🎨 生成されたMermaid図 (最初の200文字):")
            print(result["mermaid_content"][:200] + "...")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_background_service_status():
    """バックグラウンドサービス状態確認テスト"""
    print("\n🔄 バックグラウンドサービス状態確認テスト")
    try:
        response = requests.get(f"{BASE_URL}/background/status")
        print(f"📊 ステータスコード: {response.status_code}")
        print(f"📋 レスポンス:")
        pprint(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_full_automation():
    """完全自動化テスト（軽量版）"""
    print("\n🚀 完全自動化テスト (軽量版)")
    try:
        data = {
            "message": "PythonでHello Worldプログラムを作成してください",
            "create_issue": False,  # Issue作成は無効
            "generate_mermaid": True,
            "offline_mode": True  # オフラインモード
        }
        response = requests.post(f"{BASE_URL}/automation/run", json=data)
        print(f"📊 ステータスコード: {response.status_code}")
        print(f"📋 レスポンス:")
        result = response.json()
        pprint(result)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_api_docs():
    """API ドキュメント確認テスト"""
    print("\n📖 API ドキュメント確認テスト")
    try:
        # OpenAPI JSON を取得
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"📊 OpenAPI JSON ステータス: {response.status_code}")
        
        if response.status_code == 200:
            openapi_spec = response.json()
            print(f"📋 API情報:")
            print(f"   タイトル: {openapi_spec.get('info', {}).get('title', 'N/A')}")
            print(f"   バージョン: {openapi_spec.get('info', {}).get('version', 'N/A')}")
            print(f"   利用可能なパス数: {len(openapi_spec.get('paths', {}))}")
            
            # 主要なエンドポイントを表示
            paths = openapi_spec.get('paths', {})
            print(f"📋 利用可能なエンドポイント:")
            for path in sorted(paths.keys()):
                methods = list(paths[path].keys())
                print(f"   {path}: {', '.join(methods).upper()}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("🧪 FastAPI 自動化システム 総合テスト開始")
    print("=" * 50)
    
    tests = [
        ("自動化システム状態確認", test_automation_status),
        ("ヘルスチェック", test_health_check),
        ("Mermaid図生成", test_mermaid_generation),
        ("バックグラウンドサービス状態", test_background_service_status),
        ("完全自動化 (軽量版)", test_full_automation),
        ("API ドキュメント確認", test_api_docs),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 実行中: {test_name}")
        print("-" * 30)
        try:
            if test_func():
                print(f"✅ {test_name}: 成功")
                passed += 1
            else:
                print(f"❌ {test_name}: 失敗")
        except Exception as e:
            print(f"💥 {test_name}: 例外発生 - {e}")
        
        time.sleep(1)  # 各テスト間で少し待機
    
    print("\n" + "=" * 50)
    print(f"🎯 テスト結果: {passed}/{total} 成功")
    print(f"📊 成功率: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 全てのテストが成功しました！")
        print("🚀 FastAPI自動化システムは正常に動作しています")
    elif passed > total * 0.7:
        print("✅ 大部分のテストが成功しました")
        print("🔧 一部の機能に改善の余地があります")
    else:
        print("⚠️ 複数のテストが失敗しました")
        print("🔧 システムの修正が必要です")
    
    print("\n📖 詳細情報:")
    print(f"   - Swagger UI: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")
    print(f"   - サーバー状態: {BASE_URL}/automation/status")

if __name__ == "__main__":
    main()
