#!/usr/bin/env python3
"""
Memory Data Import Script
既存の作業履歴・重要データをSupabase chat_historyテーブルに自動投入
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import re
import requests

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from memory_automation_system import MemoryAutomationSystem, Memory

def import_conversation_memories():
    """これまでの会話・作業履歴を記憶として投入"""
    print("💬 Importing conversation memories...")
    
    memories = []
    
    # 重要な会話・作業履歴
    conversation_data = [
        {
            "content": """AI×人間協働開発プロジェクト開始
            
このプロジェクトでは以下を実現する：
1. SupabaseチャットとGradio・Pythonシステムの連携
2. AI社長（GitHub Copilot）によるSupabaseチャットの自動監視・応答
3. Laravel風のGradioコントローラ自動統合
4. プロンプト管理・自動システム生成（Lavelo AI）
5. AI記憶管理・Supabase統合自動化システム""",
            "type": "project",
            "importance": 95,
            "tags": ["project-start", "ai-collaboration", "supabase", "gradio", "automation"]
        },
        {
            "content": """Supabase-message-stream（React+Vite）チャットUIの成功
            
- チャットUIの起動・動作確認完了
- リアルタイムメッセージング機能動作
- Supabase chat_historyテーブルとの連携確認
- UIからの質問送信→AI応答の流れを確立""",
            "type": "chat",
            "importance": 90,
            "tags": ["supabase", "react", "vite", "chat-ui", "realtime"]
        },
        {
            "content": """Gradioメインシステム（app.py）の統合成功
            
- 複数タブ統合による統一インターフェース
- Laravel風コントローラー構造の実装
- 自動起動防止・キュー制御の完全実装
- ポート7860での安定動作確認""",
            "type": "code",
            "importance": 88,
            "tags": ["gradio", "app.py", "laravel", "integration", "tabs"]
        },
        {
            "content": """AI社長自動応答システムの実装完了
            
実装ファイル：
- simple_ai_chat.py: 基本チャット機能
- copilot_ai_responder.py: Copilot応答システム
- copilot_monitorable_ai.py: 監視可能AI
- copilot_persistent_monitor.py: 永続監視
- agent_auto_responder.py: エージェント自動応答
- simple_continuous_chat.py: 100回連続対話サイクル""",
            "type": "git",
            "importance": 92,
            "tags": ["ai-responder", "automation", "copilot", "monitoring", "chat"]
        },
        {
            "content": """Lavelo AI（プロンプト管理＆自動システム生成）の統合
            
- app/Http/Controllers/Gradio/gra_03_programfromdocs/lavelo.py実装
- Gradioタブとしての統合完了
- プロンプト管理機能の実装
- 自動システム生成機能の基盤構築""",
            "type": "code",
            "importance": 85,
            "tags": ["lavelo-ai", "prompt-management", "automation", "gradio-tab"]
        },
        {
            "content": """Supabase ERD自動生成システムの構築
            
- supabase_schema_explorer.py実装
- PostgreSQL publicスキーマ全体のERD（Mermaid）自動生成
- データベース構造の可視化
- スキーマ情報の自動取得・分析""",
            "type": "database",
            "importance": 80,
            "tags": ["supabase", "erd", "mermaid", "schema", "visualization"]
        },
        {
            "content": """GitHub Issue作成・管理システム
            
作成したIssue：
- GITHUB_ISSUE_13_PROMPT_MANAGEMENT_SYSTEM.md
- GITHUB_ISSUE_14_MEMORY_AUTOMATION_SYSTEM.md
- GITHUB_ISSUE_15_MEMORY_AUTOMATION_SYSTEM_IMPLEMENTATION.md

進行状況・設計・実装状況を詳細に記録""",
            "type": "documentation",
            "importance": 85,
            "tags": ["github", "issues", "documentation", "project-management"]
        },
        {
            "content": """Git リポジトリ管理とリモート同期
            
- 定期的なgit add/commit/pushによるリモート保存
- 重要な成果物の確実なバックアップ
- バージョン管理による変更履歴の追跡
- チーム協働のための基盤整備""",
            "type": "git",
            "importance": 75,
            "tags": ["git", "version-control", "backup", "collaboration"]
        }
    ]
    
    for data in conversation_data:
        memory = Memory(
            content=data["content"],
            memory_type=data["type"],
            importance_score=data["importance"],
            tags=data["tags"],
            metadata={
                "source": "conversation_import",
                "import_date": datetime.now().isoformat(),
                "category": "project_history"
            }
        )
        memories.append(memory)
    
    print(f"📝 Created {len(memories)} conversation memories")
    return memories


def import_code_memories():
    """重要なコードファイルを記憶として投入"""
    print("💻 Importing code memories...")
    
    memories = []
    
    # 重要なファイルリスト
    important_files = [
        {
            "path": "app.py",
            "importance": 95,
            "tags": ["main-app", "fastapi", "gradio", "integration"]
        },
        {
            "path": "memory_automation_system.py",
            "importance": 90,
            "tags": ["memory", "automation", "core-system"]
        },
        {
            "path": "simple_ai_chat.py",
            "importance": 85,
            "tags": ["ai", "chat", "supabase", "automation"]
        },
        {
            "path": "copilot_ai_responder.py",
            "importance": 88,
            "tags": ["copilot", "ai-responder", "automation"]
        },
        {
            "path": "app/Http/Controllers/Gradio/gra_03_programfromdocs/lavelo.py",
            "importance": 85,
            "tags": ["lavelo-ai", "prompt-management", "gradio"]
        },
        {
            "path": "supabase_schema_explorer.py",
            "importance": 80,
            "tags": ["supabase", "schema", "database", "erd"]
        },
        {
            "path": "routes/web.py",
            "importance": 75,
            "tags": ["routes", "laravel", "web", "api"]
        },
        {
            "path": "requirements.txt",
            "importance": 70,
            "tags": ["dependencies", "python", "packages"]
        }
    ]
    
    for file_info in important_files:
        file_path = project_root / file_info["path"]
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # ファイルサイズが大きい場合は先頭部分のみ
                if len(content) > 5000:
                    content = content[:5000] + "\n\n... (truncated for memory efficiency)"
                
                memory = Memory(
                    content=f"Code File: {file_info['path']}\n\n{content}",
                    memory_type="code",
                    importance_score=file_info["importance"],
                    tags=file_info["tags"] + [file_path.suffix[1:]] if file_path.suffix else file_info["tags"],
                    file_path=str(file_path),
                    metadata={
                        "source": "code_import",
                        "file_size": len(content),
                        "file_type": file_path.suffix,
                        "import_date": datetime.now().isoformat()
                    }
                )
                memories.append(memory)
                print(f"✅ Imported {file_info['path']}")
                
            except Exception as e:
                print(f"❌ Failed to import {file_info['path']}: {e}")
        else:
            print(f"⚠️ File not found: {file_info['path']}")
    
    print(f"💻 Created {len(memories)} code memories")
    return memories


def import_git_memories():
    """Git履歴を記憶として投入"""
    print("📝 Importing git memories...")
    
    memories = []
    
    try:
        # 最近のコミット履歴を取得（過去1週間）
        since_time = datetime.now() - timedelta(days=7)
        since_str = since_time.strftime("%Y-%m-%d")
        
        cmd = f'git log --since="{since_str}" --pretty=format:"%H|%an|%ad|%s" --date=iso'
        result = subprocess.run(
            cmd, shell=True, cwd=project_root,
            capture_output=True, text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            commit_lines = result.stdout.strip().split('\n')
            
            for line in commit_lines[:20]:  # 最新20コミット
                if line:
                    parts = line.split('|', 3)
                    if len(parts) >= 4:
                        commit_hash, author, date_str, message = parts
                        
                        # コミットの詳細を取得
                        diff_cmd = f'git show --stat {commit_hash}'
                        diff_result = subprocess.run(
                            diff_cmd, shell=True, cwd=project_root,
                            capture_output=True, text=True
                        )
                        
                        commit_content = f"Git Commit: {message}\n\nAuthor: {author}\nHash: {commit_hash}\n\n"
                        if diff_result.returncode == 0:
                            commit_content += diff_result.stdout[:2000]  # 最初の2000文字
                        
                        # 重要度を計算
                        importance = 60
                        important_keywords = ['fix', 'add', 'implement', 'feature', 'system', 'memory', 'ai']
                        for keyword in important_keywords:
                            if keyword.lower() in message.lower():
                                importance += 5
                        
                        memory = Memory(
                            content=commit_content,
                            memory_type="git",
                            importance_score=min(importance, 95),
                            tags=["git", "commit", author.lower().replace(" ", "-")] + 
                                 [kw for kw in important_keywords if kw.lower() in message.lower()],
                            metadata={
                                "source": "git_import",
                                "commit_hash": commit_hash,
                                "author": author,
                                "commit_message": message,
                                "import_date": datetime.now().isoformat()
                            }
                        )
                        memories.append(memory)
            
            print(f"📝 Created {len(memories)} git memories")
        else:
            print("⚠️ No git history found or git not available")
    
    except Exception as e:
        print(f"❌ Git import error: {e}")
    
    return memories


def import_documentation_memories():
    """ドキュメントファイルを記憶として投入"""
    print("📚 Importing documentation memories...")
    
    memories = []
    
    # ドキュメントファイル
    doc_files = [
        "README.md",
        "AUTOCREATE_COMPANY_BUSINESS_PLAN.md",
        "PROJECT_STRATEGIC_INDEX.md",
        "GITHUB_ISSUE_GENERATION_GUIDE.md",
        "GITHUB_ISSUE_WIKI_RAG_COMPLETION.md",
        "EMERGENCY_MEMORY_FOR_MIYATAKEN999.md"
    ]
    
    for doc_file in doc_files:
        file_path = project_root / doc_file
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 長いドキュメントは要約
                if len(content) > 10000:
                    content = content[:10000] + "\n\n... (document continues)"
                
                memory = Memory(
                    content=f"Documentation: {doc_file}\n\n{content}",
                    memory_type="documentation",
                    importance_score=80 if "README" in doc_file else 75,
                    tags=["documentation", "markdown", doc_file.lower().replace(".md", "").replace("_", "-")],
                    file_path=str(file_path),
                    metadata={
                        "source": "documentation_import",
                        "document_type": "markdown",
                        "import_date": datetime.now().isoformat()
                    }
                )
                memories.append(memory)
                print(f"✅ Imported {doc_file}")
                
            except Exception as e:
                print(f"❌ Failed to import {doc_file}: {e}")
        else:
            print(f"⚠️ Documentation not found: {doc_file}")
    
    print(f"📚 Created {len(memories)} documentation memories")
    return memories


def main():
    """メイン処理: 全記憶データをSupabaseに投入"""
    print("🚀 Starting Memory Data Import to Supabase")
    print("=" * 60)
    
    # 記憶システム初期化
    system = MemoryAutomationSystem()
    
    # 各カテゴリの記憶を収集
    all_memories = []
    
    # 会話履歴
    conversation_memories = import_conversation_memories()
    all_memories.extend(conversation_memories)
    
    # コードファイル
    code_memories = import_code_memories()
    all_memories.extend(code_memories)
    
    # Git履歴
    git_memories = import_git_memories()
    all_memories.extend(git_memories)
    
    # ドキュメント
    doc_memories = import_documentation_memories()
    all_memories.extend(doc_memories)
    
    print(f"\n📊 Total memories to import: {len(all_memories)}")
    
    # 記憶を処理・保存
    successful_imports = 0
    failed_imports = 0
    
    for i, memory in enumerate(all_memories):
        print(f"🔄 Processing memory {i+1}/{len(all_memories)}: {memory.memory_type}")
        
        try:
            # 記憶を処理
            processed_memory = system.processor.process_memory(memory)
            
            # 関連記憶を検索（既存の記憶から）
            existing_memories = [m for m in all_memories[:i] if hasattr(m, 'id')]
            if existing_memories:
                processed_memory.related_memories = system.processor.find_related_memories(
                    processed_memory, existing_memories[-50:]  # 最新50個から関連性を検索
                )
            
            # Supabaseに保存
            success = system.storage.save_memory(processed_memory)
            
            if success:
                successful_imports += 1
                print(f"   ✅ Saved (ID: {processed_memory.id})")
            else:
                failed_imports += 1
                print(f"   ❌ Save failed")
        
        except Exception as e:
            failed_imports += 1
            print(f"   ❌ Processing error: {e}")
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print(f"📊 Import Results:")
    print(f"   ✅ Successful: {successful_imports}")
    print(f"   ❌ Failed: {failed_imports}")
    print(f"   📊 Success Rate: {successful_imports/(successful_imports+failed_imports)*100:.1f}%")
    
    # 最終統計を生成
    try:
        report = system.generate_memory_report()
        print(f"\n📋 Final Memory Statistics:")
        print(f"   Total memories in system: {report['total_memories']}")
        print(f"   Memory types: {report['memory_types']}")
        print(f"   High importance memories: {report['importance_distribution']['high']}")
        print(f"   Recent activity (24h): {report['recent_activity']['last_24h']}")
    except Exception as e:
        print(f"⚠️ Statistics generation error: {e}")
    
    print("\n🎉 Memory Import Process Completed!")
    
    return successful_imports > 0


if __name__ == "__main__":
    # 環境変数チェック
    if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_KEY'):
        print("⚠️ Warning: SUPABASE_URL and SUPABASE_KEY environment variables not set")
        print("   Please set them before running this script for actual import")
    
    # インポート実行
    success = main()
    
    # 終了コード
    sys.exit(0 if success else 1)
