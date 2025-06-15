"""
🌐 API Routes - Laravel風REST API システム
==========

RESTful API用のルーティング + システム監視・管理API
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import sqlite3
import json
import time
import psutil
from pathlib import Path

# Laravel風のAPIレスポンスモデル
class APIResponse(BaseModel):
    """標準APIレスポンス形式"""
    success: bool = True
    message: str = "Success"
    data: Any = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class SystemInfoModel(BaseModel):
    """システム情報モデル"""
    version: str
    status: str
    components: Dict[str, Any]

class HealthCheckModel(BaseModel):
    """ヘルスチェックモデル"""
    status: str
    services: Dict[str, str]
    timestamp: str

# APIコントローラークラス
class APIController:
    """Laravel風のAPIコントローラーベースクラス"""
    
    def __init__(self):
        self.db_path = Path('/workspaces/AUTOCREATE/database/api_system.db')
        self.init_database()
    
    def init_database(self):
        """データベース初期化"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # APIリクエストログ
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    endpoint TEXT NOT NULL,
                    method TEXT NOT NULL,
                    status_code INTEGER,
                    response_time REAL,
                    ip_address TEXT
                )
            ''')
            
            conn.commit()
    
    def log_request(self, endpoint: str, method: str, status_code: int, 
                   response_time: float, ip_address: str):
        """APIリクエストログ記録"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO api_logs 
                    (endpoint, method, status_code, response_time, ip_address)
                    VALUES (?, ?, ?, ?, ?)
                ''', (endpoint, method, status_code, response_time, ip_address))
                conn.commit()
        except Exception as e:
            print(f"Error logging API request: {e}")

# システムAPI管理
class SystemAPIController(APIController):
    """システムAPI管理"""
    
    def get_system_info(self) -> SystemInfoModel:
        """システム情報取得"""
        try:
            # システム情報収集
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            components = {
                'cpu': {
                    'usage_percent': round(cpu_percent, 1),
                    'cores': psutil.cpu_count()
                },
                'memory': {
                    'usage_percent': round(memory.percent, 1),
                    'total_gb': round(memory.total / (1024**3), 2)
                },
                'disk': {
                    'usage_percent': round((disk.used / disk.total) * 100, 1),
                    'total_gb': round(disk.total / (1024**3), 2)
                }
            }
            
            status = "healthy"
            if cpu_percent > 80 or memory.percent > 90:
                status = "warning"
            
            return SystemInfoModel(
                version="1.0.0",
                status=status,
                components=components
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"System info error: {str(e)}")
    
    def health_check(self) -> HealthCheckModel:
        """ヘルスチェック"""
        try:
            import requests
            
            services = {}
            
            # Gradioサービス確認
            try:
                response = requests.get("http://localhost:7860", timeout=3)
                services['gradio'] = "healthy" if response.status_code == 200 else "unhealthy"
            except:
                services['gradio'] = "unavailable"
            
            # データベース確認
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    services['database'] = "healthy"
            except:
                services['database'] = "unhealthy"
            
            overall_status = "healthy" if all(s == "healthy" for s in services.values()) else "degraded"
            
            return HealthCheckModel(
                status=overall_status,
                services=services,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")

# コントローラーインスタンス
api_controller = APIController()
system_controller = SystemAPIController()

router = APIRouter()

# 既存のサンプルデータ
users_data = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]

@router.get("/")
async def api_root() -> Dict[str, Any]:
    """
    API ルート
    """
    return APIResponse(
        message="AI Development Platform API v1.0.0",
        data={
            "version": "1.0.0",
            "status": "operational",
            "endpoints": [
                "/api/users",
                "/api/users/{id}",
                "/api/health",
                "/api/system/info",
                "/api/system/health",
                "/api/gradio/interfaces",
                "/api/system/stats"
            ]
        }
    ).dict()

# 🚀 新しいシステム監視API群
@router.get("/system/info", response_model=APIResponse)
async def get_system_info():
    """システム情報取得API"""
    try:
        system_info = system_controller.get_system_info()
        return APIResponse(
            message="System information retrieved successfully",
            data=system_info.dict()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/health", response_model=APIResponse)
async def system_health_check():
    """システムヘルスチェックAPI"""
    try:
        health_data = system_controller.health_check()
        return APIResponse(
            message="Health check completed",
            data=health_data.dict()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gradio/interfaces", response_model=APIResponse)
async def list_gradio_interfaces():
    """Gradioインターフェース一覧API"""
    try:
        interfaces_dir = Path('/workspaces/AUTOCREATE/app/Http/Controllers/Gradio')
        interfaces = []
        
        if interfaces_dir.exists():
            for interface_dir in interfaces_dir.iterdir():
                if interface_dir.is_dir() and not interface_dir.name.startswith('__'):
                    python_files = list(interface_dir.glob('*.py'))
                    
                    interfaces.append({
                        'name': interface_dir.name,
                        'display_name': interface_dir.name.replace('gra_', '').replace('_', ' ').title(),
                        'path': str(interface_dir.relative_to(Path('/workspaces/AUTOCREATE'))),
                        'files_count': len(python_files),
                        'files': [f.name for f in python_files],
                        'status': 'available' if python_files else 'empty'
                    })
        
        return APIResponse(
            message="Gradio interfaces retrieved successfully",
            data={
                'interfaces': interfaces,
                'total_count': len(interfaces)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/stats", response_model=APIResponse)
async def get_api_stats():
    """API統計情報取得"""
    try:
        with sqlite3.connect(api_controller.db_path) as conn:
            cursor = conn.cursor()
            
            # 今日のリクエスト数
            cursor.execute('''
                SELECT COUNT(*) FROM api_logs 
                WHERE DATE(timestamp) = DATE('now')
            ''')
            today_requests = cursor.fetchone()[0] or 0
            
            # 人気エンドポイント（過去7日間）
            cursor.execute('''
                SELECT endpoint, COUNT(*) as requests, AVG(response_time) as avg_time
                FROM api_logs 
                WHERE DATE(timestamp) >= DATE('now', '-7 days')
                GROUP BY endpoint 
                ORDER BY requests DESC 
                LIMIT 5
            ''')
            popular_endpoints = cursor.fetchall()
            
            stats = {
                'today_requests': today_requests,
                'popular_endpoints': [
                    {
                        'endpoint': ep[0], 
                        'requests': ep[1],
                        'avg_response_time': round(ep[2] or 0, 3)
                    } 
                    for ep in popular_endpoints
                ],
                'last_updated': datetime.now().isoformat()
            }
            
            return APIResponse(
                message="API statistics retrieved successfully",
                data=stats
            )
    except Exception as e:
        return APIResponse(
            success=False,
            message=f"Stats error: {str(e)}",
            data={'today_requests': 0, 'popular_endpoints': []}
        )

@router.post("/system/restart", response_model=APIResponse)
async def restart_system():
    """システム再起動シミュレーション"""
    return APIResponse(
        message="System restart initiated (simulation only)",
        data={
            'restart_time': datetime.now().isoformat(),
            'estimated_downtime': '30 seconds',
            'note': 'This is a simulation. Actual restart requires manual intervention.'
        }
    )

# 既存のユーザーAPI（改良版）
@router.get("/users", response_model=APIResponse)
async def get_users():
    """ユーザー一覧取得"""
    return APIResponse(
        message="Users retrieved successfully",
        data={'users': users_data, 'total': len(users_data)}
    )

@router.get("/users/{user_id}", response_model=APIResponse)
async def get_user(user_id: int):
    """特定ユーザー取得"""
    user = next((u for u in users_data if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return APIResponse(
        message="User retrieved successfully",
        data=user
    )

@router.post("/users", response_model=APIResponse)
async def create_user(user_data: Dict[str, Any]):
    """ユーザー作成"""
    new_id = max(u["id"] for u in users_data) + 1 if users_data else 1
    new_user = {
        "id": new_id,
        "name": user_data.get("name", ""),
        "email": user_data.get("email", "")
    }
    users_data.append(new_user)
    
    return APIResponse(
        message="User created successfully",
        data=new_user
    )

@router.get("/health", response_model=APIResponse)
async def health_check():
    """APIヘルスチェック"""
    return APIResponse(
        message="API is healthy",
        data={
            "status": "healthy",
            "service": "AI Development Platform API",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )
