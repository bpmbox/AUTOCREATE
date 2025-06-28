#!/usr/bin/env python3
"""
🧪 FastAPI基本テスト
"""

import requests
import sys

def test_basic():
    try:
        print("🔍 基本接続テスト...")
        response = requests.get("http://localhost:7861/automation/status", timeout=5)
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.text}")
        return True
    except Exception as e:
        print(f"エラー: {e}")
        return False

if __name__ == "__main__":
    print("FastAPI基本テスト開始")
    if test_basic():
        print("✅ テスト成功")
        sys.exit(0)
    else:
        print("❌ テスト失敗")
        sys.exit(1)
