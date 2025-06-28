#!/usr/bin/env python3
"""
Django ASGI + FastAPI + Gradio 統合起動
========================================================
app.py から asgi.py を起動してすべて統合
"""

import uvicorn
import os
import sys
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Django設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

if __name__ == "__main__":
    print("🚀 Django ASGI + FastAPI + Gradio 統合アプリ起動中...")
    print("📡 メインURL: http://localhost:8000")
    print("🔧 Django Admin: http://localhost:8000/admin")
    print("� Gradio Chat: http://localhost:8000/gradio")
    print("� API Docs: http://localhost:8000/docs")
    
    # mysite.asgi:app を起動（Django + FastAPI + Gradio統合）
    uvicorn.run(
        "mysite.asgi:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # リロード無効（安定性向上）
        log_level="info"
    )
