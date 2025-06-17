#!/usr/bin/env python3
"""
AUTOCREATE WIKI RAG Chat システム
- WIKI RAGをチャットインターフェースに統合
- 会話履歴機能付き
- 自然な対話形式での質問応答
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# パス設定
sys.path.append(str(Path(__file__).parent))

try:
    import gradio as gr
    from wiki_rag_lite import WikiRAGLiteSystem
except ImportError as e:
    print(f"❌ 依存関係エラー: {e}")
    sys.exit(1)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WikiRAGChatSystem:
    """WIKI RAG チャットシステム"""
    
    def __init__(self):
        """初期化"""
        self.rag_system = WikiRAGLiteSystem()
        self.chat_history = []
        
        # ナレッジベース構築
        logger.info("📚 ナレッジベースを構築中...")
        if not self.rag_system.build_knowledge_base():
            logger.error("❌ ナレッジベース構築に失敗しました")
        
        logger.info("🤖 WIKI RAG Chatシステムを初期化しました")
    
    def chat_response(self, message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
        """チャット応答処理"""
        if not message.strip():
            return "", history
        
        try:
            # RAGシステムで回答生成
            result = self.rag_system.generate_answer(message)
            
            if result['confidence'] > 0.01:
                # 関連情報が見つかった場合
                response = f"""**回答:**
{result['answer'][:800]}

**信頼度:** {result['confidence']:.3f}

**関連ソース:**
"""
                for i, source in enumerate(result['sources'][:2], 1):
                    response += f"{i}. {source['source']} (類似度: {source['similarity']:.3f})\n"
                
            else:
                # 関連情報が見つからない場合
                response = f"""申し訳ございませんが、「{message}」に関する情報がナレッジベースに見つかりませんでした。

以下のようなトピックについてお答えできます：
- AUTOCREATEプロジェクトについて
- Gradioの使い方
- AI視覚自動化システム
- ChromaDBとRAGシステム
- GitFlow・開発フロー

他にご質問がございましたら、お気軽にお聞きください！"""
            
            # 履歴に追加
            history.append([message, response])
            
            return "", history
            
        except Exception as e:
            error_response = f"申し訳ございません。処理中にエラーが発生しました: {e}"
            history.append([message, error_response])
            return "", history
    
    def clear_chat(self):
        """チャット履歴クリア"""
        return []

def create_chat_interface():
    """Gradio Chatインターフェース作成"""
    
    # RAG Chatシステム初期化
    chat_system = WikiRAGChatSystem()
    
    # Gradioインターフェース
    with gr.Blocks(
        title="AUTOCREATE WIKI RAG Chat",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .chat-message {
            font-size: 14px;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🤖 AUTOCREATE WIKI RAG Chat
        
        **AI社長×無職CTO体制**による革新的なナレッジチャットシステム
        
        既存のWIKIドキュメント（94文書）から、あなたの質問に自然な対話形式で回答します。
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("""
                ### 📚 利用可能なナレッジ
                - **AUTOCREATEプロジェクト概要**
                - **Gradio開発ガイド**
                - **AI視覚自動化システム**
                - **ChromaDB・RAGシステム**
                - **GitFlow・開発プロセス**
                - **技術ドキュメント全般**
                
                ### 💡 質問例
                - "AUTOCREATEの特徴は？"
                - "Gradioの使い方を教えて"
                - "AI社長について説明して"
                - "OCR+RPAシステムとは？"
                """)
            
            with gr.Column(scale=2):
                # チャットインターフェース
                chatbot = gr.Chatbot(
                    height=500,
                    show_label=False,
                    container=True,
                    bubble_full_width=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="質問を入力してください...",
                        show_label=False,
                        scale=4,
                        container=False
                    )
                    submit_btn = gr.Button("送信", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("チャットクリア", variant="secondary", size="sm")
                    stats_btn = gr.Button("統計情報", variant="secondary", size="sm")
        
        # 統計情報表示エリア
        stats_output = gr.Markdown(visible=False)
        
        # イベントハンドラ
        msg.submit(
            chat_system.chat_response,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )
        
        submit_btn.click(
            chat_system.chat_response,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )
        
        clear_btn.click(
            chat_system.clear_chat,
            outputs=[chatbot]
        )
        
        def show_stats():
            stats = chat_system.rag_system.get_statistics()
            if 'error' in stats:
                return gr.update(value=f"❌ エラー: {stats['error']}", visible=True)
            
            stats_text = f"""
📊 **ナレッジベース統計**
- 総ドキュメント数: {stats['total_documents']}
- ベクトル特徴数: {stats['vectorizer_features']}
- 構築済み: {stats['built']}
            """
            return gr.update(value=stats_text, visible=True)
        
        stats_btn.click(
            show_stats,
            outputs=[stats_output]
        )
        
        # 初期メッセージ
        interface.load(
            lambda: [["こんにちは！", "こんにちは！AUTOCREATEのWIKI RAGチャットシステムです。\n\nプロジェクトに関する質問や、技術的な疑問など、何でもお気軽にお聞きください！\n\n94文書のナレッジベースから、最適な回答をお探しします。🤖"]],
            outputs=[chatbot]
        )
    
    return interface

def main():
    """メイン実行"""
    logger.info("🚀 AUTOCREATE WIKI RAG Chat を起動中...")
    
    interface = create_chat_interface()
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
