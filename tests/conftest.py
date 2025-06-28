"""
テスト共通設定ファイル
"""
import pytest
import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "tests" / "Feature"))

@pytest.fixture(scope="session")
def project_root():
    """プロジェクトルートディレクトリを返す"""
    return Path(__file__).parent.parent

@pytest.fixture
def temp_dir(tmp_path):
    """一時ディレクトリを作成"""
    return tmp_path

@pytest.fixture
def github_config():
    """GitHub設定（テスト用）"""
    return {
        'token': os.getenv('GITHUB_TOKEN', 'test_token'),
        'user': os.getenv('GITHUB_USER', 'test_user'),
        'repo': os.getenv('GITHUB_REPO', 'test_repo')
    }

@pytest.fixture
def supabase_config():
    """Supabase設定（テスト用）"""
    return {
        'url': os.getenv('SUPABASE_URL', 'https://test.supabase.co'),
        'key': os.getenv('SUPABASE_KEY', 'test_key'),
        'table': 'chat_history'
    }
