#!/usr/bin/env python3
"""
FastAPI Laravel-style Application with Gradio Integration
=========================================================

Laravel風のPythonアプリケーション + Gradio統合
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 で起動
"""

import os
import sys
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Gradio環境変数設定（Gradio 4.31.5 キューエラー防止）
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'false'
os.environ['GRADIO_SERVER_HOST'] = '0.0.0.0'
os.environ['GRADIO_SERVER_PORT'] = '7860'

# app.pyからGradio統合済みFastAPIアプリケーションをインポート
from app import create_fastapi_with_gradio

# アプリケーションインスタンス作成（Gradio統合済み）
app = create_fastapi_with_gradio()

@app.get("/")
async def root():
    """
    ホームページ
    """
    return {
        "message": "🚀 FastAPI + Gradio Laravel-style Application",
        "version": "1.0.0",
        "gradio_url": "/gradio",
        "api_docs": "/docs",
        "environment": os.getenv('APP_ENV', 'development')
    }

@app.get("/health")
async def health_check():
    """
    ヘルスチェック
    """
    return {
        "status": "ok",
        "app": "FastAPI + Gradio Laravel-style App",
        "gradio_status": "enabled",
        "environment": os.getenv('APP_ENV', 'development')
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting FastAPI + Gradio Laravel-style Application...")
    print("📱 Gradio UI: http://localhost:8000/gradio")
    print("🔧 API docs: http://localhost:8000/docs")
    print("🏠 Home: http://localhost:8000/")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        reload=False,  # Gradioとの相性を考慮してreloadは無効
        log_level="info"
    )
