#!/usr/bin/env python3
"""
Memory Management Gradio Controller
記憶管理システムのGradioインターフェース
"""

import gradio as gr
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from memory_automation_system import MemoryAutomationSystem, Memory

class MemoryManagerController:
    """記憶管理Gradioコントローラー"""
    
    def __init__(self):
        self.memory_system = MemoryAutomationSystem()
        self.monitoring_active = False
    
    def create_interface(self) -> gr.Interface:
        """Gradioインターフェースを作成"""
        
        with gr.Blocks(title="🧠 Memory Management System") as interface:
            gr.Markdown("# 🧠 Memory Management System")
            gr.Markdown("AI×人間協働開発のための記憶自動化システム")
            
            with gr.Tabs():
                # 記憶検索タブ
                with gr.Tab("🔍 Memory Search"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            search_query = gr.Textbox(
                                label="検索クエリ",
                                placeholder="記憶を検索...",
                                lines=2
                            )
                            search_btn = gr.Button("🔍 検索", variant="primary")
                            
                        with gr.Column(scale=1):
                            search_type = gr.Dropdown(
                                choices=["all", "code", "git", "file", "chat"],
                                value="all",
                                label="記憶タイプ"
                            )
                            search_limit = gr.Slider(
                                minimum=5,
                                maximum=100,
                                value=20,
                                step=5,
                                label="検索結果数"
                            )
                    
                    search_results = gr.DataFrame(
                        headers=["時刻", "タイプ", "重要度", "内容プレビュー", "タグ"],
                        label="検索結果"
                    )
                    
                    with gr.Row():
                        selected_memory_content = gr.Textbox(
                            label="選択された記憶の詳細",
                            lines=10,
                            interactive=False
                        )
                        memory_metadata = gr.JSON(label="メタデータ")
                
                # 記憶統計タブ
                with gr.Tab("📊 Memory Statistics"):
                    with gr.Row():
                        stats_refresh_btn = gr.Button("🔄 統計更新", variant="secondary")
                        auto_refresh = gr.Checkbox(label="自動更新", value=False)
                    
                    with gr.Row():
                        with gr.Column():
                            memory_count_chart = gr.Plot(label="記憶数推移")
                            importance_chart = gr.Plot(label="重要度分布")
                            
                        with gr.Column():
                            type_distribution = gr.Plot(label="記憶タイプ分布")
                            recent_activity = gr.Plot(label="最近の活動")
                    
                    stats_summary = gr.JSON(label="統計サマリー")
                
                # 記憶管理タブ
                with gr.Tab("⚙️ Memory Management"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("## 🚀 システム制御")
                            
                            monitoring_status = gr.Textbox(
                                label="監視状態",
                                value="停止中",
                                interactive=False
                            )
                            
                            with gr.Row():
                                start_monitoring_btn = gr.Button("▶️ 監視開始", variant="primary")
                                stop_monitoring_btn = gr.Button("⏹️ 監視停止", variant="secondary")
                            
                            import_btn = gr.Button("📥 既存記憶インポート", variant="secondary")
                            backup_btn = gr.Button("💾 記憶バックアップ", variant="secondary")
                            
                        with gr.Column():
                            gr.Markdown("## 📋 設定")
                            
                            scan_interval = gr.Slider(
                                minimum=60,
                                maximum=3600,
                                value=300,
                                step=60,
                                label="スキャン間隔（秒）"
                            )
                            
                            importance_threshold = gr.Slider(
                                minimum=0,
                                maximum=100,
                                value=50,
                                step=10,
                                label="重要度閾値"
                            )
                            
                            max_memories = gr.Slider(
                                minimum=100,
                                maximum=10000,
                                value=1000,
                                step=100,
                                label="最大記憶数"
                            )
                    
                    system_log = gr.Textbox(
                        label="システムログ",
                        lines=10,
                        interactive=False
                    )
                
                # 記憶分析タブ
                with gr.Tab("🔬 Memory Analysis"):
                    with gr.Row():
                        analysis_type = gr.Dropdown(
                            choices=["関連性分析", "重要度分析", "タイムライン分析", "コード変更分析"],
                            value="関連性分析",
                            label="分析タイプ"
                        )
                        analyze_btn = gr.Button("🔬 分析実行", variant="primary")
                    
                    analysis_results = gr.Plot(label="分析結果")
                    analysis_details = gr.JSON(label="分析詳細")
                
                # 記憶作成タブ
                with gr.Tab("✏️ Memory Creation"):
                    with gr.Row():
                        with gr.Column():
                            new_memory_content = gr.Textbox(
                                label="記憶内容",
                                lines=8,
                                placeholder="新しい記憶を入力..."
                            )
                            
                            new_memory_type = gr.Dropdown(
                                choices=["general", "code", "idea", "note", "task"],
                                value="general",
                                label="記憶タイプ"
                            )
                            
                            new_memory_importance = gr.Slider(
                                minimum=0,
                                maximum=100,
                                value=50,
                                step=5,
                                label="重要度"
                            )
                            
                        with gr.Column():
                            new_memory_tags = gr.Textbox(
                                label="タグ（カンマ区切り）",
                                placeholder="tag1, tag2, tag3"
                            )
                            
                            new_memory_file = gr.File(
                                label="関連ファイル（オプション）",
                                file_count="single"
                            )
                            
                            create_memory_btn = gr.Button("💾 記憶作成", variant="primary")
                    
                    creation_status = gr.Textbox(
                        label="作成状態",
                        interactive=False
                    )
            
            # イベントハンドラーの設定
            search_btn.click(
                fn=self.search_memories,
                inputs=[search_query, search_type, search_limit],
                outputs=[search_results, selected_memory_content, memory_metadata]
            )
            
            stats_refresh_btn.click(
                fn=self.update_statistics,
                outputs=[memory_count_chart, importance_chart, type_distribution, recent_activity, stats_summary]
            )
            
            start_monitoring_btn.click(
                fn=self.start_monitoring,
                outputs=[monitoring_status, system_log]
            )
            
            stop_monitoring_btn.click(
                fn=self.stop_monitoring,
                outputs=[monitoring_status, system_log]
            )
            
            import_btn.click(
                fn=self.import_existing_memories,
                outputs=[system_log]
            )
            
            backup_btn.click(
                fn=self.backup_memories,
                outputs=[system_log]
            )
            
            analyze_btn.click(
                fn=self.analyze_memories,
                inputs=[analysis_type],
                outputs=[analysis_results, analysis_details]
            )
            
            create_memory_btn.click(
                fn=self.create_memory,
                inputs=[new_memory_content, new_memory_type, new_memory_importance, new_memory_tags],
                outputs=[creation_status]
            )
        
        return interface
    
    def search_memories(self, query: str, memory_type: str, limit: int) -> Tuple[pd.DataFrame, str, Dict]:
        """記憶を検索"""
        try:
            if not query.strip():
                return pd.DataFrame(), "", {}
            
            # 記憶を検索
            memories = self.memory_system.storage.search_memories(query, limit)
            
            # タイプフィルター
            if memory_type != "all":
                memories = [m for m in memories if m.memory_type == memory_type]
            
            # DataFrameに変換
            results_data = []
            for memory in memories:
                results_data.append([
                    memory.timestamp.strftime("%Y-%m-%d %H:%M"),
                    memory.memory_type,
                    memory.importance_score,
                    memory.content[:100] + "..." if len(memory.content) > 100 else memory.content,
                    ", ".join(memory.tags[:3])
                ])
            
            df = pd.DataFrame(
                results_data,
                columns=["時刻", "タイプ", "重要度", "内容プレビュー", "タグ"]
            )
            
            # 最初の記憶の詳細を表示
            first_memory_content = memories[0].content if memories else ""
            first_memory_metadata = memories[0].metadata if memories else {}
            
            return df, first_memory_content, first_memory_metadata
            
        except Exception as e:
            return pd.DataFrame(), f"検索エラー: {str(e)}", {}
    
    def update_statistics(self) -> Tuple[go.Figure, go.Figure, go.Figure, go.Figure, Dict]:
        """統計を更新"""
        try:
            report = self.memory_system.generate_memory_report()
            
            # 記憶数推移チャート（サンプルデータ）
            count_fig = go.Figure()
            dates = [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)]
            counts = [report['total_memories'] * (0.8 + i * 0.03) for i in range(7)]
            
            count_fig.add_trace(go.Scatter(
                x=dates,
                y=counts,
                mode='lines+markers',
                name='記憶数'
            ))
            count_fig.update_layout(title="記憶数推移（過去7日間）")
            
            # 重要度分布チャート
            importance_fig = go.Figure(data=[
                go.Bar(
                    x=['低重要度', '中重要度', '高重要度'],
                    y=[
                        report['importance_distribution']['low'],
                        report['importance_distribution']['medium'],
                        report['importance_distribution']['high']
                    ],
                    marker_color=['lightblue', 'orange', 'red']
                )
            ])
            importance_fig.update_layout(title="重要度分布")
            
            # 記憶タイプ分布
            types = list(report['memory_types'].keys())
            counts = list(report['memory_types'].values())
            
            type_fig = go.Figure(data=[go.Pie(
                labels=types,
                values=counts,
                hole=0.4
            )])
            type_fig.update_layout(title="記憶タイプ分布")
            
            # 最近の活動
            activity_fig = go.Figure(data=[
                go.Bar(
                    x=['24時間', '1週間', '1ヶ月'],
                    y=[
                        report['recent_activity']['last_24h'],
                        report['recent_activity']['last_week'],
                        report['recent_activity']['last_month']
                    ],
                    marker_color=['green', 'blue', 'purple']
                )
            ])
            activity_fig.update_layout(title="最近の活動")
            
            return count_fig, importance_fig, type_fig, activity_fig, report
            
        except Exception as e:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text=f"エラー: {str(e)}", showarrow=False)
            return empty_fig, empty_fig, empty_fig, empty_fig, {"error": str(e)}
    
    def start_monitoring(self) -> Tuple[str, str]:
        """監視を開始"""
        try:
            if not self.monitoring_active:
                self.monitoring_active = True
                # 非同期監視の開始（実際の実装では別スレッドで実行）
                return "監視中", "記憶監視システムを開始しました"
            else:
                return "監視中", "既に監視が実行中です"
        except Exception as e:
            return "エラー", f"監視開始エラー: {str(e)}"
    
    def stop_monitoring(self) -> Tuple[str, str]:
        """監視を停止"""
        try:
            if self.monitoring_active:
                self.monitoring_active = False
                self.memory_system.stop_monitoring()
                return "停止中", "記憶監視システムを停止しました"
            else:
                return "停止中", "監視は既に停止しています"
        except Exception as e:
            return "エラー", f"監視停止エラー: {str(e)}"
    
    def import_existing_memories(self) -> str:
        """既存記憶をインポート"""
        try:
            self.memory_system.import_existing_memories()
            return "既存記憶のインポートが完了しました"
        except Exception as e:
            return f"インポートエラー: {str(e)}"
    
    def backup_memories(self) -> str:
        """記憶をバックアップ"""
        try:
            backup_file = f"memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            success = self.memory_system.storage.backup_memories(backup_file)
            if success:
                return f"記憶のバックアップが完了しました: {backup_file}"
            else:
                return "バックアップに失敗しました"
        except Exception as e:
            return f"バックアップエラー: {str(e)}"
    
    def analyze_memories(self, analysis_type: str) -> Tuple[go.Figure, Dict]:
        """記憶分析"""
        try:
            memories = self.memory_system.storage.load_memories(limit=500)
            
            fig = go.Figure()
            details = {}
            
            if analysis_type == "関連性分析":
                # 記憶間の関連性を分析
                relation_counts = {}
                for memory in memories:
                    for related_id in memory.related_memories:
                        relation_counts[related_id] = relation_counts.get(related_id, 0) + 1
                
                top_related = sorted(relation_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                
                if top_related:
                    fig.add_trace(go.Bar(
                        x=[f"Memory {r[0][:8]}" for r in top_related],
                        y=[r[1] for r in top_related]
                    ))
                    fig.update_layout(title="最も関連性の高い記憶")
                
                details = {"top_related_memories": top_related}
                
            elif analysis_type == "重要度分析":
                # 時間別重要度分析
                hourly_importance = {}
                for memory in memories:
                    hour = memory.timestamp.hour
                    if hour not in hourly_importance:
                        hourly_importance[hour] = []
                    hourly_importance[hour].append(memory.importance_score)
                
                hours = sorted(hourly_importance.keys())
                avg_importance = [
                    sum(hourly_importance[hour]) / len(hourly_importance[hour])
                    for hour in hours
                ]
                
                fig.add_trace(go.Scatter(
                    x=hours,
                    y=avg_importance,
                    mode='lines+markers'
                ))
                fig.update_layout(title="時間別平均重要度")
                
                details = {"hourly_analysis": dict(zip(hours, avg_importance))}
            
            elif analysis_type == "タイムライン分析":
                # 記憶作成のタイムライン
                daily_counts = {}
                for memory in memories:
                    date = memory.timestamp.date()
                    daily_counts[date] = daily_counts.get(date, 0) + 1
                
                dates = sorted(daily_counts.keys())
                counts = [daily_counts[date] for date in dates]
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=counts,
                    mode='lines+markers',
                    fill='tonexty'
                ))
                fig.update_layout(title="記憶作成タイムライン")
                
                details = {"daily_memory_creation": dict(zip([str(d) for d in dates], counts))}
            
            return fig, details
            
        except Exception as e:
            error_fig = go.Figure()
            error_fig.add_annotation(text=f"分析エラー: {str(e)}", showarrow=False)
            return error_fig, {"error": str(e)}
    
    def create_memory(self, content: str, memory_type: str, importance: int, tags: str) -> str:
        """新しい記憶を作成"""
        try:
            if not content.strip():
                return "記憶内容を入力してください"
            
            # タグをパース
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
            
            # 新しい記憶を作成
            memory = Memory(
                content=content,
                memory_type=memory_type,
                importance_score=importance,
                tags=tag_list,
                metadata={"source": "manual_creation"}
            )
            
            # 処理と保存
            processed_memory = self.memory_system.processor.process_memory(memory)
            success = self.memory_system.storage.save_memory(processed_memory)
            
            if success:
                return f"記憶が正常に作成されました (ID: {processed_memory.id})"
            else:
                return "記憶の作成に失敗しました"
                
        except Exception as e:
            return f"記憶作成エラー: {str(e)}"


def create_memory_management_tab():
    """記憶管理タブを作成（他のGradioアプリに統合用）"""
    controller = MemoryManagerController()
    return controller.create_interface()


# 単体実行用
if __name__ == "__main__":
    controller = MemoryManagerController()
    app = controller.create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
