#!/usr/bin/env python3
"""
🧪 AI自動化APIプラットフォーム - テストスイート
=============================================

FastAPIアプリケーションと自動化システムのテスト
"""

import os
import sys
import pytest
import asyncio
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_environment_setup():
    """環境変数とプロジェクト設定のテスト"""
    print("🔧 環境設定テスト開始")
    
    # 必要なディレクトリの存在確認
    required_dirs = ['api', 'tests', 'database', 'config']
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"必要なディレクトリが見つかりません: {dir_name}"
        print(f"   ✅ {dir_name} ディレクトリ確認")
    
    # 重要なファイルの存在確認
    required_files = [
        'app_api.py',
        'api/automation.py',
        'tests/Feature/copilot_github_cli_automation.py'
    ]
    for file_path in required_files:
        full_path = project_root / file_path
        assert full_path.exists(), f"必要なファイルが見つかりません: {file_path}"
        print(f"   ✅ {file_path} ファイル確認")
    
    print("✅ 環境設定テスト完了")

def test_fastapi_app_creation():
    """FastAPIアプリケーションの作成テスト"""
    print("🚀 FastAPIアプリケーション作成テスト開始")
    
    try:
        from app_api import create_ai_development_platform
        app = create_ai_development_platform()
        
        # 基本的なアプリケーション属性を確認
        assert hasattr(app, 'routes'), "FastAPIアプリにルートが設定されていません"
        assert len(app.routes) > 0, "ルートが登録されていません"
        
        print(f"   ✅ FastAPIアプリ作成成功 - {len(app.routes)}個のルート")
        
        # 重要なエンドポイントの存在確認
        route_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        important_paths = ['/', '/health', '/docs', '/automation/status']
        
        for path in important_paths:
            if any(path in route_path for route_path in route_paths):
                print(f"   ✅ エンドポイント確認: {path}")
            else:
                print(f"   ⚠️ エンドポイント未確認: {path}")
        
        print("✅ FastAPIアプリケーション作成テスト完了")
        return app
        
    except Exception as e:
        print(f"❌ FastAPIアプリケーション作成失敗: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_automation_system_import():
    """自動化システムのインポートテスト"""
    print("🤖 自動化システムインポートテスト開始")
    
    try:
        # GitHubCopilotAutomationのインポートテスト
        from tests.Feature.copilot_github_cli_automation import GitHubCopilotAutomation
        automation = GitHubCopilotAutomation(offline_mode=True)
        print("   ✅ GitHubCopilotAutomation インポート成功")
        
        # メソッドの存在確認
        required_methods = [
            'generate_mermaid_diagram',
            'save_mermaid_to_file',
            'create_github_issue'
        ]
        
        for method_name in required_methods:
            if hasattr(automation, method_name):
                print(f"   ✅ メソッド確認: {method_name}")
            else:
                print(f"   ⚠️ メソッド未確認: {method_name}")
        
        print("✅ 自動化システムインポートテスト完了")
        return automation
        
    except Exception as e:
        print(f"❌ 自動化システムインポート失敗: {e}")
        import traceback
        traceback.print_exc()
        raise

def test_api_automation_endpoints():
    """API自動化エンドポイントのテスト"""
    print("🔌 API自動化エンドポイントテスト開始")
    
    try:
        from api.automation import router
        assert router is not None, "automationルーターが取得できません"
        
        # ルーターのパスとタグを確認
        assert router.prefix == "/automation", f"ルータープレフィックスが正しくありません: {router.prefix}"
        assert "AI Automation" in router.tags, f"ルータータグが正しくありません: {router.tags}"
        
        print(f"   ✅ ルーター設定確認 - プレフィックス: {router.prefix}")
        print(f"   ✅ ルーター設定確認 - タグ: {router.tags}")
        
        # ルートの数を確認
        route_count = len(router.routes)
        print(f"   ✅ 自動化APIルート数: {route_count}")
        
        # 重要なルートの存在確認
        route_paths = [route.path for route in router.routes if hasattr(route, 'path')]
        important_automation_paths = ['/status', '/run', '/health']
        
        for path in important_automation_paths:
            if any(path in route_path for route_path in route_paths):
                print(f"   ✅ 自動化エンドポイント確認: {path}")
            else:
                print(f"   ⚠️ 自動化エンドポイント未確認: {path}")
        
        print("✅ API自動化エンドポイントテスト完了")
        return router
        
    except Exception as e:
        print(f"❌ API自動化エンドポイントテスト失敗: {e}")
        import traceback
        traceback.print_exc()
        raise

async def test_api_responses():
    """APIレスポンスのテスト"""
    print("📡 APIレスポンステスト開始")
    
    try:
        from fastapi.testclient import TestClient
        from app_api import create_ai_development_platform
        
        app = create_ai_development_platform()
        client = TestClient(app)
        
        # ルートエンドポイントのテスト
        response = client.get("/")
        assert response.status_code == 200, f"ルートエンドポイントが失敗: {response.status_code}"
        data = response.json()
        assert "message" in data, "レスポンスにメッセージが含まれていません"
        print("   ✅ ルートエンドポイント (/) テスト成功")
        
        # ヘルスチェックエンドポイントのテスト
        response = client.get("/health")
        assert response.status_code == 200, f"ヘルスチェックが失敗: {response.status_code}"
        data = response.json()
        assert data.get("status") == "healthy", "ヘルスチェックステータスが正常ではありません"
        print("   ✅ ヘルスチェックエンドポイント (/health) テスト成功")
        
        # Laravel風ステータスエンドポイントのテスト
        response = client.get("/laravel/status")
        assert response.status_code == 200, f"Laravel風ステータスが失敗: {response.status_code}"
        data = response.json()
        assert data.get("status") == "success", "Laravel風ステータスが正常ではありません"
        print("   ✅ Laravel風ステータスエンドポイント (/laravel/status) テスト成功")
        
        # 自動化ヘルスチェックエンドポイントのテスト
        try:
            response = client.get("/automation/health")
            if response.status_code == 200:
                print("   ✅ 自動化ヘルスチェック (/automation/health) テスト成功")
            else:
                print(f"   ⚠️ 自動化ヘルスチェック失敗: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️ 自動化ヘルスチェックエラー: {e}")
        
        print("✅ APIレスポンステスト完了")
        return client
        
    except Exception as e:
        print(f"❌ APIレスポンステスト失敗: {e}")
        import traceback
        traceback.print_exc()
        raise

def run_all_tests():
    """全テストの実行"""
    print("🧪 AI自動化APIプラットフォーム 統合テスト開始")
    print("=" * 60)
    
    tests = [
        ("環境設定", test_environment_setup),
        ("FastAPIアプリケーション", test_fastapi_app_creation),
        ("自動化システム", test_automation_system_import),
        ("API自動化エンドポイント", test_api_automation_endpoints),
        ("APIレスポンス", lambda: asyncio.run(test_api_responses()))
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n🔄 {test_name}テスト実行中...")
            result = test_func()
            results[test_name] = "✅ 成功"
            print(f"✅ {test_name}テスト完了")
        except Exception as e:
            results[test_name] = f"❌ 失敗: {str(e)}"
            print(f"❌ {test_name}テスト失敗: {e}")
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 テスト結果サマリー")
    print("=" * 60)
    
    success_count = 0
    for test_name, result in results.items():
        print(f"{result} - {test_name}")
        if "成功" in result:
            success_count += 1
    
    print(f"\n🎯 成功: {success_count}/{len(tests)} テスト")
    
    if success_count == len(tests):
        print("🎉 全てのテストが成功しました！")
        print("🚀 AI自動化APIプラットフォームは正常に動作しています")
        print("📖 Swagger UI: http://localhost:7860/docs")
        print("🎨 Gradio UI: http://localhost:7860/gradio")
    else:
        print("⚠️ 一部のテストが失敗しました")
        print("🔧 エラーを確認して修正してください")
    
    return results

if __name__ == "__main__":
    # メイン実行
    results = run_all_tests()
    
    # 正常終了コードの設定
    success_count = sum(1 for result in results.values() if "成功" in result)
    exit_code = 0 if success_count == len(results) else 1
    
    print(f"\n終了コード: {exit_code}")
    sys.exit(exit_code)
