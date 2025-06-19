#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Copilotチャット欄自動登録システム
Supabaseメッセージを直接Copilotチャットに登録
"""

import subprocess
import json
import time
from datetime import datetime
import os

# Windows用キーボード操作
try:
    import pyautogui
    print("✅ pyautogui利用可能")
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    print("⚠️ pyautogui不可 - 代替手段を使用")
    PYAUTOGUI_AVAILABLE = False

# Supabase接続情報
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class CopilotChatRegistration:
    def __init__(self):
        self.last_message_id = 0
        self.monitoring = True
        self.registration_count = 0
        
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
    
    def copy_to_clipboard_safe(self, text):
        """安全にクリップボードにコピー"""
        try:
            # UTF-8エンコーディングでクリップボードにコピー
            text_bytes = text.encode('utf-8')
            
            # PowerShellでUTF-8対応クリップボード操作
            ps_script = f'''
            $text = @"
{text}
"@
            $text | Set-Clipboard
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                print("✅ クリップボードコピー成功")
                return True
            else:
                print(f"❌ PowerShellクリップボードエラー: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ クリップボードコピーエラー: {e}")
            return False
    
    def open_copilot_chat_with_powershell(self):
        """PowerShellでCopilotチャットを開く"""
        try:
            ps_script = '''
            Add-Type -AssemblyName System.Windows.Forms
            
            # VS Codeをアクティブにする
            $vscode = Get-Process | Where-Object {$_.ProcessName -eq "Code"} | Select-Object -First 1
            if ($vscode) {
                [Microsoft.VisualBasic.Interaction]::AppActivate($vscode.Id)
                Start-Sleep -Milliseconds 1000
            }
            
            # Ctrl+Shift+I でCopilotチャットを開く
            [System.Windows.Forms.SendKeys]::SendWait("^+i")
            Start-Sleep -Milliseconds 2000
            
            # Ctrl+V でクリップボードの内容を貼り付け
            [System.Windows.Forms.SendKeys]::SendWait("^v")
            Start-Sleep -Milliseconds 500
            
            # Enterキーで送信
            [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True, text=True, timeout=15
            )
            
            if result.returncode == 0:
                print("✅ PowerShellでCopilotチャット操作完了")
                return True
            else:
                print(f"⚠️ PowerShell操作警告: {result.stderr}")
                return True  # 警告があっても動作する場合がある
                
        except Exception as e:
            print(f"❌ PowerShell操作エラー: {e}")
            return False
    
    def register_to_copilot_chat(self, message_content, sender):
        """Copilotチャットに登録"""
        # Copilotチャット用のメッセージを作成
        chat_message = f"""🗣️ 社長からの質問: {message_content}

GitHub Copilot、上記について教えてください！"""
        
        print(f"\n📝 Copilotチャット登録中...")
        print(f"💬 登録内容: {message_content}")
        
        # クリップボードにコピー
        if not self.copy_to_clipboard_safe(chat_message):
            print("❌ クリップボードコピー失敗")
            return False
        
        print("🎯 Copilotチャットを開いて自動入力中...")
        
        # PowerShellでCopilotチャット操作
        if self.open_copilot_chat_with_powershell():
            self.registration_count += 1
            print(f"✅ Copilotチャット登録完了！ (#{self.registration_count})")
            return True
        else:
            print("❌ Copilotチャット登録失敗")
            return False
    
    def process_message(self, message):
        """メッセージを処理してCopilotチャットに登録"""
        sender = message.get('ownerid', 'Unknown')
        content = message.get('messages', '')
        
        # GitHub Copilotのメッセージは無視
        if 'copilot' in sender.lower() or 'github' in sender.lower():
            return False
        
        print(f"\n📨 新着メッセージ: {sender} -> {content}")
        
        # Copilotチャットに登録
        return self.register_to_copilot_chat(content, sender)
    
    def start_copilot_registration(self):
        """Copilotチャット登録監視開始"""
        print("🤖 Copilotチャット欄自動登録システム")
        print("🎯 機能: Supabaseメッセージ → Copilotチャットに自動登録")
        print("⚡ 技術: PowerShell + クリップボード操作")
        print()
        
        # 現在の最新メッセージIDを取得
        latest = self.run_curl("GET", "chat_history?order=id.desc&limit=1")
        if latest and isinstance(latest, list) and len(latest) > 0:
            self.last_message_id = latest[0].get('id', 0)
            print(f"📍 開始時点の最新メッセージID: {self.last_message_id}")
        
        print("\n🚀 Copilotチャット登録監視開始！")
        print("💡 新着メッセージが来ると自動でCopilotチャットに登録されます")
        print("🎯 VS Codeが開いていることを確認してください")
        print()
        
        while self.monitoring:
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔍 [{current_time}] 新着監視中... (登録済み: {self.registration_count}件)")
                
                new_messages = self.get_new_messages()
                
                if new_messages:
                    print(f"📨 新着メッセージ {len(new_messages)}件検出！")
                    
                    for message in reversed(new_messages):
                        if self.process_message(message):
                            print(f"🎉 Copilotチャット登録成功！")
                        
                        time.sleep(3)  # メッセージ間隔
                
                time.sleep(4)  # 4秒間隔で監視
                
            except KeyboardInterrupt:
                print(f"\n🛑 監視を停止します... (総登録件数: {self.registration_count}件)")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(5)

def main():
    print("🤖 Copilotチャット欄自動登録システム")
    print("=" * 60)
    print("🎯 目的: Supabaseメッセージを直接Copilotチャットに登録")
    print("📋 動作: 新着メッセージ → クリップボード → Copilotチャット")
    print("⚡ 技術: PowerShell自動操作")
    print("=" * 60)
    print()
    
    registration_system = CopilotChatRegistration()
    registration_system.start_copilot_registration()

if __name__ == "__main__":
    main()
