#!/usr/bin/env python3
"""
🧪 Copilot自動化システム テストスクリプト
Laravel風のartisan testコマンドのPython版実装
"""

import os
import sys
import time
from pathlib import Path

# プロジェクトルートを追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "app" / "Console" / "Commands"))

def test_copilot_basic():
    """Copilot自動化システムの基本テスト"""
    print("🤖 Copilot自動化システムの基本テストを開始...")
    
    try:
        # 環境変数チェック
        print("📋 1. 環境変数チェック...")
        required_env = ['SUPABASE_URL', 'SUPABASE_KEY', 'GITHUB_TOKEN']
        missing_env = []
        
        for env_var in required_env:
            if not os.getenv(env_var):
                missing_env.append(env_var)
        
        if missing_env:
            print(f"⚠️ 未設定の環境変数: {', '.join(missing_env)}")
        else:
            print("✅ 必要な環境変数は全て設定済み")
        
        # ファイル存在チェック
        print("📋 2. ファイル存在チェック...")
        required_files = [
            "app/Console/Commands/copilot_github_cli_automation.py",
            "chat_coordinates.json",
            ".env"
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path}: 存在")
            else:
                print(f"❌ {file_path}: 不存在")
        
        # Copilot自動化クラスのインポートテスト
        print("📋 3. Copilot自動化クラスのインポートテスト...")
        
        try:
            from copilot_github_cli_automation import GitHubCopilotAutomation
            automation = GitHubCopilotAutomation(offline_mode=True)
            print("✅ Copilot自動化クラスのインポート成功")
            
            # 座標読み込みテスト
            print("📋 4. 座標読み込みテスト...")
            coords = automation.load_coordinates()
            if coords:
                print("✅ 座標読み込み成功")
            else:
                print("❌ 座標読み込み失敗")
            
            # Mermaid図生成テスト
            print("📋 5. Mermaid図生成テスト...")
            test_question = "テストプロジェクトを作成してください"
            mermaid_code = automation.generate_dynamic_mermaid_diagram(test_question)
            
            if mermaid_code and "graph TD" in mermaid_code:
                print("✅ Mermaid図生成成功")
                
                # Mermaidファイル保存テスト
                saved_file = automation.save_mermaid_to_file(mermaid_code, "test_mermaid")
                if os.path.exists(saved_file):
                    print(f"✅ Mermaidファイル保存成功: {saved_file}")
                else:
                    print("❌ Mermaidファイル保存失敗")
            else:
                print("❌ Mermaid図生成失敗")
            
            print("🎉 Copilot自動化システムの基本テストが完了しました！")
            return True
            
        except ImportError as e:
            print(f"❌ インポートエラー: {e}")
            return False
        except Exception as e:
            print(f"❌ テスト実行エラー: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 全体的なテストエラー: {e}")
        return False

def test_fastapi_integration():
    """FastAPI統合テスト"""
    print("🌐 FastAPI統合テストを開始...")
    
    try:
        # FastAPIアプリケーションファイルの存在確認
        if os.path.exists("app.py"):
            print("✅ app.py: 存在")
        else:
            print("❌ app.py: 不存在")
            return False
        
        # requriements.txtの確認
        if os.path.exists("requirements.txt"):
            print("✅ requirements.txt: 存在")
            
            with open("requirements.txt", "r", encoding="utf-8") as f:
                content = f.read()
                
            required_packages = ["fastapi", "uvicorn", "supabase"]
            missing_packages = []
            
            for package in required_packages:
                if package not in content.lower():
                    missing_packages.append(package)
            
            if missing_packages:
                print(f"⚠️ requirements.txtに含まれていないパッケージ: {', '.join(missing_packages)}")
            else:
                print("✅ 必要なパッケージは全てrequirements.txtに記載済み")
        
        print("🎉 FastAPI統合テストが完了しました！")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI統合テストエラー: {e}")
        return False

def test_full_workflow():
    """完全ワークフローのテスト"""
    print("🚀 完全ワークフローのテストを開始...")
    
    # 段階的テスト実行
    tests = [
        ("基本機能テスト", test_copilot_basic),
        ("FastAPI統合テスト", test_fastapi_integration)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}を実行中...")
        if test_func():
            passed_tests += 1
            print(f"✅ {test_name}: 成功")
        else:
            print(f"❌ {test_name}: 失敗")
    
    print(f"\n🎯 テスト結果: {passed_tests}/{total_tests} 成功")
    
    if passed_tests == total_tests:
        print("🎉 全てのテストが成功しました！")
        print("🚀 次のステップ: FastAPIサーバーを起動してリアルタイムテストを実行")
        return True
    else:
        print("⚠️ 一部のテストが失敗しました。問題を修正してください。")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="🧪 Copilot自動化システム テストスクリプト")
    parser.add_argument("test_type", nargs="?", default="all", 
                       choices=["all", "basic", "fastapi", "workflow"],
                       help="実行するテストタイプ")
    
    args = parser.parse_args()
    
    print("🧪 Copilot自動化システム テストスクリプト")
    print("=" * 50)
    
    if args.test_type == "basic":
        test_copilot_basic()
    elif args.test_type == "fastapi":
        test_fastapi_integration()
    elif args.test_type == "workflow":
        test_full_workflow()
    else:  # "all"
        test_full_workflow()
