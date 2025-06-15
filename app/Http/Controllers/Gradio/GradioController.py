"""
🎨 Gradio 専用コントローラー
============================

Laravel風のGradio UIコントローラー
インタラクティブなWebインターフェースを提供
"""

from app.Http.Controllers.HybridController import HybridController
import gradio as gr
from typing import Dict, Any, List, Tuple
import json
import logging
import importlib
import os
import pkgutil
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class GradioController(HybridController):
    """
    Gradio専用のLaravel風コントローラー
    インタラクティブなWebUIを提供
    """
    
    def __init__(self):
        super().__init__()
        self.interfaces = {}
        self.main_interface = None
        
    def gradio_process(self, input_text: str) -> str:
        """
        Gradio メイン処理関数
        """
        try:
            # 基本的なエコー処理（継承先で実装をオーバーライド）
            return f"処理結果: {input_text}"
        except Exception as e:
            logger.error(f"Gradio processing error: {e}")
            return f"エラーが発生しました: {e}"
    
    def create_main_interface(self) -> gr.Interface:
        """
        メインGradioインターフェースを作成
        """
        if not self.main_interface:
            self.main_interface = gr.Interface(
                fn=self.gradio_process,
                inputs=[
                    gr.Textbox(
                        label="入力テキスト",
                        placeholder="処理したいテキストを入力してください",
                        lines=3
                    )
                ],
                outputs=[
                    gr.Textbox(
                        label="処理結果",
                        lines=5
                    )
                ],
                title="🎨 Laravel風 Gradio インターフェース",
                description="FastAPI + Django + Gradio 統合システム",
                theme=gr.themes.Soft(),
                css="""
                .gradio-container {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .gr-button {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    color: white;
                }
                """
            )
            
            # Gradio 4.31.5での正しいキュー制御
            try:
                self.main_interface.enable_queue = False
                if hasattr(self.main_interface, '_queue'):
                    self.main_interface._queue = None
                print("✅ Main interface queue disabled")
                    
            except Exception as queue_error:
                print(f"⚠️ Main interface queue setup warning: {queue_error}")
            
        return self.main_interface
    
    def include_gradio_interfaces(self) -> Dict[str, gr.Interface]:
        """
        既存のGradioインターフェースを統合
        """
        interfaces = {}
        
        # 検索対象ディレクトリ
        search_dirs = [
            ("controllers", "controllers"),
            ("routers", "routers"),
            ("app.Http.Controllers", "app/Http/Controllers"),
        ]
        
        for package_name, package_path in search_dirs:
            if not os.path.exists(package_path):
                continue
                
            try:
                # パッケージ内のGradioインターフェースを検索
                for finder, name, ispkg in pkgutil.walk_packages([package_path]):
                    if ispkg:
                        continue
                    
                    try:
                        module_name = f"{package_name}.{name}"
                        module = importlib.import_module(module_name)
                        
                        # Gradioインターフェースを検索
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if isinstance(attr, gr.Interface):
                                interface_key = f"{name}_{attr_name}"
                                interfaces[interface_key] = attr
                                logger.info(f"Found Gradio interface: {interface_key}")
                                
                    except Exception as e:
                        logger.debug(f"Failed to import {module_name}: {e}")
                        
            except Exception as e:
                logger.error(f"Error scanning {package_path}: {e}")
        
        self.interfaces = interfaces
        return interfaces
    
    def create_tabbed_interface(self) -> gr.TabbedInterface:
        """
        タブ形式の統合インターフェースを作成
        """
        # 既存インターフェースを収集
        self.include_gradio_interfaces()
        
        # メインインターフェースを追加
        all_interfaces = [self.create_main_interface()]
        tab_names = ["メイン"]
        
        # 既存インターフェースを追加（キュー無効化付き）
        for name, interface in self.interfaces.items():
            # 各インターフェースのキューを無効化
            try:
                if hasattr(interface, '_queue'):
                    interface._queue = None
                if hasattr(interface, 'enable_queue'):
                    interface.enable_queue = False
                if hasattr(interface, 'queue_enabled_for_network'):
                    interface.queue_enabled_for_network = False
                print(f"✅ Interface '{name}' queue disabled")
            except Exception as e:
                print(f"⚠️ Interface '{name}' queue disable warning: {e}")
            
            all_interfaces.append(interface)
            tab_names.append(name)
        
        # タブ形式インターフェース作成
        tabbed_interface = gr.TabbedInterface(
            all_interfaces,
            tab_names,
            title="🏗️ Laravel風 統合ダッシュボード",
            css="""
            .gradio-container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .tab-nav {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            """
        )
        
        # TabbedInterface自体のキューも無効化
        try:
            if hasattr(tabbed_interface, '_queue'):
                tabbed_interface._queue = None
            if hasattr(tabbed_interface, 'enable_queue'):
                tabbed_interface.enable_queue = False
            if hasattr(tabbed_interface, 'queue_enabled_for_network'):
                tabbed_interface.queue_enabled_for_network = False
            print("✅ TabbedInterface queue completely disabled")
        except Exception as e:
            print(f"⚠️ TabbedInterface queue disable warning: {e}")
        
        return tabbed_interface
    
    async def index(self) -> Dict[str, Any]:
        """
        Gradio インターフェース一覧
        """
        self.include_gradio_interfaces()
        
        return {
            "status": "success",
            "data": {
                "available_interfaces": list(self.interfaces.keys()),
                "total_interfaces": len(self.interfaces),
                "main_interface": "available"
            },
            "message": "Gradio interfaces retrieved successfully"
        }
    
    async def store(self, request) -> Dict[str, Any]:
        """
        新規インターフェース作成（プレースホルダー）
        """
        return {
            "status": "success",
            "message": "Interface creation not yet implemented"
        }
    
    async def show(self, id: int) -> Dict[str, Any]:
        """
        特定インターフェース情報取得
        """
        interface_list = list(self.interfaces.keys())
        if id < 1 or id > len(interface_list):
            raise HTTPException(status_code=404, detail="Interface not found")
        
        interface_name = interface_list[id - 1]
        
        return {
            "status": "success",
            "data": {
                "id": id,
                "name": interface_name,
                "type": "gradio_interface"
            },
            "message": "Interface information retrieved successfully"
        }
    
    async def update(self, id: int, request) -> Dict[str, Any]:
        """
        インターフェース更新（プレースホルダー）
        """
        return {
            "status": "success",
            "message": "Interface update not yet implemented"
        }
    
    async def destroy(self, id: int) -> Dict[str, Any]:
        """
        インターフェース削除（プレースホルダー）
        """
        return {
            "status": "success",
            "message": "Interface deletion not yet implemented"
        }
    
    def setup_gradio_interfaces(self):
        """
        Gradio インターフェースをセットアップ - キューエラー防止対応
        """
        try:
            # GradioInterfaceServiceを使用してインターフェースを作成
            from app.Services.GradioInterfaceService import GradioInterfaceService
            service = GradioInterfaceService()
            tabbed_interface = service.create_tabbed_interface()
            
            # Gradio 4.31.5での正しいキュー制御
            try:
                tabbed_interface.enable_queue = False
                if hasattr(tabbed_interface, '_queue'):
                    tabbed_interface._queue = None
                print("✅ GradioController: tabbed interface queue disabled")
                    
            except Exception as queue_error:
                print(f"⚠️ GradioController: queue setup warning: {queue_error}")
            
            return tabbed_interface
            
        except Exception as e:
            print(f"❌ GradioController setup error: {e}")
            # フォールバック用のシンプルなインターフェース
            fallback_interface = self.create_main_interface()
            
            # フォールバックも同様にキュー制御
            try:
                fallback_interface.enable_queue = False
                if hasattr(fallback_interface, '_queue'):
                    fallback_interface._queue = None
                print("✅ GradioController: fallback interface queue disabled")
            except:
                pass
            
            return fallback_interface

# インスタンス作成
gradio_controller = GradioController()
router = gradio_controller.router
