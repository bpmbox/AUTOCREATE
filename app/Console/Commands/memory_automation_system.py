#!/usr/bin/env python3
"""
Memory Automation System
AI×人間協働開発のための記憶自動化システム

このシステムは以下の機能を提供します：
1. リアルタイム記憶保存
2. 知的記憶検索・復元
3. 自動バックアップ・同期
4. 記憶分析・可視化
"""

import os
import json
import time
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import re
import subprocess
import sqlite3
from concurrent.futures import ThreadPoolExecutor

# Supabase接続
import requests
from supabase import create_client, Client

# AI/NLP処理
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# 設定
SUPABASE_URL = os.getenv('SUPABASE_URL', 'YOUR_SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'YOUR_SUPABASE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('memory_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Memory:
    """記憶データクラス"""
    id: Optional[str] = None
    content: str = ""
    memory_type: str = "general"  # general, code, chat, git, file
    importance_score: int = 0  # 0-100
    tags: List[str] = None
    timestamp: datetime = None
    file_path: Optional[str] = None
    code_changes: Optional[Dict] = None
    related_memories: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.tags is None:
            self.tags = []
        if self.related_memories is None:
            self.related_memories = []
        if self.metadata is None:
            self.metadata = {}
        if self.id is None:
            self.id = self.generate_id()
    
    def generate_id(self) -> str:
        """ユニークなIDを生成"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]
        timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S")
        return f"mem_{timestamp_str}_{content_hash}"
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class MemoryCollector:
    """記憶収集器 - ファイル変更、Git履歴、チャット等を監視"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.watched_files = set()
        self.last_scan_time = datetime.now()
        
    def collect_file_changes(self) -> List[Memory]:
        """ファイル変更を記憶として収集"""
        memories = []
        
        # 最近変更されたファイルを検索
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file() and self._should_track_file(file_path):
                try:
                    stat = file_path.stat()
                    modified_time = datetime.fromtimestamp(stat.st_mtime)
                    
                    if modified_time > self.last_scan_time:
                        content = self._read_file_safely(file_path)
                        if content:
                            memory = Memory(
                                content=f"File modified: {file_path.name}\n\n{content[:1000]}",
                                memory_type="file",
                                importance_score=self._calculate_file_importance(file_path),
                                tags=self._extract_file_tags(file_path),
                                file_path=str(file_path),
                                timestamp=modified_time,
                                metadata={
                                    "file_size": stat.st_size,
                                    "file_type": file_path.suffix,
                                    "modification_type": "update"
                                }
                            )
                            memories.append(memory)
                            
                except Exception as e:
                    logger.warning(f"Error reading file {file_path}: {e}")
        
        self.last_scan_time = datetime.now()
        return memories
    
    def collect_git_history(self, since_hours: int = 24) -> List[Memory]:
        """Git履歴を記憶として収集"""
        memories = []
        
        try:
            # 最近のコミット履歴を取得
            since_time = datetime.now() - timedelta(hours=since_hours)
            since_str = since_time.strftime("%Y-%m-%d %H:%M:%S")
            
            cmd = f'git log --since="{since_str}" --pretty=format:"%H|%an|%ad|%s" --date=iso'
            result = subprocess.run(
                cmd, shell=True, cwd=self.workspace_path,
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|', 3)
                        if len(parts) >= 4:
                            commit_hash, author, date_str, message = parts
                            
                            # コミットの詳細情報を取得
                            diff_cmd = f'git show --stat {commit_hash}'
                            diff_result = subprocess.run(
                                diff_cmd, shell=True, cwd=self.workspace_path,
                                capture_output=True, text=True
                            )
                            
                            memory = Memory(
                                content=f"Git Commit: {message}\n\nAuthor: {author}\n\n{diff_result.stdout[:1000]}",
                                memory_type="git",
                                importance_score=self._calculate_commit_importance(message, diff_result.stdout),
                                tags=self._extract_commit_tags(message),
                                timestamp=datetime.fromisoformat(date_str.replace(' ', 'T')),
                                metadata={
                                    "commit_hash": commit_hash,
                                    "author": author,
                                    "commit_message": message
                                }
                            )
                            memories.append(memory)
                            
        except Exception as e:
            logger.warning(f"Error collecting git history: {e}")
        
        return memories
    
    def _should_track_file(self, file_path: Path) -> bool:
        """ファイルを追跡すべきかチェック"""
        # 除外パターン
        exclude_patterns = [
            '*.pyc', '*.pyo', '__pycache__', '.git', '.vscode',
            'node_modules', '*.log', '*.tmp', '*.temp'
        ]
        
        for pattern in exclude_patterns:
            if file_path.match(pattern) or any(part.startswith('.') for part in file_path.parts):
                return False
        
        # 追跡対象の拡張子
        track_extensions = ['.py', '.js', '.ts', '.md', '.json', '.yaml', '.yml', '.txt', '.sql']
        return file_path.suffix.lower() in track_extensions
    
    def _read_file_safely(self, file_path: Path, max_size: int = 10*1024*1024) -> Optional[str]:
        """ファイルを安全に読み込み"""
        try:
            if file_path.stat().st_size > max_size:
                return None
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Error reading file {file_path}: {e}")
            return None
    
    def _calculate_file_importance(self, file_path: Path) -> int:
        """ファイルの重要度を計算"""
        score = 50  # 基本スコア
        
        # ファイル種別による重要度
        if file_path.suffix == '.py':
            score += 20
        elif file_path.suffix in ['.md', '.txt']:
            score += 10
        elif file_path.suffix in ['.json', '.yml', '.yaml']:
            score += 15
        
        # ファイル名による重要度
        important_names = ['main', 'app', 'config', 'readme', 'requirements']
        if any(name in file_path.stem.lower() for name in important_names):
            score += 15
        
        return min(score, 100)
    
    def _extract_file_tags(self, file_path: Path) -> List[str]:
        """ファイルからタグを抽出"""
        tags = [file_path.suffix[1:]] if file_path.suffix else []
        
        # ディレクトリ名をタグとして追加
        for part in file_path.parts:
            if part != '.' and not part.startswith('.'):
                tags.append(part.lower())
        
        return tags[:5]  # 最大5個のタグ
    
    def _calculate_commit_importance(self, message: str, diff: str) -> int:
        """コミットの重要度を計算"""
        score = 50
        
        # コミットメッセージによる重要度
        important_keywords = ['fix', 'add', 'implement', 'feature', 'bug', 'security', 'performance']
        for keyword in important_keywords:
            if keyword in message.lower():
                score += 10
        
        # 変更量による重要度
        if diff:
            lines_changed = len(diff.split('\n'))
            if lines_changed > 100:
                score += 20
            elif lines_changed > 50:
                score += 10
        
        return min(score, 100)
    
    def _extract_commit_tags(self, message: str) -> List[str]:
        """コミットメッセージからタグを抽出"""
        tags = []
        
        # 一般的なコミットタイプ
        commit_types = ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']
        for ctype in commit_types:
            if ctype in message.lower():
                tags.append(ctype)
        
        # 特定のキーワード
        keywords = ['api', 'ui', 'database', 'auth', 'security', 'performance']
        for keyword in keywords:
            if keyword in message.lower():
                tags.append(keyword)
        
        return tags[:3]


class MemoryProcessor:
    """記憶処理器 - 記憶の分析、分類、関連付け"""
    
    def __init__(self):
        self.openai_client = None
        if HAS_OPENAI and OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    def process_memory(self, memory: Memory) -> Memory:
        """記憶を処理・強化"""
        # 自動タグ付け
        memory.tags.extend(self._extract_content_tags(memory.content))
        memory.tags = list(set(memory.tags))  # 重複除去
        
        # 重要度の再計算
        memory.importance_score = self._recalculate_importance(memory)
        
        # AI による内容分析（利用可能な場合）
        if self.openai_client:
            memory = self._ai_analyze_memory(memory)
        
        return memory
    
    def find_related_memories(self, memory: Memory, existing_memories: List[Memory]) -> List[str]:
        """関連する記憶を検索"""
        related = []
        
        for existing in existing_memories:
            if existing.id == memory.id:
                continue
            
            # タグベースの関連性
            common_tags = set(memory.tags) & set(existing.tags)
            if len(common_tags) >= 2:
                related.append(existing.id)
                continue
            
            # 内容の類似性（簡易版）
            similarity = self._calculate_content_similarity(memory.content, existing.content)
            if similarity > 0.5:
                related.append(existing.id)
        
        return related[:5]  # 最大5個の関連記憶
    
    def _extract_content_tags(self, content: str) -> List[str]:
        """内容からタグを抽出"""
        tags = []
        
        # プログラミング言語
        programming_languages = ['python', 'javascript', 'typescript', 'sql', 'html', 'css']
        for lang in programming_languages:
            if lang in content.lower():
                tags.append(lang)
        
        # 技術キーワード
        tech_keywords = ['api', 'database', 'gradio', 'supabase', 'ai', 'chat', 'automation']
        for keyword in tech_keywords:
            if keyword in content.lower():
                tags.append(keyword)
        
        # 関数名やクラス名を抽出
        function_pattern = r'def\s+(\w+)\s*\('
        class_pattern = r'class\s+(\w+)\s*\('
        
        functions = re.findall(function_pattern, content)
        classes = re.findall(class_pattern, content)
        
        tags.extend(functions[:3])  # 最大3個の関数名
        tags.extend(classes[:3])   # 最大3個のクラス名
        
        return [tag.lower() for tag in tags if len(tag) > 2]
    
    def _recalculate_importance(self, memory: Memory) -> int:
        """重要度を再計算"""
        score = memory.importance_score
        
        # 長い内容は重要度を上げる
        if len(memory.content) > 1000:
            score += 10
        
        # 特定のキーワードがある場合
        important_keywords = ['error', 'bug', 'fix', 'implement', 'api', 'database']
        for keyword in important_keywords:
            if keyword in memory.content.lower():
                score += 5
        
        # タグ数による重要度
        score += len(memory.tags) * 2
        
        return min(score, 100)
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """内容の類似性を計算（簡易版）"""
        # 単語レベルの類似性
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _ai_analyze_memory(self, memory: Memory) -> Memory:
        """AI による記憶分析"""
        try:
            prompt = f"""
            以下の記憶内容を分析して、以下の情報を提供してください：
            1. 3つの重要なキーワード
            2. 記憶の種類（code, documentation, discussion, error, solution など）
            3. 重要度（1-100）
            
            記憶内容:
            {memory.content[:500]}
            
            JSON形式で回答してください：
            {{
                "keywords": ["keyword1", "keyword2", "keyword3"],
                "type": "memory_type",
                "importance": 85
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # 結果を記憶に反映
            memory.tags.extend(result.get('keywords', []))
            memory.memory_type = result.get('type', memory.memory_type)
            memory.importance_score = max(memory.importance_score, result.get('importance', 0))
            
        except Exception as e:
            logger.warning(f"AI analysis failed: {e}")
        
        return memory


class MemoryStorage:
    """記憶保存器 - Supabase への永続化"""
    
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.local_cache = {}
        self._init_database()
    
    def _init_database(self):
        """データベースの初期化"""
        try:
            # chat_history テーブルの拡張を確認
            logger.info("Checking database schema...")
            
            # 必要なカラムを追加（存在しない場合）
            additional_columns = [
                "ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS memory_type VARCHAR(50) DEFAULT 'general'",
                "ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS importance_score INTEGER DEFAULT 0",
                "ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS tags TEXT[]",
                "ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS related_memories JSONB",
                "ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS file_references TEXT[]",
                "ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS code_changes JSONB",
                "ALTER TABLE chat_history ADD COLUMN IF NOT EXISTS memory_metadata JSONB"
            ]
            
            for sql in additional_columns:
                try:
                    self.supabase.rpc('execute_sql', {'sql': sql}).execute()
                    logger.info(f"Executed: {sql}")
                except Exception as e:
                    logger.warning(f"SQL execution failed (may already exist): {e}")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    def save_memory(self, memory: Memory) -> bool:
        """記憶を保存"""
        try:
            data = {
                'user_id': 'system',
                'message': memory.content,
                'memory_type': memory.memory_type,
                'importance_score': memory.importance_score,
                'tags': memory.tags,
                'related_memories': {'ids': memory.related_memories},
                'file_references': [memory.file_path] if memory.file_path else [],
                'code_changes': memory.code_changes,
                'memory_metadata': memory.metadata,
                'created_at': memory.timestamp.isoformat()
            }
            
            result = self.supabase.table('chat_history').insert(data).execute()
            
            if result.data:
                memory.id = str(result.data[0]['id'])
                self.local_cache[memory.id] = memory
                logger.info(f"Memory saved: {memory.id}")
                return True
            
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
        
        return False
    
    def load_memories(self, 
                     limit: int = 100, 
                     memory_type: Optional[str] = None,
                     since: Optional[datetime] = None) -> List[Memory]:
        """記憶を読み込み"""
        try:
            query = self.supabase.table('chat_history').select('*')
            
            if memory_type:
                query = query.eq('memory_type', memory_type)
            
            if since:
                query = query.gte('created_at', since.isoformat())
            
            query = query.order('created_at', desc=True).limit(limit)
            
            result = query.execute()
            
            memories = []
            for row in result.data:
                memory = Memory(
                    id=str(row['id']),
                    content=row['message'],
                    memory_type=row.get('memory_type', 'general'),
                    importance_score=row.get('importance_score', 0),
                    tags=row.get('tags', []),
                    related_memories=row.get('related_memories', {}).get('ids', []),
                    file_path=row.get('file_references', [None])[0],
                    code_changes=row.get('code_changes'),
                    metadata=row.get('memory_metadata', {}),
                    timestamp=datetime.fromisoformat(row['created_at'].replace('Z', '+00:00'))
                )
                memories.append(memory)
                self.local_cache[memory.id] = memory
            
            logger.info(f"Loaded {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"Failed to load memories: {e}")
            return []
    
    def search_memories(self, query: str, limit: int = 20) -> List[Memory]:
        """記憶を検索"""
        try:
            # 全文検索
            result = self.supabase.table('chat_history').select('*').text_search(
                'message', query
            ).order('importance_score', desc=True).limit(limit).execute()
            
            memories = []
            for row in result.data:
                memory = Memory(
                    id=str(row['id']),
                    content=row['message'],
                    memory_type=row.get('memory_type', 'general'),
                    importance_score=row.get('importance_score', 0),
                    tags=row.get('tags', []),
                    timestamp=datetime.fromisoformat(row['created_at'].replace('Z', '+00:00'))
                )
                memories.append(memory)
            
            logger.info(f"Found {len(memories)} memories for query: {query}")
            return memories
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def backup_memories(self, backup_path: str) -> bool:
        """記憶をバックアップ"""
        try:
            memories = self.load_memories(limit=10000)  # 大量の記憶を取得
            
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'count': len(memories),
                'memories': [memory.to_dict() for memory in memories]
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Backup completed: {backup_path} ({len(memories)} memories)")
            return True
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False


class MemoryAutomationSystem:
    """記憶自動化システムのメインクラス"""
    
    def __init__(self, workspace_path: str = "/workspaces/AUTOCREATE"):
        self.workspace_path = workspace_path
        self.collector = MemoryCollector(workspace_path)
        self.processor = MemoryProcessor()
        self.storage = MemoryStorage()
        self.running = False
        self.scan_interval = 300  # 5分間隔
        
    async def start_monitoring(self):
        """監視を開始"""
        self.running = True
        logger.info("Memory automation system started")
        
        while self.running:
            try:
                await self.scan_and_process()
                await asyncio.sleep(self.scan_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # エラー時は1分待機
    
    def stop_monitoring(self):
        """監視を停止"""
        self.running = False
        logger.info("Memory automation system stopped")
    
    async def scan_and_process(self):
        """スキャンと処理を実行"""
        logger.info("Starting memory scan...")
        
        # 既存の記憶を読み込み
        existing_memories = self.storage.load_memories(limit=1000)
        
        # 新しい記憶を収集
        new_memories = []
        
        # ファイル変更を収集
        file_memories = self.collector.collect_file_changes()
        new_memories.extend(file_memories)
        
        # Git履歴を収集
        git_memories = self.collector.collect_git_history()
        new_memories.extend(git_memories)
        
        logger.info(f"Collected {len(new_memories)} new memories")
        
        # 記憶を処理・保存
        for memory in new_memories:
            # 記憶を処理
            processed_memory = self.processor.process_memory(memory)
            
            # 関連記憶を検索
            processed_memory.related_memories = self.processor.find_related_memories(
                processed_memory, existing_memories
            )
            
            # 保存
            self.storage.save_memory(processed_memory)
    
    def import_existing_memories(self):
        """既存の記憶を一括インポート"""
        logger.info("Starting existing memory import...")
        
        # 重要なファイルを記憶としてインポート
        important_files = [
            "README.md",
            "requirements.txt",
            "app.py",
            "memory_automation_system.py",
            "docs/issues/*.md"
        ]
        
        for pattern in important_files:
            for file_path in Path(self.workspace_path).glob(pattern):
                if file_path.is_file():
                    content = self.collector._read_file_safely(file_path)
                    if content:
                        memory = Memory(
                            content=f"Imported file: {file_path.name}\n\n{content}",
                            memory_type="file",
                            importance_score=80,
                            tags=["import", "existing", file_path.suffix[1:] if file_path.suffix else ""],
                            file_path=str(file_path),
                            metadata={"import_source": "existing_files"}
                        )
                        
                        processed_memory = self.processor.process_memory(memory)
                        self.storage.save_memory(processed_memory)
        
        # Git履歴を一括インポート
        git_memories = self.collector.collect_git_history(since_hours=24*7)  # 1週間分
        for memory in git_memories:
            processed_memory = self.processor.process_memory(memory)
            self.storage.save_memory(processed_memory)
        
        logger.info("Existing memory import completed")
    
    def generate_memory_report(self) -> Dict[str, Any]:
        """記憶統計レポートを生成"""
        memories = self.storage.load_memories(limit=1000)
        
        report = {
            'total_memories': len(memories),
            'memory_types': {},
            'importance_distribution': {
                'high': 0,    # 80-100
                'medium': 0,  # 50-79
                'low': 0      # 0-49
            },
            'recent_activity': {
                'last_24h': 0,
                'last_week': 0,
                'last_month': 0
            },
            'top_tags': {},
            'file_types': {}
        }
        
        now = datetime.now()
        for memory in memories:
            # メモリタイプ別統計
            memory_type = memory.memory_type
            report['memory_types'][memory_type] = report['memory_types'].get(memory_type, 0) + 1
            
            # 重要度分布
            if memory.importance_score >= 80:
                report['importance_distribution']['high'] += 1
            elif memory.importance_score >= 50:
                report['importance_distribution']['medium'] += 1
            else:
                report['importance_distribution']['low'] += 1
            
            # 最近の活動
            time_diff = now - memory.timestamp
            if time_diff.days == 0:
                report['recent_activity']['last_24h'] += 1
            if time_diff.days <= 7:
                report['recent_activity']['last_week'] += 1
            if time_diff.days <= 30:
                report['recent_activity']['last_month'] += 1
            
            # タグ統計
            for tag in memory.tags:
                report['top_tags'][tag] = report['top_tags'].get(tag, 0) + 1
            
            # ファイルタイプ統計
            if memory.file_path:
                ext = Path(memory.file_path).suffix
                if ext:
                    report['file_types'][ext] = report['file_types'].get(ext, 0) + 1
        
        # トップタグを上位10個に制限
        report['top_tags'] = dict(sorted(report['top_tags'].items(), key=lambda x: x[1], reverse=True)[:10])
        
        return report


# CLI インターフェース
def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Automation System")
    parser.add_argument('--import-existing', action='store_true', help='Import existing memories')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring')
    parser.add_argument('--report', action='store_true', help='Generate memory report')
    parser.add_argument('--backup', type=str, help='Backup memories to file')
    parser.add_argument('--search', type=str, help='Search memories')
    
    args = parser.parse_args()
    
    system = MemoryAutomationSystem()
    
    if getattr(args, 'import_existing', False):
        system.import_existing_memories()
    
    if args.monitor:
        asyncio.run(system.start_monitoring())
    
    if args.report:
        report = system.generate_memory_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    if args.backup:
        system.storage.backup_memories(args.backup)
    
    if args.search:
        memories = system.storage.search_memories(args.search)
        for memory in memories:
            print(f"[{memory.timestamp}] {memory.memory_type}: {memory.content[:100]}...")


if __name__ == "__main__":
    main()
