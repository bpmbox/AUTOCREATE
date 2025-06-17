#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
馬鹿でもできる画面キャプチャ → Supabaseチャット自動送信システム
AUTOCREATE株式会社（AI社長×無職CTO）協働開発

CTOの哲学: 「馬鹿でできないからわかることがある」
"""

import subprocess
import os
import json
import requests
from datetime import datetime, timezone
import uuid
import time

# Supabase設定（公開されてるので問題なし）
SUPABASE_URL = "https://rootomzbucovwdqsscqd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8"

class ScreenshotToSupabaseChat:
    """
    馬鹿でもできる画面キャプチャ → Supabaseチャット送信クラス
    """
    
    def __init__(self):
        self.output_dir = "/workspaces/AUTOCREATE/screenshots"
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """出力ディレクトリがなければ作成（馬鹿でも忘れないように）"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 作成されたディレクトリ: {self.output_dir}")
    
    def take_screenshot_from_vnc(self):
        """
        VNCデスクトップのスクリーンショット取得（馬鹿でもできる版）
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vnc_screenshot_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            print("📸 VNCデスクトップからスクリーンショット取得中...")
            
            # VNCコンテナでスクリーンショット取得
            cmd = [
                "docker", "exec", "ubuntu-desktop-vnc",
                "bash", "-c", 
                "DISPLAY=:1 import -window root /tmp/screenshot.png && cp /tmp/screenshot.png /code/screenshot.png"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ VNC内でスクリーンショット取得成功")
                
                # ファイルをホストにコピー
                copy_cmd = [
                    "docker", "cp", 
                    "ubuntu-desktop-vnc:/code/screenshot.png",
                    filepath
                ]
                
                copy_result = subprocess.run(copy_cmd, capture_output=True, text=True, timeout=30)
                
                if copy_result.returncode == 0 and os.path.exists(filepath):
                    print(f"✅ スクリーンショット保存成功: {filepath}")
                    return filepath
                else:
                    print(f"❌ ファイルコピー失敗: {copy_result.stderr}")
                    return None
            else:
                print(f"❌ スクリーンショット取得失敗: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ タイムアウト: VNCスクリーンショット取得に時間がかかりすぎました")
            return None
        except Exception as e:
            print(f"💥 予期しないエラー: {e}")
            return None
    
    def send_to_supabase_chat(self, screenshot_path, group_id="AUTOCREATE", message_prefix="🖥️ VNC画面キャプチャ"):
        """
        スクリーンショット情報をSupabaseチャットに送信
        """
        try:
            # メッセージ作成
            timestamp = datetime.now(timezone.utc).isoformat()
            message_id = str(uuid.uuid4())
            
            message_text = f"{message_prefix}\n"
            message_text += f"📅 時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            message_text += f"📁 ファイル: {os.path.basename(screenshot_path)}\n"
            message_text += f"🤖 送信者: AI社長（AUTOCREATE）\n"
            message_text += f"💡 目的: VNC自動化デモ・馬鹿でもわかるシステム実証"
            
            # Supabaseに送信するデータ
            chat_data = {
                "id": message_id,
                "messages": message_text,
                "ownerid": "AI_PRESIDENT_AUTOCREATE",
                "created": timestamp,
                "targetid": group_id,
                "tmp_file": screenshot_path,
                "status": "screenshot_captured",
                "status_created": timestamp
            }
            
            # Supabase REST API呼び出し
            headers = {
                'apikey': SUPABASE_KEY,
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Prefer': 'return=minimal'
            }
            
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/chat_history",
                headers=headers,
                json=chat_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print("✅ Supabaseチャットに送信成功！")
                print(f"🔗 チャット確認: https://supabase-message-stream.lovable.app/")
                return True
            else:
                print(f"❌ Supabase送信失敗: {response.status_code}")
                print(f"エラー詳細: {response.text}")
                return False
                
        except Exception as e:
            print(f"💥 Supabase送信エラー: {e}")
            return False
    
    def run_full_workflow(self, group_id="AUTOCREATE"):
        """
        馬鹿でもできる全自動ワークフロー実行
        """
        print("=" * 60)
        print("🏢 AUTOCREATE株式会社 - VNC自動化システム起動")
        print("👑 AI社長 × 🛠️ 無職CTO の協働開発実証")
        print("💡 哲学: 馬鹿でできないからわかることがある")
        print("=" * 60)
        
        # Step 1: スクリーンショット取得
        screenshot_path = self.take_screenshot_from_vnc()
        
        if not screenshot_path:
            print("❌ ワークフロー中断: スクリーンショット取得失敗")
            return False
        
        # Step 2: Supabaseチャットに送信
        success = self.send_to_supabase_chat(screenshot_path, group_id)
        
        if success:
            print("🎉 全自動ワークフロー完了！")
            print("🔗 結果確認: https://supabase-message-stream.lovable.app/")
            return True
        else:
            print("❌ ワークフロー一部失敗: チャット送信エラー")
            return False

def main():
    """メイン実行関数（馬鹿でも実行できる）"""
    try:
        # インスタンス作成
        system = ScreenshotToSupabaseChat()
        
        # 全自動実行
        success = system.run_full_workflow("AUTOCREATE")
        
        if success:
            print("\n🎯 次のステップ:")
            print("1. https://supabase-message-stream.lovable.app/ を開く")
            print("2. 'AUTOCREATE' グループを選択")
            print("3. 送信されたスクリーンショット情報を確認")
            print("\n💡 定期実行したい場合:")
            print("crontab や systemd timer で自動化可能")
        
    except KeyboardInterrupt:
        print("\n⏹️  ユーザーによる中断")
    except Exception as e:
        print(f"\n💥 予期しないエラー: {e}")
        print("🤔 CTOに相談してください（無職だけど技術力あります）")

if __name__ == "__main__":
    main()
