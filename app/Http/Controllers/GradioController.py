"""
Gradio Controller
Laravel的なController層でGradioインターフェースのHTTPリクエストを処理
"""
import sys
import os
# パスを追加してServiceにアクセス
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from app.Services.GradioInterfaceService import GradioInterfaceService
except ImportError:
    # フォールバック用のダミークラス
    class GradioInterfaceService:
        def create_tabbed_interface(self):
            import gradio as gr
            return gr.Interface(
                fn=lambda x: "Laravel風Controller読み込み中...",
                inputs="text",
                outputs="text",
                title="🚀 Laravel風 Gradio Controller"
            )

import gradio as gr
from fastapi import FastAPI

class GradioController:
    """Gradioインターフェースのコントローラー"""
    
    def __init__(self):
        self.gradio_service = GradioInterfaceService()
        self.mounted_apps = {}  # マウントされたアプリケーションを追跡
        self._check_and_fix_database_paths()
    
    def _check_and_fix_database_paths(self):
        """データベースパスをチェックして修正"""
        try:
            from config.database import DATABASE_PATHS
            import os
            
            missing_dbs = []
            for db_name, db_path in DATABASE_PATHS.items():
                if not os.path.exists(db_path):
                    missing_dbs.append(db_name)
            
            if missing_dbs:
                print(f"⚠️ Missing databases detected: {missing_dbs}")
                self._initialize_missing_databases()
                
        except Exception as e:
            print(f"❌ Database path check failed: {e}")
    
    def _initialize_missing_databases(self):
        """不足しているデータベースを初期化"""
        try:
            from database.init_databases import create_databases
            create_databases()
            print("✅ Missing databases initialized successfully")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    
    def setup_gradio_interfaces(self):
        """Gradioインターフェースをセットアップする（エラーハンドリング強化）"""
        try:
            # データベース接続の確認
            self._verify_database_connections()
            
            # サービス層でインターフェースを作成
            tabbed_interface = self.gradio_service.create_tabbed_interface()
            
            print("✅ Gradio interfaces setup completed via Laravel-style Controller")
            return tabbed_interface
            
        except Exception as e:
            print(f"❌ Error setting up Gradio interfaces: {e}")
            # エラー時のフォールバック
            return self._create_fallback_interface(str(e))
    
    def _verify_database_connections(self):
        """データベース接続を検証"""
        try:
            from config.database import get_db_connection
            conn = get_db_connection('chat_history')
            conn.close()
            print("✅ Database connection verified")
        except Exception as e:
            print(f"⚠️ Database connection issue: {e}")
            # 再初期化を試行
            self._initialize_missing_databases()
    
    def _create_fallback_interface(self, error_message: str):
        """フォールバック用のインターフェースを作成"""
        return gr.Interface(
            fn=lambda x: f"Gradio Setup Error: {error_message}\n\nPlease check:\n1. Database connections\n2. File paths\n3. Service dependencies",
            inputs=gr.Textbox(placeholder="Enter any text to see error details..."),
            outputs="text",
            title="🚨 Laravel-style Gradio Controller Error",
            description="This is a fallback interface. Please check the system logs for more details."
        )
    
    def mount_gradio_to_fastapi(self, app: FastAPI, gradio_interfaces, mount_paths=None):
        """
        FastAPIアプリケーションに複数のGradioインターフェースをマウント
        
        Args:
            app: FastAPIアプリケーション
            gradio_interfaces: Gradioインターフェース（単体またはリスト）
            mount_paths: マウントパス（文字列またはリスト）
        """
        if mount_paths is None:
            mount_paths = ["/gradio"]
        
        # 単体の場合はリストに変換
        if not isinstance(gradio_interfaces, list):
            gradio_interfaces = [gradio_interfaces]
        if not isinstance(mount_paths, list):
            mount_paths = [mount_paths]
        
        # パスとインターフェースの数を調整
        if len(mount_paths) < len(gradio_interfaces):
            # パスが足りない場合は自動生成
            for i in range(len(mount_paths), len(gradio_interfaces)):
                mount_paths.append(f"/gradio{i+1}")
        
        mounted_count = 0
        
        for i, (interface, path) in enumerate(zip(gradio_interfaces, mount_paths)):
            try:
                # 方法1: gr.mount_gradio_app を試す (root_pathを指定)
                try:
                    # Codespacesでのポート問題を回避するため、環境変数を設定
                    import os
                    original_port = os.environ.get('PORT')
                    os.environ['PORT'] = '443'  # HTTPSポートに設定
                    
                    app = gr.mount_gradio_app(
                        app, 
                        interface, 
                        path=path,
                        app_kwargs={
                            "root_path": path,
                            "docs_url": None,  # docsを無効化
                            "redoc_url": None  # redocを無効化
                        }
                    )
                    
                    # 元のポート設定を復元
                    if original_port:
                        os.environ['PORT'] = original_port
                    elif 'PORT' in os.environ:
                        del os.environ['PORT']
                    
                    print(f"✅ Gradio interface mounted at {path} (method 1 with port fix)")
                    self.mounted_apps[path] = {"interface": interface, "method": "mount_gradio_app"}
                    mounted_count += 1
                    continue
                except Exception as e1:
                    print(f"⚠️ Method 1 failed for {path}: {e1}")
                
                # 方法2: 手動でASGIアプリとしてマウント (root_pathを指定)
                try:
                    # Codespacesでのポート問題を回避
                    import os
                    original_port = os.environ.get('PORT')
                    os.environ['PORT'] = '443'  # HTTPSポートに設定
                    
                    gradio_asgi = gr.routes.App.create_app(
                        interface, 
                        app_kwargs={
                            "root_path": path,
                            "docs_url": None,
                            "redoc_url": None
                        }
                    )
                    app.mount(path, gradio_asgi)
                    
                    # 元のポート設定を復元
                    if original_port:
                        os.environ['PORT'] = original_port
                    elif 'PORT' in os.environ:
                        del os.environ['PORT']
                    
                    print(f"✅ Gradio interface mounted at {path} (method 2 with port fix)")
                    self.mounted_apps[path] = {"interface": interface, "method": "manual_mount"}
                    mounted_count += 1
                    continue
                except Exception as e2:
                    print(f"⚠️ Method 2 failed for {path}: {e2}")
                
                # 方法3: Blocksを使った手動マウント
                try:
                    if hasattr(interface, 'app'):
                        app.mount(path, interface.app)
                        print(f"✅ Gradio interface mounted at {path} (method 3)")
                        self.mounted_apps[path] = {"interface": interface, "method": "blocks_mount"}
                        mounted_count += 1
                    else:
                        print(f"❌ Interface at {path} doesn't have app attribute")
                except Exception as e3:
                    print(f"❌ Method 3 failed for {path}: {e3}")
                    
            except Exception as general_error:
                print(f"❌ Failed to mount interface at {path}: {general_error}")
        
        print(f"🎯 Laravel風Controller: {mounted_count}/{len(gradio_interfaces)} interfaces mounted successfully")
        return app, self.mounted_apps
    
    def get_mounted_apps_info(self):
        """マウントされたアプリケーションの情報を取得"""
        return {
            "total_mounted": len(self.mounted_apps),
            "mount_points": list(self.mounted_apps.keys()),
            "details": self.mounted_apps
        }
    
    def unmount_gradio_app(self, app: FastAPI, path: str):
        """特定のパスのGradioアプリケーションをアンマウント"""
        try:
            if path in self.mounted_apps:
                # FastAPIから直接アンマウントする方法は限定的
                # 通常は再起動が必要
                del self.mounted_apps[path]
                print(f"✅ Removed {path} from tracking")
                return True
            else:
                print(f"⚠️ Path {path} not found in mounted apps")
                return False
        except Exception as e:
            print(f"❌ Error unmounting {path}: {e}")
            return False
    
    def get_interface_list(self):
        """利用可能なインターフェースの一覧を取得"""
        interfaces, names = self.gradio_service.collect_gradio_interfaces()
        return {
            "total_count": len(interfaces),
            "interface_names": names,
            "status": "success"
        }
    
    def get_categorized_interfaces(self):
        """カテゴリ別のインターフェース一覧を取得"""
        interfaces, names = self.gradio_service.collect_gradio_interfaces()
        categories = self.gradio_service.categorize_interfaces(interfaces, names)
        return categories

# Laravel風のファサードパターンでグローバルアクセスを提供
def setup_gradio_interfaces():
    """グローバル関数としてGradioインターフェースをセットアップ"""
    controller = GradioController()
    return controller.setup_gradio_interfaces()

def mount_gradio_to_fastapi(app: FastAPI, gradio_interfaces, mount_paths=None):
    """グローバル関数としてGradioをFastAPIにマウント"""
    controller = GradioController()
    return controller.mount_gradio_to_fastapi(app, gradio_interfaces, mount_paths)

def get_mounted_apps_info():
    """マウントされたアプリケーション情報を取得"""
    controller = GradioController()
    return controller.get_mounted_apps_info()
