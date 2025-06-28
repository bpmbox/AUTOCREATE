#!/usr/bin/env python3
"""
🧪 FastAPI Mermaid図生成テスト (単体)
"""

import requests
import json

def test_mermaid_single():
    print("🎨 Mermaid図生成テスト (ポート7862)")
    try:
        data = {
            "content": "FastAPIでリアルタイムチャットシステムを作成してください",
            "diagram_type": "flowchart"
        }
        response = requests.post("http://localhost:7862/automation/mermaid/generate", json=data)
        print(f"ステータス: {response.status_code}")
        result = response.json()
        print(f"レスポンス: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if "mermaid_content" in result:
            print(f"\n🎨 生成されたMermaid図:")
            print(result["mermaid_content"][:500] + "...")
        
        return response.status_code == 200
    except Exception as e:
        print(f"エラー: {e}")
        return False

if __name__ == "__main__":
    success = test_mermaid_single()
    print(f"結果: {'✅ 成功' if success else '❌ 失敗'}")
