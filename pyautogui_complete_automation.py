#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 pyautogui Copilotチャット自動入力システム（完全版）
座標取得 + 文字化け修正 + 自動Enter送信
"""

import subprocess
import json
import time
from datetime import datetime
import os

# pyautogui インポート
try:
    import pyautogui
    import pygetwindow as gw
    print("✅ pyautogui + pygetwindow利用可能")
    PYAUTOGUI_AVAILABLE = True
    
    # pyautogui設定
    pyautogui.FAILSAFE = True  # 左上角移動で緊急停止
    pyautogui.PAUSE = 0.1     # 操作間隔
    
except ImportError:
    print("❌ pyautoguiまたはpygetwindowがインストールされていません")
    PYAUTOGUI_AVAILABLE = False

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class PyAutoGUICopilotAutomation:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        self.automation_count = 0
        
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
    
    def get_current_coordinates(self):
        """現在のマウス座標を取得"""
        try:
            x, y = pyautogui.position()
            screen_size = pyautogui.size()
            return {
                'x': x,
                'y': y,
                'screen_width': screen_size.width,
                'screen_height': screen_size.height
            }
        except:
            return {'x': 0, 'y': 0, 'screen_width': 1920, 'screen_height': 1080}
    
    def find_vscode_window(self):
        """VS Codeウィンドウを見つけてアクティブにする"""
        try:
            vscode_windows = []
            for window in gw.getAllWindows():
                if 'visual studio code' in window.title.lower() or 'vscode' in window.title.lower():
                    vscode_windows.append(window)
            
            if vscode_windows:
                vscode_window = vscode_windows[0]
                vscode_window.activate()
                print(f"✅ VS Code ウィンドウアクティブ: {vscode_window.title}")
                time.sleep(1)
                return True
            else:
                print("⚠️ VS Codeウィンドウが見つかりません")
                return False
                
        except Exception as e:
            print(f"❌ ウィンドウ検索エラー: {e}")
            return False
    
    def copy_to_clipboard_utf8(self, text):
        """UTF-8対応クリップボードコピー（文字化け解決）"""
        try:
            # PowerShellでUTF-8対応コピー
            ps_script = f'''
            $text = @"
{text}
"@
            $text | Set-Clipboard
            '''
            subprocess.run(["powershell", "-Command", ps_script], check=True)
            return True
        except Exception as e:
            print(f"❌ クリップボードエラー: {e}")
            return False
    
    def automate_copilot_chat_complete(self, message_content, coordinates):
        """Copilotチャット完全自動化（座標情報付き）"""
        try:
            print("🤖 完全自動化開始...")
            
            # 座標情報付きメッセージを作成
            enhanced_message = f"""🗣️ 社長からの質問: {message_content}

📍 座標情報:
- マウス位置: X={coordinates['x']}, Y={coordinates['y']}
- 画面サイズ: {coordinates['screen_width']}x{coordinates['screen_height']}
- 検出時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

GitHub Copilot、上記について教えてください！"""
            
            print(f"📝 送信メッセージ: {message_content}")
            print(f"📍 座標: X={coordinates['x']}, Y={coordinates['y']}")
            
            # 1. VS Codeをアクティブにする
            if not self.find_vscode_window():
                print("⚠️ VS Codeを手動でアクティブにしてください")
                time.sleep(3)
            
            # 2. Ctrl+Shift+I でCopilotチャットを開く
            print("⌨️ Ctrl+Shift+I でCopilotチャット開始...")
            pyautogui.hotkey('ctrl', 'shift', 'i')
            time.sleep(2)
            
            # 3. メッセージをクリップボードにコピー
            print("📋 メッセージをクリップボードにコピー中...")
            if self.copy_to_clipboard_utf8(enhanced_message):
                print("✅ クリップボードコピー成功")
                
                # 4. Ctrl+V で貼り付け
                print("⌨️ Ctrl+V で貼り付け中...")
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                
                # 5. Enterキーで送信
                print("📤 Enterキーで自動送信中...")
                pyautogui.press('enter')
                time.sleep(1)
                
                self.automation_count += 1
                print(f"✅ 完全自動化成功！ (#{self.automation_count})")
                return True
            else:
                # フォールバック
                print("⚠️ フォールバック: 簡易メッセージ送信")
                pyautogui.write(f"Message: {message_content}", interval=0.05)
                pyautogui.press('enter')
                return True
            
        except pyautogui.FailSafeException:
            print("🛑 緊急停止が実行されました（マウスが左上角に移動）")
            return False
        except Exception as e:
            print(f"❌ 自動化エラー: {e}")
            return False
    
    def process_message_with_coordinates(self, message):
        """座標情報付きでメッセージを処理"""
        sender = message.get('ownerid', 'Unknown')
        content = message.get('messages', '')
        
        # GitHub Copilotのメッセージは無視
        if 'copilot' in sender.lower() or 'github' in sender.lower():
            return False
        
        print(f"\n📨 新着メッセージ: {sender} -> {content}")
        
        # 現在の座標を取得
        coordinates = self.get_current_coordinates()
        
        # 完全自動化実行
        return self.automate_copilot_chat_complete(content, coordinates)
    
    def start_coordinate_monitoring(self):
        """座標監視システム開始"""
        print("🤖 pyautogui Copilotチャット完全自動化システム")
        print("🎯 機能: 座標取得 + 文字化け修正 + 自動Enter送信")
        print("⚡ 技術: pyautogui + クリップボード + 座標追跡")
        print()
        
        if not PYAUTOGUI_AVAILABLE:
            print("❌ pyautogui利用不可 - システム終了")
            return
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        print("\n🚀 完全自動化監視開始！")
        print("💡 新着メッセージが来ると座標付きで自動化されます")
        print("🎯 VS Codeが表示されていることを確認してください")
        print("🛑 緊急停止: マウスを画面左上角に移動")
        print()
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                coords = self.get_current_coordinates()
                print(f"🔍 [{current_time}] 監視中... (X:{coords['x']}, Y:{coords['y']}) (自動化済み: {self.automation_count}件)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        if self.process_message_with_coordinates(message):
                            print(f"🎉 完全自動化成功！")
                        
                        time.sleep(3)  # メッセージ間隔
                
                time.sleep(4)  # 4秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総自動化件数: {self.automation_count}件)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(5)

def main():
    print("🤖 pyautogui Copilotチャット完全自動化システム")
    print("=" * 70)
    print("🎯 目的: 座標取得 + 文字化け修正 + 自動Enter送信")
    print("📋 機能:")
    print("  - リアルタイム座標追跡")
    print("  - UTF-8対応日本語入力")
    print("  - VS Code自動検出")
    print("  - 自動Enter送信")
    print("  - 緊急停止機能")
    print("⚡ 技術: pyautogui + PowerShell + 座標監視")
    print("=" * 70)
    print()
    
    automation_system = PyAutoGUICopilotAutomation()
    automation_system.start_coordinate_monitoring()

if __name__ == "__main__":
    main()
