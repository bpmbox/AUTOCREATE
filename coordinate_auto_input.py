#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 座標取得 & Copilotチャット自動入力システム
コンソールの座標情報を取得してCopilotチャットに自動入力
"""

import subprocess
import json
import time
from datetime import datetime
import os

# pyautogui インポート
try:
    import pyautogui
    print("✅ pyautogui利用可能")
    PYAUTOGUI_AVAILABLE = True
    # pyautoguiの安全機能を設定
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
except ImportError:
    print("❌ pyautoguiインポートエラー")
    PYAUTOGUI_AVAILABLE = False

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class CoordinateAutoInputSystem:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        self.auto_input_count = 0
        self.target_coordinates = []
        
    def get_current_coordinates(self):
        """現在のマウス座標を取得"""
        if not PYAUTOGUI_AVAILABLE:
            return None
        
        try:
            x, y = pyautogui.position()
            return {"x": x, "y": y}
        except Exception as e:
            print(f"❌ 座標取得エラー: {e}")
            return None
    
    def scan_screen_coordinates(self):
        """画面の重要な座標をスキャン"""
        coordinates_info = []
        
        if not PYAUTOGUI_AVAILABLE:
            return coordinates_info
        
        try:
            # 現在のマウス位置
            current_pos = self.get_current_coordinates()
            if current_pos:
                coordinates_info.append(f"現在のマウス位置: X:{current_pos['x']} Y:{current_pos['y']}")
            
            # 画面サイズ
            screen_width, screen_height = pyautogui.size()
            coordinates_info.append(f"画面サイズ: {screen_width}x{screen_height}")
            
            # VS Codeウィンドウを探す
            try:
                vscode_icon = pyautogui.locateOnScreen('vscode_icon.png', confidence=0.8)
                if vscode_icon:
                    coordinates_info.append(f"VS Codeアイコン: X:{vscode_icon.left} Y:{vscode_icon.top}")
            except:
                coordinates_info.append("VS Codeアイコン: 検出できませんでした")
            
            return coordinates_info
            
        except Exception as e:
            print(f"❌ 画面スキャンエラー: {e}")
            return []
    
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
        result = self.run_curl("GET", f"chat_history?order=id.desc&limit=3")
        
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
    
    def auto_input_to_copilot_chat(self, message_content):
        """pyautoguiでCopilotチャットに自動入力"""
        if not PYAUTOGUI_AVAILABLE:
            print("❌ pyautogui利用不可")
            return False
        
        try:
            print("🎯 Copilotチャット自動入力開始...")
            
            # 座標情報を取得
            coordinates_info = self.scan_screen_coordinates()
            
            # Copilotチャット用メッセージを作成
            chat_message = f"""📍 座標情報付きメッセージ:

🗣️ 社長からの質問: {message_content}

📊 現在の座標情報:
{chr(10).join(coordinates_info)}

GitHub Copilot、上記について教えてください！"""
            
            print(f"📝 入力予定メッセージ: {message_content}")
            print(f"📍 座標情報: {len(coordinates_info)}件取得")
            
            # 1. Ctrl+Shift+I でCopilotチャットを開く
            print("🎯 Copilotチャットを開く...")
            pyautogui.hotkey('ctrl', 'shift', 'i')
            time.sleep(2)
            
            # 2. チャット入力欄に自動入力
            print("⌨️ メッセージ自動入力中...")
            pyautogui.write(chat_message, interval=0.01)
            time.sleep(1)
            
            # 3. Enterで送信
            print("📤 メッセージ送信...")
            pyautogui.press('enter')
            
            self.auto_input_count += 1
            print(f"✅ 自動入力完了！ (#{self.auto_input_count})")
            return True
            
        except Exception as e:
            print(f"❌ 自動入力エラー: {e}")
            return False
    
    def process_message_with_coordinates(self, message):
        """座標情報付きでメッセージを処理"""
        sender = message.get('ownerid', 'Unknown')
        content = message.get('messages', '')
        
        # GitHub Copilotのメッセージは無視
        if 'copilot' in sender.lower() or 'github' in sender.lower():
            return False
        
        print(f"\n📨 新着メッセージ: {sender} -> {content}")
        
        # 座標付き自動入力実行
        return self.auto_input_to_copilot_chat(content)
    
    def start_coordinate_monitoring(self):
        """座標監視システム開始"""
        print("🎯 座標取得 & Copilotチャット自動入力システム")
        print("📍 機能: コンソール座標情報をCopilotチャットに自動入力")
        print("⚡ 技術: pyautogui + 座標スキャン + 自動入力")
        print()
        
        if not PYAUTOGUI_AVAILABLE:
            print("❌ pyautogui利用不可 - システム終了")
            return
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        print("\n🚀 座標監視開始！")
        print("💡 新着メッセージが来ると座標情報付きでCopilotチャットに自動入力されます")
        print("🎯 VS Codeが表示されていることを確認してください")
        print()
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                current_coords = self.get_current_coordinates()
                coords_str = f"X:{current_coords['x']} Y:{current_coords['y']}" if current_coords else "取得失敗"
                
                print(f"🔍 [{current_time}] 座標監視中... 現在位置:{coords_str} (自動入力済み: {self.auto_input_count}件)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        if self.process_message_with_coordinates(message):
                            print(f"🎉 座標付き自動入力成功！")
                        
                        time.sleep(3)  # メッセージ間隔
                
                time.sleep(4)  # 4秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総自動入力件数: {self.auto_input_count}件)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(5)

def main():
    print("🎯 座標取得 & Copilotチャット自動入力システム")
    print("=" * 70)
    print("📍 目的: コンソールの座標情報をCopilotチャットに自動入力")
    print("📋 機能:")
    print("  - リアルタイム座標取得")
    print("  - 画面スキャン")
    print("  - pyautogui自動入力")
    print("  - VS Code自動検出")
    print("⚡ 技術: pyautogui + 座標システム")
    print("=" * 70)
    print()
    
    coordinate_system = CoordinateAutoInputSystem()
    coordinate_system.start_coordinate_monitoring()

if __name__ == "__main__":
    main()
