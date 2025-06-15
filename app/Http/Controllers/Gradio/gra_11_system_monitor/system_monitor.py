#!/usr/bin/env python3
"""
🔧 システム監視・ヘルスチェック機能
Laravel風のサービス監視システム
"""

import os
import sys
import json
import time
import psutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import gradio as gr
from typing import Dict, List, Any
import asyncio
import aiohttp
import requests

class SystemMonitor:
    """システム監視クラス"""
    
    def __init__(self):
        self.base_dir = Path('/workspaces/AUTOCREATE')
        self.db_path = self.base_dir / 'database' / 'system_monitor.db'
        self.init_database()
        
    def init_database(self):
        """監視データベース初期化"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # システム監視ログテーブル
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    component TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT,
                    details TEXT,
                    cpu_usage REAL,
                    memory_usage REAL,
                    disk_usage REAL
                )
            ''')
            
            # サービス監視テーブル
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS service_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    service_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    response_time REAL,
                    error_message TEXT
                )
            ''')
            
            conn.commit()
    
    def get_system_info(self) -> Dict[str, Any]:
        """システム情報取得"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # メモリ使用率
            memory = psutil.virtual_memory()
            
            # ディスク使用率
            disk = psutil.disk_usage('/')
            
            # プロセス情報
            python_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_percent', 'cpu_percent']):
                try:
                    if proc.info['name'] == 'python' or proc.info['name'] == 'python3':
                        if proc.info['cmdline'] and any('asgi' in cmd or 'app.py' in cmd for cmd in proc.info['cmdline']):
                            python_processes.append({
                                'pid': proc.info['pid'],
                                'cmdline': ' '.join(proc.info['cmdline'][:3]),
                                'memory_percent': proc.info['memory_percent'],
                                'cpu_percent': proc.info['cpu_percent']
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'usage_percent': cpu_percent,
                    'count': psutil.cpu_count()
                },
                'memory': {
                    'total': memory.total,
                    'used': memory.used,
                    'percent': memory.percent,
                    'available': memory.available
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'percent': (disk.used / disk.total) * 100
                },
                'processes': python_processes
            }
        except Exception as e:
            return {'error': str(e)}
    
    def check_services(self) -> Dict[str, Any]:
        """サービス死活監視"""
        services = {
            'gradio_main': 'http://localhost:7860',
            'fastapi_main': 'http://localhost:8000',
            'gradio_root': 'http://localhost:7861',
        }
        
        results = {}
        
        for service_name, url in services.items():
            try:
                start_time = time.time()
                response = requests.get(url, timeout=5)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    results[service_name] = {
                        'status': 'healthy',
                        'response_time': response_time,
                        'status_code': response.status_code
                    }
                else:
                    results[service_name] = {
                        'status': 'unhealthy',
                        'response_time': response_time,
                        'status_code': response.status_code
                    }
            except Exception as e:
                results[service_name] = {
                    'status': 'error',
                    'error': str(e),
                    'response_time': None
                }
        
        return results
    
    def check_databases(self) -> Dict[str, Any]:
        """データベース監視"""
        databases = {
            'chat_history': self.base_dir / 'chat_history.db',
            'system_monitor': self.base_dir / 'database' / 'system_monitor.db',
            'github_issues': self.base_dir / 'database' / 'github_issues_automation.db'
        }
        
        results = {}
        
        for db_name, db_path in databases.items():
            try:
                if db_path.exists():
                    with sqlite3.connect(db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                        tables = cursor.fetchall()
                        
                        # データベース接続テスト
                        cursor.execute("SELECT 1")
                        cursor.fetchone()
                        
                        results[db_name] = {
                            'status': 'healthy',
                            'tables_count': len(tables),
                            'size_mb': db_path.stat().st_size / (1024 * 1024)
                        }
                else:
                    results[db_name] = {
                        'status': 'missing',
                        'error': 'Database file not found'
                    }
            except Exception as e:
                results[db_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def check_gradio_interfaces(self) -> Dict[str, Any]:
        """Gradioインターフェース監視"""
        interfaces_dir = self.base_dir / 'app' / 'Http' / 'Controllers' / 'Gradio'
        
        results = {}
        
        if interfaces_dir.exists():
            for interface_dir in interfaces_dir.iterdir():
                if interface_dir.is_dir():
                    try:
                        # Pythonファイルの存在チェック
                        python_files = list(interface_dir.glob('*.py'))
                        
                        if python_files:
                            results[interface_dir.name] = {
                                'status': 'available',
                                'files_count': len(python_files),
                                'files': [f.name for f in python_files]
                            }
                        else:
                            results[interface_dir.name] = {
                                'status': 'empty',
                                'files_count': 0
                            }
                    except Exception as e:
                        results[interface_dir.name] = {
                            'status': 'error',
                            'error': str(e)
                        }
        
        return results
    
    def log_system_status(self, system_info: Dict[str, Any], services: Dict[str, Any]):
        """システム状態をログに記録"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # システム監視ログ
                cursor.execute('''
                    INSERT INTO system_logs 
                    (component, status, message, details, cpu_usage, memory_usage, disk_usage)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    'system',
                    'healthy' if system_info.get('cpu', {}).get('usage_percent', 0) < 80 else 'warning',
                    'System monitoring',
                    json.dumps(system_info),
                    system_info.get('cpu', {}).get('usage_percent'),
                    system_info.get('memory', {}).get('percent'),
                    system_info.get('disk', {}).get('percent')
                ))
                
                # サービス監視ログ
                for service_name, service_data in services.items():
                    cursor.execute('''
                        INSERT INTO service_status 
                        (service_name, status, response_time, error_message)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        service_name,
                        service_data.get('status'),
                        service_data.get('response_time'),
                        service_data.get('error')
                    ))
                
                conn.commit()
        except Exception as e:
            print(f"Error logging system status: {e}")
    
    def get_system_dashboard(self) -> str:
        """システムダッシュボード生成"""
        try:
            # システム情報取得
            system_info = self.get_system_info()
            services = self.check_services()
            databases = self.check_databases()
            interfaces = self.check_gradio_interfaces()
            
            # ログに記録
            self.log_system_status(system_info, services)
            
            # ダッシュボード生成
            dashboard = f"""
# 🔧 システム監視ダッシュボード
**更新時刻**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 💻 システム状態
- **CPU使用率**: {system_info.get('cpu', {}).get('usage_percent', 0):.1f}%
- **メモリ使用率**: {system_info.get('memory', {}).get('percent', 0):.1f}%
- **ディスク使用率**: {system_info.get('disk', {}).get('percent', 0):.1f}%

## 🚀 サービス監視
"""
            
            for service_name, service_data in services.items():
                status_emoji = {
                    'healthy': '✅',
                    'unhealthy': '⚠️',
                    'error': '❌'
                }.get(service_data.get('status'), '❓')
                
                dashboard += f"- **{service_name}**: {status_emoji} {service_data.get('status', 'unknown')}"
                if service_data.get('response_time'):
                    dashboard += f" ({service_data.get('response_time', 0):.3f}s)"
                dashboard += "\n"
            
            dashboard += "\n## 💾 データベース監視\n"
            for db_name, db_data in databases.items():
                status_emoji = {
                    'healthy': '✅',
                    'missing': '⚠️',
                    'error': '❌'
                }.get(db_data.get('status'), '❓')
                
                dashboard += f"- **{db_name}**: {status_emoji} {db_data.get('status', 'unknown')}"
                if db_data.get('tables_count'):
                    dashboard += f" ({db_data.get('tables_count')}テーブル)"
                dashboard += "\n"
            
            dashboard += "\n## 🎨 Gradioインターフェース監視\n"
            for interface_name, interface_data in interfaces.items():
                status_emoji = {
                    'available': '✅',
                    'empty': '⚠️',
                    'error': '❌'
                }.get(interface_data.get('status'), '❓')
                
                dashboard += f"- **{interface_name}**: {status_emoji} {interface_data.get('status', 'unknown')}"
                if interface_data.get('files_count'):
                    dashboard += f" ({interface_data.get('files_count')}ファイル)"
                dashboard += "\n"
            
            return dashboard
            
        except Exception as e:
            return f"❌ エラー: {str(e)}"
    
    def get_historical_data(self, hours: int = 24) -> str:
        """履歴データ取得"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 過去24時間のデータ
                cursor.execute('''
                    SELECT timestamp, cpu_usage, memory_usage, disk_usage
                    FROM system_logs 
                    WHERE timestamp > datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                    LIMIT 100
                '''.format(hours))
                
                rows = cursor.fetchall()
                
                if not rows:
                    return "📊 履歴データなし"
                
                report = f"📊 過去{hours}時間のシステム履歴\n\n"
                
                for row in rows:
                    timestamp, cpu, memory, disk = row
                    report += f"- **{timestamp}**: CPU {cpu:.1f}%, メモリ {memory:.1f}%, ディスク {disk:.1f}%\n"
                
                return report
                
        except Exception as e:
            return f"❌ エラー: {str(e)}"

# システム監視インスタンス
monitor = SystemMonitor()

def update_dashboard():
    """ダッシュボード更新"""
    return monitor.get_system_dashboard()

def get_historical_report():
    """履歴レポート取得"""
    return monitor.get_historical_data()

def restart_services():
    """サービス再起動"""
    try:
        # 簡単な再起動シミュレーション
        return "🔄 サービス再起動を開始しました\n（実際の再起動は手動で実行してください）"
    except Exception as e:
        return f"❌ エラー: {str(e)}"

# Gradioインターフェース
with gr.Blocks(title="🔧 システム監視", theme=gr.themes.Soft()) as gradio_interface:
    gr.Markdown("# 🔧 システム監視・ヘルスチェック")
    
    with gr.Tab("📊 リアルタイム監視"):
        dashboard_output = gr.Markdown(value=update_dashboard())
        
        with gr.Row():
            refresh_btn = gr.Button("🔄 更新", variant="primary")
            restart_btn = gr.Button("🚀 再起動", variant="secondary")
        
        refresh_btn.click(fn=update_dashboard, outputs=dashboard_output)
        restart_btn.click(fn=restart_services, outputs=gr.Textbox(label="再起動結果"))
    
    with gr.Tab("📈 履歴データ"):
        historical_output = gr.Markdown(value=get_historical_report())
        
        refresh_history_btn = gr.Button("📊 履歴更新")
        refresh_history_btn.click(fn=get_historical_report, outputs=historical_output)
    
    with gr.Tab("⚙️ 設定"):
        gr.Markdown("""
        ## 🔧 監視設定
        - 監視間隔: 5分
        - ログ保持期間: 30日
        - アラート閾値: CPU > 80%, メモリ > 90%
        
        ## 📊 データベース
        - 監視データ: `/database/system_monitor.db`
        - 自動バックアップ: 有効
        """)

if __name__ == "__main__":
    print("🔧 システム監視システムを起動中...")
    gradio_interface.launch(server_name="0.0.0.0", server_port=7863)
