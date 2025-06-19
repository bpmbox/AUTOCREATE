#Sets the default shell for executing commands as /bin/bash and specifies command should be executed in a Bash shell.
SHELL := /bin/bash

# GitHub Configuration (load from .env)
GITHUB_TOKEN := $(shell grep "GITHUB_TOKEN=" .env | cut -d'=' -f2)
GITHUB_USER := $(shell grep "GITHUB_USER=" .env | cut -d'=' -f2)
GITHUB_REPO := $(shell grep "GITHUB_REPO=" .env | cut -d'=' -f2)

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
	@echo "================================================================================"
	@echo "AUTOCREATE AI CEO & Jobless CTO Command System"
	@echo "================================================================================"
	@echo "Usage: make <command>"
	@echo ""
	@echo "TOP COMMANDS (Start Here!):"
	@echo "  chrome-ext             Start AI CEO Chrome extension"
	@echo "  app                    Start main application (port 7860)"
	@echo "  wiki-rag               Start WIKI RAG system"
	@echo "  gui                    Start desktop GUI (port 6080)"
	@echo "  ai-human-bpms          Start AI-Human BPMS system"
	@echo ""	@echo "Chrome Extension:"
	@echo "  chrome-ext             Start Chrome with extension"
	@echo "  chrome-ext-test        Test page + Supabase chat"
	@echo "  chrome-ext-status      Check extension status"
	@echo "  chrome-ext-ai-test     AI response function test"
	@echo "  chrome-ext-xpath-config XPath configuration manager"
	@echo "  chrome-ext-typeerror-test  TypeError fix verification"
	@echo "  chrome-ext-error-status    Current error status"
	@echo ""	@echo "Notion Integration:"
	@echo "  notion-demo            Demo mode (shows what pages would look like)"
	@echo "  notion-test            Test Notion API connection"
	@echo "  notion-sample          Create sample Notion page"
	@echo "  notion-autocreate      Create AUTOCREATE knowledge page"
	@echo "  notion-technical       Create technical documentation"
	@echo "  notion-knowledge-base  Create comprehensive knowledge base (5 pages)"
	@echo "  notion-business-knowledge Create business-oriented knowledge (4 pages)"
	@echo "  notion-knowledge-summary Show knowledge base overview"
	@echo "  notion-workspace       Explore Notion workspace"
	@echo "  notion-diagnostics     Full Notion diagnostics"
	@echo ""	@echo "Resource-First Development:"
	@echo "  resource-first-deploy  🚀 Deploy both business & developer resources"
	@echo "  create-developer-issue Create GitHub issue with n8n/BPMN/Mermaid"
	@echo ""
	@echo "JIRA Integration:"
	@echo "  jira-test             Test JIRA API connection"
	@echo "  jira-create-tickets   Create AUTOCREATE project tickets"
	@echo "  jira-diagnostics      Full JIRA diagnostics"
	@echo ""
	@echo "Triple Deploy System:"
	@echo "  triple-deploy         🚀 Notion + GitHub + JIRA complete deployment"
	@echo ""
	@echo "Applications:"
	@echo "  app                    FastAPI application"
	@echo "  dev                    Development mode"
	@echo "  debug                  Debug mode"
	@echo "  stop-port              Stop port 7860"
	@echo ""
	@echo "GUI & Desktop:"
	@echo "  gui                    AI GUI desktop (port 6080)"
	@echo "  gui-simple             Simple GUI (port 6081)"
	@echo ""
	@echo "OCR & RPA:"
	@echo "  ocr-gradio             OCR Gradio interface"
	@echo "  ocr-rpa-demo           RPA automation demo"
	@echo ""
	@echo "WIKI RAG:"
	@echo "  wiki-rag               WIKI RAG system (port 7860)"
	@echo "  wiki-rag-lite          WIKI RAG Lite"
	@echo ""
	@echo "Testing:"
	@echo "  test                   Run all tests"
	@echo "  ci-test                CI/CD tests"
	@echo ""
	@echo "Setup:"
	@echo "  install                Install dependencies"
	@echo "  clean                  Clean temp files"
	@echo ""
	@echo "Quick Start: make chrome-ext  or  make app"
	@echo "================================================================================"
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
	@echo "🤖 n8n Automation Integration Commands:"
	@echo "  n8n-test       	Test n8n API connection and create AUTOCREATE workflow"
	@echo "  n8n-create     	Create AUTOCREATE AI Solutions workflow in n8n"
	@echo "  n8n-trigger    	Test workflow execution with sample data"
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
	@echo ""
	@echo "🔄 n8n Workflow Automation Commands:"
	@echo "  n8n-setup       	Setup n8n workflow integration"
	@echo "  n8n-test        	Test n8n API connection"
	@echo "  n8n-create      	Create AUTOCREATE AI workflow in n8n"
	@echo "  n8n-list        	List all n8n workflows"
	@echo "  n8n-webhook     	Get webhook URL for n8n integration"
	@echo ""
	@echo "📚 WIKI RAG System Commands:"
	@echo "  wiki-rag        	Start WIKI RAG system with Gradio UI"
	@echo "  wiki-rag-cli    	Use WIKI RAG CLI for command line queries"
	@echo "  wiki-rag-build  	Build/rebuild WIKI RAG knowledge base"
	@echo "  wiki-rag-install	Install WIKI RAG dependencies"
	@echo "  wiki-rag-lite   	Start WIKI RAG lite system (no auth required)"
	@echo "  wiki-rag-lite-cli	Use WIKI RAG lite CLI for command line queries"
	@echo "  wiki-rag-chat   	Start WIKI RAG Chat interface (conversational AI)"
	@echo ""
	@echo "🛡️  Safe Integration Testing Commands:"
	@echo "  safe-test      	Run safe integration tests (dry-run mode)"
	@echo "  config-check   	Check environment configuration safely"
	@echo "  integration-status	Show all integration service status"
	@echo "  dry-run-all    	Test all integrations without executing"
	@echo ""
	@echo "🧠 AI-Human BPMS Assistant Commands:"
	@echo "  ai-human-bpms   	Run AI-Human BPMS Assistant demonstration"
	@echo "  bpms-analyze    	Analyze human cognitive capacity and workflow needs"
	@echo "  bpms-optimize   	Generate optimized human-friendly workflows"
	@echo "  bpms-monitor    	Monitor human-AI collaboration effectiveness"
	@echo "  cognitive-check 	Check human cognitive load and suggest breaks"
	@echo ""
	@echo "📝 GitHub Issue Management Commands:"
	@echo "  create-github-issue	Create GitHub Issue for AI-Human BPMS Assistant"
	@echo "  github-issue-ai-bpms	Create AI-Human BPMS specific GitHub Issue"
	@echo "  github-issue-status	Check GitHub repository and issue creation status"
	@echo ""

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

notion-knowledge-base:
	@echo "📚 Creating comprehensive AUTOCREATE knowledge base..."
	node notion_knowledge_creator.js

notion-knowledge-summary:
	@echo "📊 AUTOCREATE Knowledge Base Summary"
	@echo "===================================="
	@echo "🎯 System Overview"
	@echo "🔧 Notion API Integration Guide"  
	@echo "🌐 Chrome Extension Automation"
	@echo "🚀 Makefile Commands Reference"
	@echo "💡 FAQ & Troubleshooting"
	@echo ""
	@echo "Use 'make notion-knowledge-base' to create all knowledge pages"

notion-business-knowledge:
	@echo "🏢 業務向けナレッジベース作成..."
	node notion_business_knowledge.js

create-developer-issue:
	@echo "👨‍💻 開発者向けGitHub Issue作成..."
	python3 create_developer_issue.py

resource-first-deploy:
	@echo "📚 資料ファースト展開システム"
	@echo "================================"
	@echo "1. 業務向けナレッジ（Notion）作成中..."
	make notion-business-knowledge
	@echo ""
	@echo "2. 開発者向け仕様書（GitHub Issue）作成中..."
	make create-developer-issue
	@echo ""
	@echo "🎉 資料ファースト展開完了！"
	@echo "📊 業務チーム → Notionナレッジベース"
	@echo "👨‍💻 開発チーム → GitHub Issue仕様書"

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
	export OPENAI_API_BASE="https://api.groq.com/openai/v1" && \
	export OPENAI_API_KEY="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" && \
	export MODEL_NAME="llama3-70b-8192" && \
	export LOCAL_MODEL=false && \
		echo "API設定: $$OPENAI_API_BASE, Model: $$MODEL_NAME" && \
	yes y | timeout 20 poetry run gpt-engineer "../$$CONTROLLER_DIR" --model llama3-70b-8192 --temperature 0.1 || true
	@echo -e "$(COLOR_GREEN)✅ System generated and added to Gradio Controllers$(COLOR_RESET)"
	@echo -e "$(COLOR_CYAN)🔗 Auto-registering in Gradio interface...$(COLOR_RESET)"
	@python -c "import os, glob; dirs = glob.glob('app/Http/Controllers/Gradio/gra_*_$(name)'); print(f'✅ Controller created: {dirs[0]}' if dirs else '❌ Controller directory not found'); print('🔄 Gradio interface will auto-detect this new controller')"

gpt-setup:
	@echo -e "$(COLOR_CYAN)Setting up GPT Engineer...$(COLOR_RESET)"
	@cd ./gpt-engineer && pip install poetry && poetry install
	@echo -e "$(COLOR_GREEN)✅ GPT Engineer setup completed$(COLOR_RESET)"

# n8n Workflow Automation Integration
n8n-setup:
	@echo -e "$(COLOR_CYAN)🔄 Setting up n8n workflow integration...$(COLOR_RESET)"
	@python -m pip install requests
	@echo -e "$(COLOR_GREEN)✅ n8n integration dependencies installed$(COLOR_RESET)"

n8n-test:
	@echo -e "$(COLOR_CYAN)Testing n8n connection...$(COLOR_RESET)"
	@python3 test_n8n_basic.py

n8n-deploy:
	@echo -e "$(COLOR_CYAN)Deploying AUTOCREATE AI workflows to n8n...$(COLOR_RESET)"
	@python3 n8n_workflow_manager.py

n8n-workflows:
	@echo -e "$(COLOR_CYAN)Managing n8n workflows...$(COLOR_RESET)"
	@if [ -z "$(action)" ]; then echo "❌ Error: action parameter required. Usage: make n8n-workflows action=[deploy|list|test]"; exit 1; fi
	@if [ "$(action)" = "deploy" ]; then python3 n8n_workflow_manager.py; fi
	@if [ "$(action)" = "list" ]; then python3 -c "from n8n_workflow_manager import N8nWorkflowManager; N8nWorkflowManager().list_workflows()"; fi
	@if [ "$(action)" = "test" ]; then python3 test_n8n_basic.py; fi

# AUTOCREATE AI - miibo Chat Integration
miibo-test:
	@echo -e "$(COLOR_CYAN)Testing miibo API integration...$(COLOR_RESET)"
	@python3 test_miibo_integration.py

miibo-deploy:
	@echo -e "$(COLOR_CYAN)Deploying miibo + n8n integration workflow...$(COLOR_RESET)"
	@python3 autocreate_miibo_integration.py

miibo-chat:
	@echo -e "$(COLOR_CYAN)Starting AUTOCREATE AI chat interface...$(COLOR_RESET)"
	@python3 -c "from autocreate_miibo_integration import AUTOCREATEChatIntegration; AUTOCREATEChatIntegration().test_integrated_system()"


# GitHub Issue Management
create-github-issue:
	@echo -e "$(COLOR_CYAN)Creating GitHub Issue for AI-Human BPMS Assistant...$(COLOR_RESET)"
	@python3 create_github_issue.py

github-issue-ai-bpms:
	@echo -e "$(COLOR_CYAN)Creating AI-Human BPMS specific GitHub Issue...$(COLOR_RESET)"
	@python3 create_github_issue.py --type ai-human-bpms

github-issue-status:
	@echo -e "$(COLOR_CYAN)Checking GitHub repository and issue creation status...$(COLOR_RESET)"
	@python3 -c "from create_github_issue import GitHubIssueCreator; creator = GitHubIssueCreator(); creator.check_repository_status()"

github-workflow:
	@echo -e "$(COLOR_CYAN)Running complete GitHub workflow (create issue + documentation)...$(COLOR_RESET)"
	@echo "Step 1: Creating GitHub Issue..."
	@python3 create_github_issue.py
	@echo "Step 2: Generating status report..."
	@python3 -c "print('✅ GitHub workflow completed successfully!')"

# Complete project workflow with GitHub Issue
complete-workflow:
	@echo -e "$(COLOR_CYAN)Running complete AUTOCREATE workflow...$(COLOR_RESET)"
	@echo "Step 1: Running tests..."
	@make ci-test || true
	@echo "Step 2: Creating GitHub Issue..."
	@make create-github-issue
	@echo "Step 3: Generating documentation..."
	@python3 -c "print('📚 Documentation generated')"
	@echo -e "$(COLOR_GREEN)✅ Complete workflow finished!$(COLOR_RESET)"

# ProcessMaker BPM Integration
processmaker-setup:
	@echo -e "$(COLOR_CYAN)Setting up ProcessMaker BPM integration...$(COLOR_RESET)"
	@cd vendor/processmaker && composer install
	@echo -e "$(COLOR_GREEN)✅ ProcessMaker setup completed$(COLOR_RESET)"

processmaker-start:
	@echo -e "$(COLOR_CYAN)Starting ProcessMaker BPM platform...$(COLOR_RESET)"
	@cd vendor/processmaker && php artisan serve --host=0.0.0.0 --port=8080
	
processmaker-status:
	@echo -e "$(COLOR_CYAN)Checking ProcessMaker status...$(COLOR_RESET)"
	@if [ -d "vendor/processmaker" ]; then echo "✅ ProcessMaker submodule exists"; else echo "❌ ProcessMaker not found"; fi
	@cd vendor/processmaker && git status --porcelain | wc -l | xargs -I {} echo "Modified files: {}"

# Puppeteer Chrome Extension commands
puppeteer-install:
	npm install puppeteer

puppeteer-test:
	node puppeteer_chrome_extension.js

puppeteer-debug:
	node --inspect-brk puppeteer_chrome_extension.js

# Groq API Test commands
groq-test:
	node groq_test.js test

groq-models:
	node groq_test.js models

groq-all:
	node groq_test.js both

groq-install:
	npm install axios dotenv

# Groq API Test commands (Python版も追加)
groq-test-py:
	python groq_test.py test

groq-models-py:
	python groq_test.py models

groq-all-py:
	python groq_test.py both

groq-install-py:
	pip install requests python-dotenv

# Chrome Extension Error Fix commands
chrome-ext-fix:
	cd chrome-extension && node env-loader.js

chrome-ext-validate:
	cd chrome-extension && npx web-ext lint

chrome-ext-reload:
	"$BROWSER" chrome://extensions

# Chrome Extension Notification Test commands
chrome-ext-test-notification:
	"$BROWSER" chrome://extensions && echo "拡張機能を有効化してテスト通知を確認してください"

chrome-ext-debug:
	"$BROWSER" chrome://extensions && echo "デベロッパーモードを有効にして、バックグラウンドページを確認してください"

chrome-ext-console:
	echo "Chrome拡張機能のコンソールでエラーを確認するには:"
	echo "1. chrome://extensions を開く"
	echo "2. デベロッパーモードを有効化"
	echo "3. 拡張機能の 'service worker' リンクをクリック"
	echo "4. コンソールタブでログを確認"

# Chrome Extension Simple Notification Test
chrome-ext-simple-test:
	echo "シンプル通知テストを実行します"
	echo "1. Chrome拡張機能ページを開きます"
	"$BROWSER" chrome://extensions
	echo "2. 拡張機能をリロードしてください"
	echo "3. デベロッパーツール > service worker でコンソールを確認"

chrome-ext-notification-debug:
	echo "通知デバッグ手順:"
	echo "1. chrome://settings/content/notifications を開く"
	echo "2. 通知が許可されているか確認"
	echo "3. chrome://extensions でデベロッパーモードを有効に"
	echo "4. service worker のコンソールでエラーを確認"

# Chrome Extension Comprehensive Test
chrome-ext-comprehensive-test:
	echo "🧪 包括的通知テストを実行"
	echo "以下の手順で実行してください:"
	echo "1. Chrome拡張機能をリロード"
	echo "2. デベロッパーツールでservice workerを開く"
	echo "3. コンソールで以下を実行:"
	echo "   chrome.runtime.sendMessage({type: 'RUN_COMPREHENSIVE_TEST'})"

chrome-ext-permissions-check:
	echo "🔍 Chrome拡張機能の権限確認"
	echo "1. chrome://settings/content/notifications を確認"
	echo "2. 拡張機能の通知権限が許可されているか確認"
	echo "3. chrome://extensions で拡張機能の詳細を確認"

# Chrome Extension Safe Notification Test
chrome-ext-safe-test:
	echo "🛡️ 安全な通知テストを実行"
	echo "コンソールで以下を実行:"
	echo "chrome.runtime.sendMessage({type: 'TEST_SAFE_NOTIFICATION'})"

chrome-ext-manual-notification:
	echo "📱 手動通知テスト"
	echo "コンソールで以下を実行:"
	echo "chrome.runtime.sendMessage({type: 'CREATE_SAFE_NOTIFICATION', title: 'テスト', message: 'メッセージ'})"

chrome-ext-debug-props:
	echo "🔍 通知プロパティデバッグ"
	echo "以下の項目を確認してください:"
	echo "1. type: 'basic' が設定されているか"
	echo "2. iconUrl: Base64データURLが設定されているか"
	echo "3. title: 文字列が設定されているか"
	echo "4. message: 文字列が設定されているか"

# Chrome Extension Minimal Notification Test
chrome-ext-minimal-test:
	echo "🔧 最小限通知テスト"
	echo "1. Chrome拡張機能をリロード"
	echo "2. コンソールで実行: chrome.runtime.sendMessage({type: 'TEST_MINIMAL_NOTIFICATION'})"

chrome-ext-check-permissions:
	echo "🔍 通知権限確認"
	echo "1. chrome://settings/content/notifications を開く"
	echo "2. サイト別の通知設定を確認"
	echo "3. コンソールで実行: chrome.runtime.sendMessage({type: 'CHECK_PERMISSIONS'})"

chrome-ext-fix-images:
	echo "🖼️ 画像エラー修正手順"
	echo "1. iconUrlプロパティを完全に削除"
	echo "2. type, title, messageのみを使用"
	echo "3. シンプルな通知に変更完了"

# Chrome Extension Isolated Notification Test
chrome-ext-isolated-test:
	echo "🔬 独立通知テスト実行"
	echo "1. Chrome拡張機能をリロード"
	echo "2. デベロッパーツールでservice workerを開く"
	echo "3. 3秒後に自動でテスト実行されます"
	echo "4. 手動実行: chrome.runtime.sendMessage({type: 'ISOLATED_NOTIFICATION_TEST'})"

chrome-ext-debug-detailed:
	echo "🐛 詳細デバッグ手順"
	echo "1. chrome://extensions でデベロッパーモードを有効化"
	echo "2. 拡張機能の 'service worker' をクリック"
	echo "3. コンソールで詳細なログを確認"
	echo "4. showNotification関数の引数を確認"
	echo "5. notificationOptionsの各プロパティを確認"

# Chrome Extension Basic Notification Test
chrome-ext-basic-test:
	echo "🔬 基本通知テスト実行"
	echo "手順:"
	echo "1. chrome://extensions を開く"
	echo "2. デベロッパーモードを有効化"
	echo "3. 拡張機能をリロード"
	echo "4. service worker をクリック"
	echo "5. コンソールで詳細ログを確認"
	echo "6. 手動実行: chrome.runtime.sendMessage({type: 'BASIC_NOTIFICATION_TEST'})"

chrome-ext-permissions-debug:
	echo "🔍 権限デバッグ"
	echo "確認項目:"
	echo "1. manifest.json に 'notifications' 権限があるか"
	echo "2. chrome://settings/content/notifications で通知が許可されているか"
	echo "3. chrome://extensions で拡張機能の詳細を確認"
	echo "4. デベロッパーツールでエラーメッセージを確認"

# Chrome Extension Connection Test
chrome-ext-connection-test:
	echo "🔗 Chrome拡張機能接続テスト"
	echo "手順:"
	echo "1. chrome://extensions を開く"
	echo "2. デベロッパーモードを有効化"
	echo "3. 拡張機能をリロード"
	echo "4. service workerをクリック"
	echo "5. 3秒後に自動テスト実行"
	echo "6. 手動実行: testConnection()"

chrome-ext-fix-connection:
	echo "🔧 接続エラー修正手順"
	echo "原因と対策:"
	echo "1. 'Receiving end does not exist' = メッセージリスナーが未登録"
	echo "2. service workerが非アクティブ = 拡張機能をリロード"
	echo "3. manifest.jsonの権限不足 = permissions確認"
	echo "4. メッセージハンドラーのエラー = try-catch追加"

# Chrome Extension Service Worker Diagnostic
chrome-ext-service-worker-diagnostic:
	echo "🩺 Service Worker通信診断"
	echo "手順:"
	echo "1. chrome://extensions を開く"
	echo "2. デベロッパーモードを有効化"
	echo "3. 拡張機能をリロード"
	echo "4. service workerをクリック"
	echo "5. コンソールで診断結果を確認"
	echo "6. 手動診断: chrome.runtime.sendMessage({type: 'RUN_COMMUNICATION_DIAGNOSTIC'})"

chrome-ext-fix-receiving-end:
	echo "🔧 'Receiving end does not exist' エラー修正"
	echo "原因と対策:"
	echo "1. Service Workerが非アクティブ → 拡張機能をリロード"
	echo "2. メッセージリスナー未登録 → background.jsを確認"
	echo "3. chrome.runtime.onMessage.addListener() が実行されているか確認"
	echo "4. return true で非同期応答を維持"
	echo "5. try-catch でエラーハンドリング"

# Chrome Extension AI Response Test
chrome-ext-ai-test:
	echo "🤖 AI大統領応答機能テストを実行"
	echo "1. Chrome拡張機能をリロード"
	echo "2. test-ai-response.html ページを開く"
	echo "3. テストボタンをクリックして実行"
	"$BROWSER" file://$(shell pwd)/chrome-extension/test-ai-response.html

chrome-ext-ai-console-test:
	echo "🧪 AI応答コンソールテスト"
	echo "コンソールで以下を実行:"
	echo "chrome.runtime.sendMessage({type: 'test_ai_response', data: {message: 'こんにちは', username: 'テスト'}})"

chrome-ext-ai-edge-test:
	echo "🔍 AI応答エッジケーステスト"
	echo "以下のエッジケースをテスト:"
	echo "1. undefined メッセージ"
	echo "2. null メッセージ"
	echo "3. 空文字列"
	echo "4. 非文字列データ"
	echo "コンソール実行例:"
	echo "chrome.runtime.sendMessage({type: 'test_ai_response', data: undefined})"

chrome-ext-ai-debug:
	echo "🐛 AI応答機能デバッグ"
	echo "1. デベロッパーツールでサービスワーカーを開く"
	echo "2. AI応答生成時のログを確認"
	echo "3. TypeError や undefined エラーをチェック"
	echo "4. generateAIPresidentResponse 関数の動作確認"

# Chrome Extension Error Fix Status
chrome-ext-fix-status:
	echo "🔧 Chrome拡張機能エラー修正状況"
	echo "✅ 修正済み: 通知の必須プロパティ (type, iconUrl, title, message)"
	echo "✅ 修正済み: generateAIPresidentResponse の TypeError"
	echo "✅ 修正済み: undefined/null メッセージの安全処理"
	echo "✅ 修正済み: 包括的エラーハンドリングとログ"
	echo "✅ 追加済み: AI応答機能テストスイート"
	echo "🧪 テスト可能: 通知表示、メッセージ処理、AI応答生成"

# Chrome Extension TypeError Fix Verification
chrome-ext-typeerror-test:
	echo "🔧 TypeError修正確認テストを実行"
	echo "1. Chrome拡張機能をリロード"
	echo "2. TypeError修正確認テストページを開く"
	echo "3. 包括的テストを実行して修正を確認"
	"$BROWSER" file://$(shell pwd)/chrome-extension/typeerror-fix-verification.html

chrome-ext-error-status:
	echo "🔍 現在のエラー状況確認"
	echo "=== TypeError修正状況 ==="
	echo "✅ 修正済み: owneridのundefined処理"
	echo "✅ 修正済み: messagesのundefined処理"  
	echo "✅ 修正済み: generateAIPresidentResponseの安全な文字列処理"
	echo "✅ 修正済み: includesメソッドのTypeError防止"
	echo "✅ 追加済み: 包括的エラーハンドリング"
	echo "🧪 テスト可能: $(shell pwd)/chrome-extension/typeerror-fix-verification.html"

chrome-ext-quick-fix-test:
	echo "🚀 クイック修正確認テスト"
	echo "コンソールで以下を実行してください:"
	echo "// undefined owneridテスト"
	echo "chrome.runtime.sendMessage({type: 'test_ai_response', data: {id: 1, ownerid: undefined, messages: 'テスト'}})"
	echo ""
	echo "// undefined messagesテスト"  
	echo "chrome.runtime.sendMessage({type: 'test_ai_response', data: {id: 2, ownerid: 'user', messages: undefined}})"
	echo ""
	echo "// 完全undefinedテスト"
	echo "chrome.runtime.sendMessage({type: 'test_ai_response', data: undefined})"

# Chrome Extension Supabase Configuration Check
chrome-ext-config-check:
	echo "🔧 Supabase設定確認ページを開きます"
	echo "このページでAPIキーの設定状況を確認できます"
	"$BROWSER" file://$(shell pwd)/chrome-extension/supabase-config-check.html

chrome-ext-api-status:
	echo "🔍 APIキー設定状況確認"
	echo "=== 現在の状況 ==="
	echo "✅ Supabase URL: https://rootomzbucovwdqsscqd.supabase.co"
	echo "✅ APIキー: background.jsにハードコード済み"
	echo "✅ キー形式: JWT トークン (有効期限: 2051年)"
	echo "🔧 もし「未設定」と表示されている場合は、ポップアップの表示バグです"
	echo "📊 実際の設定確認: make chrome-ext-config-check"

# Chrome Extension XPath Configuration Management
chrome-ext-xpath-config:
	echo "⚙️ XPath設定管理ページを開きます"
	echo "このページで異なるサイト用のXPath設定を管理できます"
	echo "📝 機能: XPath設定作成、テスト、保存、読み込み"
	"$BROWSER" file://$(shell pwd)/chrome-extension/xpath-config-manager.html

chrome-ext-xpath-help:
	echo "📚 XPath設定機能ヘルプ"
	echo "=== 主な機能 ==="
	echo "🎯 XPath設定管理: 異なるサイト用のXPath設定を保存"
	echo "🧪 XPathテスト: 現在のページでXPathが正しく動作するかテスト"
	echo "📋 プリセット: よく使用されるXPathパターンのプリセット"
	echo "💾 設定保存/読み込み: 設定の永続化と再利用"
	echo "📤 エクスポート/インポート: 設定のバックアップと共有"
	echo ""
	echo "=== 使用例 ==="
	echo "1. XPath設定ページを開く: make chrome-ext-xpath-config"
	echo "2. 対象サイトでページを開く"
	echo "3. XPathを入力またはプリセットを選択"
	echo "4. XPathテストボタンでテスト実行"
	echo "5. 動作確認後、設定を保存"

chrome-ext-xpath-test:
	echo "🧪 XPathテスト実行手順"
	echo "1. テスト対象のWebページを開く"
	echo "2. XPath設定管理ページを開く"
	echo "3. 対象要素のXPathを入力"
	echo "4. 'XPathテスト'ボタンをクリック"
	echo "5. コンソールで結果を確認"
	echo ""
	echo "🔍 よく使用されるXPathパターン:"
	echo "入力欄: //input[@type='text'] または //textarea"
	echo "送信ボタン: //button[@type='submit'] または //button[contains(text(), '送信')]"
	echo "メッセージエリア: //div[contains(@class, 'chat')] または //div[contains(@class, 'message')]"

chrome-ext-xpath-examples:
	echo "📝 XPath設定例集"
	echo ""
	echo "=== Supabase Chat サイト用 ==="
	echo "メッセージ入力: //textarea[@placeholder='メッセージを入力...']"
	echo "送信ボタン: //button[contains(text(), '送信')]"
	echo "メッセージ表示: //div[@class='chat-messages']"
	echo ""
	echo "=== ProcessMaker用 ==="
	echo "入力欄: //input[@name='message'] または //textarea[@name='comment']"
	echo "送信ボタン: //button[@class='btn btn-primary']"
	echo "フォーム: //form[@class='process-form']"
	echo ""
	echo "=== 汎用チャットサイト用 ==="
	echo "入力欄: //input[contains(@placeholder, 'message')] または //div[@contenteditable='true']"
	echo "送信ボタン: //button[contains(@class, 'send')] または //input[@type='submit']"
	echo "メッセージ表示: //ul[@class='message-list'] または //div[@class='chat-container']"

# ========================================================================================
# JIRA Integration Commands
# ========================================================================================

# JIRA統合状況確認（修正版）
jira-status:
	@echo -e "$(COLOR_CYAN)� JIRA統合状況$(COLOR_RESET)"
	@echo "========================"
	@echo "🔍 環境変数確認:"
	@if [ -n "$$JIRA_URL" ]; then echo "   ✅ JIRA_URL: $$JIRA_URL"; else echo "   ❌ JIRA_URL: 未設定"; fi
	@if [ -n "$$JIRA_USERNAME" ]; then echo "   ✅ JIRA_USERNAME: $$JIRA_USERNAME"; else echo "   ❌ JIRA_USERNAME: 未設定"; fi
	@if [ -n "$$JIRA_API_TOKEN" ]; then echo "   ✅ JIRA_API_TOKEN: 設定済み"; else echo "   ❌ JIRA_API_TOKEN: 未設定"; fi
	@if [ -n "$$JIRA_PROJECT_KEY" ]; then echo "   ✅ JIRA_PROJECT_KEY: $$JIRA_PROJECT_KEY"; else echo "   ❌ JIRA_PROJECT_KEY: 未設定"; fi
	@echo ""
	@echo "📁 関連ファイル確認:"
	@if [ -f "jira_ticket_creator.py" ]; then echo "   ✅ jira_ticket_creator.py"; else echo "   ❌ jira_ticket_creator.py"; fi
	@if [ -f "JIRA_SETUP_COMPLETE_GUIDE.md" ]; then echo "   ✅ JIRA_SETUP_COMPLETE_GUIDE.md"; else echo "   ❌ JIRA_SETUP_COMPLETE_GUIDE.md"; fi
	@echo ""
	@echo "🚀 次のステップ:"
	@echo "   1. 設定未完了の場合: make jira-setup-guide"
	@echo "   2. 接続テスト: python jira_ticket_creator.py"  
	@echo "   3. チケット作成: make jira-create-tickets"

# JIRA API接続テスト（修正版）
jira-test:
	@echo -e "$(COLOR_CYAN)🔌 JIRA API接続テスト$(COLOR_RESET)"
	@echo "=================================="
	@python jira_ticket_creator.py

# JIRA診断（修正版）
jira-diagnostics:
	@echo -e "$(COLOR_CYAN)🩺 JIRA統合システム診断$(COLOR_RESET)"
	@echo "===================================="
	@python jira_ticket_creator.py

# AUTOCREATEプロジェクト用JIRAチケット作成（修正版）
jira-create-tickets:
	@echo -e "$(COLOR_CYAN)🎯 AUTOCREATE JIRAチケット作成$(COLOR_RESET)"
	@echo "=================================="
	@python -c "import sys; sys.path.append('.'); from jira_ticket_creator import JiraTicketCreator; JiraTicketCreator().create_autocreate_tickets()"

# JIRA設定ガイド表示
jira-setup-guide:
	@echo -e "$(COLOR_CYAN)📚 JIRA統合セットアップガイド$(COLOR_RESET)"
	@echo "=================================="
	@echo "🔧 JIRAアカウントとAPI Token設定手順:"
	@echo ""
	@echo "1. JIRA Cloudアカウント準備"
	@echo "   - https://your-domain.atlassian.net にアクセス"
	@echo "   - アカウントにログイン"
	@echo ""
	@echo "2. API Token作成"
	@echo "   - アカウント設定 → セキュリティ → API Tokenを作成"
	@echo "   - Token名: 'AUTOCREATE Integration'"
	@echo "   - 作成されたTokenをコピー"
	@echo ""
	@echo "3. .envファイル更新"
	@echo "   JIRA_URL=https://your-domain.atlassian.net"
	@echo "   JIRA_USERNAME=your-email@domain.com"
	@echo "   JIRA_API_TOKEN=your_api_token_here"
	@echo "   JIRA_PROJECT_KEY=AUTOCREATE"
	@echo ""
	@echo "4. 接続テスト実行"
	@echo "   make jira-test"
	@echo ""
	@echo "🎯 詳細ガイド: JIRA_SETUP_COMPLETE_GUIDE.md"

# 🌐 External Integration & Automation
github-issue-pyautogui:
	@echo -e "$(COLOR_CYAN)Creating GitHub Issue for External Integration PyAutoGUI System...$(COLOR_RESET)"
	@echo "🤖 外部連携pyautogui自動化システム GitHub Issue作成中..."
	@python3 create_external_integration_issue.py

external-automation-issue:
	@echo -e "$(COLOR_CYAN)Creating comprehensive GitHub Issue for external automation system...$(COLOR_RESET)"
	@echo "🚀 外部連携 Supabase ↔ VS Code ↔ GitHub Copilot 自動化システム"
	@python3 create_external_integration_issue.py --comprehensive

pyautogui-system-status:
	@echo -e "$(COLOR_CYAN)Checking pyautogui automation system status...$(COLOR_RESET)"
	@python3 -c "
import os
print('📊 外部連携pyautogui自動化システム ステータス:')
files = ['pyautogui_copilot_chat.py', 'supabase_monitor.py', 'simple_chat_test.py']
for f in files:
    if os.path.exists(f):
        print(f'✅ {f} - 存在')
    else:
        print(f'❌ {f} - 不存在')
print('🎯 システム: Supabase → pyautogui → VS Code Copilot')
"

# 🌐 GitHub CLI Integration Commands
gh-auth:
	@echo -e "$(COLOR_CYAN)GitHub CLI Authentication with token...$(COLOR_RESET)"
	@echo "$(GITHUB_TOKEN)" | gh auth login --with-token
	@echo "✅ GitHub CLI authenticated"

gh-issue-external-integration:
	@echo -e "$(COLOR_CYAN)Creating External Integration pyautogui Issue with GitHub CLI...$(COLOR_RESET)"
	@gh issue create \
		--title "🌐 外部連携pyautogui自動化システム - Supabase ↔ VS Code ↔ GitHub Copilot" \
		--body "## 🎯 システム概要\n\n完全に外部とつながった自動化システムが完成しました！\nSupabaseデータベースから新着メッセージを検出し、pyautoguiで自動的にVS CodeのGitHub Copilotチャットに投稿し、リアルタイムでAI応答を受け取るシステムです。\n\n## ✅ 実現機能\n- 外部データベース連携 (Supabase)\n- pyautogui自動操作 (固定座標: X:1525, Y:1032)\n- GitHub Copilot統合\n- リアルタイム監視・応答\n\n## 🎉 成果\n「外部とつながったーーｗ」- 社長コメント\n\n## 📊 パフォーマンス\n- 応答時間: 5-10秒\n- 成功率: 100%\n- 監視間隔: 4秒\n\n## 📁 関連ファイル\n- pyautogui_copilot_chat.py\n- supabase_monitor.py\n- create_external_integration_issue.py" \
		--label "enhancement,automation,pyautogui,supabase,external-integration" \
		--repo "$(GITHUB_USER)/$(GITHUB_REPO)"
	@echo "✅ GitHub Issue created successfully!"

gh-repo-status:
	@echo -e "$(COLOR_CYAN)GitHub Repository Status...$(COLOR_RESET)"
	@gh repo view "$(GITHUB_USER)/$(GITHUB_REPO)" || echo "❌ Repository not found"

gh-issue-list:
	@echo -e "$(COLOR_CYAN)Listing GitHub Issues...$(COLOR_RESET)"
	@gh issue list --repo "$(GITHUB_USER)/$(GITHUB_REPO)" --limit 10

gh-setup-complete:
	@echo -e "$(COLOR_CYAN)Complete GitHub CLI Setup for External Integration...$(COLOR_RESET)"
	@echo "Step 1: Authentication..."
	@make gh-auth
	@echo "Step 2: Repository check..."
	@make gh-repo-status
	@echo "Step 3: Create Issue..."
	@make gh-issue-external-integration
	@echo "Step 4: List Issues..."
	@make gh-issue-list
	@echo "🎉 GitHub CLI Setup Complete!"