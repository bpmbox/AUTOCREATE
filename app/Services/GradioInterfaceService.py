"""
Gradio Interface Service
Laravel的なService層でGradioインターフェースの管理を行う
"""
import shutil
import gradio as gr
import importlib
import os
import pkgutil
import traceback

class GradioInterfaceService:
    """Gradioインターフェース管理クラス - 統合キュー対応"""
    
    def __init__(self):
        self.gradio_interfaces = {}
        self.interface_names = []
        print("🔄 GradioInterfaceService: Individual queue setup DISABLED")
        print("⚠️ GradioInterfaceService: Queue will be set only at unified launch")
    
    def collect_gradio_interfaces(self):
        """全てのGradioインターフェースを収集する（統合起動用）- Laravel風構造対応"""
        print("🔄 === UNIFIED GRADIO COLLECTION START ===")
        print("⚠️  Individual .launch() calls are DISABLED")
        print("🎯 Only collecting interfaces for unified TabbedInterface")
        
        self.gradio_interfaces = {}
        
        # Laravel風検索対象ディレクトリを指定
        search_dirs = [
            "app/Http/Controllers/Gradio",  # Laravel風のGradioディレクトリのみ
        ]
        
        # 各検索ディレクトリをスキャン
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                print(f"📂 Scanning directory: {search_dir}")
                self._scan_directory(search_dir)
        
        # 名前とインターフェースのリストを更新
        self.interface_names = list(self.gradio_interfaces.keys())
        print(f"🎯 Collected {len(self.gradio_interfaces)} Gradio Interfaces: {self.interface_names}")
        print("🔄 === UNIFIED GRADIO COLLECTION END ===")
        
        return list(self.gradio_interfaces.values()), self.interface_names
    
    def _scan_directory(self, base_dir):
        """ディレクトリをスキャンしてGradioインターフェースを探す"""
        for root, dirs, files in os.walk(base_dir):
            if "__pycache__" in root:
                continue
                
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    file_path = os.path.join(root, file)
                    module_name = file[:-3]  # .py を除去
                    
                    # モジュールパスを構築
                    rel_path = os.path.relpath(root, '.')
                    module_path = rel_path.replace(os.sep, '.') + '.' + module_name
                    
                    try:
                        self._load_gradio_interface(module_path, module_name)
                    except Exception as e:
                        print(f"⚠️ Error loading {module_path}: {e}")
                        continue
    
    def _load_gradio_interface(self, module_path, module_name):
        """モジュールからGradioインターフェースをロードする"""
        try:
            print(f"Trying to import {module_path}")
            module = importlib.import_module(module_path)
            print(f"Successfully imported {module_path}")

            # `gradio_interface` を持つモジュールのみ追加
            if hasattr(module, "gradio_interface"):
                print(f"Found gradio_interface in {module_path}")

                # 美しいタイトルを生成
                display_name = self._generate_interface_title(module_name, module)
                
                # 名前の一意性を保証
                unique_name = self._ensure_unique_name(display_name)

                # インターフェースを処理
                interface = self._process_interface(module.gradio_interface, module_name)
                
                if interface:
                    self.gradio_interfaces[unique_name] = interface
                    
        except ModuleNotFoundError as e:
            print(f"ModuleNotFoundError: {module_path} - {e}")
        except AttributeError as e:
            print(f"AttributeError in {module_path}: {e}")
        except Exception as e:
            print(f"Failed to import {module_path}: {e}")
            print(traceback.format_exc())
    
    def _generate_interface_title(self, base_name, module):
        """インターフェースのタイトルを生成する"""
        # 特定のモジュールに対する美しいタイトルマッピング
        title_mapping = {
            'beginner_guide_system': '🚀 初心者ガイド',
            'conversation_history': '💬 会話履歴管理',
            'conversation_logger': '📝 会話ログ',
            'conversation_demo': '🎯 会話履歴統合デモ',
            'contbk_unified_dashboard': '🎯 ContBK統合ダッシュボード',
            'hasura': '🗄️ Hasura API',
            'Chat': '💬 チャット',
            'OpenInterpreter': '🤖 AI インタープリター',
            'programfromdoc': '📄 ドキュメント生成',
            'gradio_interface': '🚀 AI開発プラットフォーム',
            'lavelo': '💾 プロンプト管理システム',
            'rides': '🚗 データベース管理',
            'files': '📁 ファイル管理',
            'gradio': '🌐 HTML表示',
            'rpa_automation': '🤖 RPA自動化システム',
            'github_issue_dashboard': '🚀 GitHub ISSUE自動化',
            'github_issue_automation': '🤖 GitHub ISSUE自動生成システム',
            'integrated_approval_system': '🎯 統合承認システム',
            'integrated_dashboard': '🚀 統合管理ダッシュボード',
            'ui_verification_system': '🔧 UI検証・システム診断',
        }
        
        # モジュールにtitle属性があるかチェック
        if hasattr(module, 'interface_title'):
            return module.interface_title
        elif base_name in title_mapping:
            return title_mapping[base_name]
        else:
            # デフォルトの美しいタイトル生成
            formatted_name = base_name.replace('_', ' ').title()
            return f"✨ {formatted_name}"
    
    def _ensure_unique_name(self, display_name):
        """名前の一意性を保証する"""
        unique_name = display_name
        count = 1

        # 重複がある場合は番号を付与
        while unique_name in self.gradio_interfaces:
            unique_name = f"{display_name} ({count})"
            count += 1
            
        return unique_name
    
    def _process_interface(self, interface, base_name):
        """インターフェースを処理する（個別起動は行わない）- オブジェクトのみ準備"""
        # Check if it's a factory function by checking if it's callable but not a Gradio object
        # Gradio objects have 'queue' method, regular functions don't
        if callable(interface) and not hasattr(interface, 'queue'):
            try:
                interface = interface()
            except Exception as call_error:
                print(f"Failed to call factory function for {base_name}: {call_error}")
                return None  # Skip this interface if factory function fails
        
        # ⚠️ 重要: ここでは個別起動やlaunch()を行わない
        # インターフェースオブジェクトの準備のみ行う
        try:
            # launchメソッドが無効化されているかチェック
            if hasattr(interface, 'launch'):
                if hasattr(interface.launch, '__name__') and interface.launch.__name__ == 'disabled_launch':
                    print(f"🚫 Launch method DISABLED for {base_name} - Good!")
                else:
                    print(f"⚠️  Launch method still ACTIVE for {base_name}")
            
            # 個別インスタンスではキューを設定しない
            print(f"⚠️ Individual queue setup SKIPPED for {base_name}")
            print(f"🔄 Queue will be configured only at unified launch")
            
            # 起動防止のための強力な対策
            if hasattr(interface, 'auto_launch'):
                interface.auto_launch = False
            if hasattr(interface, 'share'):
                interface.share = False
            if hasattr(interface, 'server'):
                interface.server = None  # サーバーオブジェクトを無効化
            if hasattr(interface, 'launch_kwargs'):
                interface.launch_kwargs = {}  # launch引数をクリア
            if hasattr(interface, 'launch_method'):
                interface.launch_method = None  # launchメソッドを無効化
            if hasattr(interface, 'is_running'):
                interface.is_running = False  # 実行状態をFalseに
            
            # ⚠️ 最強対策: launchメソッドを無害なダミー関数に置き換え
            if hasattr(interface, 'launch'):
                def dummy_launch(*args, **kwargs):
                    print(f"⚠️ LAUNCH BLOCKED for {base_name} - Use unified TabbedInterface instead!")
                    return None
                interface.launch = dummy_launch
                print(f"🛡️ Launch method blocked for {base_name}")
                
            print(f"✅ Interface object prepared (LAUNCH PREVENTION): {base_name}")
                
        except Exception as e:
            print(f"⚠️ Queue setup warning for {base_name}: {e}")
        
        return interface
    
    def categorize_interfaces(self, interfaces, names):
        """インターフェースをユーザーフレンドリーなカテゴリ別に分類"""
        categories = {
            "スタート": [],             # 初心者ガイド・チュートリアル
            "チャット": [],             # 会話・質問・対話
            "AI作成": [],              # プログラム・コード生成
            "文書作成": [],             # ドキュメント・プロンプト
            "管理": [],                # システム・データ管理
            "開発": [],               # 開発ツール・テスト
            "その他": []              # その他の機能
        }
        
        # カテゴリマッピングロジックをここに実装
        # ... (元のコードから移植)
        
        return categories
    
    def create_tabbed_interface(self):
        """タブ付きGradioインターフェースを作成する（統合起動）- Gradio 4.24.0対応"""
        print("🚀 === CREATING UNIFIED TABBED INTERFACE ===")
        interfaces, names = self.collect_gradio_interfaces()
        
        if not interfaces:
            print("⚠️ No interfaces found - creating default interface")
            # インターフェースが見つからない場合のデフォルト
            default_interface = gr.Interface(
                fn=lambda x: "No Gradio interfaces found",
                inputs="text",
                outputs="text",
                title="No Interfaces Available"
            )
            # デフォルトインターフェースもキュー設定をスキップ
            print("⚠️ Default interface - queue setup SKIPPED")
            return default_interface
        
        # タブ付きインターフェースを作成
        print(f"🎯 Creating TabbedInterface with {len(interfaces)} tabs")
        tabbed_interface = gr.TabbedInterface(
            interface_list=interfaces,
            tab_names=names,
            title="🚀 AI Development Platform - Laravel風統合システム"
        )
        
        # TabbedInterfaceでもキュー設定はスキップ（app.pyで統合設定）
        print("⚠️ TabbedInterface - queue setup SKIPPED")
        print("🔄 Queue will be configured at unified launch in app.py")
        
        print("🚀 ✅ UNIFIED TABBED INTERFACE CREATED - Ready for single launch!")
        return tabbed_interface
