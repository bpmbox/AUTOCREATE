"""
🧪 GitHub Copilot自動化システム - pytest設定
包括的なテストスイート設定
"""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# テスト用の環境変数設定
load_dotenv('.env.test', override=False)
load_dotenv('.env', override=False)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def pytest_configure(config):
    """pytest設定"""
    # カスタムマーカーの登録
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests") 
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "github: Tests that require GitHub API")
    config.addinivalue_line("markers", "supabase: Tests that require Supabase connection")
    config.addinivalue_line("markers", "automation: Automation system tests")
    config.addinivalue_line("markers", "mermaid: Mermaid diagram generation tests")
    config.addinivalue_line("markers", "offline: Tests that can run offline")
    config.addinivalue_line("markers", "online: Tests that require internet connection")

@pytest.fixture(scope="session")
def test_env():
    """テスト環境の設定"""
    return {
        'debug_mode': True,
        'offline_mode': False,
        'test_mode': True
    }

@pytest.fixture(scope="session") 
def github_config():
    """GitHub設定（テスト用）"""
    return {
        'repo': 'bpmbox/AUTOCREATE',
        'token': os.getenv('GITHUB_TOKEN', ''),
        'test_issue_number': 64
    }

@pytest.fixture(scope="session")
def supabase_config():
    """Supabase設定（テスト用）"""
    return {
        'url': os.getenv('SUPABASE_URL', ''),
        'key': os.getenv('SUPABASE_KEY', ''),
        'table': 'chat_history'
    }

@pytest.fixture
def temp_mermaid_file(tmp_path):
    """一時的なMermaid図ファイル"""
    mermaid_file = tmp_path / "test_diagram.mermaid"
    return mermaid_file

@pytest.fixture
def sample_chat_data():
    """テスト用チャットデータ"""
    return {
        'id': 'test-123',
        'user_message': 'テスト用質問',
        'user_name': 'test_user',
        'created_at': '2025-06-28T12:00:00Z',
        'channel': 'test_channel'
    }

def pytest_collection_modifyitems(config, items):
    """テスト実行順序の調整"""
    # オフラインテストを最初に実行
    offline_items = []
    online_items = []
    
    for item in items:
        if item.get_closest_marker("offline"):
            offline_items.append(item)
        else:
            online_items.append(item)
    
    items[:] = offline_items + online_items
