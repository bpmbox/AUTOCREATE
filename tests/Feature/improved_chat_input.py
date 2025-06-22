#!/usr/bin/env python3
"""
🎯 改良版チャット欄自動入力システム

確実な文字入力のための最適化版
"""

import pyautogui
import time
import pyperclip
from datetime import datetime

class ImprovedChatInput:
    def __init__(self):
        self.coordinates = []
        
        # PyAutoGUI設定
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05  # より高速化
        
        print("🚀 改良版チャット入力システム初期化完了")
    
    def secure_focus_and_input(self, x, y, message):
        """確実なフォーカス確保と文字入力"""
        success = False
        
        print(f"   🎯 座標 ({x}, {y}) にフォーカス確保中...")
        
        # ステップ1: 確実なフォーカス確保
        for attempt in range(3):
            pyautogui.click(x, y)
            time.sleep(0.1)
        
        time.sleep(0.3)  # フォーカス安定待機
        
        # ステップ2: 内容クリア
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.2)
        
        # ステップ3: 文字入力（複数方法で試行）
        print(f"   ⌨️  '{message}' 入力中...")
        
        # 方法1: 直接入力
        try:
            pyautogui.write(message, interval=0.08)
            time.sleep(0.5)
            
            # 入力確認（簡易）
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            success = True
            print(f"   ✅ 直接入力成功")
            
        except Exception as e:
            print(f"   ⚠️ 直接入力失敗: {e}")
            
            # 方法2: クリップボード経由
            try:
                pyperclip.copy(message)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                success = True
                print(f"   ✅ クリップボード入力成功")
                
            except Exception as e2:
                print(f"   ❌ 全ての入力方法失敗: {e2}")
        
        return success
    
    def quick_test_input(self, x, y, test_message="Hello World"):
        """クイックテスト入力"""
        print(f"\n🚀 クイックテスト開始")
        print(f"📍 座標: ({x}, {y})")
        print(f"📝 メッセージ: '{test_message}'")
        
        countdown = 3
        for i in range(countdown, 0, -1):
            print(f"   開始まで {i}秒...")
            time.sleep(1)
        
        success = self.secure_focus_and_input(x, y, test_message)
        
        if success:
            print(f"🎉 クイックテスト成功！")
            
            # 送信確認
            send = input("📤 このメッセージを送信しますか？ (y/n): ").strip().lower()
            if send == 'y':
                pyautogui.press('enter')
                print("📤 送信完了")
            else:
                # クリア
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('delete')
                print("🧹 メッセージクリア完了")
        else:
            print("❌ クイックテスト失敗")
        
        return success

def main():
    print("🎯 改良版チャット欄自動入力システム")
    print("\n💡 特徴:")
    print("- より確実なフォーカス確保")
    print("- 複数入力方法の自動切替")
    print("- クイックテスト機能")
    
    print("\n📋 使用方法:")
    print("1. VS CodeでCopilotチャットを開く")
    print("2. チャット入力欄にマウスを置く")
    print("3. 座標を記録")
    print("4. クイックテストで動作確認")
    
    # 座標入力
    print("\n📍 座標入力:")
    try:
        x = int(input("X座標を入力: "))
        y = int(input("Y座標を入力: "))
    except ValueError:
        print("❌ 無効な座標です")
        return
    
    # メッセージ入力
    message = input("テストメッセージを入力 (空白でデフォルト): ").strip()
    if not message:
        message = "Hello from improved chat input!"
    
    # テスト実行
    system = ImprovedChatInput()
    system.quick_test_input(x, y, message)
    
    print("\n✨ お疲れ様でした！")

if __name__ == "__main__":
    main()
