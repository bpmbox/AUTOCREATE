# GitHub Copilot Automation System - Makefile
# GitHub Copilot automation system commands

# Default settings
PYTHON := python
PYTEST := pytest
PIP := pip
ARTISAN := $(PYTHON) artisan

# 🎨 Laravel風 Artisan クイックコマンド
.PHONY: artisan-test artisan-start artisan-routes artisan-gradio artisan-cicd
artisan-test:
	@echo "🧪 Copilot自動化システムテスト実行..."
	$(ARTISAN) test:copilot

artisan-start:
	@echo "🚀 FastAPIサーバー起動..."
	$(ARTISAN) fastapi:start

artisan-routes:
	@echo "🛣️ アクティブルート確認..."
	$(ARTISAN) route:active

artisan-gradio:
	@echo "🎨 Gradio機能一覧..."
	$(ARTISAN) gradio:list

artisan-cicd:
	@echo "🔄 完全CI/CDパイプライン実行..."
	$(ARTISAN) cicd full

# 便利なエイリアス
.PHONY: quick-test quick-start quick-routes
quick-test: artisan-test
quick-start: artisan-start  
quick-routes: artisan-routes

# Help display (default)
.PHONY: help
help:
	@echo "GitHub Copilot Automation System - Makefile"
	@echo "============================================"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run pytest (all automated tests)"
	@echo "  make test-all         - Run all tests (pytest + system tests)"
	@echo "  make test-unified     - Run unified test mode"
	@echo "  make test-local       - Run local test mode"
	@echo "  make test-cli         - Run CLI integration test"
	@echo "  make test-filtering   - Run filtering logic test"
	@echo ""
	@echo "System operations:"
	@echo "  make run-menu         - Start command menu"
	@echo "  make run-unified      - Start unified test mode"
	@echo "  make run-local        - Start local test mode"
	@echo "  make run-cli          - Start CLI integration test"
	@echo "  make run-monitoring   - Start safe monitoring mode"
	@echo ""
	@echo "Environment management:"
	@echo "  make install          - Install dependencies"
	@echo "  make install-dev      - Install dev dependencies"
	@echo "  make clean            - Clean temporary files"
	@echo "  make clean-mermaid    - Clean Mermaid files"
	@echo "  make clean-all        - Clean all files"
	@echo ""
	@echo "Information:"
	@echo "  make status           - Check system status"
	@echo "  make env-check        - Check environment settings"
	@echo "  make github-auth      - Check GitHub auth status"
	@echo ""

# ================================
# 🧪 テスト関連コマンド
# ================================

# pytest実行（全テスト）
.PHONY: test
test:
	@echo "🧪 pytest実行開始..."
	$(PYTHON) -m pytest test_automation_pytest.py -v --tb=short --color=yes
	@echo "✅ pytest実行完了"

# 全テストモード実行
.PHONY: test-all
test-all: test test-unified test-local test-cli
	@echo "🎉 全テストモード実行完了！"
	@echo "🧪 全テスト実行開始"
	$(PYTEST) test_unified_automation.py -v --tb=short

# 統一テストモード実行
.PHONY: test-unified
test-unified:
	@echo "🔄 統一テストモード実行..."
	$(PYTHON) tests/Feature/copilot_github_cli_automation.py --mode 5 --offline

# ローカルテストモード実行
.PHONY: test-local
test-local:
	@echo "🏠 ローカルテストモード実行..."
	$(PYTHON) tests/Feature/copilot_github_cli_automation.py --mode 3 --offline

# GitHub CLI統合テスト実行
.PHONY: test-cli
test-cli:
	@echo "🔧 GitHub CLI統合テスト実行..."
	$(PYTHON) tests/Feature/copilot_github_cli_automation.py --mode 4 --offline

# フィルタリングテスト実行
.PHONY: test-filtering
test-filtering:
	@echo "🔍 フィルタリングテスト実行..."
	$(PYTHON) -c "from tests.Feature.copilot_github_cli_automation import GitHubCopilotAutomation; GitHubCopilotAutomation(offline_mode=True).test_copilot_keyword_filtering()"

# ================================
# 🔧 システム操作コマンド
# ================================

.PHONY: run-menu
run-menu:
	@echo "🚀 コマンドメニュー起動"
	$(PYTHON) tests/Feature/copilot_github_cli_automation.py

.PHONY: run-unified
run-unified:
	@echo "🧪 統一テストモード起動"
	@echo "5" | $(PYTHON) tests/Feature/copilot_github_cli_automation.py

.PHONY: run-local
run-local:
	@echo "🏠 ローカルテストモード起動"
	@echo "3" | $(PYTHON) tests/Feature/copilot_github_cli_automation.py

.PHONY: run-cli
run-cli:
	@echo "🔧 CLI統合テスト起動"
	@echo "4" | $(PYTHON) tests/Feature/copilot_github_cli_automation.py

.PHONY: run-monitoring
run-monitoring:
	@echo "🛡️ 安全監視モード起動"
	@echo "1" | $(PYTHON) tests/Feature/copilot_github_cli_automation.py

# ================================
# 📦 環境管理コマンド
# ================================

.PHONY: install
install:
	@echo "📦 依存関係インストール"
	$(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev:
	@echo "📦 開発用依存関係インストール"
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov pytest-mock

.PHONY: clean
clean:
	@echo "🧹 一時ファイル削除"
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf *.pyc
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

.PHONY: clean-mermaid
clean-mermaid:
	@echo "🧹 Mermaidファイル削除"
	rm -f *.mermaid
	rm -f auto_dev_flow_*.mermaid
	rm -f test_mermaid_*.mermaid
	rm -f local_test_*.mermaid
	rm -f pytest_mermaid_*.mermaid

.PHONY: clean-all
clean-all: clean clean-mermaid
	@echo "🧹 全ファイル削除完了"

# ================================
# 📊 情報表示コマンド
# ================================

.PHONY: status
status:
	@echo "📊 システム状態確認"
	@echo ""
	@echo "🐍 Python環境:"
	$(PYTHON) --version
	@echo ""
	@echo "📦 主要パッケージ:"
	$(PIP) show supabase || echo "  supabase: 未インストール"
	$(PIP) show pyautogui || echo "  pyautogui: 未インストール"
	$(PIP) show pytest || echo "  pytest: 未インストール"
	@echo ""
	@echo "📁 プロジェクトファイル:"
	@ls -la tests/Feature/copilot_github_cli_automation.py 2>/dev/null || echo "  メインファイル: 存在しません"
	@ls -la test_unified_automation.py 2>/dev/null || echo "  テストファイル: 存在しません"
	@ls -la .env 2>/dev/null || echo "  .env: 存在しません"

.PHONY: env-check
env-check:
	@echo "🔧 環境設定確認"
	@echo ""
	@echo "📋 .envファイル確認:"
	@if [ -f .env ]; then \
		echo "  ✅ .envファイル存在"; \
		echo "  📝 主要設定:"; \
		grep -E "^(SUPABASE_URL|GITHUB_TOKEN|DEBUG_MODE)" .env 2>/dev/null | sed 's/^/    /' || echo "    ⚠️ 主要設定が見つかりません"; \
	else \
		echo "  ❌ .envファイルが存在しません"; \
	fi

.PHONY: github-auth
github-auth:
	@echo "🔐 GitHub認証状態確認"
	@gh auth status || echo "❌ GitHub CLI未認証 - 'gh auth login' を実行してください"

# ================================
# 🚀 一括実行コマンド
# ================================

.PHONY: full-test
full-test: clean install-dev test-all
	@echo "✅ フルテストサイクル完了"

.PHONY: quick-start
quick-start: env-check github-auth run-unified
	@echo "🚀 クイックスタート完了"

.PHONY: dev-setup
dev-setup: install-dev env-check github-auth
	@echo "🔧 開発環境セットアップ完了"
	@echo ""
	@echo "📋 次のステップ:"
	@echo "  make test-quick       - クイックテスト実行"
	@echo "  make run-menu         - システム起動"

# ================================
# 📊 レポート生成
# ================================

.PHONY: test-report
test-report:
	@echo "📊 テストレポート生成"
	$(PYTEST) test_unified_automation.py --tb=short --quiet
	@echo ""
	@echo "📁 生成されたファイル:"
	@ls -la *.mermaid 2>/dev/null | head -5 || echo "  Mermaidファイル: なし"
	@echo ""
	@echo "💾 ディスク使用量:"
	@du -sh . | sed 's/^/  /'

# ================================
# 🆘 緊急時コマンド
# ================================

.PHONY: emergency-stop
emergency-stop:
	@echo "🆘 緊急停止"
	@pkill -f "python.*copilot_github_cli_automation" || echo "停止対象プロセスなし"
	@pkill -f "uvicorn" || echo "uvicornプロセスなし"

.PHONY: reset-system
reset-system: emergency-stop clean-all
	@echo "🔄 システムリセット完了"
	@echo "💡 次回起動: make quick-start"
