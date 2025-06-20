#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VS Code拡張機能テストスクリプト
拡張機能のコマンドが利用可能かチェック
"""

import subprocess
import json
import time

def test_vscode_extension():
    """VS Code拡張機能のテスト"""
    print("🔍 VS Code拡張機能テスト開始")
    
    # VS Codeのコマンドリストを取得
    try:
        print("📋 VS Codeコマンド一覧を取得中...")
        result = subprocess.run([
            "code", "--list-extensions", "--show-versions"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ VS Code拡張機能一覧:")
            print(result.stdout)
        else:
            print(f"❌ コマンド実行失敗: {result.stderr}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # 我々の拡張機能のコマンドをテスト
    commands_to_test = [
        "copilotSupabaseMonitor.startMonitoring",
        "copilotSupabaseMonitor.stopMonitoring", 
        "copilotSupabaseMonitor.testConnection"
    ]
    
    print("\n🧪 拡張機能コマンドテスト:")
    for cmd in commands_to_test:
        print(f"   📤 テスト中: {cmd}")
        try:
            # VS Codeコマンドを実行
            result = subprocess.run([
                "code", "--command", cmd
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print(f"   ✅ {cmd} - 成功")
            else:
                print(f"   ❌ {cmd} - 失敗: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ {cmd} - タイムアウト")
        except Exception as e:
            print(f"   ❌ {cmd} - エラー: {e}")
    
    print("\n🎯 手動確認方法:")
    print("1. VS Codeでコマンドパレットを開く (Ctrl+Shift+P)")
    print("2. 以下のコマンドを検索:")
    print("   - 🚀 Supabase監視開始")
    print("   - 🛑 Supabase監視停止") 
    print("   - 🔍 接続テスト")
    print("3. コマンドが表示されれば拡張機能は読み込み済み")

if __name__ == "__main__":
    test_vscode_extension()
