#!/usr/bin/env python3
"""
🎯 チャット欄テスト用座標登録システム

Copilot extensionのチャット欄で登録をテスト
"""

import pyautogui
import time
from datetime import datetime

class ChatTestRegistration:
    def __init__(self):
        self.coordinates = []
        self.test_messages = [
            "Hello",  # 英語テスト
            "Test message",
            "こんにちは",  # 日本語テスト開始
            "テストメッセージです",
            "座標登録のテストを行っています",
            "自動入力が成功しました",
            "ありがとうございました",
            "日本語入力テスト完了"
        ]
        
        # PyAutoGUI設定
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        print("🚀 チャット欄テスト用座標登録システム初期化完了")
        
    def show_menu(self):
        """メニュー表示"""
        print("\n" + "="*50)
        print("🎯 チャット欄テスト用座標登録システム")
        print("="*50)
        print("📋 コマンド:")
        print("   1 : 📍 座標記録（4秒待機）")
        print("   2 : 🚀 チャット欄に自動入力テスト")
        print("   3 : 📋 座標一覧表示")
        print("   4 : 🗑️  座標削除")
        print("   0 : 🚪 終了")
        print("="*50)
        print("💡 使用方法:")
        print("   1. Copilot extensionのチャット欄を開く")
        print("   2. チャット入力欄にマウスを置く")
        print("   3. コマンド1で座標記録")
        print("   4. コマンド2で自動入力テスト")
        print("="*50)
        
    def get_mouse_position(self):
        """マウス位置取得"""
        try:
            x, y = pyautogui.position()
            return x, y
        except Exception as e:
            print(f"❌ 位置取得エラー: {e}")
            return None, None
    
    def record_coordinate(self):
        """座標記録（4秒待機）"""
        print("📍 4秒後に座標記録します")
        print("🎯 Copilotチャット入力欄にマウスを移動してください")
        
        # 4秒カウントダウン
        for i in range(4, 0, -1):
            print(f"   記録まで {i}秒...")
            time.sleep(1)
        
        x, y = self.get_mouse_position()
        if x is not None and y is not None:
            timestamp = datetime.now().strftime('%H:%M:%S')
            coord_record = {
                'index': len(self.coordinates) + 1,
                'x': x,
                'y': y,
                'timestamp': timestamp            }
            
            self.coordinates.append(coord_record)
            print(f"✅ 座標#{len(self.coordinates)}記録: ({x}, {y}) at {timestamp}")
            
            # テストクリック
            try:
                pyautogui.click(x, y)
                print("   ✅ テストクリック成功")
                time.sleep(0.5)
            except Exception as e:
                print(f"   ❌ テストクリック失敗: {e}")
            
            return True
        return False
    
    def auto_input_chat(self):
        """チャット欄に自動入力テスト"""
        if not self.coordinates:
            print("⚠️ 記録された座標がありません")
            return
        
        print(f"\n🚀 チャット欄自動入力テスト開始")
        print("💡 記録した座標にテストメッセージを順番に入力します")
        
        # 最終確認
        print("⚠️  本当に自動入力を実行しますか？")
        confirmation = input("実行する場合は 'yes' を入力: ").strip().lower()
        
        if confirmation != 'yes':
            print("❌ 自動入力をキャンセルしました")
            return
        
        print("🔄 3秒後に自動入力開始...")
        for i in range(3, 0, -1):
            print(f"   開始まで {i}秒...")
            time.sleep(1)
        
        print("🚀 自動入力開始！")
        
        success_count = 0
        
        # 記録された座標（通常は1個）を使用
        coord = self.coordinates[0]  # 最初の座標を使用
        
        for i, message in enumerate(self.test_messages):
            try:
                print(f"\n📍 [{i+1}/{len(self.test_messages)}] メッセージ入力: '{message}'")
                
                # ステップ1: チャット欄をクリック（複数回確実に）
                print(f"   🎯 チャット欄クリック... ({coord['x']}, {coord['y']})")
                
                # フォーカス確保のため複数回クリック + 待機
                for click_attempt in range(5):  # 5回に増やす
                    pyautogui.click(coord['x'], coord['y'])
                    time.sleep(0.3)
                    print(f"   👆 クリック{click_attempt + 1}/5")
                
                # フォーカス確認のためTabキーを試す
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.click(coord['x'], coord['y'])  # 再度クリック
                time.sleep(0.8)  # 長めに待機
                print(f"   ✅ フォーカス確保完了")
                
                # ステップ2: 既存内容クリア（念のため）
                print(f"   🧹 内容クリア...")
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.2)
                pyautogui.press('delete')
                time.sleep(0.2)
                  # ステップ3: メッセージ入力（日本語対応版）
                print(f"   ⌨️  メッセージ入力中...")
                
                # 日本語文字を含むかチェック
                is_japanese = any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FAF' for char in message)
                
                if is_japanese:
                    print(f"   🇯🇵 日本語メッセージ検出")
                else:
                    print(f"   🔤 英語メッセージ")
                
                input_success = False
                
                # 方法1: クリップボード経由（日本語で最も確実）
                try:
                    import pyperclip
                    pyperclip.copy(message)
                    time.sleep(0.3)  # クリップボードコピー待機
                    pyautogui.hotkey('ctrl', 'v')
                    
                    if is_japanese:
                        time.sleep(2.0)  # 日本語の場合は長めに待機
                    else:
                        time.sleep(1.0)
                    
                    print(f"   ✅ クリップボード経由完了")
                    input_success = True
                except Exception as e:
                    print(f"   ⚠️ クリップボード失敗: {e}")
                    
                    # 方法2: 直接入力（英語のみ推奨）
                    if not is_japanese:
                        try:
                            pyautogui.write(message, interval=0.15)
                            time.sleep(1.0)
                            print(f"   ✅ 直接入力完了")
                            input_success = True
                        except Exception as e2:
                            print(f"   ⚠️ 直接入力失敗: {e2}")
                    else:
                        print(f"   ⚠️ 日本語のため直接入力をスキップ")
                
                if not input_success:
                    print(f"   ⚠️ 文字入力に失敗しました")
                    continue
                
                # ステップ4: 入力確認と送信オプション
                print(f"   📝 入力完了。チャット欄を確認してください")
                time.sleep(2)  # 確認時間
                
                send_message = input(f"   📤 メッセージ '{message}' を送信しますか？ (y/n/s=スキップ): ").strip().lower()
                if send_message == 'y':
                    print(f"   📤 送信中...")
                    pyautogui.press('enter')
                    time.sleep(3)  # 送信後の待機時間を長く
                    print(f"   ✅ 送信完了")
                elif send_message == 's':
                    print(f"   ⏩ このメッセージをスキップ")
                    # メッセージをクリアしてスキップ
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('delete')
                    time.sleep(0.5)
                    continue
                else:
                    print(f"   ⏸️  送信をスキップしました")
                    # メッセージをクリアしておく
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('delete')
                    time.sleep(0.5)
                
                success_count += 1
                print(f"   ✅ 完了！")
                
                # 次のメッセージ前に少し待機
                if i < len(self.test_messages) - 1:
                    time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ エラー: {e}")
                time.sleep(2)
        
        print(f"\n🎉 チャット欄自動入力テスト完了！")
        print(f"📊 結果: {success_count}/{len(self.test_messages)} 成功")
        
        return success_count
    
    def show_coordinates(self):
        """座標一覧表示"""
        if not self.coordinates:
            print("⚠️ 記録された座標がありません")
            return
        
        print(f"\n📍 記録座標一覧 ({len(self.coordinates)}個)")
        print("-" * 60)
        for i, coord in enumerate(self.coordinates):
            print(f"{coord['index']:2d}. ({coord['x']:4d}, {coord['y']:4d}) {coord['timestamp']}")
    
    def delete_coordinate(self):
        """座標削除"""
        if self.coordinates:
            removed = self.coordinates.pop()
            print(f"🗑️  座標削除: #{removed['index']} ({removed['x']}, {removed['y']})")
        else:
            print("⚠️ 削除する座標がありません")
    
    def run(self):
        """メインループ"""
        self.show_menu()
        
        while True:
            try:
                x, y = self.get_mouse_position()
                print(f"\n🖱️  現在のマウス位置: ({x}, {y})")
                print(f"📝 記録済み座標: {len(self.coordinates)}個")
                
                choice = input("コマンド入力 (1-4, 0=終了): ").strip()
                
                if choice == '1':
                    # 座標記録
                    self.record_coordinate()
                    
                elif choice == '2':
                    # チャット欄自動入力テスト
                    self.auto_input_chat()
                    
                elif choice == '3':
                    # 座標一覧表示
                    self.show_coordinates()
                    
                elif choice == '4':
                    # 座標削除
                    self.delete_coordinate()
                    
                elif choice == '0':
                    print("🚪 システム終了")
                    break
                    
                else:
                    print("❌ 無効なコマンドです")
                    
            except KeyboardInterrupt:
                print("\n⚠️ 中断されました")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
        
        # 終了時に座標表示
        if self.coordinates:
            print("\n📋 最終記録座標:")
            self.show_coordinates()
        
        print("✨ システム終了完了")

def main():
    print("🎯 チャット欄テスト用座標登録システム")
    print("\n✨ 特徴:")
    print("- Copilot extensionのチャット欄でテスト")
    print("- 座標記録してメッセージ自動入力")
    print("- 送信の可否を選択可能")
    
    print("\n📋 テスト手順:")
    print("1. VS CodeでCopilot extensionのチャットを開く")
    print("2. チャット入力欄にマウスを置く")
    print("3. コマンド1で座標記録")
    print("4. コマンド2で自動入力テスト実行")
    
    print("\n⚠️ 注意:")
    print("- チャット入力欄の中央にマウスを置く")
    print("- 送信するかどうかは選択できます")
    print("- マウス左上角移動で緊急停止")
    
    print("\n開始しますか？ (Enter で開始)")
    input()
    
    system = ChatTestRegistration()
    system.run()
    
    print("\n✨ お疲れ様でした！")

if __name__ == "__main__":
    main()
