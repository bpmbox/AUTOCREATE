#!/usr/bin/env python3
"""
Local Memory Data Import
ローカル環境での記憶データ投入（モック使用）
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# モック適用
def apply_supabase_mock():
    """Supabaseクライアントをモックに置き換え"""
    import memory_automation_system
    
    class MockSupabaseClient:
        def __init__(self):
            self.mock_data = []
            self.next_id = 1
        
        def table(self, table_name):
            return MockTable(self)
        
        def rpc(self, function_name, params=None):
            return MockResult(True)
    
    class MockTable:
        def __init__(self, client):
            self.client = client
        
        def insert(self, data):
            data['id'] = self.client.next_id
            self.client.next_id += 1
            self.client.mock_data.append(data)
            return MockResult(data)
        
        def select(self, columns='*'):
            return self
        
        def execute(self):
            return MockResult(self.client.mock_data.copy())
    
    class MockResult:
        def __init__(self, data):
            self.data = data if isinstance(data, list) else [data] if data else []
    
    def mock_create_client(url, key):
        return MockSupabaseClient()
    
    memory_automation_system.create_client = mock_create_client

# 元のスクリプトから関数をインポート
apply_supabase_mock()

from memory_automation_system import MemoryAutomationSystem, Memory

def create_project_memories():
    """プロジェクト記憶を作成"""
    memories = []
    
    # 重要な会話・作業履歴
    conversation_data = [
        {
            "content": """AI×人間協働開発プロジェクト開始
            
このプロジェクトでは以下を実現：
1. SupabaseチャットとGradio・Pythonシステムの連携
2. AI社長（GitHub Copilot）によるSupabaseチャットの自動監視・応答
3. Laravel風のGradioコントローラ自動統合
4. プロンプト管理・自動システム生成（Lavelo AI）
5. AI記憶管理・Supabase統合自動化システム

記憶自動化システム（memory_automation_system.py）を実装し、
AI/人間の記憶・作業履歴を永続化、自動化システムのissue化・着手完了。""",
            "type": "project",
            "importance": 95,
            "tags": ["project-start", "ai-collaboration", "supabase", "gradio", "automation", "memory-system"]
        },
        {
            "content": """Supabase-message-stream（React+Vite）チャットUIの成功
            
- チャットUIの起動・動作確認完了
- リアルタイムメッセージング機能動作
- Supabase chat_historyテーブルとの連携確認
- UIからの質問送信→AI応答の流れを確立
- AI社長自動応答システムとの統合完了""",
            "type": "chat",
            "importance": 90,
            "tags": ["supabase", "react", "vite", "chat-ui", "realtime", "ai-responder"]
        },
        {
            "content": """記憶自動化システムの実装完了

ファイル構成：
- memory_automation_system.py: メインシステム
- app/Http/Controllers/Gradio/gra_04_memory/memory_manager.py: Gradio統合
- test_memory_local.py: テストスイート
- import_memory_local.py: データ投入スクリプト

機能：
- リアルタイム記憶保存・復元・検索・バックアップ
- AI知的検索・推薦システム
- Gradioインターフェース統合
- 自動分類・タグ付けシステム""",
            "type": "code",
            "importance": 92,
            "tags": ["memory-automation", "implementation", "gradio", "ai-search", "backup"]
        },
        {
            "content": """GitHub Issue管理システムの構築

作成したIssue：
- GITHUB_ISSUE_13_PROMPT_MANAGEMENT_SYSTEM.md
- GITHUB_ISSUE_14_MEMORY_AUTOMATION_SYSTEM.md  
- GITHUB_ISSUE_15_MEMORY_AUTOMATION_SYSTEM_IMPLEMENTATION.md

進行状況・設計・実装状況を詳細に記録し、
AI×人間協働開発のための体系的なプロジェクト管理を確立。""",
            "type": "documentation",
            "importance": 85,
            "tags": ["github", "issues", "documentation", "project-management", "ai-collaboration"]
        },
        {
            "content": """Lavelo AI（プロンプト管理＆自動システム生成）の統合

- app/Http/Controllers/Gradio/gra_03_programfromdocs/lavelo.py実装
- Gradioタブとしての統合完了
- プロンプト管理機能の実装
- 自動システム生成機能の基盤構築
- Laravel風コントローラー自動統合構造の完成""",
            "type": "code",
            "importance": 85,
            "tags": ["lavelo-ai", "prompt-management", "automation", "gradio-tab", "laravel"]
        }
    ]
    
    for data in conversation_data:
        memory = Memory(
            content=data["content"],
            memory_type=data["type"],
            importance_score=data["importance"],
            tags=data["tags"],
            metadata={
                "source": "project_import",
                "import_date": datetime.now().isoformat(),
                "category": "project_history"
            }
        )
        memories.append(memory)
    
    return memories

def create_code_memories():
    """重要なコードファイルから記憶を作成"""
    memories = []
    
    important_files = [
        ("memory_automation_system.py", 95, ["core-system", "memory", "automation"]),
        ("app.py", 90, ["main-app", "fastapi", "gradio"]),
        ("test_memory_local.py", 85, ["testing", "validation", "quality-assurance"]),
        ("import_memory_local.py", 80, ["data-import", "automation", "setup"])
    ]
    
    for file_name, importance, tags in important_files:
        file_path = project_root / file_name
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 概要を抽出
                lines = content.split('\n')
                docstring = ""
                for line in lines[:20]:
                    if '"""' in line or "'''" in line:
                        docstring += line + "\n"
                
                summary_content = f"Code File: {file_name}\n\nFile Summary:\n{docstring}\n\nTotal Lines: {len(lines)}"
                
                memory = Memory(
                    content=summary_content,
                    memory_type="code",
                    importance_score=importance,
                    tags=tags + [file_path.suffix[1:]] if file_path.suffix else tags,
                    file_path=str(file_path),
                    metadata={
                        "source": "code_import",
                        "file_size": len(content),
                        "line_count": len(lines),
                        "file_type": file_path.suffix
                    }
                )
                memories.append(memory)
                
            except Exception as e:
                print(f"⚠️ Failed to process {file_name}: {e}")
    
    return memories

def create_git_memories():
    """Git履歴から記憶を作成"""
    memories = []
    
    try:
        # 最近のコミット履歴を取得
        cmd = 'git log --oneline -10'
        result = subprocess.run(
            cmd, shell=True, cwd=project_root,
            capture_output=True, text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            commits = result.stdout.strip().split('\n')
            
            for commit in commits:
                if commit:
                    memory = Memory(
                        content=f"Git Commit: {commit}",
                        memory_type="git",
                        importance_score=70,
                        tags=["git", "commit", "development"],
                        metadata={
                            "source": "git_import",
                            "commit_summary": commit
                        }
                    )
                    memories.append(memory)
    
    except Exception as e:
        print(f"⚠️ Git history import failed: {e}")
    
    return memories

def main():
    """メイン処理"""
    print("🚀 Starting Local Memory Data Import")
    print("=" * 60)
    
    # 記憶システム初期化
    system = MemoryAutomationSystem()
    print("✅ Memory system initialized (mock mode)")
    
    # 各カテゴリの記憶を収集
    all_memories = []
    
    print("📝 Creating project memories...")
    project_memories = create_project_memories()
    all_memories.extend(project_memories)
    print(f"✅ Created {len(project_memories)} project memories")
    
    print("💻 Creating code memories...")
    code_memories = create_code_memories()
    all_memories.extend(code_memories)
    print(f"✅ Created {len(code_memories)} code memories")
    
    print("📝 Creating git memories...")
    git_memories = create_git_memories()
    all_memories.extend(git_memories)
    print(f"✅ Created {len(git_memories)} git memories")
    
    print(f"\n📊 Total memories to process: {len(all_memories)}")
    
    # 記憶を処理・保存
    successful_imports = 0
    failed_imports = 0
    
    for i, memory in enumerate(all_memories):
        try:
            # 記憶を処理
            processed_memory = system.processor.process_memory(memory)
            
            # 関連記憶を検索
            existing_memories = [m for m in all_memories[:i] if hasattr(m, 'id')]
            if existing_memories:
                processed_memory.related_memories = system.processor.find_related_memories(
                    processed_memory, existing_memories[-10:]
                )
            
            # 保存（モック環境）
            success = system.storage.save_memory(processed_memory)
            
            if success:
                successful_imports += 1
                print(f"   ✅ Processed: {processed_memory.memory_type} - {processed_memory.content[:50]}...")
            else:
                failed_imports += 1
                print(f"   ❌ Failed: {memory.memory_type}")
        
        except Exception as e:
            failed_imports += 1
            print(f"   ❌ Error processing {memory.memory_type}: {e}")
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print(f"📊 Import Results:")
    print(f"   ✅ Successful: {successful_imports}")
    print(f"   ❌ Failed: {failed_imports}")
    print(f"   📊 Success Rate: {successful_imports/(successful_imports+failed_imports)*100:.1f}%")
    
    # 記憶をJSONファイルにバックアップ
    backup_file = f"memory_backup_local_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'total_memories': len(all_memories),
            'successful_imports': successful_imports,
            'memories': [memory.to_dict() for memory in all_memories]
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Backup created: {backup_file}")
        print(f"📊 Backup contains {len(all_memories)} memories")
    
    except Exception as e:
        print(f"⚠️ Backup failed: {e}")
    
    print("\n🎉 Local Memory Import Process Completed!")
    print("📝 Note: This was a local simulation with mock Supabase")
    print("🔧 For production, configure SUPABASE_URL and SUPABASE_KEY")
    
    return successful_imports > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
