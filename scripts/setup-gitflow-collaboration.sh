#!/bin/bash

# 🏢 GitFlow協働開発システム - セットアップスクリプト

echo "🏢 人間・AI協働開発会社 - GitFlowシステム初期化"
echo "=================================================="

# 現在のディレクトリ確認
if [ ! -f "app.py" ] && [ ! -f "mysite/asgi.py" ]; then
    echo "❌ エラー: AUTOCREATEプロジェクトのルートディレクトリで実行してください"
    exit 1
fi

echo "📍 プロジェクトルート確認: $(pwd)"

# Git設定確認
if [ ! -d ".git" ]; then
    echo "🔧 Git初期化..."
    git init
    git add .
    git commit -m "🎉 Initial commit: AI-Human Collaboration Project"
fi

# GitFlow初期化
echo "🌿 GitFlow初期化..."
if ! command -v git-flow &> /dev/null; then
    echo "📦 git-flowをインストール中..."
    # Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y git-flow
    # macOS
    elif command -v brew &> /dev/null; then
        brew install git-flow
    else
        echo "⚠️ 手動でgit-flowをインストールしてください: https://github.com/nvie/gitflow/wiki/Installation"
        exit 1
    fi
fi

# GitFlow設定
echo "⚙️ GitFlow設定中..."
git flow init -d  # デフォルト設定で初期化

# ブランチ保護ルール（ローカル設定）
echo "🛡️ ブランチ保護設定..."
git config branch.main.description "🚀 本番環境 - 安定したリリース版"
git config branch.develop.description "🔧 開発統合環境 - 機能統合・テスト"

# Git設定（協働開発用）
echo "🤝 協働開発用Git設定..."
git config merge.tool vimdiff
git config core.editor "code --wait"  # VSCode as default editor
git config pull.rebase true
git config branch.autosetupmerge always
git config branch.autosetuprebase always

# GitHubテンプレート確認
echo "📋 GitHubテンプレート確認..."
if [ -d ".github/ISSUE_TEMPLATE" ] && [ -f ".github/pull_request_template.md" ]; then
    echo "✅ Issue・PRテンプレート設置済み"
else
    echo "⚠️ GitHubテンプレートが見つかりません"
fi

# Git hooks設定
echo "🪝 Git hooks設定..."
mkdir -p .git/hooks

# Pre-commit hook（コード品質チェック）
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "🔍 Pre-commit: コード品質チェック実行中..."

# Python構文チェック
python -m py_compile app.py mysite/asgi.py routes/api.py 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Python構文エラーが検出されました"
    exit 1
fi

# 基本的なテスト実行（存在する場合）
if [ -f "tests/test_basic.py" ]; then
    python -m pytest tests/test_basic.py -q
    if [ $? -ne 0 ]; then
        echo "❌ 基本テストが失敗しました"
        exit 1
    fi
fi

echo "✅ Pre-commit チェック完了"
EOF

chmod +x .git/hooks/pre-commit

# Commit-msg hook（コミットメッセージ形式チェック）
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
commit_regex='^(feat|fix|docs|style|refactor|test|chore|ai-collab)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ コミットメッセージが規約に合いません"
    echo "📋 形式: type(scope): description"
    echo "📋 例: feat(chat): AIチャット機能を追加"
    echo "📋 types: feat, fix, docs, style, refactor, test, chore, ai-collab"
    exit 1
fi
EOF

chmod +x .git/hooks/commit-msg

# 協働開発用エイリアス設定
echo "🔗 Git協働開発エイリアス設定..."
git config alias.co checkout
git config alias.br branch
git config alias.ci commit
git config alias.st status
git config alias.unstage 'reset HEAD --'
git config alias.last 'log -1 HEAD'
git config alias.visual '!gitk'

# GitFlow協働用エイリアス
git config alias.feature-start '!git flow feature start'
git config alias.feature-finish '!git flow feature finish'
git config alias.release-start '!git flow release start'
git config alias.release-finish '!git flow release finish'

# 協働開発専用エイリアス
git config alias.ai-commit '!f() { git commit -m "ai-collab: $1"; }; f'
git config alias.human-commit '!f() { git commit -m "feat: $1"; }; f'
git config alias.collab-merge '!f() { git merge --no-ff -m "Merge: Human-AI collaboration - $1"; }; f'

# Make targets追加
echo "🛠️ Makefileに協働開発ターゲット追加..."
if ! grep -q "gitflow-setup" Makefile; then
    cat >> Makefile << 'EOF'

# GitFlow協働開発コマンド
.PHONY: gitflow-setup feature-start feature-finish collab-commit collab-status

gitflow-setup:
	@echo -e "$(COLOR_CYAN)GitFlow協働開発システム初期化...$(COLOR_RESET)"
	@./scripts/setup-gitflow-collaboration.sh

feature-start:
	@echo -e "$(COLOR_CYAN)新機能開発開始: $(name)$(COLOR_RESET)"
	@git flow feature start $(name)
	@echo -e "$(COLOR_GREEN)Feature branch 'feature/$(name)' 作成完了$(COLOR_RESET)"

feature-finish:
	@echo -e "$(COLOR_CYAN)機能開発完了: $(name)$(COLOR_RESET)"
	@git flow feature finish $(name)
	@echo -e "$(COLOR_GREEN)Feature branch 'feature/$(name)' マージ完了$(COLOR_RESET)"

collab-commit:
	@echo -e "$(COLOR_CYAN)協働開発コミット実行...$(COLOR_RESET)"
	@git add .
	@git ai-commit "$(message)"

collab-status:
	@echo -e "$(COLOR_CYAN)協働開発状況確認...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)Current branch:$(COLOR_RESET) $(shell git branch --show-current)"
	@echo -e "$(COLOR_GREEN)GitFlow status:$(COLOR_RESET)"
	@git flow version
	@echo -e "$(COLOR_GREEN)Pending changes:$(COLOR_RESET)"
	@git status --short
EOF
fi

# スクリプト自体を実行可能にする
chmod +x scripts/setup-gitflow-collaboration.sh 2>/dev/null || true

# 初期ブランチの作成とコミット
echo "🌱 初期開発ブランチセットアップ..."
if ! git show-ref --verify --quiet refs/heads/develop; then
    git checkout -b develop
    git checkout main
fi

# 成功メッセージ
echo ""  
echo "🎉 GitFlow協働開発システム初期化完了！"
echo "=================================================="
echo ""
echo "🚀 使用可能な協働開発コマンド:"
echo "  📋 make feature-start name=機能名    # 新機能開発開始"
echo "  📋 make feature-finish name=機能名   # 機能開発完了・マージ"
echo "  📋 make collab-commit message=内容   # 協働開発コミット"
echo "  📋 make collab-status                # 開発状況確認"
echo ""
echo "🌿 GitFlowコマンド:"
echo "  📋 git flow feature start 機能名    # Feature branch作成"
echo "  📋 git flow feature finish 機能名   # Feature branchマージ"
echo "  📋 git flow release start バージョン # Release branch作成"
echo ""
echo "🤝 協働開発の準備完了 - あなたと私の会社、開始です！"
echo "📚 詳細: wikigit/GitFlow-Collaboration-Company.md を参照"
