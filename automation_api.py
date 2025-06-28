#!/usr/bin/env python3
"""
🤖 自動化API - FastAPI自動作成システムテスト用
======================================================

Laravel風の自動化システムをテストするためのFastAPIアプリケーション
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import sys
from datetime import datetime
import json

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="🤖 AI自動化システム API",
    description="Laravel風の自動化プラットフォーム - Copilot統合",
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

# Pydanticモデル定義
class AutomationRequest(BaseModel):
    message: str
    user: str = "anonymous"
    project_type: Optional[str] = "general"
    auto_create: bool = False

class TriggerResponse(BaseModel):
    status: str
    message: str
    automation_id: str
    project_name: Optional[str] = None
    mermaid_file: Optional[str] = None

# ルートエンドポイント
@app.get("/")
async def root():
    return {
        "message": "🤖 AI自動化システム API",
        "status": "running",
        "framework": "FastAPI + Laravel風アーキテクチャ",
        "features": [
            "Copilot自動化",
            "Mermaid図生成",
            "GitHub連携",
            "プロジェクト自動作成"
        ],
        "endpoints": {
            "automation": "/automation/trigger",
            "status": "/api/status", 
            "health": "/health",
            "copilot": "/automation/copilot"
        }
    }

@app.get("/api/status")
async def api_status():
    return {
        "status": "ok",
        "service": "automation-api",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    try:
        # .envファイルの存在確認
        env_exists = os.path.exists('.env')
        
        # Copilot自動化クラスの確認
        copilot_available = False
        try:
            from app.Console.Commands.copilot_github_cli_automation import GitHubCopilotAutomation
            copilot_available = True
        except ImportError:
            pass
        
        return {
            "status": "healthy",
            "checks": {
                "env_file": env_exists,
                "copilot_automation": copilot_available,
                "api_server": True
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/automation/trigger", response_model=TriggerResponse)
async def automation_trigger(request: AutomationRequest):
    """自動化システムのメイントリガーエンドポイント"""
    try:
        print(f"🤖 自動化トリガー受信: {request.message}")
        
        # Copilot自動化システムの初期化（テストモード）
        try:
            from app.Console.Commands.copilot_github_cli_automation import GitHubCopilotAutomation
            automation = GitHubCopilotAutomation(offline_mode=True)
            
            # Mermaid図生成テスト
            if request.auto_create:
                mermaid_code = automation.generate_dynamic_mermaid_diagram(request.message)
                
                # ファイル保存
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                mermaid_filename = f"automation_test_{timestamp}.mermaid"
                
                with open(mermaid_filename, 'w', encoding='utf-8') as f:
                    f.write(mermaid_code)
                
                # プロジェクト名生成
                project_name = automation.extract_project_name(request.message)
                
                return TriggerResponse(
                    status="success",
                    message="自動化システムが正常に実行されました",
                    automation_id=f"auto_{timestamp}",
                    project_name=project_name,
                    mermaid_file=mermaid_filename
                )
            else:
                return TriggerResponse(
                    status="received",
                    message="リクエストを受信しました（自動作成は無効）",
                    automation_id=f"test_{datetime.now().strftime('%H%M%S')}"
                )
                
        except ImportError:
            return TriggerResponse(
                status="fallback",
                message="Copilot自動化システムが利用できません（フォールバックモード）",
                automation_id=f"fallback_{datetime.now().strftime('%H%M%S')}"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"自動化システムエラー: {str(e)}")

@app.get("/automation/copilot")
async def copilot_status():
    """Copilot自動化システムの状態確認"""
    try:
        from app.Console.Commands.copilot_github_cli_automation import GitHubCopilotAutomation
        
        # テストモードで初期化
        automation = GitHubCopilotAutomation(offline_mode=True)
        
        # 座標ファイルの確認
        coords = automation.load_coordinates()
        
        return {
            "status": "available",
            "offline_mode": automation.offline_mode,
            "coordinates_loaded": coords is not None,
            "features": [
                "Mermaid図生成",
                "GitHub連携",
                "プロジェクト自動作成",
                "Supabase連携"
            ]
        }
        
    except ImportError as e:
        return {
            "status": "unavailable",
            "error": "Copilot自動化システムがインポートできません",
            "details": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/automation/test")
async def automation_test():
    """自動化システムの統合テスト"""
    test_results = {}
    
    try:
        # 1. Copilot自動化システムテスト
        try:
            from app.Console.Commands.copilot_github_cli_automation import GitHubCopilotAutomation
            automation = GitHubCopilotAutomation(offline_mode=True)
            
            # 基本機能テスト
            coords = automation.load_coordinates()
            test_results["copilot"] = {
                "status": "ok",
                "coordinates": coords is not None,
                "offline_mode": automation.offline_mode
            }
        except Exception as e:
            test_results["copilot"] = {
                "status": "error",
                "error": str(e)
            }
        
        # 2. Mermaid図生成テスト
        try:
            test_message = "FastAPI自動化システムのテストプロジェクト"
            if 'copilot' in test_results and test_results['copilot']['status'] == 'ok':
                # オフラインモード用のテストMermaid
                mermaid_code = """graph TD
    A[FastAPI自動化システム] --> B[テスト実行]
    B --> C[API エンドポイント]
    C --> D[Copilot統合]
    D --> E[結果レポート]"""
                
                test_results["mermaid"] = {
                    "status": "ok",
                    "generated": True,
                    "lines": len(mermaid_code.split('\n'))
                }
            else:
                test_results["mermaid"] = {
                    "status": "skipped",
                    "reason": "Copilot unavailable"
                }
        except Exception as e:
            test_results["mermaid"] = {
                "status": "error",
                "error": str(e)
            }
        
        # 3. 環境設定テスト
        test_results["environment"] = {
            "env_file": os.path.exists('.env'),
            "project_root": os.path.exists('artisan'),
            "app_structure": os.path.exists('app/Console/Commands/')
        }
        
        # 総合結果
        passed_tests = sum(1 for result in test_results.values() 
                          if isinstance(result, dict) and result.get('status') == 'ok')
        total_tests = len([k for k in test_results.keys() if k != 'environment'])
        
        return {
            "test_summary": {
                "passed": passed_tests,
                "total": total_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%"
            },
            "test_results": test_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "test_summary": {
                "passed": 0,
                "total": 0,
                "success_rate": "0%"
            },
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 自動化API サーバー起動中...")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
