"""
🧪 Custom Pytest Fixtures and Utilities
自動化システム用のカスタムフィクスチャとユーティリティ
"""

import pytest
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

@pytest.fixture(scope="session")
def test_data_dir():
    """テストデータディレクトリ"""
    return Path(__file__).parent / "test_data"

@pytest.fixture
def sample_chat_messages():
    """サンプルチャットメッセージコレクション"""
    return [
        {
            'id': 'msg-001',
            'user_message': 'Reactでダッシュボードを作成したい',
            'user_name': 'frontend_dev',
            'created_at': '2025-06-28T10:00:00Z',
            'channel': 'development'
        },
        {
            'id': 'msg-002', 
            'user_message': 'Python APIサーバーの実装',
            'user_name': 'backend_dev',
            'created_at': '2025-06-28T11:00:00Z',
            'channel': 'backend'
        },
        {
            'id': 'msg-003',
            'user_message': 'データベース設計の相談',
            'user_name': 'db_admin',
            'created_at': '2025-06-28T12:00:00Z',
            'channel': 'database'
        }
    ]

@pytest.fixture
def mock_supabase_client():
    """モックSupabaseクライアント"""
    mock_client = Mock()
    mock_table = Mock()
    
    # サンプルデータ
    sample_data = {
        'data': [
            {
                'id': 'test-123',
                'user_message': 'モックテスト用メッセージ',
                'user_name': 'mock_user',
                'created_at': '2025-06-28T12:00:00Z'
            }
        ]
    }
    
    mock_table.select.return_value.order.return_value.limit.return_value.execute.return_value = sample_data
    mock_client.table.return_value = mock_table
    
    return mock_client

@pytest.fixture
def mock_github_cli():
    """モックGitHub CLIコマンド"""
    def mock_subprocess_run(*args, **kwargs):
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Test output"
        mock_result.stderr = ""
        return mock_result
    
    with patch('subprocess.run', side_effect=mock_subprocess_run):
        yield mock_subprocess_run

@pytest.fixture
def clean_environment():
    """クリーンなテスト環境"""
    # 環境変数のバックアップ
    original_env = os.environ.copy()
    
    # テスト用環境変数設定
    test_env = {
        'DEBUG_MODE': 'True',
        'TEST_MODE': 'True',
        'OFFLINE_MODE': 'True'
    }
    
    for key, value in test_env.items():
        os.environ[key] = value
    
    yield test_env
    
    # 環境変数の復元
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def temp_workspace(tmp_path):
    """一時的なワークスペース"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    
    # 基本的なプロジェクト構造を作成
    (workspace / "src").mkdir()
    (workspace / "tests").mkdir()
    (workspace / "docs").mkdir()
    
    # テスト用ファイル作成
    (workspace / "README.md").write_text("# Test Project")
    (workspace / "package.json").write_text('{"name": "test-project"}')
    
    original_cwd = os.getcwd()
    os.chdir(workspace)
    
    yield workspace
    
    os.chdir(original_cwd)

@pytest.fixture
def mermaid_validator():
    """Mermaid図の検証ユーティリティ"""
    def validate_mermaid_syntax(content):
        """基本的なMermaid構文チェック"""
        checks = {
            'has_graph_declaration': content.strip().startswith('graph TB'),
            'has_arrows': '-->' in content,
            'has_nodes': '[' in content and ']' in content,
            'has_start_node': 'START[' in content,
            'has_end_node': 'END[' in content,
            'proper_line_breaks': '\n' in content,
            'no_syntax_errors': not any(error in content for error in ['<error>', 'undefined'])
        }
        return checks
    
    def validate_mermaid_content(content, expected_keywords):
        """Mermaid図の内容検証"""
        content_checks = {
            'contains_keywords': all(keyword in content for keyword in expected_keywords),
            'appropriate_length': 100 < len(content) < 5000,
            'japanese_support': any(ord(char) > 127 for char in content) if any(ord(char) > 127 for char in ''.join(expected_keywords)) else True
        }
        return content_checks
    
    return {
        'validate_syntax': validate_mermaid_syntax,
        'validate_content': validate_mermaid_content
    }

@pytest.fixture
def performance_monitor():
    """パフォーマンス監視ユーティリティ"""
    import time
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.measurements = {}
        
        def start(self):
            self.start_time = time.time()
        
        def measure(self, operation_name):
            if self.start_time is None:
                raise ValueError("start()を最初に呼び出してください")
            
            elapsed = time.time() - self.start_time
            self.measurements[operation_name] = elapsed
            return elapsed
        
        def get_measurements(self):
            return self.measurements.copy()
        
        def assert_performance(self, operation_name, max_seconds):
            if operation_name not in self.measurements:
                raise ValueError(f"測定されていない操作: {operation_name}")
            
            actual_time = self.measurements[operation_name]
            assert actual_time <= max_seconds, f"{operation_name}の実行時間が制限を超過: {actual_time:.2f}s > {max_seconds}s"
    
    return PerformanceMonitor()

@pytest.fixture
def github_issue_mock():
    """GitHub Issue操作のモック"""
    class GitHubIssueMock:
        def __init__(self):
            self.issues = []
            self.next_id = 1
        
        def create_issue(self, title, body, labels=None):
            issue = {
                'id': self.next_id,
                'title': title,
                'body': body,
                'labels': labels or [],
                'state': 'open',
                'created_at': '2025-06-28T12:00:00Z'
            }
            self.issues.append(issue)
            self.next_id += 1
            return issue
        
        def get_issue(self, issue_id):
            for issue in self.issues:
                if issue['id'] == issue_id:
                    return issue
            return None
        
        def list_issues(self, state='open'):
            return [issue for issue in self.issues if issue['state'] == state]
        
        def close_issue(self, issue_id, comment=None):
            issue = self.get_issue(issue_id)
            if issue:
                issue['state'] = 'closed'
                if comment:
                    issue['close_comment'] = comment
                return True
            return False
    
    return GitHubIssueMock()

@pytest.fixture(autouse=True)
def test_logging(caplog):
    """テスト用ログ設定"""
    import logging
    caplog.set_level(logging.DEBUG)
    yield caplog

# マーカー用のスキップフィクスチャ
@pytest.fixture(autouse=True)
def skip_online_tests_if_offline(request):
    """オフライン環境でオンラインテストをスキップ"""
    if request.node.get_closest_marker("online"):
        if os.getenv('OFFLINE_MODE', 'False').lower() == 'true':
            pytest.skip("オフラインモードのためオンラインテストをスキップ")

@pytest.fixture(autouse=True) 
def skip_slow_tests_if_fast_mode(request):
    """高速モードでスローテストをスキップ"""
    if request.node.get_closest_marker("slow"):
        if os.getenv('FAST_TEST_MODE', 'False').lower() == 'true':
            pytest.skip("高速テストモードのためスローテストをスキップ")

# エラー回復テスト用フィクスチャ
@pytest.fixture
def error_simulation():
    """エラーシミュレーション用ユーティリティ"""
    class ErrorSimulator:
        @staticmethod
        def network_error():
            """ネットワークエラーをシミュレート"""
            from requests.exceptions import ConnectionError
            raise ConnectionError("模擬ネットワークエラー")
        
        @staticmethod
        def file_permission_error():
            """ファイル権限エラーをシミュレート"""
            raise PermissionError("模擬ファイル権限エラー")
        
        @staticmethod
        def api_rate_limit_error():
            """API制限エラーをシミュレート"""
            class MockResponse:
                status_code = 429
                text = "Rate limit exceeded"
            
            from requests.exceptions import HTTPError
            error = HTTPError("429 Client Error: Too Many Requests")
            error.response = MockResponse()
            raise error
    
    return ErrorSimulator()
