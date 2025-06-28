#!/usr/bin/env python3
"""
🚀 AI自動化システム - FastAPI バックグラウンドループ統合
=======================================================

FastAPIサーバー起動時に自動化システムのバックグラウンドループを開始
"""

import asyncio
import threading
import time
from datetime import datetime
from typing import Optional
from fastapi import BackgroundTasks
import os

class BackgroundAutomationService:
    """バックグラウンド自動化サービス"""
    
    def __init__(self):
        self.is_running = False
        self.background_thread: Optional[threading.Thread] = None
        self.automation_system = None
        self.loop_interval = 30  # 30秒間隔
        self.last_check = None
        
    def start_background_service(self):
        """バックグラウンドサービス開始"""
        if self.is_running:
            print("⚠️ バックグラウンドサービスは既に実行中です")
            return
            
        print("🚀 バックグラウンド自動化サービス開始中...")
        
        # 自動化システム初期化（オンラインモード）
        try:
            from tests.Feature.copilot_github_cli_automation import GitHubCopilotAutomation
            self.automation_system = GitHubCopilotAutomation(offline_mode=False)  # オンラインモードに変更
            print("✅ 自動化システム初期化完了 (オンラインモード)")
        except Exception as e:
            print(f"❌ 自動化システム初期化失敗: {e}")
            return
            
        # バックグラウンドスレッド開始
        self.is_running = True
        self.background_thread = threading.Thread(
            target=self._background_loop,
            daemon=True,
            name="AutomationBackgroundService"
        )
        self.background_thread.start()
        print("✅ バックグラウンドスレッド開始完了")
        
    def stop_background_service(self):
        """バックグラウンドサービス停止"""
        if not self.is_running:
            return
            
        print("🛑 バックグラウンド自動化サービス停止中...")
        self.is_running = False
        
        if self.background_thread and self.background_thread.is_alive():
            self.background_thread.join(timeout=5)
            
        print("✅ バックグラウンドサービス停止完了")
        
    def _background_loop(self):
        """バックグラウンドループ実行"""
        print(f"🔄 バックグラウンドループ開始 (間隔: {self.loop_interval}秒)")
        
        processed_count = 0
        
        while self.is_running:
            try:
                self.last_check = datetime.now()
                
                # Supabaseから新しい質問をチェック
                if hasattr(self.automation_system, 'check_for_new_questions'):
                    new_questions = self.automation_system.check_for_new_questions()
                    
                    if new_questions:
                        print(f"📨 新しい質問を検出: {len(new_questions)}件")
                        
                        for question in new_questions:
                            try:
                                # 自動化処理実行
                                result = self.automation_system.process_question_automatically(question)
                                if result:
                                    processed_count += 1
                                    print(f"✅ 質問処理完了 (累計: {processed_count}件)")
                                else:
                                    print("⚠️ 質問処理に失敗")
                                    
                            except Exception as e:
                                print(f"❌ 質問処理エラー: {e}")
                    else:
                        print("📭 新しい質問なし")
                else:
                    print("⚠️ check_for_new_questions メソッドが利用できません")
                    
            except Exception as e:
                print(f"❌ バックグラウンドループエラー: {e}")
                
            # 指定間隔で待機
            for _ in range(self.loop_interval):
                if not self.is_running:
                    break
                time.sleep(1)
                
        print("🔚 バックグラウンドループ終了")
        
    def get_status(self):
        """バックグラウンドサービス状態取得"""
        return {
            "is_running": self.is_running,
            "thread_alive": self.background_thread.is_alive() if self.background_thread else False,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "loop_interval": self.loop_interval,
            "automation_system_loaded": self.automation_system is not None
        }

# グローバルサービスインスタンス
background_service = BackgroundAutomationService()

def get_background_service():
    """バックグラウンドサービスインスタンス取得"""
    return background_service