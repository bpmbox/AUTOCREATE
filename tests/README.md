# 🧪 GitHub Copilot自動化システム - テストスイート

## 📋 概要
包括的なpytestテストスイートで、GitHub Copilot自動化システムの品質を保証します。

## 🏗️ テスト構造
```
tests/
├── unit/               # ユニットテスト
├── integration/        # 統合テスト
├── e2e/               # エンドツーエンドテスト
├── fixtures.py        # カスタムフィクスチャ
└── conftest.py        # pytest設定
```

## 🚀 テスト実行方法

### 📦 基本実行
```bash
# 全テスト実行
pytest

# 詳細出力
pytest -v

# 特定ディレクトリのみ
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

### 🏷️ マーカー別実行
```bash
# オフラインテストのみ
pytest -m offline

# オンラインテスト（要ネット接続）
pytest -m online

# 高速テストのみ
pytest -m "not slow"

# GitHub API関連
pytest -m github

# Supabase関連
pytest -m supabase

# Mermaid図生成
pytest -m mermaid

# 自動化システム
pytest -m automation
```

### ⚡ パフォーマンステスト
```bash
# スローテストも含む完全実行
pytest -m "slow"

# パフォーマンス重視
pytest -m "not slow" --tb=line
```

## 🔧 環境設定

### 📄 .env.test ファイル（オプション）
```bash
# テスト専用環境変数
DEBUG_MODE=True
TEST_MODE=True
OFFLINE_MODE=False
FAST_TEST_MODE=False

# GitHub設定（実際のテスト用）
GITHUB_TOKEN=your_test_token
GITHUB_REPO=your_test_repo

# Supabase設定（実際のテスト用）
SUPABASE_URL=your_test_url
SUPABASE_KEY=your_test_key
```

### 🌐 オンライン・オフラインモード
```bash
# オフラインモード（外部API不要）
export OFFLINE_MODE=True
pytest -m offline

# オンラインモード（外部API使用）
export OFFLINE_MODE=False
pytest -m online
```

## 📊 テストカバレッジ

### 🎯 ユニットテスト
- ✅ Mermaid図生成
- ✅ ファイル名サニタイズ
- ✅ プロンプト生成
- ✅ プロジェクト名生成
- ✅ エラーハンドリング

### 🔗 統合テスト
- ✅ Supabase接続
- ✅ GitHub API連携
- ✅ ファイルシステム操作
- ✅ ワークフロー統合

### 🌍 E2Eテスト
- ✅ 完全自動化フロー
- ✅ リアルタイム処理
- ✅ 複数プロジェクト処理
- ✅ エラー回復

## ⚙️ CI/CD統合

### GitHub Actions例
```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -m "offline" --cov=tests
      - run: pytest -m "online" --cov=tests
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
```

## 🔍 デバッグ・トラブルシューティング

### ログ確認
```bash
# 詳細ログ出力
pytest -v -s --log-cli-level=DEBUG

# 失敗テストのみ再実行
pytest --lf

# 特定テスト実行
pytest tests/unit/test_automation_core.py::TestGitHubCopilotAutomation::test_mermaid_diagram_generation
```

### 一般的な問題
1. **Supabase接続エラー**: `.env`ファイルの設定確認
2. **GitHub API制限**: トークン・権限確認
3. **ファイル権限**: 実行権限・ディスク容量確認
4. **パフォーマンス**: システムリソース確認

## 📈 品質メトリクス

### カバレッジ目標
- ユニットテスト: 90%以上
- 統合テスト: 80%以上
- E2Eテスト: 主要フロー100%

### パフォーマンス目標
- Mermaid図生成: 2秒以内
- プロンプト生成: 1秒以内
- 完全フロー: 10秒以内

## 🛠️ カスタマイズ

### 新しいテスト追加
1. 適切なディレクトリ（unit/integration/e2e）に配置
2. 適切なマーカーを設定
3. フィクスチャを活用
4. ドキュメント更新

### フィクスチャ拡張
`tests/fixtures.py`でカスタムフィクスチャを追加可能

### マーカー追加
`conftest.py`でカスタムマーカーを登録可能

## 📞 サポート

問題が発生した場合は、詳細なログと環境情報を含めてIssueを作成してください。
