#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖱️ Python画面操作 自動入力システム
pyautoguiを使ってブラウザの入力欄に自動でメッセージを入力
"""

import time
import subprocess
import json
from datetime import datetime

try:
    import pyautogui
    print("✅ pyautogui利用可能")
except ImportError:
    print("❌ pyautoguiがインストールされていません")
    print("📦 インストール中...")
    subprocess.run(["pip", "install", "pyautogui"], check=True)
    import pyautogui
    print("✅ pyautoguiインストール完了")

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class AutoInputSystem:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        # 安全設定
        pyautogui.FAILSAFE = True  # マウスを画面左上角に移動すると緊急停止
        pyautogui.PAUSE = 0.5  # 操作間の待機時間
        
    def setup_safety_check(self):
        """安全確認とセットアップ"""
        print("🛡️ 安全設定確認")
        print("⚠️ 緊急停止: マウスを画面左上角(0,0)に移動")
        print("⏰ 5秒後に開始します...")
        
        for i in range(5, 0, -1):
            print(f"⏰ {i}秒...")
            time.sleep(1)
        
        print("🚀 自動入力システム開始！")
        
    def run_curl(self, method, endpoint, data=None):
        """curlでSupabase APIを呼び出し"""
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        
        cmd = [
            "curl", "-s", "-X", method, url,
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            "-H", f"apikey: {SUPABASE_ANON_KEY}"
        ]
        
        if data:
            cmd.extend(["-d", json.dumps(data)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0 and result.stdout:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return None
            return None
        except Exception as e:
            print(f"❌ API呼び出しエラー: {e}")
            return None
    
    def get_new_messages(self):
        """新着メッセージを取得"""
        result = self.run_curl("GET", f"chat_history?order=id.desc&limit=5")
        
        if result and isinstance(result, list):
            new_messages = []
            for msg in result:
                msg_id = msg.get('id', 0)
                if msg_id > self.last_message_id:
                    new_messages.append(msg)
            
            if new_messages:
                self.last_message_id = max(msg.get('id', 0) for msg in new_messages)
            
            return new_messages
        return []
    
    def generate_response(self, message_content):
        """メッセージに対する応答を生成"""
        content = message_content.lower()
        
        responses = {
            "おはよう": "🌅 おはようございます！素晴らしい一日にしましょう！",
            "こんにちは": "👋 こんにちは！お疲れ様です！",
            "進捗": "📈 プロジェクトは順調に進んでいます！完成度85%です。",
            "売上": "💰 今月の売上は前月比120%と絶好調です！",
            "会議": "📅 次の会議は14時からです。資料準備完了しています。",
            "テスト": "🧪 テストメッセージを受信しました！システム正常動作中です。"
        }
        
        for keyword, response in responses.items():
            if keyword in content:
                return response
        
        return f"🤖 メッセージ「{message_content}」を受信しました。GitHub Copilotが対応いたします！"
    
    def find_input_field(self):
        """入力欄を探してクリック"""
        print("🔍 画面上の入力欄を探しています...")
        
        # 一般的な入力欄のテキストパターンを検索
        input_patterns = [
            "メッセージを入力",
            "Type a message",
            "Enter message",
            "メッセージ",
            "チャット"
        ]
        
        for pattern in input_patterns:
            try:
                location = pyautogui.locateOnScreen(pattern, confidence=0.8)
                if location:
                    center = pyautogui.center(location)
                    pyautogui.click(center)
                    print(f"✅ 入力欄発見・クリック: {pattern}")
                    return True
            except:
                continue
        
        # パターンが見つからない場合は画面中央下部をクリック
        screen_width, screen_height = pyautogui.size()
        fallback_x = screen_width // 2
        fallback_y = int(screen_height * 0.8)  # 画面下部80%の位置
        
        print(f"⚠️ 入力欄自動検出失敗。フォールバック位置をクリック: ({fallback_x}, {fallback_y})")
        pyautogui.click(fallback_x, fallback_y)
        return True
    
    def type_response(self, response_text):
        """応答テキストを自動入力"""
        try:
            print(f"⌨️ 自動入力開始: {response_text}")
            
            # 入力欄を探してクリック
            self.find_input_field()
            time.sleep(0.5)
            
            # 既存のテキストをクリア
            pyautogui.hotkey('ctrl', 'a')  # 全選択
            time.sleep(0.2)
            
            # 応答テキストを入力
            pyautogui.write(response_text, interval=0.05)  # 文字間隔50ms
            time.sleep(0.5)
            
            # Enterキーで送信
            pyautogui.press('enter')
            
            print("✅ 自動入力完了")
            return True
            
        except Exception as e:
            print(f"❌ 自動入力エラー: {e}")
            return False
    
    def display_message_info(self, message):
        """新着メッセージ情報を表示"""
        print("\n" + "🎯" * 30)
        print("📨 新着メッセージ検出！")
        print("🎯" * 30)
        print(f"👤 送信者: {message.get('ownerid', 'Unknown')}")
        print(f"💬 内容: {message.get('messages', '')}")
        print(f"🕐 時刻: {message.get('created', '')}")
        print("🎯" * 30)
    
    def start_auto_input_monitoring(self):
        """自動入力監視システム開始"""
        print("🖱️ Python画面操作 自動入力システム")
        print("🎯 機能: Supabaseメッセージ検出 → 画面の入力欄に自動入力")
        print("🛡️ 安全機能: マウス左上角移動で緊急停止")
        
        self.setup_safety_check()
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        input_count = 0
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] 新着メッセージ監視中... (自動入力: {input_count}回)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        sender = message.get('ownerid', '').lower()
                        content = message.get('messages', '')
                        
                        # GitHub Copilotのメッセージは無視
                        if 'copilot' in sender or 'github' in sender:
                            continue
                        
                        # メッセージ情報表示
                        self.display_message_info(message)
                        
                        # 応答生成
                        response = self.generate_response(content)
                        print(f"🤖 生成された応答: {response}")
                        
                        # 画面操作で自動入力
                        if self.type_response(response):
                            input_count += 1
                            print(f"✅ 自動入力成功 (#{input_count})")
                        else:
                            print("❌ 自動入力失敗")
                        
                        time.sleep(2)  # メッセージ間隔
                
                time.sleep(3)  # 3秒間隔で監視
                
            except pyautogui.FailSafeException:
                print("\n🛑 緊急停止が実行されました（マウスが左上角に移動）")
                break
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総自動入力: {input_count}回)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(5)

def main():
    print("🖱️ Python画面操作 自動入力システム")
    print("📋 使用方法:")
    print("1. ブラウザでチャットページを開いてください")
    print("2. このシステムを起動します")
    print("3. Supabaseに新着メッセージが来ると自動で入力欄に応答を入力します")
    print()
    
    auto_input = AutoInputSystem()
    auto_input.start_auto_input_monitoring()

if __name__ == "__main__":
    main()
