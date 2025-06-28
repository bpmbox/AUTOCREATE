#!/usr/bin/env python3
"""
🧪 AI自動化API - 実際のテスト実行
===============================

実際にAPIサーバーにリクエストを送信してテスト
"""

import requests
import json
import time
from datetime import datetime

def test_api_server():
    """APIサーバーのテスト"""
    base_url = "http://localhost:7860"
    
    print("🚀 AI自動化API 実テスト開始")
    print("=" * 50)
    
    # 1. ヘルスチェック
    print("🔍 1. ヘルスチェックテスト")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ ヘルスチェック成功")
            print(f"   📊 レスポンス: {response.json()}")
        else:
            print(f"   ❌ ヘルスチェック失敗: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ヘルスチェックエラー: {e}")
    
    # 2. システム状態確認
    print("\n🔍 2. システム状態確認テスト")
    try:
        response = requests.get(f"{base_url}/automation/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("   ✅ システム状態取得成功")
            print(f"   📊 GitHub CLI: {status.get('github_cli_available', 'unknown')}")
            print(f"   📊 Supabase: {status.get('supabase_connected', 'unknown')}")
            print(f"   📊 システム状態: {status.get('status', 'unknown')}")
        else:
            print(f"   ❌ システム状態取得失敗: {response.status_code}")
    except Exception as e:
        print(f"   ❌ システム状態エラー: {e}")
    
    # 3. Laravel風API状態確認
    print("\n🔍 3. Laravel風API状態確認テスト")
    try:
        response = requests.get(f"{base_url}/laravel/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("   ✅ Laravel風API正常")
            print(f"   📊 ステータス: {status.get('status', 'unknown')}")
            print(f"   📊 機能: {len(status.get('features', []))}個")
        else:
            print(f"   ❌ Laravel風API失敗: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Laravel風APIエラー: {e}")
    
    # 4. Mermaid図生成テスト（軽量）
    print("\n🔍 4. Mermaid図生成テスト")
    try:
        mermaid_request = {
            "content": "シンプルなテストフロー",
            "diagram_type": "flowchart"
        }
        
        response = requests.post(
            f"{base_url}/automation/mermaid/generate",
            json=mermaid_request,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Mermaid図生成成功")
            print(f"   📊 生成時刻: {result.get('generated_at', 'unknown')}")
            if result.get('mermaid_content'):
                print(f"   📊 図コンテンツ: {len(result['mermaid_content'])}文字")
        else:
            print(f"   ❌ Mermaid図生成失敗: {response.status_code}")
            if response.text:
                print(f"   エラー詳細: {response.text[:200]}...")
                
    except Exception as e:
        print(f"   ❌ Mermaid図生成エラー: {e}")
    
    # 5. APIドキュメント確認
    print("\n🔍 5. APIドキュメント確認テスト")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        if response.status_code == 200:
            openapi_spec = response.json()
            print("   ✅ OpenAPI仕様取得成功")
            print(f"   📊 タイトル: {openapi_spec.get('info', {}).get('title', 'unknown')}")
            print(f"   📊 バージョン: {openapi_spec.get('info', {}).get('version', 'unknown')}")
            
            # パス数を確認
            paths = openapi_spec.get('paths', {})
            print(f"   📊 エンドポイント数: {len(paths)}")
            
            # 主要エンドポイントを表示
            key_endpoints = ['/automation/run', '/automation/status', '/automation/mermaid/generate']
            for endpoint in key_endpoints:
                if endpoint in paths:
                    print(f"   ✅ エンドポイント確認: {endpoint}")
                else:
                    print(f"   ⚠️ エンドポイント未確認: {endpoint}")
                    
        else:
            print(f"   ❌ OpenAPI仕様取得失敗: {response.status_code}")
    except Exception as e:
        print(f"   ❌ OpenAPI仕様エラー: {e}")
    
    # テスト結果サマリー
    print("\n" + "=" * 50)
    print("🎯 AI自動化API実テスト完了!")
    print("📖 Swagger UI: http://localhost:7860/docs")
    print("📚 ReDoc: http://localhost:7860/redoc")
    print("🔗 API Root: http://localhost:7860/")
    print("\n🤖 他のAIからの利用例:")
    print("   curl -X GET 'http://localhost:7860/automation/status'")
    print("   curl -X POST 'http://localhost:7860/automation/mermaid/generate' \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"content\":\"テストフロー\",\"diagram_type\":\"flowchart\"}'")

if __name__ == "__main__":
    test_api_server()
