# 📁 プロジェクト構造詳細ガイド

## 🎯 ディレクトリ構造完全解説

このページでは、FastAPI Django Main Liveプロジェクトの**実際のフォルダー構造**と、**各ディレクトリの具体的な役割**を詳しく説明します。

## 🏗️ ルートディレクトリ構造

```
fastapi_django_main_live/
├── 📁 __pycache__/              # Python バイトコードキャッシュ
├── 📄 __init__.py               # Pythonパッケージマーカー
├── 📄 app.py                    # メインアプリケーションエントリーポイント
├── 📄 app_debug.py             # デバッグ用アプリケーション
├── 📄 app_light.py             # 軽量版アプリケーション
├── 📄 app_simple.py            # シンプル版アプリケーション
├── 📄 app.log                  # アプリケーションログ
├── 📄 artisan                  # Laravel風CLIツール ⭐
├── 📄 main.py                  # FastAPI メインファイル
├── 📄 manage.py                # Django管理コマンド
├── 📄 Makefile                 # ビルド・デプロイ自動化
├── 📄 requirements.txt         # Python依存関係
├── 📄 pyproject.toml          # Python プロジェクト設定
├── 📄 poetry.lock             # Poetry ロックファイル
├── 📄 package.json            # Node.js 依存関係
├── 📄 pytest.ini             # テスト設定
├── 📄 setup.cfg               # セットアップ設定
├── 📄 Dockerfile              # Docker コンテナ設定
├── 📄 docker-compose.yml      # Docker Compose設定
├── 📄 README.md               # プロジェクト説明
├── 📄 LICENSE                 # ライセンス
└── 📄 .gitignore              # Git除外設定
```

## 🏢 Laravel風アプリケーション構造

### 📁 app/ - アプリケーションコア
```
app/
├── 📄 __init__.py
├── 📁 __pycache__/
├── 📁 Http/                     # HTTP処理層
│   ├── 📁 Controllers/          # コントローラー群
│   │   ├── 📄 GradioController.py    # Gradio統合制御
│   │   ├── 📄 HybridController.py    # ハイブリッド機能
│   │   ├── 📁 Api/              # API専用コントローラー
│   │   ├── 📁 Web/              # Web UI コントローラー
│   │   └── 📁 Gradio/           # Gradio専用コントローラー
│   └── 📁 Middleware/           # ミドルウェア
├── 📁 Models/                   # データモデル
├── 📁 Services/                 # ビジネスロジック層
├── 📁 app_core/                 # アプリケーション中核
└── 📁 command/                  # コマンド処理
```

**役割**: Laravel風のアプリケーション構造で、MVC分離とビジネスロジックの整理

### 📁 bootstrap/ - アプリケーション起動
```
bootstrap/
├── 📄 __init__.py
├── 📄 app.py                    # アプリケーション初期化
├── 📄 bootstrap_app.py          # 起動プロセス
├── 📁 __pycache__/
└── 📁 core/                     # 起動コア機能
```

**役割**: アプリケーションの起動とサービス初期化

### 📁 config/ - 設定管理
```
config/
├── 📄 __init__.py
├── 📄 app.py                    # アプリケーション設定
├── 📄 database.py               # データベース設定
└── 📁 __pycache__/
```

**役割**: 環境固有の設定とコンフィギュレーション管理

## 🗄️ データ・ストレージ構造

### 📁 database/ - データベース関連
```
database/
├── 📁 migrations/               # データベースマイグレーション
├── 📁 seeders/                  # 初期データ投入
└── 📁 controllers/              # データベース操作専用コントローラー
```

**役割**: データベーススキーマ管理と初期データ設定

### 📁 storage/ - ファイルストレージ
```
storage/
├── 📁 app/                      # アプリケーションファイル
├── 📁 logs/                     # ログファイル
├── 📁 cache/                    # キャッシュデータ
└── 📁 uploads/                  # アップロードファイル
```

**役割**: ファイル保存、ログ管理、キャッシュ管理

### 📁 chroma/ - ベクターデータベース
```
chroma/
├── 📄 chroma.sqlite3            # ChromaDB SQLite
└── 📁 1303e1ad-d2ff-495f-b987-6ef0f8327781/  # コレクションデータ
```

**役割**: AI埋め込みベクター検索とRAG機能

## 🌐 Web・フロントエンド構造

### 📁 templates/ - Jinja2テンプレート
```
templates/
├── 📄 base.html                 # ベーステンプレート
├── 📄 dashboard.html            # ダッシュボード
├── 📄 tool_redirect.html        # ツールリダイレクト
├── 📄 tool_not_found.html       # 404ページ
└── 📄 api_docs.html             # API文書
```

**役割**: HTML テンプレート管理（Jinja2エンジン）

### 📁 static/ - 静的ファイル
```
static/
└── 📁 css/
    └── 📄 main.css              # メインスタイルシート
```

**役割**: CSS、JavaScript、画像などの静的アセット

### 📁 public/ - 公開ファイル
```
public/
├── 📄 index.html                # メインエントリーポイント
└── 📁 assets/                   # 公開アセット
```

**役割**: Web公開用ファイル（Laravel Public/と同等）

### 📁 resources/ - リソース
```
resources/
├── 📁 views/                    # ビューファイル
├── 📁 css/                      # 開発用CSS
└── 📁 js/                       # 開発用JavaScript
```

**役割**: 開発用リソース（コンパイル前のファイル）

## 🛤️ ルーティング・コントローラー

### 📁 routes/ - ルーティング定義
```
routes/
├── 📄 web.py                    # Web ルート
├── 📄 api.py                    # API ルート
└── 📁 laravel_routes/           # Laravel風ルーティング
```

**役割**: URL ルーティング定義（Laravel Routes/と同等）

### 📁 controllers/ - 機能別コントローラー
```
controllers/
├── 📁 gra_01_chat/              # チャット機能
│   ├── 📄 chat.py               # チャット処理
│   └── 📄 gradio_interface      # Gradio UI定義
├── 📁 gra_02_openInterpreter/   # OpenInterpreter
├── 📁 contbk_unified_dashboard/ # 統合ダッシュボード
├── 📁 github_issue_creator/     # GitHub Issue作成
├── 📁 rpa_screenshot/           # RPA画像取得
└── 📁 ...                       # その他機能
```

**役割**: 機能ごとの独立したコントローラーとGradio UI

## 🐍 Django統合構造

### 📁 mysite/ - Django プロジェクト
```
mysite/
├── 📄 __init__.py
├── 📄 asgi.py                   # ASGI設定（FastAPI+Django統合）
├── 📄 settings.py               # Django設定
├── 📄 urls.py                   # Django URL設定
├── 📄 wsgi.py                   # WSGI設定
├── 📄 logger.py                 # ログ設定
├── 📁 routers/                  # FastAPI ルーター
│   ├── 📄 gradio.py             # Gradio統合ルーター
│   ├── 📄 fastapi.py            # FastAPI ルーター
│   └── 📄 database.py           # データベースルーター
├── 📁 interpreter/              # OpenInterpreter統合
└── 📁 config/                   # 設定管理
```

**役割**: Django + FastAPI の統合ハブ

### 📁 polls/ - Django アプリ例
```
polls/
├── 📄 __init__.py
├── 📄 admin.py                  # Django管理画面
├── 📄 apps.py                   # アプリ設定
├── 📄 models.py                 # Djangoモデル
├── 📄 tests.py                  # テスト
├── 📄 views.py                  # Djangoビュー
└── 📁 migrations/               # マイグレーション
```

**役割**: Django標準アプリケーション構造

## 🔧 開発・ツール構造

### 📁 vendor/ - 外部ライブラリ
```
vendor/
├── 📁 open-interpreter/         # OpenInterpreter統合
├── 📁 dify-setup/               # Dify AI プラットフォーム
├── 📁 docker-gui-setup/         # Docker GUI セットアップ
├── 📁 simple_ai_env/            # AI環境設定
└── 📁 LLaMA-Factory/            # LLaMA ファインチューニング
```

**役割**: 外部パッケージと大規模ライブラリ

### 📁 tests/ - テストスイート
```
tests/
├── 📄 __init__.py
├── 📄 test_logger.py            # ログ機能テスト
└── 📁 unit/                     # ユニットテスト
```

**役割**: 自動テストとQA

### 📁 scripts/ - スクリプト
```
scripts/
├── 📄 setup.py                 # セットアップスクリプト
├── 📄 deploy.sh                # デプロイスクリプト
└── 📄 backup.py                # バックアップスクリプト
```

**役割**: 運用・管理スクリプト

## 📚 ドキュメント・情報

### 📁 docs/ - ドキュメント
```
docs/
├── 📄 README.md                 # プロジェクト説明
├── 📄 API.md                    # API仕様
├── 📄 DEPLOYMENT.md             # デプロイガイド
└── 📁 images/                   # 画像資料
```

**役割**: プロジェクト文書化

### 📁 wiki/ - GitHub Wiki
```
wiki/
├── 📄 Home.md                   # Wikiホーム
├── 📄 System-Architecture.md    # アーキテクチャ
├── 📄 Implemented-Features.md   # 実装機能
├── 📄 Jinja2-Template-Integration.md  # テンプレート統合
├── 📄 Laravel-Style-Architecture.md   # Laravel風構造
└── 📄 _Sidebar.md               # サイドバー
```

**役割**: GitHub Wiki 管理

## 🗃️ データファイル

### データベースファイル
```
📄 db.sqlite3                    # Django メインDB
📄 conversation_history.db       # 会話履歴DB
📄 prompts.db                    # プロンプト管理DB
```

### 設定・キャッシュ
```
📁 cache/                        # 各種キャッシュファイル
📁 flagged/                      # Gradio フラグ付きデータ
```

## 🚀 実行ファイル・エントリーポイント

### メインアプリケーション
- **`artisan`** ⭐ - Laravel風CLIツール
- **`app.py`** - メインアプリケーション
- **`main.py`** - FastAPI エントリーポイント
- **`manage.py`** - Django管理コマンド

### デバッグ・開発用
- **`app_debug.py`** - デバッグモード
- **`app_light.py`** - 軽量版
- **`app_simple.py`** - シンプル版

## 🎯 この構造の設計思想

### 🏆 Laravel MVC + Python の融合
1. **馴染みやすさ**: Laravel開発者なら直感的に理解可能
2. **Python力活用**: Django ORM + FastAPI + Gradio の強力な機能
3. **拡張性**: 新機能追加時の構造的一貫性
4. **保守性**: 各層の明確な分離と責任範囲

### 🔄 自動統合システム
```python
# controllers/ 配下の自動検出例
def include_gradio_interfaces():
    for root, dirs, files in os.walk("controllers"):
        for file in files:
            if hasattr(module, 'gradio_interface'):
                # 自動統合
                interfaces[name] = module.gradio_interface
```

### 🛡️ エンタープライズ対応
- **セキュリティ**: 適切な分離とアクセス制御
- **スケーラビリティ**: モジュラー設計
- **可読性**: 標準的なMVC構造
- **テスタビリティ**: 各層の独立テスト可能

## 📈 開発フロー例

### 新機能追加の手順
1. **`./artisan make:controller NewFeatureController`** - コントローラー生成
2. **`controllers/new_feature/gradio_interface`** - UI作成
3. **`routes/web.py`** - ルート追加（必要に応じて）
4. **自動統合** - システムが自動検出・統合

### ファイル配置ルール
```
controllers/feature_name/
├── 📄 controller.py             # メイン処理
├── 📄 gradio_interface         # UI定義（この名前で自動検出）
├── 📄 models.py                # データモデル
├── 📄 services.py              # ビジネスロジック
└── 📄 tests.py                 # テスト
```

---

*この構造は、Laravel の優れた設計思想をPython で実現し、AI時代のWeb開発に最適化された革新的なアーキテクチャです。* 🚀
