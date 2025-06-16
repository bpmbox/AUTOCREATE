import gradio as gr
import sys
import os

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.append(project_root)

from mysite.libs.utilities import chat_with_interpreter, completion, process_file,no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb
import psycopg2
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from mysite.interpreter.process import no_process_file,process_file,process_nofile
#from controllers.gra_04_database.rides import test_set_lide
import requests
import os
from datetime import datetime
from controllers.gra_03_programfromdocs.system_automation import SystemAutomation

# 記憶自動化システムの統合
try:
    from memory_automation_system import MemoryAutomationSystem, Memory
    MEMORY_SYSTEM_AVAILABLE = True
    print("✅ Memory automation system imported successfully")
except ImportError as e:
    print(f"⚠️ Memory automation system not available: {e}")
    MEMORY_SYSTEM_AVAILABLE = False

# Supabase接続（記憶管理システム用）
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'YOUR_SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'YOUR_SUPABASE_KEY')
    SUPABASE_AVAILABLE = SUPABASE_URL != 'YOUR_SUPABASE_URL' and SUPABASE_KEY != 'YOUR_SUPABASE_KEY'
    if SUPABASE_AVAILABLE:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connection established for memory integration")
    else:
        print("⚠️ Supabase credentials not configured")
        supabase = None
except ImportError:
    print("⚠️ Supabase client not available")
    SUPABASE_AVAILABLE = False
    supabase = None

# Supabase記憶管理機能
def get_memories_from_supabase(memory_type: str = None, limit: int = 50) -> List[dict]:
    """Supabaseのchat_historyテーブルから記憶を取得"""
    if not SUPABASE_AVAILABLE or not supabase:
        print("⚠️ Supabase not available, returning empty memory list")
        return []
    
    try:
        query = supabase.table('chat_history').select('*')
        
        # 記憶タイプでフィルタ
        if memory_type and memory_type != "all":
            query = query.eq('memory_type', memory_type)
        
        # 重要度でソート（statusフィールドを使用）
        query = query.order('created', desc=True).limit(limit)
        
        result = query.execute()
        
        if result.data:
            # プロンプト形式に変換
            memories = []
            for row in result.data:
                # statusから重要度を抽出
                importance_score = 70  # デフォルト
                if row.get('status') and 'importance_' in str(row['status']):
                    try:
                        importance_score = int(row['status'].replace('importance_', ''))
                    except:
                        pass
                
                memory_data = {
                    'id': row['id'],
                    'title': f"[{row.get('group_name', 'general')}] {(row.get('messages') or '')[:50]}...",
                    'content': row.get('messages', ''),
                    'memory_type': row.get('group_name', 'general'),
                    'importance_score': importance_score,
                    'tags': [row.get('targetid', 'general')],
                    'created_at': row.get('created'),
                    'github_url': '',
                    'repository_name': '',
                    'system_type': row.get('group_name', 'general'),
                    'execution_status': 'available'
                }
                memories.append(memory_data)
            
            print(f"✅ Supabase memories retrieved: {len(memories)} items")
            return memories
        else:
            print("ℹ️ No memories found in Supabase")
            return []
            
    except Exception as e:
        print(f"❌ Supabase memory retrieval error: {e}")
        return []

def search_memories_in_supabase(query: str, limit: int = 20) -> List[dict]:
    """Supabaseで記憶を検索"""
    if not SUPABASE_AVAILABLE or not supabase:
        return []
    
    try:
        # messagesフィールドで検索
        result = supabase.table('chat_history').select('*').ilike(
            'messages', f'%{query}%'
        ).order('created', desc=True).limit(limit).execute()
        
        memories = []
        for row in result.data:
            importance_score = 70
            if row.get('status') and 'importance_' in str(row['status']):
                try:
                    importance_score = int(row['status'].replace('importance_', ''))
                except:
                    pass
            
            memory_data = {
                'id': row['id'],
                'title': f"🔍 {(row.get('messages') or '')[:40]}...",
                'content': row.get('messages', ''),
                'memory_type': row.get('group_name', 'general'),
                'importance_score': importance_score,
                'tags': [row.get('targetid', 'general')],
                'created_at': row.get('created'),
                'system_type': row.get('group_name', 'general')
            }
            memories.append(memory_data)
        
        print(f"✅ Memory search results: {len(memories)} items")
        return memories
        
    except Exception as e:
        print(f"❌ Memory search error: {e}")
        return []

def save_prompt_to_supabase(title: str, content: str, memory_type: str = "prompt", 
                           importance_score: int = 70, tags: List[str] = None) -> str:
    """プロンプトをSupabaseの記憶として保存"""
    if not SUPABASE_AVAILABLE or not supabase:
        print(f"⚠️ Supabase not available, cannot save prompt: {title}")
        return "❌ Supabase接続が利用できません"
    
    try:
        if not title.strip() or not content.strip():
            return "❌ タイトルと内容は必須です"
        
        # 記憶データを準備
        memory_data = {
            'ownerid': 'lavelo_system',
            'messages': f"Prompt: {title}\n\n{content}",
            'targetid': f'prompt_{memory_type}',
            'created': datetime.now().isoformat(),
            'status': f'importance_{importance_score}',
            'group_name': 'lavelo_prompts'
        }
        
        result = supabase.table('chat_history').insert(memory_data).execute()
        
        if result.data:
            memory_id = result.data[0]['id']
            print(f"✅ Prompt saved to Supabase: {title} (ID: {memory_id})")
            return f"✅ プロンプト「{title}」をSupabase記憶として保存しました\n📁 記憶ID: {memory_id}"
        else:
            return "❌ Supabase保存に失敗しました"
            
    except Exception as e:
        print(f"❌ Supabase prompt save error: {e}")
        return f"❌ 保存エラー: {e}"

def get_prompt_by_memory_id(memory_id: int) -> Tuple[str, str, str, str]:
    """記憶IDからプロンプト詳細を取得"""
    if not SUPABASE_AVAILABLE or not supabase:
        return get_prompt_details(memory_id)
    
    try:
        result = supabase.table('chat_history').select('*').eq('id', memory_id).execute()
        
        if result.data:
            row = result.data[0]
            content = row.get('messages', '')
            
            # タイトルを生成
            title = content[:50] if content else "プロンプト"
            
            return (
                content,
                '',  # github_url
                row.get('group_name', 'general'),  # system_type
                title  # repository_name
            )
        else:
            return "", "", "", ""
            
    except Exception as e:
        print(f"❌ Memory retrieval error: {e}")
        return "", "", "", ""

def get_prompts_local() -> List[dict]:
    """フォールバック: ローカルの空データを返す"""
    print("⚠️ Supabase not available, returning empty prompt list")
    return []

def save_prompt_local(title: str, content: str) -> str:
    """フォールバック: ローカル保存メッセージを返す"""
    print(f"⚠️ Supabase not available, cannot save prompt: {title}")
    return "❌ Supabase接続が利用できません"

# Supabase記憶管理システム
def init_db():
    """Supabaseプロンプトデータベースの初期化"""
    if not SUPABASE_AVAILABLE or not supabase:
        print("⚠️ Supabase not available for initialization")
        return
    
    try:
        # デフォルトプロンプトの確認と追加
        existing_prompts = supabase.table('chat_history').select('id').eq('group_name', 'lavelo_prompts').execute()
        
        if not existing_prompts.data:
            print("📝 Adding default prompts to Supabase...")
            default_prompts = [
                {
                    'title': "社員プロフィールシステム",
                    'content': "社員プロフィール管理システム\n- ユーザー登録\n- プロフィール編集\n- 検索機能\n- 管理機能",
                    'system_type': "web_system"
                },
                {
                    'title': "FastAPI + SQLAlchemy",
                    'content': "FastAPIとSQLAlchemyを使用したAPIの作成\n- ユーザー管理\n- 認証機能\n- CRUD操作",
                    'system_type': "api_system"
                },
                {
                    'title': "Gradio Interface",
                    'content': "Gradioインターフェースの作成\n- ファイルアップロード\n- チャット機能\n- データ表示",
                    'system_type': "interface_system"
                },
                {
                    'title': "LINE画像検索システム",
                    'content': "LINEからの画像を検索するシステム\n- doPost受信\n- 画像保存\n- S3アップロード\n- シークレット管理",
                    'system_type': "line_system"
                },
            ]
            
            for prompt_data in default_prompts:
                save_prompt_to_supabase(
                    title=prompt_data['title'],
                    content=prompt_data['content'],
                    memory_type='prompt',
                    importance_score=75,
                    tags=[prompt_data['system_type']]
                )
        
        print("✅ Supabaseプロンプトデータベース初期化完了")
        
    except Exception as e:
        print(f"❌ Supabase初期化エラー: {e}")

def save_prompt(title: str, content: str, github_url: str = "", system_type: str = "general") -> str:
    """プロンプトをSupabaseに保存（統一インターフェース）"""
    # GitHubURLが指定されている場合は、それも含めて保存
    full_content = content
    if github_url:
        full_content += f"\n\nGitHub Repository: {github_url}"
    
    # タグを準備
    tags = ['prompt', system_type]
    if github_url:
        repo_name = github_url.split('/')[-1].replace('.git', '') if github_url.endswith('.git') else github_url.split('/')[-1]
        tags.append(repo_name)
    
    return save_prompt_to_supabase(
        title=title,
        content=full_content,
        memory_type='prompt',
        importance_score=70,
        tags=tags
    )

def get_prompts() -> List[Tuple]:
    """Supabaseから全プロンプトを取得（従来インターフェース互換）"""
    if not SUPABASE_AVAILABLE or not supabase:
        print("⚠️ Supabase not available")
        return []
    
    try:
        # プロンプトタイプの記憶を取得
        result = supabase.table('chat_history').select('*').eq('group_name', 'lavelo_prompts').order('created', desc=True).execute()
        
        prompts = []
        for row in result.data:
            messages = row.get('messages', '')
            title = messages[:50] if messages else "プロンプト"
            
            # 従来の形式に変換
            prompts.append((
                row['id'],  # id
                title,  # title
                row.get('group_name', 'prompt'),  # system_type
                row.get('targetid', 'general'),  # repository_name (targetidで代用)
                'available',  # execution_status
                row.get('created', '')  # created_at
            ))
        
        print(f"✅ Supabaseプロンプト取得: {len(prompts)}件")
        return prompts
    except Exception as e:
        print(f"❌ Supabaseプロンプト取得エラー: {e}")
        return []

def get_prompt_content(prompt_id: int) -> str:
    """Supabaseから指定IDのプロンプト内容を取得"""
    if not SUPABASE_AVAILABLE or not supabase:
        print("⚠️ Supabase not available")
        return ""
    
    try:
        result = supabase.table('chat_history').select('message').eq('id', prompt_id).execute()
        
        if result.data:
            print(f"✅ Supabaseプロンプト内容取得: ID {prompt_id}")
            return result.data[0]['message']
        else:
            print(f"❌ プロンプトが見つかりません: ID {prompt_id}")
            return ""
            
    except Exception as e:
        print(f"❌ Supabaseプロンプト内容取得エラー: {e}")
        return ""

def get_prompt_details(prompt_id: int) -> Tuple[str, str, str, str]:
    """Supabaseから指定IDのプロンプト詳細を取得"""
    return get_prompt_by_memory_id(prompt_id)

def update_execution_status(prompt_id: int, status: str) -> None:
    """Supabaseで実行ステータスを更新"""
    if not SUPABASE_AVAILABLE or not supabase:
        print("⚠️ Supabase not available for status update")
        return
    
    try:
        # ステータスを更新
        supabase.table('chat_history').update({
            'status': f'execution_{status}',
            'status_created': datetime.now().isoformat()
        }).eq('id', prompt_id).execute()
        
        print(f"✅ Supabaseステータス更新: ID {prompt_id} -> {status}")
        
    except Exception as e:
        print(f"❌ Supabaseステータス更新エラー: {e}")

def delete_prompt(prompt_id: int) -> str:
    """Supabaseからプロンプトを削除"""
    if not SUPABASE_AVAILABLE or not supabase:
        return "❌ Supabase接続エラー"
    
    try:
        result = supabase.table('chat_history').delete().eq('id', prompt_id).execute()
        
        if result.data:
            print(f"✅ Supabaseプロンプト削除: ID {prompt_id}")
            return f"✅ プロンプト ID {prompt_id} を削除しました"
        else:
            return f"❌ プロンプト ID {prompt_id} が見つかりません"
            
    except Exception as e:
        print(f"❌ Supabaseプロンプト削除エラー: {e}")
        return f"❌ 削除エラー: {e}"

def update_prompt_display():
    """プロンプト一覧の表示を更新（Supabase統合版）"""
    try:
        # Supabaseから記憶を取得
        memories = get_memories_from_supabase(memory_type=None, limit=50)
        
        if memories:
            # テーブル形式でデータを準備
            table_data = []
            for memory in memories:
                # 日時の表示を短くする
                date_str = (memory.get('created_at') or '')[:16] if memory.get('created_at') else ""
                
                # システムタイプのアイコンを追加
                memory_type = memory.get('memory_type', 'general')
                type_icon = {
                    'lavelo_prompts': '📝',
                    'prompt': '📝',
                    'code': '💻',
                    'git': '📝',
                    'file': '📄',
                    'chat': '💬', 
                    'documentation': '📚',
                    'web_system': '🌐',
                    'api_system': '🔗',
                    'interface_system': '🖥️',
                    'line_system': '📱',
                    'general': '📄'
                }.get(memory_type, '📄')
                
                # 重要度による色分け
                importance = memory.get('importance_score', 0)
                if importance >= 80:
                    status_icon = '🔥'  # 高重要度
                elif importance >= 60:
                    status_icon = '⭐'  # 中重要度
                else:
                    status_icon = '📋'  # 低重要度
                
                # タグ表示
                tags = memory.get('tags', []) or []
                tag_display = ', '.join(str(tag) for tag in tags[:3]) if tags else '未分類'
                
                table_data.append([
                    memory['id'], 
                    f"{type_icon} {memory.get('title', '無題')}", 
                    tag_display,
                    f"{status_icon} {importance}点",
                    date_str
                ])
            
            return table_data
        else:
            return [["データなし", "", "", "", ""]]
            
    except Exception as e:
        print(f"❌ Display update error: {e}")
        return [["エラー", str(e), "", "", ""]]

def search_prompts_display(query: str):
    """プロンプト検索結果の表示更新"""
    try:
        if not query.strip():
            return update_prompt_display()
        
        # Supabaseで検索
        memories = search_memories_in_supabase(query, limit=30)
        
        if memories:
            table_data = []
            for memory in memories:
                date_str = (memory.get('created_at') or '')[:16] if memory.get('created_at') else ""
                memory_type = memory.get('memory_type', 'general')
                importance = memory.get('importance_score', 0)
                
                type_icon = {
                    'lavelo_prompts': '📝',
                    'prompt': '📝',
                    'code': '💻',
                    'git': '📝',
                    'file': '📄',
                    'chat': '💬',
                    'documentation': '📚',
                    'general': '📄'
                }.get(memory_type, '📄')
                
                # 検索結果マーク
                search_icon = '🔍'
                
                table_data.append([
                    memory['id'],
                    f"{search_icon} {type_icon} {memory.get('title', '無題')}",
                    f"重要度: {importance}",
                    f"タイプ: {memory_type}",
                    date_str
                ])
            
            return table_data
        else:
            return [["検索結果なし", f"「{query}」に関する記憶が見つかりませんでした", "", "", ""]]
            
    except Exception as e:
        print(f"❌ Search display error: {e}")
        return [["検索エラー", str(e), "", "", ""]]
    return []

val = """
# 社員がプロフィールを登録・公開し、お互いに参照できるシステム

## 機能

## LINEのクレーム対応システムの作成
- クレームがあった用語をAPIでナレッジに登録するシステム
- APIキー agentキーをいれ
- 否定語に対する　文言に隊しての設定をする

### ユーザー登録

- ユーザー登録画面で、ユーザー名とパスワードを入力して登録ボタンを押すことにより、新規ユーザーを登録することができる。
- ユーザー名は、既存のユーザーと重複してはいけない。
- ユーザー登録に成功したら、ログイン済み状態として、ユーザー一覧画面へ遷移する。

### ログイン

- ログイン画面で、ユーザー名とパスワードを入力してログインボタンを押すことにより、ログインすることができる。
- ログインに成功したら、ユーザー一覧画面へ遷移する。

### チーム一覧・作成

- チームの一覧が、チームの作成日時降順で表示される。
- チーム名を入力して作成ボタンを押すと、チームが作成される。
- チームの作成後、本画面が再表示される。

### プロフィール編集

- 自身の`所属チーム`・`プロフィール`・`タグ`を編集できる。
- 所属チームは、既存チームからの選択式とする。
- プロフィールは自由入力とする。
- タグは自由入力で、複数入力できるようにする。

### ユーザー一覧・検索

- デフォルトでは全てのユーザーが一覧表示される。
- 検索条件を入力して検索ボタンを押すと、検索条件がプロフィールに部分一致するユーザーのみにフィルタリングできる。
- 一覧は、ユーザー登録日時の降順で表示される。
- 表示内容は、`ユーザー名`・`プロフィール`で、`プロフィール`は先頭10文字と三点リーダーを表示する。
- ユーザー名をクリックすると、そのユーザーのユーザー詳細画面へ遷移する。
- `チーム一覧へ`をクリックすると、チーム一覧画面へ遷移する。

### ユーザー詳細画面

- 特定のユーザーの、`ユーザー名`・`所属チーム`・`プロフィール`・`タグ`が表示される。
- プロフィールの表示はマークダウンに対応させる。
- `一覧へ`リンクをクリックすると、ユーザー一覧画面へ遷移する。

## あなたが作成するもの

バックエンドのプログラム一式を作成してください。
フロントエンドのプログラムは不要です。

- `/api`ディレクトリ以下に作成。
- Python/FastAPI/SQLAlchemyを使う。
- DBはSQLiteを使う。
- 必要に応じて外部ライブラリを使う。
- クラウドや外部サービス(外部API)は使わない。
- .gitignoreを含めること。
- バックエンド
@app.post("
def lumbda_function():

gradio_interface でメイン関数から読み込めるようにして

googleappsscript
ラインの画像検索システム

ファイルは１ファイルで作成して。
１ファイル１機能で難しくしたくない

1,lineからデータがくる
2,doPostで取得
3.typeがイメージの場合はドライブに保存
4,保存したデータをS3にアップロード
5.データはシークレットから取得
6,plantumlでフローの作成
7,システムドキュメントの作成

gradio は gradio_interface というBlock名で作成
fastapiはrouter の作成

"""

def send_to_google_chat(message: str):
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAANwDF_KE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=qSigSPSbTINJITgO30iGKnyeY48emcUJd9LST7FBLLY'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    data = {'text': message}
    response = requests.post(webhook_url, headers=headers, json=data)
    response.raise_for_status()

def process_file_and_notify(*args, **kwargs):
    # 実行前にステータスを更新
    try:
        prompt_content = args[0] if args else ""
        if prompt_content.strip():
            # Supabaseでプロンプト検索（内容完全一致）
            if SUPABASE_AVAILABLE and supabase:
                result = supabase.table('chat_history').select('id').ilike('messages', f'%{prompt_content}%').execute()
                if result.data:
                    update_execution_status(result.data[0]['id'], 'running')
    except Exception as e:
        print(f"実行前ステータス更新エラー: {e}")
    
    # プロンプトを実行
    result = process_nofile(*args, **kwargs)
    
    # Google Chatに通知
    send_to_google_chat(f"🚀 システム生成完了\n```\n{result[:500]}...\n```")
    
    # プロンプト実行後、内容をSupabaseに保存・更新
    try:
        prompt_content = args[0] if args else ""
        if prompt_content.strip():
            # 実行されたプロンプトのタイトルを生成（最初の行または最初の50文字）
            title_lines = prompt_content.strip().split('\n')
            title = title_lines[0][:50] if title_lines[0] else "実行されたプロンプト"
            if title.startswith('#'):
                title = title[1:].strip()
            
            # Supabaseで既存のプロンプトか確認
            if SUPABASE_AVAILABLE and supabase:
                result = supabase.table('chat_history').select('id').ilike('messages', f'%{prompt_content[:100]}%').execute()
                
                if result.data:
                    # 既存プロンプトのステータスを更新
                    update_execution_status(result.data[0]['id'], 'completed')
                else:
                    # 新しい実行履歴として保存
                    save_prompt(f"実行履歴: {title}", prompt_content, "", "execution_log")
            
    except Exception as e:
        print(f"実行履歴保存エラー: {e}")
        # エラー時はステータスを失敗に更新
        try:
            if SUPABASE_AVAILABLE and supabase:
                result = supabase.table('chat_history').select('id').ilike('messages', f'%{prompt_content[:100]}%').execute()
                if result.data:
                    update_execution_status(result.data[0]['id'], 'failed')
        except:
            pass
    
    return result

def process_file_and_notify_enhanced(*args, **kwargs):
    """拡張版: プロンプト実行 + 自動GitHub連携"""
    # 実行前にステータスを更新
    try:
        prompt_content = args[0] if args else ""
        folder_name = args[1] if len(args) > 1 else "generated_systems"
        github_token = args[2] if len(args) > 2 else ""
        
        if prompt_content.strip():
            # Supabaseでプロンプト検索（完全一致）
            if SUPABASE_AVAILABLE and supabase:
                result = supabase.table('chat_history').select('id').eq('message', f"Prompt: \n\n{prompt_content}").execute()
                if result.data:
                    update_execution_status(result.data[0]['id'], 'running')
    except Exception as e:
        print(f"実行前ステータス更新エラー: {e}")
    
    # プロンプトを実行
    result = process_nofile(*args, **kwargs)
    
    # 自動化パイプラインを実行
    enhanced_result = result
    if github_token and len(github_token) > 10:  # GitHub tokenが設定されている場合
        try:
            automation = SystemAutomation(github_token)
            
            # リポジトリ名を生成
            title_lines = prompt_content.strip().split('\n')
            repo_name = title_lines[0][:30] if title_lines[0] else "generated-system"
            repo_name = repo_name.replace('#', '').strip().replace(' ', '-').lower()
            
            # 生成されたフォルダのパス
            generated_folder = os.path.join(project_root, folder_name)
            
            # 自動化パイプライン実行
            automation_result = automation.full_automation_pipeline(
                generated_folder,
                repo_name,
                f"GPT-ENGINEERで生成されたシステム: {repo_name}"
            )
            
            if automation_result['success']:
                enhanced_result += f"\n\n🚀 自動化完了!\n"
                enhanced_result += f"📁 GitHub: {automation_result['github_repo']['url']}\n"
                enhanced_result += f"🔧 統合されたController: {len(automation_result.get('controllers_found', []))}件"
                
                # Google Chatに詳細通知
                send_to_google_chat(f"""🎉 システム自動生成・統合完了!
                
📊 **生成システム**: {repo_name}
🔗 **GitHub**: {automation_result['github_repo']['url']}
🔧 **Controller統合**: {len(automation_result.get('controllers_found', []))}件
📱 **ステータス**: 運用準備完了
""")
            else:
                enhanced_result += f"\n\n⚠️ 自動化エラー: {automation_result.get('error', '不明')}"
                
        except Exception as e:
            enhanced_result += f"\n\n❌ 自動化エラー: {str(e)}"
    else:
        # 従来の通知
        send_to_google_chat(f"🚀 システム生成完了\n```\n{result[:500]}...\n```")
    
    # プロンプト実行後、内容をSupabaseに保存・更新（拡張版）
    try:
        prompt_content = args[0] if args else ""
        if prompt_content.strip():
            # 実行されたプロンプトのタイトルを生成（最初の行または最初の50文字）
            title_lines = prompt_content.strip().split('\n')
            title = title_lines[0][:50] if title_lines[0] else "実行されたプロンプト"
            if title.startswith('#'):
                title = title[1:].strip()
            
            # Supabaseで既存のプロンプトか確認
            if SUPABASE_AVAILABLE and supabase:
                result = supabase.table('chat_history').select('id').ilike('messages', f'%{prompt_content[:100]}%').execute()
                
                if result.data:
                    # 既存プロンプトのステータスを更新
                    update_execution_status(result.data[0]['id'], 'completed')
                else:
                    # 新しい実行履歴として保存
                    save_prompt(f"実行履歴: {title}", prompt_content, "", "execution_log")
            
    except Exception as e:
        print(f"実行履歴保存エラー: {e}")
        # エラー時はステータスを失敗に更新
        try:
            if SUPABASE_AVAILABLE and supabase:
                result = supabase.table('chat_history').select('id').ilike('messages', f'%{prompt_content[:100]}%').execute()
                if result.data:
                    update_execution_status(result.data[0]['id'], 'failed')
        except:
            pass
    
    return enhanced_result

# ...existing code...

def load_prompt_to_textbox(evt: gr.SelectData):
    """テーブルクリック時にプロンプト内容をテキストボックスに読み込む"""
    try:
        if evt.index is not None and len(evt.index) >= 2:
            # テーブルの行インデックスから prompt_id を取得
            prompts = get_prompts()
            if evt.index[0] < len(prompts):
                prompt_id = prompts[evt.index[0]][0]  # 最初の列がID
                content, github_url, system_type, repo_name = get_prompt_details(prompt_id)
                return content, github_url, system_type
    except Exception as e:
        print(f"プロンプト読み込みエラー: {e}")
    return "", "", "general"

# 自動検出システム用のメタデータ
interface_title = "💾 プロンプト管理システム"
interface_description = "Supabaseベースのプロンプト管理とコード生成"

# AI用の高度なプロンプトテンプレート
ai_system_prompts = {
    "microservice_api": """
# 高性能マイクロサービスAPI設計

## 要件
- FastAPI + SQLAlchemy + Alembic
- JWT認証、RBAC権限管理
- OpenAPI仕様書自動生成
- Redis キャッシュ、Celery非同期処理
- Docker コンテナ化
- CI/CD パイプライン（GitHub Actions）
- 監視・ログ・メトリクス（Prometheus + Grafana）

## アーキテクチャ
- Clean Architecture パターン
- Repository パターン
- 依存性注入（DI）
- イベント駆動設計

## セキュリティ
- OWASP準拠
- SQL injection防止
- CORS設定
- Rate limiting

## テスト
- 単体テスト（pytest）
- 統合テスト
- E2Eテスト
- カバレッジ90%以上

作成してください。
""",
    
    "ai_chat_system": """
# AI チャットシステム（RAG対応）

## 機能
- リアルタイムチャット（WebSocket）
- AI応答（OpenAI API, Claude API）
- RAG（Retrieval-Augmented Generation）
- ベクトルデータベース（Chroma, Pinecone）
- ファイルアップロード・解析
- 会話履歴管理
- ユーザー管理・認証

## 技術スタック
- Frontend: React + TypeScript + Tailwind CSS
- Backend: FastAPI + SQLAlchemy
- Vector DB: Chroma
- Cache: Redis
- Queue: Celery

## AI機能
- 文書の埋め込み生成
- セマンティック検索
- コンテキスト理解
- マルチモーダル対応（画像、PDF）

gradio_interface として作成してください。
""",

    "blockchain_dapp": """
# ブロックチェーン DApp開発

## 要件
- Solidity スマートコントラクト
- Web3.js フロントエンド
- MetaMask連携
- IPFS ファイルストレージ
- OpenZeppelin セキュリティ
- Hardhat 開発環境

## 機能
- NFT マーケットプレイス
- DAO ガバナンス
- DeFi プロトコル
- ステーキング機能

## セキュリティ
- リエントランシー攻撃防止
- オーバーフロー対策
- アクセス制御

作成してください。
""",

    "devops_infrastructure": """
# DevOps インフラストラクチャ

## 要件
- Kubernetes クラスター設計
- Terraform インフラコード
- Ansible 設定管理
- CI/CD パイプライン
- 監視・アラート
- ログ集約
- セキュリティ

## 技術
- AWS/GCP/Azure
- Docker/Podman
- GitLab/GitHub Actions
- Prometheus/Grafana
- ELK Stack
- Helm Charts

## セキュリティ
- Secret管理（Vault）
- ネットワークセキュリティ
- コンプライアンス

作成してください。
"""
}

def add_ai_system_prompts():
    """AI用の高度なシステムプロンプトをSupabaseに追加"""
    try:
        if not SUPABASE_AVAILABLE or not supabase:
            print("⚠️ Supabase not available for AI prompts")
            return
            
        for title, content in ai_system_prompts.items():
            # Supabaseで既存チェック
            existing = supabase.table('chat_history').select('id').ilike('message', f"%{title}%").execute()
            
            if not existing.data:
                system_type = "ai_generated"
                github_url = f"https://github.com/ai-systems/{title.replace('_', '-')}"
                
                # Supabaseに追加
                save_prompt_to_supabase(
                    title=f"🤖 AI: {title}",
                    content=content,
                    memory_type='prompt',
                    importance_score=80,
                    tags=['ai_generated', system_type, title.replace('_', '-')]
                )
                print(f"✅ AI プロンプト追加: {title}")
        
    except Exception as e:
        print(f"❌ AI プロンプト追加エラー: {e}")

# データベース初期化
init_db()
# AI用の高度なプロンプトを追加
add_ai_system_prompts()

with gr.Blocks() as gradio_interface:
    gr.Markdown("# 🚀 プロンプト管理＆自動システム生成")
    gr.Markdown("プロンプトでGPT-ENGINEERを使ってシステムを作成し、GitHubにアップして自動化")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📚 プロンプト一覧")
            
            # プロンプト一覧テーブル
            prompt_table = gr.Dataframe(
                headers=["ID", "タイトル", "リポジトリ", "ステータス", "作成日時"],
                datatype=["number", "str", "str", "str", "str"],
                value=update_prompt_display(),
                interactive=False
            )
            
            # 更新ボタン
            refresh_btn = gr.Button("🔄 一覧更新", variant="secondary")
            
            # プロンプト保存エリア
            gr.Markdown("## 💾 プロンプト保存")
            with gr.Row():
                save_title = gr.Textbox(label="タイトル", placeholder="プロンプトのタイトルを入力")
            with gr.Row():
                github_url_input = gr.Textbox(label="GitHub URL", placeholder="https://github.com/username/repository")
                system_type_dropdown = gr.Dropdown(
                    choices=["general", "web_system", "api_system", "interface_system", "line_system"],
                    value="general",
                    label="システムタイプ"
                )
            with gr.Row():
                save_btn = gr.Button("💾 保存", variant="primary")
            save_result = gr.Textbox(label="保存結果", interactive=False)
        
        with gr.Column(scale=2):
            gr.Markdown("## ⚡ プロンプト実行・システム生成")
            
            # メインのプロンプト入力エリア
            prompt_input = gr.Textbox(
                label="プロンプト内容", 
                lines=12,
                value=val,
                placeholder="プロンプトを入力するか、左の一覧からクリックして選択してください"
            )
            
            with gr.Row():
                selected_github_url = gr.Textbox(label="選択中のGitHub URL", interactive=False)
                selected_system_type = gr.Textbox(label="システムタイプ", interactive=False)
            
            with gr.Row():
                folder_name = gr.Textbox(label="フォルダ名", value="generated_systems")
                github_token = gr.Textbox(label="GitHub Token", value="***********************", type="password")
            
            execute_btn = gr.Button("🚀 システム生成実行", variant="primary", size="lg")
            
            with gr.Row():
                auto_github_checkbox = gr.Checkbox(label="🔄 GitHub自動連携", value=True)
                auto_integrate_checkbox = gr.Checkbox(label="🔧 Controller自動統合", value=True)
            
            result_output = gr.Textbox(label="実行結果", lines=8, interactive=False)
            
            gr.Markdown("## 📋 システム生成フロー")
            gr.Markdown("""
            1. **プロンプト入力** → GPT-ENGINEERでシステム生成
            2. **GitHubアップ** → 指定リポジトリに自動プッシュ  
            3. **Controller自動認識** → 新しいRouterが自動で利用可能に
            4. **Google Chat通知** → 生成完了をチームに通知
            """)
    
    # イベントハンドラー
    prompt_table.select(
        fn=load_prompt_to_textbox,
        outputs=[prompt_input, selected_github_url, selected_system_type]
    )
    
    refresh_btn.click(
        fn=update_prompt_display,
        outputs=prompt_table
    )
    
    save_btn.click(
        fn=lambda title, content, github_url, system_type: save_prompt(title, content, github_url, system_type),
        inputs=[save_title, prompt_input, github_url_input, system_type_dropdown],
        outputs=save_result
    ).then(
        fn=update_prompt_display,
        outputs=prompt_table
    ).then(
        fn=lambda: ("", "", "general"),
        outputs=[save_title, github_url_input, system_type_dropdown]
    )
    
    execute_btn.click(
        fn=process_file_and_notify_enhanced,
        inputs=[prompt_input, folder_name, github_token],
        outputs=result_output
    ).then(
        fn=update_prompt_display,
        outputs=prompt_table
    )

if __name__ == "__main__":
    # データベース初期化
    init_db()
    
    # Gradioアプリケーションの起動
    print("🚀 Lavelo AI システム起動中...")
    print("💡 プロンプト管理・システム生成・AI協働システム")
    print("🌐 アクセス: http://localhost:7860")
    
    # Laravelシステムとの連携設定
    gradio_interface.title = "Lavelo AI - Laravel統合システム"
    gradio_interface.description = "AI×人間協働開発のためのプロンプト管理・システム生成・自動化システム"
    
    # Laravel統合モードで起動
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=False,
        debug=True,
        show_error=True,
        quiet=False
    )

# Laravel Controller統合用の関数エクスポート
def get_gradio_app():
    """LaravelからGradioアプリを取得する関数"""
    init_db()
    return gradio_interface

def run_lavelo_system():
    """Laravelから直接実行する関数"""
    if __name__ != "__main__":
        init_db()
        return gradio_interface.launch(
            server_name="0.0.0.0", 
            server_port=7860,
            share=False,
            prevent_thread_lock=True
        )