#!/usr/bin/env python3
"""
AUTOCREATE株式会社 - Gradio OCR分析システム
AI社長×無職CTO体制による画像解析インターフェース

Features:
- スクリーンショット → GAS OCR API → 結果表示
- kinkaimasu.jp専用解析モード
- リアルタイム結果表示
- Colab対応
"""

import gradio as gr
import requests
import base64
import json
import io
from PIL import Image
import pandas as pd
from datetime import datetime
import os

class AutocreateOCRAnalyzer:
    def __init__(self, gas_api_url=None):
        """
        初期化
        Args:
            gas_api_url (str): GAS API URL
        """
        self.gas_api_url = gas_api_url or os.getenv('GAS_OCR_API_URL', '')
        self.analysis_history = []
    
    def analyze_image(self, image, analysis_type="general"):
        """
        画像をOCR解析
        Args:
            image: PIL Image または numpy array
            analysis_type (str): 'general' or 'kinkaimasu'
        Returns:
            dict: 解析結果
        """
        try:
            # PIL Imageに変換
            if hasattr(image, 'shape'):  # numpy array
                image = Image.fromarray(image)
            
            # Base64エンコード
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # GAS APIに送信
            payload = {
                'image': base64_image,
                'fileName': f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png',
                'type': analysis_type
            }
            
            if not self.gas_api_url:
                return {
                    "success": False,
                    "error": "GAS API URLが設定されていません",
                    "timestamp": datetime.now().isoformat()
                }
            
            response = requests.post(self.gas_api_url, data=payload, timeout=30)
            result = response.json()
            
            # 履歴に追加
            self.analysis_history.append({
                'timestamp': datetime.now(),
                'type': analysis_type,
                'result': result
            })
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"解析エラー: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def format_analysis_result(self, result):
        """
        解析結果を整形して表示用テキストに変換
        Args:
            result (dict): GAS APIからの結果
        Returns:
            str: 整形されたテキスト
        """
        if not result.get('success'):
            return f"❌ エラー: {result.get('error', '不明なエラー')}"
        
        data = result.get('data', {})
        
        # 基本情報
        output = [
            "🎯 **AUTOCREATE株式会社 OCR解析結果**",
            f"📅 解析時刻: {data.get('timestamp', 'N/A')}",
            f"🔍 解析タイプ: {data.get('type', 'general')}",
            f"📊 信頼度: {data.get('confidence', 0)}%",
            "",
            "📝 **抽出テキスト:**",
            f"```\n{data.get('ocrText', '').strip()}\n```",
            ""
        ]
        
        # 画面要素
        elements = data.get('elements', [])
        if elements:
            output.extend([
                "🖥️ **検出された画面要素:**",
                *[f"- {elem.get('type', 'unknown')}: {elem.get('text', '')}" for elem in elements[:10]],
                ""
            ])
        
        # キーワード
        keywords = data.get('keywords', [])
        if keywords:
            output.extend([
                "🔑 **抽出キーワード:**",
                f"{', '.join(keywords[:20])}",
                ""
            ])
        
        # kinkaimasu.jp専用分析
        if data.get('type') == 'kinkaimasu':
            output.extend([
                "💰 **kinkaimasu.jp専用分析:**",
                f"- サイト判定: {'✅ kinkaimasu.jpサイト' if data.get('isKinkamasuSite') else '❌ 異なるサイト'}",
            ])
            
            # 金価格情報
            gold_prices = data.get('goldPrices', [])
            if gold_prices:
                output.extend([
                    "- 金価格情報:",
                    *[f"  - {price.get('text', '')}" for price in gold_prices[:5]]
                ])
            
            # システム情報
            system_info = data.get('systemInfo', {})
            if system_info:
                output.extend([
                    "- システム情報:",
                    f"  - SSL対応: {'✅' if system_info.get('hasSSL') else '❌'}",
                    f"  - WordPress: {'✅' if system_info.get('hasWordpress') else '❌'}",
                    f"  - レスポンシブ: {'✅' if system_info.get('isResponsive') else '❌'}"
                ])
            
            # 改善提案
            improvements = data.get('improvements', [])
            if improvements:
                output.extend([
                    "",
                    "🚀 **改善提案:**",
                    *[f"- {imp.get('suggestion', '')} ({imp.get('priority', 'medium')}優先度)" 
                      for imp in improvements[:5]]
                ])
            
            # ビジネス価値
            business_value = data.get('businessValue', {})
            if business_value:
                output.extend([
                    "",
                    "📈 **ビジネス価値分析:**",
                    f"- スコア: {business_value.get('score', 0)}/100",
                    f"- 評価: {business_value.get('recommendation', 'N/A')}",
                    f"- 評価要因: {', '.join(business_value.get('factors', []))}"
                ])
        
        # サマリー
        if data.get('summary'):
            output.extend([
                "",
                "📋 **サマリー:**",
                data.get('summary', '')
            ])
        
        return "\n".join(output)
    
    def get_analysis_history_df(self):
        """
        解析履歴をDataFrameで返す
        Returns:
            pd.DataFrame: 解析履歴
        """
        if not self.analysis_history:
            return pd.DataFrame(columns=['時刻', 'タイプ', '成功', '信頼度'])
        
        history_data = []
        for item in self.analysis_history[-20:]:  # 最新20件
            result = item['result']
            data = result.get('data', {}) if result.get('success') else {}
            
            history_data.append({
                '時刻': item['timestamp'].strftime('%H:%M:%S'),
                'タイプ': item['type'],
                '成功': '✅' if result.get('success') else '❌',
                '信頼度': f"{data.get('confidence', 0)}%",
                'テキスト長': len(data.get('ocrText', '')),
                '要素数': len(data.get('elements', []))
            })
        
        return pd.DataFrame(history_data)

# グローバルアナライザーインスタンス
analyzer = AutocreateOCRAnalyzer()

def analyze_screenshot(image, analysis_type):
    """Gradio用の解析関数"""
    if image is None:
        return "画像をアップロードしてください。", pd.DataFrame()
    
    result = analyzer.analyze_image(image, analysis_type)
    formatted_result = analyzer.format_analysis_result(result)
    history_df = analyzer.get_analysis_history_df()
    
    return formatted_result, history_df

def set_gas_api_url(url):
    """GAS API URLを設定"""
    analyzer.gas_api_url = url.strip()
    return f"✅ GAS API URL設定完了: {url[:50]}{'...' if len(url) > 50 else ''}"

# Gradioインターフェース構築
def create_gradio_interface():
    """Gradioインターフェースを作成"""
    
    with gr.Blocks(
        title="AUTOCREATE株式会社 - AI視覚自動化システム",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        """
    ) as interface:
        
        # ヘッダー
        gr.HTML("""
        <div class="main-header">
            <h1>🏢 AUTOCREATE株式会社</h1>
            <h2>🤖 AI視覚自動化システム - OCR画像解析</h2>
            <p><strong>AI社長×無職CTO体制</strong> による革新的画像解析プラットフォーム</p>
        </div>
        """)
        
        with gr.Tab("🔍 OCR解析"):
            with gr.Row():
                with gr.Column(scale=1):
                    # 設定セクション
                    gr.Markdown("### ⚙️ API設定")
                    gas_url_input = gr.Textbox(
                        label="GAS API URL",
                        placeholder="https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec",
                        lines=2
                    )
                    set_url_btn = gr.Button("URL設定", variant="secondary")
                    url_status = gr.Textbox(label="設定状況", interactive=False)
                    
                    # 画像アップロード
                    gr.Markdown("### 📸 画像アップロード")
                    image_input = gr.Image(
                        label="解析したい画像",
                        type="pil",
                        height=300
                    )
                    
                    # 解析設定
                    analysis_type = gr.Radio(
                        choices=[
                            ("一般解析", "general"),
                            ("kinkaimasu.jp専用", "kinkaimasu")
                        ],
                        value="general",
                        label="解析タイプ"
                    )
                    
                    analyze_btn = gr.Button("🚀 OCR解析実行", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    # 結果表示
                    gr.Markdown("### 📊 解析結果")
                    result_output = gr.Markdown(
                        value="解析結果がここに表示されます...",
                        height=400
                    )
        
        with gr.Tab("📈 解析履歴"):
            gr.Markdown("### 📋 最近の解析履歴")
            history_df = gr.Dataframe(
                headers=['時刻', 'タイプ', '成功', '信頼度', 'テキスト長', '要素数'],
                interactive=False
            )
            refresh_history_btn = gr.Button("🔄 履歴更新")
        
        with gr.Tab("ℹ️ システム情報"):
            gr.Markdown("""
            ### 🏢 AUTOCREATE株式会社 AI視覚自動化システム
            
            #### 🎯 システム概要
            - **AI社長×無職CTO体制**による革新的な画像解析システム
            - Google Apps Script OCR機能を活用した高精度テキスト抽出
            - kinkaimasu.jp専用解析機能で業界特化型分析を実現
            
            #### 🚀 主要機能
            1. **画像OCR解析** - Google Docs OCR APIによる高精度テキスト抽出
            2. **要素検出** - ボタン、入力フィールド、リンクの自動認識
            3. **キーワード抽出** - ビジネス重要キーワードの自動抽出
            4. **システム分析** - WordPress、SSL、レスポンシブ対応の検出
            5. **改善提案** - AI視点での具体的改善アドバイス
            
            #### 🔧 技術スタック
            - **フロントエンド**: Gradio (Python)
            - **バックエンド**: Google Apps Script
            - **OCRエンジン**: Google Docs OCR API
            - **データ保存**: Google Spreadsheet
            - **画像処理**: PIL (Python Imaging Library)
            
            #### 💡 使用方法
            1. 上部の「API設定」でGAS URLを設定
            2. 解析したい画像をアップロード
            3. 解析タイプを選択（一般 or kinkaimasu.jp専用）
            4. 「OCR解析実行」ボタンをクリック
            5. 結果を確認・活用
            
            #### 🏛️ AI社長の理念
            > **「これからはシステムは重要でなく、AIと共存してアイデア・知恵・データをどう活かすか、それが入ったシステムが大事」**
            """)
        
        # イベントハンドラー
        set_url_btn.click(
            fn=set_gas_api_url,
            inputs=[gas_url_input],
            outputs=[url_status]
        )
        
        analyze_btn.click(
            fn=analyze_screenshot,
            inputs=[image_input, analysis_type],
            outputs=[result_output, history_df]
        )
        
        refresh_history_btn.click(
            fn=lambda: analyzer.get_analysis_history_df(),
            inputs=[],
            outputs=[history_df]
        )
    
    return interface

if __name__ == "__main__":
    # Gradioアプリ起動
    interface = create_gradio_interface()
    
    # 起動設定
    launch_kwargs = {
        "server_name": "0.0.0.0",
        "server_port": 7860,
        "share": True,  # Colab対応
        "debug": True
    }
    
    # 環境変数でポート変更可能
    if os.getenv('PORT'):
        launch_kwargs['server_port'] = int(os.getenv('PORT'))
    
    print("🚀 AUTOCREATE株式会社 AI視覚自動化システム 起動中...")
    print("🏛️ AI社長×無職CTO体制による画像解析プラットフォーム")
    
    interface.launch(**launch_kwargs)
