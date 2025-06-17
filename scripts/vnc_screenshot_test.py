#!/usr/bin/env python3
"""
VNC画面キャプチャテスト

初心者でもわかる簡単なVNCスクリーンショット機能
AI社長 × CTO の協働開発
"""

import subprocess
import datetime
import os
from pathlib import Path

def test_vnc_screenshot():
    """VNC画面キャプチャのテスト実行"""
    print("🏢 AUTOCREATE VNC画面キャプチャテスト")
    print("AI社長 × 無職CTO の協働システム")
    print()
    
    # スクリーンショットディレクトリ作成
    screenshot_dir = Path("./screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    
    # タイムスタンプ
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = f"vnc_test_{timestamp}.png"
    screenshot_path = screenshot_dir / screenshot_file
    
    try:
        print("🖥️ VNCコンテナ状態確認...")
        
        # Dockerコンテナ確認
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=ubuntu-desktop-vnc"],
            capture_output=True, text=True
        )
        
        if "ubuntu-desktop-vnc" not in result.stdout:
            print("❌ VNCコンテナが見つかりません")
            print("   docker-compose -f docker-compose-vnc.yml up -d を実行してください")
            return False
        
        print("✅ VNCコンテナ稼働中")
        
        print(f"📸 スクリーンショット撮影中...")
        
        # VNCコンテナ内でスクリーンショット撮影
        screenshot_cmd = [
            "docker", "exec", "ubuntu-desktop-vnc",
            "bash", "-c", "DISPLAY=:1 scrot /tmp/screenshot_test.png"
        ]
        
        result = subprocess.run(screenshot_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ VNC内スクリーンショット成功")
        else:
            print(f"❌ VNC内スクリーンショット失敗: {result.stderr}")
            return False
        
        print("📂 ファイルコピー中...")
        
        # ファイルをホストにコピー
        copy_cmd = [
            "docker", "cp", 
            "ubuntu-desktop-vnc:/tmp/screenshot_test.png",
            str(screenshot_path)
        ]
        
        result = subprocess.run(copy_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ スクリーンショット保存成功: {screenshot_path}")
        else:
            print(f"❌ ファイルコピー失敗: {result.stderr}")
            return False
        
        # ファイルサイズ確認
        if screenshot_path.exists():
            file_size = screenshot_path.stat().st_size
            print(f"📊 ファイルサイズ: {file_size} bytes")
            
            if file_size > 1000:  # 1KB以上なら成功とみなす
                print("🎉 VNC画面キャプチャテスト成功！")
                print(f"🖼️ 保存先: {screenshot_path}")
                return True
            else:
                print("⚠️ ファイルサイズが小さすぎます（画面キャプチャ失敗の可能性）")
                return False
        else:
            print("❌ スクリーンショットファイルが見つかりません")
            return False
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return False

def main():
    """メイン関数"""
    success = test_vnc_screenshot()
    
    print()
    if success:
        print("🎯 テスト結果: 成功")
        print("💡 次のステップ: Supabaseログ連携、自動WIKI更新など")
    else:
        print("💥 テスト結果: 失敗")
        print("🔧 トラブルシューティング:")
        print("   1. VNCコンテナが起動しているか確認")
        print("   2. scrot がインストールされているか確認")
        print("   3. DISPLAY設定が正しいか確認")
    
    print()
    print("👥 AI社長 × CTO の協働開発、継続中！")

if __name__ == "__main__":
    main()
