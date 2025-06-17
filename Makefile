#Sets the default shell for executing commands as /bin/bash and specifies command should be executed in a Bash shell.
SHELL := /bin/bash

# Color codes for terminal output
COLOR_RESET=\033[0m
COLOR_CYAN=\033[1;36m
COLOR_GREEN=\033[1;32m

# Defines the targets help, install, dev-install, and run as phony targets.
.PHONY: help install run dev debug app server test clean requirements ci-test ci-quick ci-full stop-port gui gui-auto gui-stop gui-logs gui-restart gui-simple

#sets the default goal to help when no target is specified on the command line.
.DEFAULT_GOAL := help

#Disables echoing of commands.
.SILENT:

#Sets the variable name to the second word from the MAKECMDGOALS.
name := $(word 2,$(MAKECMDGOALS))

#Defines a target named help.
help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo "  help           	Return this message with usage instructions."
	@echo "  install        	Will install the dependencies using Poetry."
	@echo "  run <folder_name>  Runs GPT Engineer on the folder with the given name."
	@echo "  generated_systems <name>  Generate system using GPT Engineer with prompts"
	@echo "  runs <name>     	Run GPT Engineer system generation"
	@echo "  app            	Run the main FastAPI application (app.py) - auto stops port 7860"
	@echo "  dev            	Run the application in development mode with hot reload - auto stops port 7860"
	@echo "  debug          	Run the application in debug mode (no reload) - auto stops port 7860"
	@echo "  server         	Run the ASGI server directly with uvicorn - auto stops port 7860"	@echo "  gui            	Start AI GUI Desktop Environment (http://localhost:6080)"
	@echo "  gui-auto       	Auto-start GUI with browser launch"
	@echo "  gui-simple     	Start simple GUI environment (http://localhost:6081)"
	@echo "  gui-stop       	Stop GUI Desktop Environment"
	@echo "  gui-restart    	Restart GUI Desktop Environment"
	@echo "  gui-logs       	Show GUI logs"
	@echo "  stop-port      	Stop any process running on port 7860"
	@echo "  ci-test        	Run CI/CD automated tests"
	@echo "  ci-quick       	Run quick CI test (no GitHub Issue)"
	@echo "  ci-full        	Run full CI pipeline with GitHub Issue"
	@echo "  ci-comprehensive	Run comprehensive controller tests"
	@echo "  ci-real-api      	Run real Gradio API tests"
	@echo "  test           	Run all tests"
	@echo "  requirements   	Install Python requirements from requirements.txt"
	@echo "  clean          	Clean up temporary files and caches"
	@echo ""
	@echo "🏢 AI-Human Collaboration Company Commands:"
	@echo "  gitflow-setup   	Initialize GitFlow collaboration system"
	@echo "  feature-start   	Start new feature development (usage: make feature-start name=feature-name)"
	@echo "  feature-finish  	Finish feature development (usage: make feature-finish name=feature-name)"
	@echo "  collab-commit   	Make collaboration commit (usage: make collab-commit message='commit message')"
	@echo ""
	@echo "🤖 OCR RPA Automation Commands:"
	@echo "  ocr-rpa-demo    	Run OCR RPA automation demo (kinkaimasu.jp)"
	@echo "  ocr-rpa-config  	Edit OCR RPA configuration"
	@echo "  ocr-rpa-report  	Generate latest automation report"
	@echo "  ocr-rpa-clean   	Clean OCR RPA temporary files"
	@echo "  vnc-auto        	Run VNC desktop automation demo"
	@echo "  jupyter-ocr     	Launch Jupyter notebook for OCR RPA demo"
	@echo "  screenshots-view	View collected screenshots"
	@echo ""
	@echo "📚 WIKI RAG System Commands:"
	@echo "  wiki-rag        	Start WIKI RAG system with Gradio UI"
	@echo "  wiki-rag-cli    	Use WIKI RAG CLI for command line queries"
	@echo "  wiki-rag-build  	Build/rebuild WIKI RAG knowledge base"
	@echo "  wiki-rag-install	Install WIKI RAG dependencies"
	@echo "  wiki-rag-lite   	Start WIKI RAG lite system (no auth required)"
	@echo "  wiki-rag-lite-cli	Use WIKI RAG lite CLI for command line queries"
	@echo "  wiki-rag-chat   	Start WIKI RAG Chat interface (conversational AI)"

#Defines a target named install. This target will install the project using Poetry.
install: poetry-install install-pre-commit farewell

#Defines a target named poetry-install. This target will install the project dependencies using Poetry.
poetry-install:
	@echo -e "$(COLOR_CYAN)Installing project with Poetry...$(COLOR_RESET)" && \
	poetry install

#Defines a target named install-pre-commit. This target will install the pre-commit hooks.
install-pre-commit:
	export OPENAI_API_BASE="https://api.groq.com/openai/v1/chat/completions"
	export OPENAI_API_KEY="sk-key-from-open-router"
	export MODEL_NAME="meta-llama/llama-3-8b-instruct:extended"
	export LOCAL_MODEL=true
	@echo -e "$(COLOR_CYAN)Installing pre-commit hooks...$(COLOR_RESET)" && \
	poetry run pre-commit install

#Defines a target named farewell. This target will print a farewell message.
farewell:
	@echo -e "$(COLOR_GREEN)All done!$(COLOR_RESET)"

#Defines a target named run. This target will run GPT Engineer on the folder with the given name.


run:
	@echo -e "$(COLOR_CYAN)Running Lavelo AI Automation Test...$(COLOR_RESET)" && \
	python lavelo_automation_test.py --mode=full_test

runbabyagi:
	cd ./babyagi && python babyagi.py $(name)

install:
	@echo -e "$(COLOR_CYAN)Installing dependencies...$(COLOR_RESET)"
	pip install -r requirements.txt


# Counts the lines of code in the project
cloc:
	cloc . --exclude-dir=node_modules,dist,build,.mypy_cache,benchmark --exclude-list-file=.gitignore --fullpath --not-match-d='docs/_build' --by-file

ssh:
	ssh-keygen -t rsa -b 4096 \-f ~/.ssh/id_rsa_new

# Application commands
stop-port:
	@echo -e "$(COLOR_CYAN)Stopping processes on port 7860...$(COLOR_RESET)"
	@if lsof -ti:7860 > /dev/null 2>&1; then \
		echo -e "$(COLOR_CYAN)Found process on port 7860, stopping...$(COLOR_RESET)"; \
		kill -9 $$(lsof -ti:7860) 2>/dev/null || true; \
		sleep 2; \
	else \
		echo -e "$(COLOR_GREEN)No process found on port 7860$(COLOR_RESET)"; \
	fi

app: stop-port
	@echo -e "$(COLOR_CYAN)Starting FastAPI application...$(COLOR_RESET)"
	SPACE_ID="" python app.py

dev: stop-port
	@echo -e "$(COLOR_CYAN)Starting application in development mode...$(COLOR_RESET)"
	SPACE_ID="" python app.py

debug: stop-port
	@echo -e "$(COLOR_CYAN)Starting application in debug mode...$(COLOR_RESET)"
	SPACE_ID="" python app.py --debug

server: stop-port
	@echo -e "$(COLOR_CYAN)Starting ASGI server directly...$(COLOR_RESET)"
	uvicorn mysite.asgi:app --host 0.0.0.0 --port 7860 --reload

# Requirements and dependencies
requirements:
	@echo -e "$(COLOR_CYAN)Installing Python requirements...$(COLOR_RESET)"
	pip install -r requirements.txt

# Testing
test:
	@echo -e "$(COLOR_CYAN)Running tests...$(COLOR_RESET)"
	python -m pytest tests/ -v

# Utility commands
clean:
	@echo -e "$(COLOR_CYAN)Cleaning up temporary files...$(COLOR_RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

# Database commands
migrate:
	@echo -e "$(COLOR_CYAN)Running database migrations...$(COLOR_RESET)"
	python manage.py migrate

makemigrations:
	@echo -e "$(COLOR_CYAN)Creating database migrations...$(COLOR_RESET)"
	python manage.py makemigrations

# Docker commands
docker-build:
	@echo -e "$(COLOR_CYAN)Building Docker image...$(COLOR_RESET)"
	docker-compose build

docker-up:
	@echo -e "$(COLOR_CYAN)Starting Docker containers...$(COLOR_RESET)"
	docker-compose up -d

docker-down:
	@echo -e "$(COLOR_CYAN)Stopping Docker containers...$(COLOR_RESET)"
	docker-compose down

# GUI commands
gui:
	@echo -e "$(COLOR_CYAN)Starting AI GUI Desktop Environment...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)GUI will be available at: http://localhost:6080$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)VNC direct access: localhost:5901$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)Default credentials: copilot/copilot$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml up -d

gui-auto:
	@echo -e "$(COLOR_CYAN)Auto-starting GUI with browser launch...$(COLOR_RESET)"
	./scripts/start_gui_auto.sh

gui-stop:
	@echo -e "$(COLOR_CYAN)Stopping GUI Desktop Environment...$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml down

gui-logs:
	@echo -e "$(COLOR_CYAN)Showing GUI logs...$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml logs -f

gui-restart:
	@echo -e "$(COLOR_CYAN)Restarting GUI Desktop Environment...$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml restart

gui-simple:
	@echo -e "$(COLOR_CYAN)Starting simple GUI environment...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)GUI will be available at: http://localhost:6081$(COLOR_RESET)"
	docker-compose -f docker-compose-gui.yml up -d

# CI/CD commands
ci-test:
	@echo -e "$(COLOR_CYAN)Running CI/CD automated tests...$(COLOR_RESET)"
	chmod +x quick_ci_test.sh
	./quick_ci_test.sh

ci-quick:
	@echo -e "$(COLOR_CYAN)Running quick CI test (no GitHub Issue)...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py --no-github-issue

ci-full:
	@echo -e "$(COLOR_CYAN)Running full CI pipeline with GitHub Issue...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py

ci-verbose:
	@echo -e "$(COLOR_CYAN)Running CI pipeline with verbose output...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py --verbose

ci-comprehensive:
	@echo -e "$(COLOR_CYAN)Running comprehensive controller tests...$(COLOR_RESET)"
	python3 comprehensive_controller_test.py

ci-comprehensive-issue:
	@echo -e "$(COLOR_CYAN)Running comprehensive tests with GitHub Issue...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py --comprehensive

ci-real-api:
	@echo -e "$(COLOR_CYAN)Running real Gradio API tests...$(COLOR_RESET)"
	python3 real_gradio_api_tester.py

ci-all:
	@echo -e "$(COLOR_CYAN)Running all tests (comprehensive + real API + GitHub Issues)...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py

# 🏢 AI-Human Collaboration Company Commands
.PHONY: gitflow-setup feature-start feature-finish collab-commit collab-status

gitflow-setup:
	@echo -e "$(COLOR_CYAN)GitFlow協働開発システム初期化...$(COLOR_RESET)"
	@chmod +x scripts/setup-gitflow-collaboration.sh
	@./scripts/setup-gitflow-collaboration.sh

feature-start:
	@if [ -z "$(name)" ]; then \
		echo -e "$(COLOR_CYAN)使用方法: make feature-start name=機能名$(COLOR_RESET)"; \
		echo -e "$(COLOR_CYAN)例: make feature-start name=ai-chat-enhancement$(COLOR_RESET)"; \
		exit 1; \
	fi
	@echo -e "$(COLOR_CYAN)新機能開発開始: $(name)$(COLOR_RESET)"
	@git flow feature start $(name)
	@echo -e "$(COLOR_GREEN)Feature branch 'feature/$(name)' 作成完了$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)協働開発を開始してください！$(COLOR_RESET)"

feature-finish:
	@if [ -z "$(name)" ]; then \
		echo -e "$(COLOR_CYAN)使用方法: make feature-finish name=機能名$(COLOR_RESET)"; \
		echo -e "$(COLOR_CYAN)例: make feature-finish name=ai-chat-enhancement$(COLOR_RESET)"; \
		exit 1; \
	fi
	@echo -e "$(COLOR_CYAN)機能開発完了: $(name)$(COLOR_RESET)"
	@git flow feature finish $(name)
	@echo -e "$(COLOR_GREEN)Feature branch 'feature/$(name)' マージ完了$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)Wiki文書化を忘れずに！$(COLOR_RESET)"

collab-commit:
	@if [ -z "$(message)" ]; then \
		echo -e "$(COLOR_CYAN)使用方法: make collab-commit message='コミットメッセージ'$(COLOR_RESET)"; \
		echo -e "$(COLOR_CYAN)例: make collab-commit message='AIチャット機能改善'$(COLOR_RESET)"; \
		exit 1; \
	fi
	@echo -e "$(COLOR_CYAN)協働開発コミット実行...$(COLOR_RESET)"
	@git add .
	@git commit -m "ai-collab: $(message)"
	@echo -e "$(COLOR_GREEN)協働開発コミット完了: $(message)$(COLOR_RESET)"

collab-status:
	@echo -e "$(COLOR_CYAN)協働開発状況確認...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)Current branch:$(COLOR_RESET) $$(git branch --show-current)"
	@echo -e "$(COLOR_GREEN)Recent commits:$(COLOR_RESET)"
	@git log --oneline -5
	@echo -e "$(COLOR_GREEN)Pending changes:$(COLOR_RESET)"
	@git status --short
	@echo -e "$(COLOR_GREEN)GitFlow features:$(COLOR_RESET)"
	@git branch | grep feature/ || echo "  No active feature branches"

# 📋 GitHub Issue生成コマンド
generate-issues:
	@echo "🚀 戦略的インデックス → GitHub Issues 生成中..."
	@python scripts/generate_strategic_issues.py
	@echo "✅ Issues生成完了"
	@echo "📊 GitHub Issues: https://github.com/$(GITHUB_USER)/AUTOCREATE/issues"

close-completed-issues:
	@echo "✅ 完了済みIssueのクローズ処理"
	@echo "Phase 1完了Issues (#001-#005) をクローズします"

# 🤖 AI Vision & OCR Commands
ocr-install:
	@echo "📦 OCR分析用パッケージインストール中..."
	@pip install -r requirements_ocr.txt
	@echo "✅ OCR依存関係インストール完了"

ocr-gradio:
	@$(MAKE) stop-port
	@echo "🚀 AUTOCREATE OCR Gradio起動中..."
	@echo "🏛️ AI社長×無職CTO体制による画像解析システム"
	@python gradio_ocr_analyzer.py

gas-login:
	@echo "🔐 Google Apps Script CLI認証"
	@clasp login

gas-push:
	@echo "📤 GAS OCR API をアップロード中..."
	@cd gas-ocr-api && clasp push
	@echo "✅ GAS API デプロイ完了"
	@echo "🔗 Web App URLを取得してGradioに設定してください"

screenshot-ocr:
	@echo "📸 スクリーンショット撮影 → OCR解析"
	@docker exec ubuntu-desktop-vnc bash -c "DISPLAY=:1 scrot /tmp/auto_screenshot_$$(date +%Y%m%d_%H%M%S).png"
	@echo "🔍 撮影完了 - Gradioでアップロードして解析してください"

# OCRパイプライン全体テスト
ocr-pipeline:
	@echo "🚀 OCR分析パイプライン全体テスト"
	@$(MAKE) screenshot-ocr

# 🤖 OCR RPA Automation Commands
ocr-rpa-demo:
	@echo "🚀 AUTOCREATE OCR RPA自動化デモ開始"
	@echo "🏛️ AI社長×無職CTO体制による知的自動化"
	@mkdir -p screenshots reports
	@python scripts/ocr_rpa_automation.py
	@echo "✅ OCR RPA デモ完了"

ocr-rpa-config:
	@echo "⚙️ OCR RPA設定エディタ"
	@if [ ! -f config/ocr_rpa_config.json ]; then \
		echo "❌ 設定ファイルが見つかりません"; \
		echo "📁 config/ocr_rpa_config.json を作成してください"; \
	else \
		echo "📝 設定ファイルを開きます..."; \
		nano config/ocr_rpa_config.json; \
	fi

ocr-rpa-report:
	@echo "📋 最新のOCR RPA自動化レポート"
	@if [ -d reports ]; then \
		echo "📊 利用可能なレポートファイル:"; \
		ls -la reports/*.json 2>/dev/null | tail -5 || echo "❌ レポートファイルが見つかりません"; \
		echo ""; \
		echo "最新レポートの内容:"; \
		ls -t reports/*.json 2>/dev/null | head -1 | xargs cat 2>/dev/null | jq '.metadata, .technical_results, .business_value' 2>/dev/null || echo "❌ 有効なJSONレポートが見つかりません"; \
	else \
		echo "❌ reportsディレクトリが見つかりません"; \
		echo "💡 make ocr-rpa-demo を先に実行してください"; \
	fi

ocr-rpa-clean:
	@echo "🧹 OCR RPA一時ファイルクリーンアップ"
	@rm -rf screenshots/*.png reports/*.json
	@echo "✅ スクリーンショットとレポートファイルをクリーンアップしました"

vnc-auto:
	@echo "🖥️ VNCデスクトップ自動操作デモ"
	@echo "🏛️ AI社長×無職CTO体制によるフル自動化"
	@python scripts/vnc_desktop_automation.py
	@echo "✅ VNC自動操作デモ完了"

jupyter-ocr:
	@echo "📓 Jupyter OCR RPA デモノートブック起動"
	@echo "🏛️ 誰でも使えるAI自動化システム"
	@jupyter lab AUTOCREATE_OCR_RPA_Demo.ipynb --ip=0.0.0.0 --port=8889 --no-browser --allow-root
	@echo "🌐 アクセス: http://localhost:8889"

screenshots-view:
	@echo "📸 収集済みスクリーンショット一覧"
	@if [ -d screenshots ]; then \
		echo "📊 スクリーンショットファイル:"; \
		ls -la screenshots/*.png 2>/dev/null || echo "❌ スクリーンショットが見つかりません"; \
		echo ""; \
		echo "💡 最新のスクリーンショット:"; \
		ls -t screenshots/*.png 2>/dev/null | head -1 | xargs file 2>/dev/null || echo "ファイル情報を取得できません"; \
	else \
		echo "❌ screenshotsディレクトリが見つかりません"; \
		echo "💡 make vnc-auto または make ocr-rpa-demo を先に実行してください"; \
	fi

# OCR + RPA 自動化関連コマンド
.PHONY: ocr-rpa-loop ocr-rpa-test notebook-demo

ocr-rpa-loop: ## OCR + RPA 自動化ループを実行
	@echo "🚀 OCR + RPA 自動化ループ実行中..."
	python scripts/ocr_rpa_automation_loop.py

ocr-rpa-test: ## OCR + RPA システムをテスト
	@echo "🧪 OCR + RPA システムテスト中..."
	python ocr_rpa_test.py

notebook-demo: ## Jupyter Notebook デモを起動
	@echo "📱 Jupyter Notebook デモ起動中..."
	jupyter notebook AUTOCREATE_AI_Vision_Automation_Complete_Guide.ipynb

notebook-colab: ## Google Colab 用のノートブック情報を表示
	@echo "🌐 Google Colab でのノートブック使用方法:"
	@echo "1. 以下のURLにアクセス:"
	@echo "   https://colab.research.google.com/"
	@echo "2. GitHubからノートブックをインポート:"
	@echo "   AUTOCREATE_AI_Vision_Automation_Complete_Guide.ipynb"
	@echo "3. 'ランタイム' → 'すべてのセルを実行' をクリック"

hybrid-ocr: ## ハイブリッドOCR解析システム実行
	@echo "🔧 ハイブリッドOCR解析システム実行中..."
	python scripts/hybrid_ocr_analyzer.py

local-ocr: ## ローカルOCR解析システム実行
	@echo "🏠 ローカルOCR解析システム実行中..."
	python scripts/local_ocr_analyzer.py

gas-status: ## GAS OCR APIの状態確認
	@echo "📡 GAS OCR API状態確認中..."
	@python -c "import requests; r=requests.get('https://script.google.com/macros/s/1ISqaty-oD30b559LXJ5q6dkXYp1H888dxP4uSjK9osgDUm6wDm9rUOOz/exec', timeout=10); print(f'Status: {r.status_code}, Response: {r.text[:100]}...')" || echo "❌ GAS API接続失敗"

ocr-demo: ## OCR解析システム全般デモ
	@echo "🎭 OCR解析システム全般デモ実行中..."
	@echo "1. ハイブリッドOCR解析:"
	@python scripts/hybrid_ocr_analyzer.py
	@echo "\n2. 自動化ループテスト:"
	@python scripts/ocr_rpa_automation_loop.py

# GitHub Issue・Project管理
.PHONY: issues create-issue list-issues project-status

issues: ## Issue一覧を表示
	@echo "📋 AUTOCREATE プロジェクト Issue一覧:"
	@gh issue list --label "task,ai-ceo,cto-jobless,ocr-rpa,kinkaimasu"

create-issue: ## 新しいIssueを作成（対話式）
	@echo "📝 新しいIssue作成:"
	@gh issue create

list-issues: ## ラベル別Issue一覧
	@echo "🏛️ AI社長関連Issue:"
	@gh issue list --label "ai-ceo" || echo "なし"
	@echo "\n🔧 無職CTO関連Issue:"  
	@gh issue list --label "cto-jobless" || echo "なし"
	@echo "\n🏪 kinkaimasu.jp案件:"
	@gh issue list --label "kinkaimasu" || echo "なし"
	@echo "\n🤖 OCR+RPA関連:"
	@gh issue list --label "ocr-rpa" || echo "なし"

project-status: ## プロジェクト全体状況確認
	@echo "🚀 AUTOCREATE プロジェクト状況:"
	@echo "📊 総Issue数: $$(gh issue list --json number | jq '. | length')"
	@echo "🔥 高優先度Issue: $$(gh issue list --label 'priority:high' --json number | jq '. | length')"
	@echo "✅ 完了Issue: $$(gh issue list --state closed --json number | jq '. | length')"
	@echo "🏛️ AI社長担当: $$(gh issue list --label 'ai-ceo' --json number | jq '. | length')"
	@echo "🔧 無職CTO担当: $$(gh issue list --label 'cto-jobless' --json number | jq '. | length')"

github-setup: ## GitHub設定確認・初期設定
	@echo "⚙️ GitHub設定状況:"
	@gh auth status
	@echo "\n📋 ラベル一覧:"
	@gh label list || echo "ラベル取得エラー"
	@echo "\n📊 リモート設定:"
	@git remote -v

selector-install: ## セレクター分析システム用パッケージインストール
	@echo "📦 セレクター分析システム用パッケージインストール中..."
	pip install -r requirements_selector.txt
	@echo "✅ セレクター分析システム用パッケージインストール完了"

selector-analyze: ## セレクター分析システムでkinkaimasu.jp分析
	@echo "🎯 セレクター分析システム実行中..."
	python scripts/selector_analyzer.py

selector-demo: ## セレクター分析システムデモ（Selenium使用）
	@echo "🚀 セレクター分析システムデモ実行..."
	@echo "注意: Chrome/Chromiumが必要です"
	python scripts/selector_analyzer.py

smart-automation: ## スマート自動化システム（OCR + セレクター統合）
	@echo "🧠 スマート自動化システム実行中..."
	@echo "1. ハイブリッドOCR解析:"
	@python scripts/hybrid_ocr_analyzer.py
	@echo "\n2. セレクター分析:"
	@python scripts/selector_analyzer.py
	@echo "\n✅ スマート自動化システム完了"

# =============================================================================
# 🤖 WIKI RAG System Commands
# =============================================================================

.PHONY: wiki-rag wiki-rag-cli wiki-rag-build wiki-rag-install

wiki-rag-install: ## Install WIKI RAG system dependencies
	@echo -e "$(COLOR_CYAN)Installing WIKI RAG dependencies...$(COLOR_RESET)"
	pip install -r requirements_wiki_rag.txt
	@echo -e "$(COLOR_GREEN)✅ WIKI RAG dependencies installed!$(COLOR_RESET)"

wiki-rag-build: ## Build/rebuild WIKI RAG knowledge base
	@echo -e "$(COLOR_CYAN)Building WIKI RAG knowledge base...$(COLOR_RESET)"
	python scripts/wiki_rag_cli.py build --force
	@echo -e "$(COLOR_GREEN)✅ WIKI RAG knowledge base built!$(COLOR_RESET)"

wiki-rag: stop-port wiki-rag-install ## Start WIKI RAG system with Gradio UI
	@echo -e "$(COLOR_CYAN)Starting WIKI RAG system...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)🌐 Gradio interface will be available at: http://localhost:7860$(COLOR_RESET)"
	python scripts/wiki_rag_system.py

wiki-rag-cli: wiki-rag-install ## Use WIKI RAG CLI for command line queries
	@echo -e "$(COLOR_CYAN)WIKI RAG CLI Usage:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)Query:$(COLOR_RESET) python scripts/wiki_rag_cli.py query 'your question'"
	@echo -e "  $(COLOR_GREEN)Search:$(COLOR_RESET) python scripts/wiki_rag_cli.py search 'keyword'"  
	@echo -e "  $(COLOR_GREEN)Stats:$(COLOR_RESET) python scripts/wiki_rag_cli.py stats"
	@echo -e "  $(COLOR_GREEN)Build:$(COLOR_RESET) python scripts/wiki_rag_cli.py build"
	@echo ""
	@echo -e "$(COLOR_CYAN)Example usage:$(COLOR_RESET)"
	@echo -e "  python scripts/wiki_rag_cli.py query 'Gradioの使い方は？'"

wiki-rag-lite: stop-port ## Start WIKI RAG lite system (no HuggingFace auth required)
	@echo -e "$(COLOR_CYAN)Starting WIKI RAG Lite system...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)🌐 Gradio interface will be available at: http://localhost:7860$(COLOR_RESET)"
	python scripts/wiki_rag_lite.py

wiki-rag-lite-cli: ## Use WIKI RAG Lite CLI for command line queries
	@echo -e "$(COLOR_CYAN)WIKI RAG Lite CLI Usage:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)Query:$(COLOR_RESET) python scripts/wiki_rag_lite_cli.py query 'your question'"
	@echo -e "  $(COLOR_GREEN)Search:$(COLOR_RESET) python scripts/wiki_rag_lite_cli.py search 'keyword'"  
	@echo -e "  $(COLOR_GREEN)Stats:$(COLOR_RESET) python scripts/wiki_rag_lite_cli.py stats"
	@echo -e "  $(COLOR_GREEN)Build:$(COLOR_RESET) python scripts/wiki_rag_lite_cli.py build"
	@echo ""
	@echo -e "$(COLOR_CYAN)Example usage:$(COLOR_RESET)"
	@echo -e "  python scripts/wiki_rag_lite_cli.py query 'Gradioの使い方は？'"

wiki-rag-chat: stop-port ## Start WIKI RAG Chat interface (conversational AI)
	@echo -e "$(COLOR_CYAN)Starting WIKI RAG Chat system...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)🤖 Chat interface will be available at: http://localhost:7860$(COLOR_RESET)"
	python scripts/wiki_rag_chat.py

# Lavelo AI 自動化テストコマンド
test-lavelo:
	@echo -e "$(COLOR_CYAN)Running Lavelo AI Basic Test...$(COLOR_RESET)"
	@python lavelo_automation_test.py --mode=basic

test-supabase:
	@echo -e "$(COLOR_CYAN)Testing Supabase Connection...$(COLOR_RESET)"
	@python lavelo_automation_test.py --mode=supabase_test

test-memory:
	@echo -e "$(COLOR_CYAN)Testing Memory System...$(COLOR_RESET)"
	@python lavelo_automation_test.py --mode=memory_test

test-import:
	@echo -e "$(COLOR_CYAN)Testing Lavelo Import...$(COLOR_RESET)"
	@python lavelo_automation_test.py --mode=import_test

test-full:
	@echo -e "$(COLOR_CYAN)Running Full Lavelo AI Test Suite...$(COLOR_RESET)"
	@python lavelo_automation_test.py --mode=full_test

# GPT Engineer System Generation
generated_systems:
	@echo -e "$(COLOR_CYAN)Running GPT Engineer System Generation for $(COLOR_GREEN)$(name)$(COLOR_CYAN)...$(COLOR_RESET)"
	@if [ -z "$(name)" ]; then echo "❌ Error: name parameter is required. Usage: make generated_systems name=your_system_name"; exit 1; fi
	@echo -e "$(COLOR_CYAN)Creating new Gradio controller directory...$(COLOR_RESET)"
	@mkdir -p "app/Http/Controllers/Gradio/gra_$(shell printf "%02d" $$(ls -1d app/Http/Controllers/Gradio/gra_* 2>/dev/null | wc -l | xargs expr 1 +))_$(name)"
	@CONTROLLER_DIR="app/Http/Controllers/Gradio/gra_$(shell printf "%02d" $$(ls -1d app/Http/Controllers/Gradio/gra_* 2>/dev/null | wc -l | xargs expr 1 +))_$(name)" && \
	echo -e "$(COLOR_CYAN)Copying prompts for $(name)...$(COLOR_RESET)" && \
	if [ -d "generated_projects/$(name)" ]; then \
		cp -r "generated_projects/$(name)/." "$$CONTROLLER_DIR/"; \
	fi && \
	cd ./gpt-engineer && \
	echo -e "y\ny\ny" | poetry run gpt-engineer "../$$CONTROLLER_DIR" --model gpt-4 --temperature 0.1
	@echo -e "$(COLOR_GREEN)✅ System generated and added to Gradio Controllers$(COLOR_RESET)"
	@echo -e "$(COLOR_CYAN)🔗 Auto-registering in Gradio interface...$(COLOR_RESET)"
	@python -c "import os, glob; dirs = glob.glob('app/Http/Controllers/Gradio/gra_*_$(name)'); print(f'✅ Controller created: {dirs[0]}' if dirs else '❌ Controller directory not found'); print('🔄 Gradio interface will auto-detect this new controller')"

gpt-setup:
	@echo -e "$(COLOR_CYAN)Setting up GPT Engineer...$(COLOR_RESET)"
	@cd ./gpt-engineer && pip install poetry && poetry install
	@echo -e "$(COLOR_GREEN)✅ GPT Engineer setup completed$(COLOR_RESET)"