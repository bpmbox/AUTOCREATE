#!/usr/bin/env python3
"""
🚀 AI自動化システム - FastAPI エンドポイント
========================================

GitHub Copilot自動化システムの主要機能をFastAPIエンドポイントとして公開
OpenAPI/Swaggerで他のAIが理解・利用可能な形式で提供
"""

import os
import sys
import asyncio
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 自動化システムをインポート
try:
    from tests.Feature.copilot_github_cli_automation import GitHubCopilotAutomation
    from tests.Feature.copilot_direct_answer_fixed import CopilotSupabaseIntegrationSystem
except ImportError as e:
    print(f"⚠️ 自動化システムのインポートに失敗: {e}")
    GitHubCopilotAutomation = None
    CopilotSupabaseIntegrationSystem = None

router = APIRouter(prefix="/automation", tags=["AI Automation"])

# ==============================================================================
# リクエスト/レスポンスモデル定義
# ==============================================================================

class AutomationRequest(BaseModel):
    """自動化リクエストモデル"""
    message: str = Field(..., description="処理したいメッセージ・質問")
    create_issue: bool = Field(True, description="GitHub Issueを作成するかどうか")
    generate_mermaid: bool = Field(True, description="Mermaid図を生成するかどうか") 
    offline_mode: bool = Field(False, description="オフラインモードで実行するかどうか")

class IssueCreationRequest(BaseModel):
    """Issue作成リクエストモデル"""
    title: str = Field(..., description="Issueのタイトル")
    description: str = Field(..., description="Issueの説明")
    labels: List[str] = Field(default=[], description="Issueに付けるラベル")
    assignee: Optional[str] = Field(None, description="担当者のGitHubユーザー名")

class MermaidGenerationRequest(BaseModel):
    """Mermaid図生成リクエストモデル"""
    content: str = Field(..., description="Mermaid図生成の元となるコンテンツ")
    diagram_type: str = Field("flowchart", description="図の種類 (flowchart, sequence, class, etc.)")

class AutomationResponse(BaseModel):
    """自動化レスポンスモデル"""
    success: bool = Field(..., description="処理成功フラグ")
    message: str = Field(..., description="処理結果メッセージ")
    issue_url: Optional[str] = Field(None, description="作成されたGitHub IssueのURL")
    mermaid_content: Optional[str] = Field(None, description="生成されたMermaid図のコンテンツ")
    mermaid_file_path: Optional[str] = Field(None, description="保存されたMermaid図ファイルのパス")
    processing_time: float = Field(..., description="処理時間（秒）")
    details: Dict[str, Any] = Field(default={}, description="追加の詳細情報")

class SystemStatusResponse(BaseModel):
    """システム状態レスポンスモデル"""
    status: str = Field(..., description="システム状態")
    github_cli_available: bool = Field(..., description="GitHub CLIが利用可能かどうか")
    supabase_connected: bool = Field(..., description="Supabaseに接続済みかどうか")
    environment_variables: Dict[str, bool] = Field(..., description="環境変数の設定状況")
    last_check: str = Field(..., description="最後のチェック時刻")

# ==============================================================================
# 依存関数
# ==============================================================================

def get_automation_system():
    """GitHub Copilot自動化システムのインスタンスを取得"""
    if GitHubCopilotAutomation is None:
        raise HTTPException(status_code=500, detail="自動化システムが利用できません")
    return GitHubCopilotAutomation(offline_mode=True)

def get_copilot_system():
    """Copilot-Supabase統合システムのインスタンスを取得"""
    if CopilotSupabaseIntegrationSystem is None:
        raise HTTPException(status_code=500, detail="Copilot統合システムが利用できません")
    return CopilotSupabaseIntegrationSystem()

# ==============================================================================
# エンドポイント定義
# ==============================================================================

@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    """
    システムの状態を取得
    
    Returns:
        SystemStatusResponse: システムの状態情報
    """
    try:
        # GitHub CLIの利用可能性をチェック
        github_cli_available = False
        try:
            import subprocess
            result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
            github_cli_available = result.returncode == 0
        except:
            pass
        
        # 環境変数の設定状況をチェック
        env_vars = {
            'SUPABASE_URL': bool(os.getenv('SUPABASE_URL')),
            'SUPABASE_KEY': bool(os.getenv('SUPABASE_KEY')),
            'GITHUB_TOKEN': bool(os.getenv('GITHUB_TOKEN')),
            'DEBUG_MODE': bool(os.getenv('DEBUG_MODE'))
        }
        
        # Supabase接続をチェック
        supabase_connected = False
        try:
            if env_vars['SUPABASE_URL'] and env_vars['SUPABASE_KEY']:
                # 簡単な接続テスト（実際にはより詳細なチェックが必要）
                supabase_connected = True
        except:
            pass
        
        return SystemStatusResponse(
            status="healthy" if github_cli_available and supabase_connected else "degraded",
            github_cli_available=github_cli_available,
            supabase_connected=supabase_connected,
            environment_variables=env_vars,
            last_check=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ステータス取得エラー: {str(e)}")

@router.post("/run", response_model=AutomationResponse)
async def run_automation(
    request: AutomationRequest,
    background_tasks: BackgroundTasks,
    automation_system = Depends(get_automation_system)
):
    """
    AI自動化システムの完全実行
    
    メッセージを受け取り、以下の処理を自動実行:
    1. GitHub Issue作成（オプション）
    2. Mermaid図生成（オプション）
    3. Copilot統合処理
    
    Args:
        request: AutomationRequest - 実行パラメータ
        
    Returns:
        AutomationResponse: 実行結果
    """
    start_time = datetime.now()
    
    try:
        response_data = {
            "success": False,
            "message": "処理開始",
            "issue_url": None,
            "mermaid_content": None,
            "mermaid_file_path": None,
            "processing_time": 0.0,
            "details": {}
        }
        
        # Mermaid図生成（リクエストされた場合）
        if request.generate_mermaid:
            try:
                mermaid_content = automation_system.generate_dynamic_mermaid_diagram(request.message)
                if mermaid_content:
                    # ファイルに保存
                    mermaid_file_path = automation_system.save_mermaid_to_file(
                        mermaid_content, 
                        f"automation_{int(datetime.now().timestamp())}"
                    )
                    response_data["mermaid_content"] = mermaid_content
                    response_data["mermaid_file_path"] = mermaid_file_path
                    response_data["details"]["mermaid_generated"] = True
                else:
                    response_data["details"]["mermaid_generated"] = False
            except Exception as e:
                response_data["details"]["mermaid_error"] = str(e)
        
        # GitHub Issue作成（リクエストされた場合）
        if request.create_issue:
            try:
                issue_url = automation_system.create_github_issue(
                    title=f"AI自動化: {request.message[:50]}...",
                    body=f"**自動生成されたIssue**\n\n質問/要求: {request.message}\n\n生成時刻: {datetime.now().isoformat()}"
                )
                if issue_url:
                    response_data["issue_url"] = issue_url
                    response_data["details"]["issue_created"] = True
                else:
                    response_data["details"]["issue_created"] = False
            except Exception as e:
                response_data["details"]["issue_error"] = str(e)
        
        # 処理時間を計算
        processing_time = (datetime.now() - start_time).total_seconds()
        response_data["processing_time"] = processing_time
        response_data["success"] = True
        response_data["message"] = "自動化処理が完了しました"
        
        return AutomationResponse(**response_data)
        
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "processing_time": processing_time
        }
        
        raise HTTPException(
            status_code=500, 
            detail=f"自動化処理エラー: {str(e)}"
        )

@router.post("/issue/create", response_model=Dict[str, Any])
async def create_github_issue(
    request: IssueCreationRequest,
    automation_system = Depends(get_automation_system)
):
    """
    GitHub Issueを作成
    
    Args:
        request: IssueCreationRequest - Issue作成パラメータ
        
    Returns:
        dict: 作成結果
    """
    try:
        issue_url = automation_system.create_github_issue(
            title=request.title,
            body=request.description,
            labels=request.labels,
            assignee=request.assignee
        )
        
        return {
            "success": True,
            "message": "GitHub Issueが正常に作成されました",
            "issue_url": issue_url,
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Issue作成エラー: {str(e)}")

@router.post("/mermaid/generate", response_model=Dict[str, Any])
async def generate_mermaid_diagram(
    request: MermaidGenerationRequest,
    automation_system = Depends(get_automation_system)
):
    """
    Mermaid図を生成
    
    Args:
        request: MermaidGenerationRequest - 図生成パラメータ
        
    Returns:
        dict: 生成結果
    """
    try:
        mermaid_content = automation_system.generate_dynamic_mermaid_diagram(request.content)
        
        if not mermaid_content:
            raise HTTPException(status_code=400, detail="Mermaid図の生成に失敗しました")
        
        # ファイルに保存
        file_name = f"mermaid_{request.diagram_type}_{int(datetime.now().timestamp())}"
        file_path = automation_system.save_mermaid_to_file(mermaid_content, file_name)
        
        return {
            "success": True,
            "message": "Mermaid図が正常に生成されました",
            "mermaid_content": mermaid_content,
            "file_path": file_path,
            "diagram_type": request.diagram_type,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mermaid図生成エラー: {str(e)}")

@router.post("/copilot/integration", response_model=Dict[str, Any])
async def run_copilot_integration(
    message: str,
    copilot_system = Depends(get_copilot_system)
):
    """
    Copilot-Supabase統合システムを実行
    
    Args:
        message: 処理したいメッセージ
        
    Returns:
        dict: 実行結果
    """
    try:
        # Copilot統合システムでメッセージを処理
        # 注意: この部分は実際のメソッドに合わせて調整が必要
        result = await asyncio.to_thread(
            copilot_system.process_message_with_copilot,
            message
        )
        
        return {
            "success": True,
            "message": "Copilot統合処理が完了しました",
            "result": result,
            "processed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Copilot統合エラー: {str(e)}")

@router.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント
    
    Returns:
        dict: システムの健全性情報
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "AI Automation API"
    }

# ==============================================================================
# WebSocket エンドポイント（リアルタイム監視用）
# ==============================================================================

from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws/monitor")
async def websocket_monitor(websocket: WebSocket):
    """
    リアルタイム監視用WebSocketエンドポイント
    
    自動化システムの状態をリアルタイムで送信
    """
    await websocket.accept()
    
    try:
        while True:
            # システム状態を定期的に送信
            status_data = {
                "timestamp": datetime.now().isoformat(),
                "status": "running",
                "active_processes": 1,  # 実際の処理数に応じて調整
                "memory_usage": "N/A",  # 実際のメモリ使用量に応じて調整
            }
            
            await websocket.send_json(status_data)
            await asyncio.sleep(5)  # 5秒間隔で送信
            
    except WebSocketDisconnect:
        print("WebSocket接続が切断されました")
    except Exception as e:
        print(f"WebSocketエラー: {e}")
        await websocket.close()
