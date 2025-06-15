import os
import sys
from django.core.asgi import get_asgi_application

# Laravel風のGradio統合のためのパス追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = get_asgi_application()

# app.pyの統合FastAPIアプリを使用
sys.path.append('/workspaces/AUTOCREATE')

try:
    # app.pyファイルから直接インポート
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_module", "/workspaces/AUTOCREATE/app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    app = app_module.create_fastapi_with_gradio()
    print("✅ Using unified FastAPI app from app.py")
except Exception as e:
    print(f"❌ Failed to load unified app: {e}")
    import traceback
    traceback.print_exc()
    
    # フォールバック: 基本的なFastAPIアプリ
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("⚠️ Using fallback FastAPI app")
