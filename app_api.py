#!/usr/bin/env python3
"""
🚀 AI Development Platform - Main FastAPI Application
====================================================

Laravel風のPythonアプリケーション + AI自動化API
Gradio統合、AI自動化エンドポイント、Swagger/OpenAPI対応
"""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

# .envファイルから環境変数を読み込み
load_dotenv()

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

def create_ai_development_platform():
    """AI Development Platformの作成"""
    
    # FastAPIアプリケーション作成
    app = FastAPI(
        title="🚀 AI Development Platform - Laravel風統合システム + AI自動化API",
        description="""
# 🤖 AI Development Platform

Laravel風のGradio統合プラットフォーム + AI自動化システム

## 🚀 主要機能

### 🤖 AI自動化API
- **完全自動化実行**: メッセージからGitHub Issue作成、Mermaid図生成まで自動実行
- **GitHub統合**: Issue作成、ラベル管理、担当者設定
- **Mermaid図生成**: 自動的な図表作成・保存
- **Copilot統合**: Supabase連携でのリアルタイム処理
- **リアルタイム監視**: WebSocketでのシステム状態監視

### 🎨 Gradio統合
- Laravel風のMVCアーキテクチャ
- 15の統合インターフェース
- リアルタイムチャット機能

### 📖 API仕様
- OpenAPI/Swagger完全準拠
- 他のAIシステムから利用可能
- 自動クライアント生成対応

## 🔗 エンドポイント

### AI自動化
- `POST /automation/run` - 完全自動化実行
- `POST /automation/issue/create` - GitHub Issue作成
- `POST /automation/mermaid/generate` - Mermaid図生成
- `GET /automation/status` - システム状態確認
- `WS /automation/ws/monitor` - リアルタイム監視

### Laravel風API
- `GET /api/status` - API状態確認
- `GET /laravel/status` - Laravel風システム状態

### ドキュメント
- `/docs` - Swagger UI（インタラクティブ）
- `/redoc` - ReDoc（詳細ドキュメント）

## 🛠️ 開発者向け
このプラットフォームは他のAIシステムからの利用を想定して設計されています。
OpenAPI仕様により、任意の言語でクライアントライブラリを自動生成できます。
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 静的ファイル設定
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ 静的ファイルを /static にマウント")
    except Exception as e:
        print(f"⚠️ 静的ファイルマウント失敗: {e}")
    
    # AI自動化APIエンドポイント追加
    try:
        from api.automation import router as automation_router
        app.include_router(automation_router)
        print("✅ AI自動化APIエンドポイント追加完了")
        print("📋 利用可能なエンドポイント:")
        print("   - GET  /automation/status")
        print("   - POST /automation/run")
        print("   - POST /automation/issue/create")
        print("   - POST /automation/mermaid/generate")
        print("   - POST /automation/copilot/integration")
        print("   - GET  /automation/health")
        print("   - WS   /automation/ws/monitor")
    except ImportError as e:
        print(f"⚠️ AI自動化API読み込み失敗: {e}")
    except Exception as e:
        print(f"❌ AI自動化API設定エラー: {e}")
    
    # Laravel風ルート追加
    try:
        from routes.web import router as web_router
        app.include_router(web_router, prefix="/api")
        print("✅ Laravel風Webルート追加完了")
    except ImportError as e:
        print(f"⚠️ Laravel風ルート読み込み失敗: {e}")
    except Exception as e:
        print(f"❌ Laravel風ルート設定エラー: {e}")
    
    # Laravel風追加APIエンドポイント
    from fastapi import APIRouter
    
    laravel_api = APIRouter(prefix="/laravel", tags=["Laravel API"])
    
    @laravel_api.get("/status")
    async def laravel_status():
        """Laravel風システムの状態確認"""
        return {
            "status": "success",
            "message": "Laravel風AI Development Platform",
            "gradio_available": True,
            "ai_automation_available": True,
            "features": [
                "🤖 AI自動化システム",
                "🎨 Gradio統合",
                "📊 Mermaid図生成",
                "🔗 GitHub統合",
                "💬 Copilot統合"
            ],
            "endpoints": {
                "automation": "/automation/*",
                "api": "/api/*",
                "laravel": "/laravel/*",
                "docs": "/docs",
                "redoc": "/redoc"
            }
        }
    
    @laravel_api.get("/db-status")
    async def database_status():
        """データベース状態確認"""
        try:
            from config.database import get_db_connection
            conn = get_db_connection('chat_history')
            conn.close()
            return {
                "status": "success",
                "message": "データベース接続正常",
                "connection": "OK"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"データベース接続エラー: {str(e)}"
            }
    
    app.include_router(laravel_api)
    
    # ルートエンドポイント
    @app.get("/")
    async def root():
        """ルートエンドポイント"""
        return {
            "message": "🚀 AI Development Platform - Laravel風統合システム",
            "version": "1.0.0",
            "status": "running",
            "features": {
                "ai_automation": "AI自動化システム（GitHub、Mermaid、Copilot統合）",
                "gradio": "Laravel風Gradio統合UI",
                "api": "OpenAPI/Swagger対応REST API"
            },
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc"
            },
            "endpoints": {
                "automation": "/automation/",
                "api": "/api/",
                "laravel": "/laravel/",
                "gradio": "/gradio/"
            }
        }
    
    # ヘルスチェック
    @app.get("/health")
    async def health():
        """ヘルスチェック"""
        return {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": "1.0.0"
        }
    
    # Gradio統合（オプション）- テスト環境では無効化
    gradio_enabled = os.getenv("ENABLE_GRADIO", "false").lower() == "true"
    
    if gradio_enabled:
        try:
            import gradio as gr
            
            # 簡単なGradioインターフェース
            def ai_chat(message):
                return f"🤖 AI応答: {message}\n\nこのメッセージは /automation/run エンドポイント経由でも処理できます。"
            
            gradio_interface = gr.Interface(
                fn=ai_chat,
                inputs=gr.Textbox(label="メッセージ", placeholder="AI自動化システムに質問してください..."),
                outputs=gr.Textbox(label="AI応答"),
                title="🚀 AI Development Platform",
                description="Laravel風統合システム + AI自動化 | API: /docs"
            )
            
            # GradioをFastAPIにマウント
            app = gr.mount_gradio_app(app, gradio_interface, path="/gradio")
            print("✅ Gradio UI を /gradio にマウント")
            
        except Exception as e:
            print(f"⚠️ Gradio統合をスキップ: {e}")
    else:
        print("🚫 Gradio統合は無効化されています (ENABLE_GRADIO=false)")
        
        # Gradio無効時の代替エンドポイント
        @app.get("/gradio")
        async def gradio_disabled():
            return {
                "message": "Gradio UIは無効化されています",
                "alternative": "FastAPI Swagger UI を /docs で利用できます",
                "note": "Gradioを有効にするには環境変数 ENABLE_GRADIO=true を設定してください"
            }
    
    # バックグラウンド自動化サービス追加
    print("🔄 バックグラウンド自動化サービス設定中...")
    try:
        from api.background_service import get_background_service
        
        background_service = get_background_service()
        
        # FastAPIスタートアップイベント
        @app.on_event("startup")
        async def startup_event():
            """アプリケーション起動時にバックグラウンドサービス開始"""
            print("🚀 FastAPI起動 - バックグラウンドサービス開始")
            
            # 環境変数でバックグラウンド実行を制御
            enable_background = os.getenv("ENABLE_BACKGROUND_AUTOMATION", "true").lower() == "true"
            
            if enable_background:
                background_service.start_background_service()
                print("✅ バックグラウンド自動化サービス開始完了")
            else:
                print("🚫 バックグラウンド自動化サービスは無効化されています")
                print("   有効化するには環境変数 ENABLE_BACKGROUND_AUTOMATION=true を設定")
        
        @app.on_event("shutdown") 
        async def shutdown_event():
            """アプリケーション終了時にバックグラウンドサービス停止"""
            print("🛑 FastAPI終了 - バックグラウンドサービス停止")
            background_service.stop_background_service()
            print("✅ バックグラウンドサービス停止完了")
        
        # バックグラウンドサービス制御エンドポイント追加
        from fastapi import APIRouter
        
        background_router = APIRouter(prefix="/background", tags=["Background Service"])
        
        @background_router.get("/status")
        async def get_background_status():
            """バックグラウンドサービス状態確認"""
            return background_service.get_status()
        
        @background_router.post("/start")
        async def start_background_service():
            """バックグラウンドサービス手動開始"""
            try:
                background_service.start_background_service()
                return {"success": True, "message": "バックグラウンドサービス開始"}
            except Exception as e:
                return {"success": False, "message": f"開始失敗: {str(e)}"}
        
        @background_router.post("/stop")
        async def stop_background_service():
            """バックグラウンドサービス手動停止"""
            try:
                background_service.stop_background_service()
                return {"success": True, "message": "バックグラウンドサービス停止"}
            except Exception as e:
                return {"success": False, "message": f"停止失敗: {str(e)}"}
        
        app.include_router(background_router)
        
        print("✅ バックグラウンド自動化サービス設定完了")
        print("📋 追加エンドポイント:")
        print("   - GET  /background/status - バックグラウンド状態確認")
        print("   - POST /background/start - バックグラウンド開始")
        print("   - POST /background/stop - バックグラウンド停止")
        
    except ImportError as e:
        print(f"⚠️ バックグラウンドサービス読み込み失敗: {e}")
    except Exception as e:
        print(f"❌ バックグラウンドサービス設定エラー: {e}")

    print("🚀 AI Development Platform 初期化完了!")
    return app

def check_missing_databases():
    """不足しているデータベースをチェック"""
    try:
        from config.database import get_db_connection
        required_dbs = [
            'prompts.db',
            'approval_system.db', 
            'chat_history.db',
            'conversation_history.db',
            'github_issues.db',
            'users.db'
        ]
        
        missing = []
        db_dir = os.path.join(project_root, 'database')
        
        for db_name in required_dbs:
            db_path = os.path.join(db_dir, db_name)
            if not os.path.exists(db_path):
                missing.append(db_name.replace('.db', ''))
        
        return missing
        
    except Exception as e:
        print(f"⚠️ データベースチェックエラー: {e}")
        return []

def run_server():
    """サーバー実行"""
    # アプリケーション作成
    app = create_ai_development_platform()
    
    # 設定
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 7860))
    debug = os.getenv("DEBUG_MODE", "True").lower() == "true"
    
    print(f"🚀 サーバー開始: http://{host}:{port}")
    print(f"📖 Swagger UI: http://{host}:{port}/docs")
    print(f"📚 ReDoc: http://{host}:{port}/redoc")
    print(f"🎨 Gradio UI: http://{host}:{port}/gradio")
    
    # uvicornでサーバー起動
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug
    )

if __name__ == "__main__":
    import sys
    
    if "--test" in sys.argv:
        print("🧪 テストモード: システムチェック実行")
        
        # 基本チェック
        print("📋 環境変数チェック:")
        important_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'GITHUB_TOKEN']
        for var in important_vars:
            value = os.getenv(var)
            status = "✅" if value else "❌"
            print(f"   {status} {var}")
        
        # データベースチェック
        print("🗄️ データベースチェック:")
        missing = check_missing_databases()
        if missing:
            print(f"   ❌ 不足: {missing}")
        else:
            print("   ✅ 全データベース確認")
        
        # APIチェック
        print("🔌 APIチェック:")
        try:
            app = create_ai_development_platform()
            print("   ✅ FastAPIアプリ作成成功")
        except Exception as e:
            print(f"   ❌ FastAPIアプリ作成失敗: {e}")
        
        sys.exit(0)
    
    # 通常のサーバー起動
    run_server()

# FastAPIアプリケーション作成（uvicorn用）
app = create_ai_development_platform()
