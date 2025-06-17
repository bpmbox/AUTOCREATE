"""
Web Routes
==========

ウェブアプリケーション用のルーティング
Laravel風の構成でGradio読み込みを改善
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
import gradio as gr
import sys
import os

# Laravel風Controller のパスを追加
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

router = APIRouter()
templates = Jinja2Templates(directory="resources/views")

# Gradioインターフェースのキャッシュ
gradio_cache = {}

def initialize_gradio_with_error_handling():
    """
    Laravel風のGradio初期化（エラーハンドリング付き）
    データベース接続とパス設定を修正
    """
    try:
        # データベースパスの確認と修正
        from config.database import get_db_path, DATABASE_PATHS
        import os
        
        # 必要なデータベースが存在するか確認
        missing_dbs = []
        for db_name, db_path in DATABASE_PATHS.items():
            if not os.path.exists(db_path):
                missing_dbs.append(db_name)
        
        if missing_dbs:
            print(f"⚠️ Missing databases: {missing_dbs}")
            # データベース初期化を実行
            try:
                from database.init_databases import main as init_db
                init_db()
                print("✅ Databases initialized successfully")
            except Exception as db_error:
                print(f"❌ Database initialization failed: {db_error}")
        
        # Laravel風Controller経由でGradio初期化
        from app.Http.Controllers.GradioController import GradioController
        controller = GradioController()
        tabbed_interface = controller.setup_gradio_interfaces()
        
        print("✅ Gradio interfaces initialized successfully")
        return tabbed_interface
        
    except Exception as e:
        print(f"❌ Error initializing Gradio: {e}")
        # フォールバック用の簡単なインターフェース
        return gr.Interface(
            fn=lambda x: f"Gradio initialization error: {str(e)}",
            inputs="text",
            outputs="text",
            title="🚨 Gradio Error"
        )

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    ホームページ
    """
    return templates.TemplateResponse("welcome.html", {
        "request": request,
        "title": "Welcome to FastAPI Laravel"
    })

# Gradio統合エンドポイント - Laravel風でエラーハンドリング改善
@router.get("/gradio")
async def gradio_interface():
    """Laravel風のGradio統合インターフェース"""
    try:
        tabbed_interface = initialize_gradio_with_error_handling()
        # GradioをASGIアプリとして返す
        return gr.routes.App.create_app(tabbed_interface)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Gradio initialization failed: {str(e)}"}
        )

# テスト用のシンプルなログイン画面
@router.get("/login", response_class=HTMLResponse)
async def simple_login(request: Request):
    """
    シンプルなログイン画面（テスト用）
    """
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Tools Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-card {
                background: white;
                border-radius: 15px;
                padding: 40px;
                max-width: 400px;
                width: 100%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .title {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #555;
                font-weight: bold;
            }
            input {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                box-sizing: border-box;
            }
            input:focus {
                border-color: #667eea;
                outline: none;
            }
            .btn {
                width: 100%;
                background: #667eea;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #5a67d8;
            }
            .tools-list {
                margin-top: 30px;
                text-align: center;
            }
            .tool-link {
                display: inline-block;
                margin: 5px;
                padding: 10px 15px;
                background: #f0f0f0;
                color: #333;
                text-decoration: none;
                border-radius: 5px;
                font-size: 14px;
            }
            .tool-link:hover {
                background: #667eea;
                color: white;
            }
            .current-url {
                background: #e2e8f0;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                font-size: 14px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
            }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h1 class="title">🚀 AI Tools Login</h1>
            
            <div class="current-url">
                📍 現在のURL: <strong>""" + str(request.url) + """</strong>
            </div>
            
            <form action="/dashboard" method="get">
                <div class="form-group">
                    <label for="username">👤 ユーザー名</label>
                    <input type="text" id="username" name="username" placeholder="ユーザー名を入力" required>
                </div>
                
                <div class="form-group">
                    <label for="password">🔒 パスワード</label>
                    <input type="password" id="password" name="password" placeholder="パスワードを入力" required>
                </div>
                
                <button type="submit" class="btn">🚀 ログイン</button>
            </form>
            
            <div class="tools-list">
                <h3>🛠️ 利用可能なツール</h3>
                <a href="/gradio" class="tool-link">🌐 Gradio</a>
                <a href="/dashboard" class="tool-link">📊 ダッシュボード</a>
                <a href="/tools" class="tool-link">🔧 ツール一覧</a>
            </div>
        </div>
    </body>
    </html>
    """)

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = "guest"):
    """
    ダッシュボード - Laravel風のレイアウト
    """
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 AI Development Dashboard</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px 0; }}
            .header-content {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
            .logo {{ font-size: 24px; font-weight: bold; }}
            .user-info {{ font-size: 16px; }}
            .main-content {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; }}
            .tools-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .tool-card {{ background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: transform 0.2s; }}
            .tool-card:hover {{ transform: translateY(-2px); }}
            .tool-title {{ font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #333; }}
            .tool-description {{ color: #666; margin-bottom: 15px; line-height: 1.5; }}
            .tool-url {{ font-family: monospace; background: #f1f5f9; padding: 8px 12px; border-radius: 6px; font-size: 14px; margin-bottom: 15px; }}
            .tool-btn {{ background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 6px; text-decoration: none; display: inline-block; transition: background 0.2s; }}
            .tool-btn:hover {{ background: #5a67d8; }}
            .url-info {{ background: #e2e8f0; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #667eea; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="header-content">
                <div class="logo">🚀 AI Development Platform</div>
                <div class="user-info">👤 {username}</div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="url-info">
                <strong>📍 現在のURL:</strong> {request.url}
            </div>
            
            <div class="tools-grid">
                <div class="tool-card">
                    <div class="tool-title">Gradio Direct</div>
                    <div class="tool-description">統合Gradioインターフェース</div>
                    <div class="tool-url">/gradio</div>
                    <a href="/gradio" class="tool-btn" target="_blank">開く</a>
                </div>
                
                <div class="tool-card">
                    <div class="tool-title">Tools Dashboard</div>
                    <div class="tool-description">全ツールの統合管理画面</div>
                    <div class="tool-url">/tools</div>
                    <a href="/tools" class="tool-btn" target="_blank">開く</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

# 個別Gradioマウント機能
def mount_gradio_interface(app: FastAPI, interface_name: str, mount_path: str):
    """
    特定のGradioインターフェースを指定されたパスにマウント
    
    Args:
        app: FastAPIアプリケーション
        interface_name: Gradioインターフェース名
        mount_path: マウントパス（例："/tools/chat"）
    """
    try:
        # Laravel風Controller経由でインターフェース取得
        try:
            from app.Http.Controllers.GradioController import GradioController
            controller = GradioController()
            interfaces, names = controller.gradio_service.collect_gradio_interfaces()
            
            # 指定されたインターフェースを検索
            target_interface = None
            for interface, name in zip(interfaces, names):
                if interface_name.lower() in name.lower():
                    target_interface = interface
                    break
            
            if target_interface:
                # Gradioをマウント
                gradio_asgi = gr.routes.App.create_app(target_interface)
                app.mount(mount_path, gradio_asgi)
                gradio_cache[mount_path] = {
                    "interface": target_interface,
                    "name": interface_name,
                    "mounted": True
                }
                return True, f"✅ {interface_name} mounted at {mount_path}"
            else:
                return False, f"❌ Interface '{interface_name}' not found"
                
        except ImportError:
            # フォールバック: 直接インターフェース作成
            fallback_interface = gr.Interface(
                fn=lambda x: f"Hello from {interface_name}!",
                inputs="text",
                outputs="text",
                title=f"{interface_name} Interface"
            )
            gradio_asgi = gr.routes.App.create_app(fallback_interface)
            app.mount(mount_path, gradio_asgi)
            gradio_cache[mount_path] = {
                "interface": fallback_interface,
                "name": interface_name,
                "mounted": True,
                "fallback": True
            }
            return True, f"✅ Fallback {interface_name} mounted at {mount_path}"
            
    except Exception as e:
        return False, f"❌ Error mounting {interface_name}: {str(e)}"

# システム統合テスト
@router.get("/test/integration")
async def test_integration():
    """
    システム統合テスト - Laravel風構成の動作確認
    """
    test_results = {
        "database_connection": False,
        "gradio_initialization": False,
        "controller_access": False,
        "service_layer": False
    }
    
    try:
        # データベース接続テスト
        from config.database import get_db_connection
        conn = get_db_connection('chat_history')
        conn.close()
        test_results["database_connection"] = True
    except Exception as e:
        test_results["database_error"] = str(e)
    
    try:
        # Gradio初期化テスト
        tabbed_interface = initialize_gradio_with_error_handling()
        test_results["gradio_initialization"] = True
    except Exception as e:
        test_results["gradio_error"] = str(e)
    
    try:
        # Controller アクセステスト
        from app.Http.Controllers.GradioController import GradioController
        controller = GradioController()
        test_results["controller_access"] = True
    except Exception as e:
        test_results["controller_error"] = str(e)
    
    try:
        # Service層テスト
        from app.Services.GradioInterfaceService import GradioInterfaceService
        service = GradioInterfaceService()
        test_results["service_layer"] = True
    except Exception as e:
        test_results["service_error"] = str(e)
    
    return JSONResponse(content=test_results)
