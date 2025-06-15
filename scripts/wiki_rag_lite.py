#!/usr/bin/env python3
"""
AUTOCREATE WIKI RAG システム（軽量版）
- HuggingFace認証不要
- シンプルなTF-IDFベクトル化
- 既存WIKIからの質問応答
"""

import os
import sys
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import re

# 標準ライブラリと軽量な依存関係のみ
try:
    import chromadb
    from chromadb.config import Settings
    import gradio as gr
    import numpy as np
    import pandas as pd
    import markdown
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError as e:
    print(f"❌ 依存関係エラー: {e}")
    print("📦 以下のコマンドで軽量版依存関係をインストールしてください:")
    print("pip install chromadb gradio numpy pandas markdown beautifulsoup4 python-dotenv scikit-learn")
    sys.exit(1)

# 環境変数の読み込み
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/AUTOCREATE/wiki_rag_lite.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class WikiRAGLiteSystem:
    """WIKI RAG システム（軽量版）"""
    
    def __init__(self, wiki_paths: List[str] = None, chroma_path: str = None):
        """初期化"""
        self.wiki_paths = wiki_paths or [
            "/workspaces/AUTOCREATE/wikigit",
            "/workspaces/AUTOCREATE/AUTOCREATE.wiki",
            "/workspaces/AUTOCREATE/docs"
        ]
        self.chroma_path = chroma_path or "/workspaces/AUTOCREATE/chroma/wiki_rag_lite"
        
        # TF-IDFベクトライザー（日本語対応改善）
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            token_pattern=r'[a-zA-Z0-9\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+',
            min_df=1,
            max_df=0.98,
            lowercase=True,
            analyzer='word'
        )
        
        # データ格納用
        self.documents = []
        self.document_vectors = None
        self.built = False
        
        logger.info("🚀 WIKI RAG システム（軽量版）を初期化しました")
    
    def load_wiki_documents(self) -> List[Dict[str, Any]]:
        """WIKIドキュメント読み込み"""
        documents = []
        
        for wiki_path in self.wiki_paths:
            if not os.path.exists(wiki_path):
                logger.warning(f"⚠️ パスが存在しません: {wiki_path}")
                continue
            
            try:
                for root, dirs, files in os.walk(wiki_path):
                    for filename in files:
                        if filename.endswith('.md'):
                            file_path = os.path.join(root, filename)
                            
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Markdownを HTMLに変換してからテキスト抽出
                            html = markdown.markdown(content)
                            soup = BeautifulSoup(html, 'html.parser')
                            clean_text = soup.get_text()
                            
                            # テキスト前処理
                            processed_text = self._preprocess_text(clean_text)
                            
                            if len(processed_text.strip()) > 50:  # 短すぎる文書は除外
                                doc = {
                                    'content': processed_text,
                                    'original_content': content,
                                    'source': filename,
                                    'path': file_path,
                                    'source_type': 'wiki',
                                    'wiki_path': wiki_path,
                                    'loaded_at': datetime.now().isoformat()
                                }
                                documents.append(doc)
                
                logger.info(f"📄 {len([d for d in documents if d['wiki_path'] == wiki_path])}個のドキュメントを読み込み: {wiki_path}")
                
            except Exception as e:
                logger.error(f"❌ ドキュメント読み込みエラー ({wiki_path}): {e}")
        
        logger.info(f"📚 合計 {len(documents)}個のWIKIドキュメントを読み込み")
        return documents
    
    def _preprocess_text(self, text: str) -> str:
        """テキスト前処理"""
        # 改行・空白の正規化
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # 特殊文字の除去（基本的な文字のみ残す）
        text = re.sub(r'[^\w\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF。、！？]', ' ', text)
        
        return text.strip()
    
    def build_knowledge_base(self, force_rebuild: bool = False):
        """ナレッジベース構築"""
        if self.built and not force_rebuild:
            logger.info("✅ 既存のナレッジベースを使用")
            return True
        
        try:
            # WIKIドキュメント読み込み
            logger.info("📚 WIKIドキュメントを読み込み中...")
            self.documents = self.load_wiki_documents()
            
            if not self.documents:
                logger.error("❌ 読み込むドキュメントがありません")
                return False
            
            # TF-IDF ベクトル化
            logger.info("🔄 TF-IDF ベクトル化中...")
            document_texts = [doc['content'] for doc in self.documents]
            self.document_vectors = self.vectorizer.fit_transform(document_texts)
            
            self.built = True
            logger.info(f"✅ ナレッジベース構築完了 ({len(self.documents)}件)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ナレッジベース構築エラー: {e}")
            return False
    
    def search_knowledge(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """ナレッジ検索"""
        if not self.built:
            logger.error("❌ ナレッジベースが構築されていません")
            return []
        
        try:
            # クエリをベクトル化
            query_processed = self._preprocess_text(query)
            query_vector = self.vectorizer.transform([query_processed])
            
            # コサイン類似度計算
            similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
            
            # 上位k件の結果を取得
            top_indices = np.argsort(similarities)[::-1][:k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.01:  # 最低類似度しきい値を下げる
                    results.append({
                        'content': self.documents[idx]['content'],
                        'metadata': {
                            'source': self.documents[idx]['source'],
                            'path': self.documents[idx]['path'],
                            'source_type': self.documents[idx]['source_type']
                        },
                        'similarity_score': float(similarities[idx]),
                        'source': self.documents[idx]['source']
                    })
            
            logger.info(f"🔍 '{query}' に対して {len(results)}件の結果を取得")
            return results
            
        except Exception as e:
            logger.error(f"❌ ナレッジ検索エラー: {e}")
            return []
    
    def generate_answer(self, query: str, max_context_length: int = 2000) -> Dict[str, Any]:
        """回答生成"""
        try:
            # 関連ナレッジ検索
            search_results = self.search_knowledge(query, k=3)
            
            if not search_results:
                return {
                    'answer': 'このクエリに関連する情報が見つかりませんでした。',
                    'sources': [],
                    'confidence': 0.0
                }
            
            # コンテキスト構築
            context_parts = []
            sources = []
            
            for result in search_results:
                context_parts.append(result['content'])
                sources.append({
                    'source': result['source'],
                    'similarity': result['similarity_score']
                })
            
            context = '\n\n'.join(context_parts)[:max_context_length]
            
            # 簡単な回答生成
            answer = self._generate_simple_answer(query, context, search_results)
            
            return {
                'answer': answer,
                'sources': sources,
                'confidence': search_results[0]['similarity_score'] if search_results else 0.0,
                'context_used': context[:500] + '...' if len(context) > 500 else context
            }
            
        except Exception as e:
            logger.error(f"❌ 回答生成エラー: {e}")
            return {
                'answer': f'回答生成中にエラーが発生しました: {e}',
                'sources': [],
                'confidence': 0.0
            }
    
    def _generate_simple_answer(self, query: str, context: str, search_results: List[Dict]) -> str:
        """簡単な回答生成"""
        if not search_results:
            return "関連する情報が見つかりませんでした。"
        
        best_result = search_results[0]
        answer_parts = [
            f"**質問:** {query}",
            "",
            f"**回答:**",
            best_result['content'][:800] + ('...' if len(best_result['content']) > 800 else ''),
            "",
            f"**ソース:** {best_result['metadata'].get('source', 'unknown')}",
            f"**信頼度:** {best_result['similarity_score']:.2f}"
        ]
        
        return '\n'.join(answer_parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """統計情報取得"""
        if not self.built:
            return {'error': 'ナレッジベースが構築されていません'}
        
        return {
            'total_documents': len(self.documents),
            'vectorizer_features': self.vectorizer.max_features,
            'wiki_paths': self.wiki_paths,
            'built': self.built
        }

def create_gradio_interface(rag_system: WikiRAGLiteSystem):
    """Gradio Webインターフェース作成"""
    
    def query_knowledge(question: str, max_results: int = 5):
        """ナレッジ質問処理"""
        if not question.strip():
            return "質問を入力してください。", ""
        
        try:
            result = rag_system.generate_answer(question)
            
            # 回答フォーマット
            answer = result['answer']
            
            # ソース情報
            sources_info = "**関連ソース:**\n"
            for i, source in enumerate(result['sources'][:3], 1):
                sources_info += f"{i}. {source['source']} (類似度: {source['similarity']:.3f})\n"
            
            return answer, sources_info
            
        except Exception as e:
            logger.error(f"❌ 質問処理エラー: {e}")
            return f"エラーが発生しました: {e}", ""
    
    def rebuild_knowledge_base():
        """ナレッジベース再構築"""
        try:
            success = rag_system.build_knowledge_base(force_rebuild=True)
            if success:
                stats = rag_system.get_statistics()
                return f"✅ ナレッジベースを再構築しました\n📊 総ドキュメント数: {stats.get('total_documents', 0)}"
            else:
                return "❌ ナレッジベース再構築に失敗しました"
        except Exception as e:
            return f"❌ エラー: {e}"
    
    def show_statistics():
        """統計情報表示"""
        stats = rag_system.get_statistics()
        if 'error' in stats:
            return f"❌ エラー: {stats['error']}"
        
        return f"""
📊 **WIKI RAG システム（軽量版）統計**

🔢 総ドキュメント数: {stats['total_documents']}
🔧 ベクトル特徴数: {stats['vectorizer_features']}
📚 WIKIパス: {', '.join(stats['wiki_paths'])}
✅ 構築済み: {stats['built']}
        """
    
    # Gradioインターフェース
    with gr.Blocks(title="AUTOCREATE WIKI RAG Lite", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🤖 AUTOCREATE WIKI RAG System (軽量版)
        
        **AI社長×無職CTO体制**による革新的なナレッジ検索システム（軽量版）
        
        TF-IDFベクトル化を使用した高速検索・回答システム
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                question_input = gr.Textbox(
                    label="質問",
                    placeholder="例: Gradioの使い方を教えてください",
                    lines=2
                )
                
                max_results = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    label="最大検索結果数"
                )
                
                submit_btn = gr.Button("🔍 質問する", variant="primary")
                
            with gr.Column(scale=1):
                rebuild_btn = gr.Button("🔄 ナレッジベース再構築")
                stats_btn = gr.Button("📊 統計情報")
        
        with gr.Row():
            with gr.Column():
                answer_output = gr.Markdown(label="回答")
                
            with gr.Column():
                sources_output = gr.Markdown(label="関連ソース")
        
        with gr.Row():
            system_output = gr.Markdown(label="システム情報")
        
        # イベントハンドラ
        submit_btn.click(
            query_knowledge,
            inputs=[question_input, max_results],
            outputs=[answer_output, sources_output]
        )
        
        rebuild_btn.click(
            rebuild_knowledge_base,
            outputs=[system_output]
        )
        
        stats_btn.click(
            show_statistics,
            outputs=[system_output]
        )
        
        # 初期統計表示
        interface.load(
            show_statistics,
            outputs=[system_output]
        )
    
    return interface

def main():
    """メイン実行"""
    logger.info("🚀 AUTOCREATE WIKI RAG システム（軽量版）を開始...")
    
    # RAGシステム初期化
    rag_system = WikiRAGLiteSystem()
    
    # ナレッジベース構築
    logger.info("📚 ナレッジベースを構築中...")
    if not rag_system.build_knowledge_base():
        logger.error("❌ ナレッジベース構築に失敗しました")
        return
    
    # Webインターフェース起動
    logger.info("🌐 Webインターフェースを起動中...")
    interface = create_gradio_interface(rag_system)
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
