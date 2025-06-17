#!/usr/bin/env python3
"""
AUTOCREATE WIKI RAGシステム
- 既存のWIKIコンテンツをベクトル化
- 自然言語での質問・回答システム
- ChromaDBを使用したベクトル検索
"""

import os
import sys
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# 依存関係のインポート
try:
    import chromadb
    from chromadb.config import Settings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain.schema import Document
    import gradio as gr
    import numpy as np
    import pandas as pd
    import markdown
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ 依存関係エラー: {e}")
    print("📦 以下のコマンドで依存関係をインストールしてください:")
    print("pip install -r requirements_wiki_rag.txt")
    sys.exit(1)

# 環境変数の読み込み
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/AUTOCREATE/wiki_rag.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class WikiRAGSystem:
    """WIKI RAGシステム"""
    
    def __init__(self, wiki_paths: List[str] = None, chroma_path: str = None):
        """初期化"""
        self.wiki_paths = wiki_paths or [
            "/workspaces/AUTOCREATE/wikigit",
            "/workspaces/AUTOCREATE/AUTOCREATE.wiki",
            "/workspaces/AUTOCREATE/docs"
        ]
        self.chroma_path = chroma_path or "/workspaces/AUTOCREATE/chroma/wiki_rag"
        self.collection_name = "wiki_knowledge"
        
        # テキスト分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", "。", ".", " ", ""]
        )
        
        # 埋め込みモデル（軽量で認証不要）
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # ChromaDB設定
        self.chroma_client = None
        self.vectorstore = None
        
        logger.info("🚀 WIKI RAGシステムを初期化しました")
    
    def initialize_chroma(self):
        """ChromaDB初期化"""
        try:
            # ChromaDBクライアント作成
            os.makedirs(self.chroma_path, exist_ok=True)
            
            self.chroma_client = chromadb.PersistentClient(
                path=self.chroma_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # コレクション作成・取得
            try:
                collection = self.chroma_client.get_collection(name=self.collection_name)
                logger.info(f"✅ 既存コレクション '{self.collection_name}' を取得")
            except:
                collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "AUTOCREATE WIKI Knowledge Base"}
                )
                logger.info(f"🆕 新規コレクション '{self.collection_name}' を作成")
            
            # LangChain Vectorstore作成
            self.vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ChromaDB初期化エラー: {e}")
            return False
    
    def load_wiki_documents(self) -> List[Document]:
        """WIKIドキュメント読み込み"""
        documents = []
        
        for wiki_path in self.wiki_paths:
            if not os.path.exists(wiki_path):
                logger.warning(f"⚠️ パスが存在しません: {wiki_path}")
                continue
            
            try:
                # Markdownファイル読み込み
                loader = DirectoryLoader(
                    wiki_path,
                    glob="**/*.md",
                    loader_cls=TextLoader,
                    loader_kwargs={'encoding': 'utf-8'},
                    recursive=True
                )
                
                wiki_docs = loader.load()
                
                # メタデータ追加
                for doc in wiki_docs:
                    doc.metadata.update({
                        'source_type': 'wiki',
                        'wiki_path': wiki_path,
                        'loaded_at': datetime.now().isoformat()
                    })
                
                documents.extend(wiki_docs)
                logger.info(f"📄 {len(wiki_docs)}個のドキュメントを読み込み: {wiki_path}")
                
            except Exception as e:
                logger.error(f"❌ ドキュメント読み込みエラー ({wiki_path}): {e}")
        
        logger.info(f"📚 合計 {len(documents)}個のWIKIドキュメントを読み込み")
        return documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """ドキュメント前処理"""
        processed_docs = []
        
        for doc in documents:
            try:
                # Markdownを HTMLに変換してからテキスト抽出
                html = markdown.markdown(doc.page_content)
                soup = BeautifulSoup(html, 'html.parser')
                clean_text = soup.get_text()
                
                # テキスト分割
                chunks = self.text_splitter.split_text(clean_text)
                
                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) > 50:  # 短すぎるチャンクは除外
                        chunk_doc = Document(
                            page_content=chunk,
                            metadata={
                                **doc.metadata,
                                'chunk_index': i,
                                'chunk_count': len(chunks)
                            }
                        )
                        processed_docs.append(chunk_doc)
                
            except Exception as e:
                logger.error(f"❌ ドキュメント処理エラー: {e}")
        
        logger.info(f"✂️ {len(processed_docs)}個のチャンクに分割")
        return processed_docs
    
    def build_knowledge_base(self, force_rebuild: bool = False):
        """ナレッジベース構築"""
        if not self.initialize_chroma():
            return False
        
        try:
            # 既存データ確認
            existing_count = self.vectorstore._collection.count()
            
            if existing_count > 0 and not force_rebuild:
                logger.info(f"📖 既存のナレッジベースを使用 ({existing_count}件)")
                return True
            
            if force_rebuild and existing_count > 0:
                logger.info("🔄 ナレッジベースを再構築中...")
                self.chroma_client.delete_collection(self.collection_name)
                self.initialize_chroma()
            
            # WIKIドキュメント読み込み・処理
            logger.info("📚 WIKIドキュメントを読み込み中...")
            documents = self.load_wiki_documents()
            
            if not documents:
                logger.error("❌ 読み込むドキュメントがありません")
                return False
            
            logger.info("⚙️ ドキュメントを処理中...")
            processed_docs = self.process_documents(documents)
            
            if not processed_docs:
                logger.error("❌ 処理されたドキュメントがありません")
                return False
            
            # ベクトル化・格納
            logger.info("🔄 ベクトル化・格納中...")
            self.vectorstore.add_documents(processed_docs)
            
            final_count = self.vectorstore._collection.count()
            logger.info(f"✅ ナレッジベース構築完了 ({final_count}件)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ナレッジベース構築エラー: {e}")
            return False
    
    def search_knowledge(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """ナレッジ検索"""
        if not self.vectorstore:
            logger.error("❌ ベクトルストアが初期化されていません")
            return []
        
        try:
            # 類似度検索
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'similarity_score': score,
                    'source': doc.metadata.get('source', 'unknown')
                })
            
            logger.info(f"🔍 '{query}' に対して {len(formatted_results)}件の結果を取得")
            return formatted_results
            
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
            
            # 簡単な回答生成（実際のLLMなしの場合）
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
        """簡単な回答生成（LLMなしバージョン）"""
        # 最も関連性の高い結果を基に回答を構築
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
        if not self.vectorstore:
            return {'error': 'ベクトルストアが初期化されていません'}
        
        try:
            count = self.vectorstore._collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection_name,
                'chroma_path': self.chroma_path,
                'wiki_paths': self.wiki_paths
            }
        except Exception as e:
            return {'error': str(e)}

def create_gradio_interface(rag_system: WikiRAGSystem):
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
📊 **WIKI RAGシステム統計**

🔢 総ドキュメント数: {stats['total_documents']}
📁 コレクション名: {stats['collection_name']}
💾 Chromaパス: {stats['chroma_path']}
📚 WIKIパス: {', '.join(stats['wiki_paths'])}
        """
    
    # Gradioインターフェース
    with gr.Blocks(title="AUTOCREATE WIKI RAG System", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🤖 AUTOCREATE WIKI RAG System
        
        既存のWIKIナレッジを使った自然言語Q&Aシステム
        
        ## 使い方
        1. 質問を自然言語で入力
        2. 関連するWIKI情報を自動検索
        3. 関連度の高い回答を取得
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                question_input = gr.Textbox(
                    label="質問",
                    placeholder="例: Gradioインターフェースの作成方法は？",
                    lines=2
                )
                
                max_results = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    label="最大結果数"
                )
                
                query_btn = gr.Button("🔍 質問する", variant="primary")
                
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
        query_btn.click(
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
    logger.info("🚀 AUTOCREATE WIKI RAGシステムを開始...")
    
    # RAGシステム初期化
    rag_system = WikiRAGSystem()
    
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
