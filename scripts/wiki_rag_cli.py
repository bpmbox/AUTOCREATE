#!/usr/bin/env python3
"""
AUTOCREATE WIKI RAG CLI
- コマンドラインから直接WIKI検索・質問
- バッチ処理・スクリプト連携用
"""

import sys
import argparse
from pathlib import Path

# パス設定
sys.path.append(str(Path(__file__).parent))

from wiki_rag_system import WikiRAGSystem

def main():
    parser = argparse.ArgumentParser(description="AUTOCREATE WIKI RAG CLI")
    
    subparsers = parser.add_subparsers(dest='command', help='使用可能なコマンド')
    
    # build コマンド
    build_parser = subparsers.add_parser('build', help='ナレッジベース構築')
    build_parser.add_argument('--force', action='store_true', help='強制再構築')
    
    # query コマンド
    query_parser = subparsers.add_parser('query', help='質問・検索')
    query_parser.add_argument('question', help='質問内容')
    query_parser.add_argument('--max-results', type=int, default=3, help='最大結果数')
    query_parser.add_argument('--verbose', action='store_true', help='詳細表示')
    
    # search コマンド
    search_parser = subparsers.add_parser('search', help='キーワード検索')
    search_parser.add_argument('keyword', help='検索キーワード')
    search_parser.add_argument('--max-results', type=int, default=5, help='最大結果数')
    
    # stats コマンド
    stats_parser = subparsers.add_parser('stats', help='統計情報表示')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # RAGシステム初期化
    rag_system = WikiRAGSystem()
    
    if args.command == 'build':
        print("📚 ナレッジベースを構築中...")
        success = rag_system.build_knowledge_base(force_rebuild=args.force)
        if success:
            stats = rag_system.get_statistics()
            print(f"✅ 構築完了 ({stats.get('total_documents', 0)}件)")
        else:
            print("❌ 構築に失敗しました")
            sys.exit(1)
    
    elif args.command == 'query':
        print(f"🔍 質問: {args.question}")
        print("-" * 50)
        
        result = rag_system.generate_answer(args.question)
        
        print("📝 回答:")
        print(result['answer'])
        print()
        
        if args.verbose:
            print("📊 詳細情報:")
            print(f"信頼度: {result['confidence']:.3f}")
            print("\n関連ソース:")
            for i, source in enumerate(result['sources'], 1):
                print(f"{i}. {source['source']} ({source['similarity']:.3f})")
    
    elif args.command == 'search':
        print(f"🔍 検索: {args.keyword}")
        print("-" * 50)
        
        results = rag_system.search_knowledge(args.keyword, k=args.max_results)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['source']} (類似度: {result['similarity_score']:.3f})")
            print(result['content'][:200] + ('...' if len(result['content']) > 200 else ''))
    
    elif args.command == 'stats':
        stats = rag_system.get_statistics()
        if 'error' in stats:
            print(f"❌ エラー: {stats['error']}")
            sys.exit(1)
        
        print("📊 WIKI RAGシステム統計")
        print("-" * 30)
        print(f"総ドキュメント数: {stats['total_documents']}")
        print(f"コレクション名: {stats['collection_name']}")
        print(f"Chromaパス: {stats['chroma_path']}")
        print("WIKIパス:")
        for path in stats['wiki_paths']:
            print(f"  - {path}")

if __name__ == "__main__":
    main()
