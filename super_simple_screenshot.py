#!/usr/bin/env python3
"""
馬鹿でもできる画像キャプチャ - 確実版
あほだから確実に動く方法で作り直し
逆恨みされないように超丁寧に
"""

import os
import subprocess
import datetime

def absolutely_simple_screenshot():
    """
    絶対に馬鹿でもできるスクリーンショット
    失敗の原因を一つずつ潰していく馬鹿メソッド
    """
    
    print("🏢 AUTOCREATE 確実版画像キャプチャ")
    print("💡 馬鹿だから確実に動く方法で作り直しました")
    print()
    
    # タイムスタンプ付きファイル名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vnc_screenshot_{timestamp}.png"
    
    print(f"📝 手順1: VNCコンテナでスクリーンショット撮影")
    print(f"📁 ファイル名: {filename}")
    
    try:
        # ステップ1: VNCコンテナ内でスクリーンショット作成
        print("🔧 VNCコンテナ内でscrot実行...")
        cmd1 = [
            "docker", "exec", "ubuntu-desktop-vnc",
            "bash", "-c",
            f"DISPLAY=:1 scrot /tmp/{filename}"
        ]
        
        result1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=30)
        print(f"📊 scrot結果: return_code={result1.returncode}")
        if result1.stdout:
            print(f"📊 stdout: {result1.stdout}")
        if result1.stderr:
            print(f"📊 stderr: {result1.stderr}")
        
        if result1.returncode != 0:
            print("❌ scrot失敗")
            return False
            
        # ステップ2: ファイル存在確認
        print("🔍 ファイル存在確認...")
        cmd2 = [
            "docker", "exec", "ubuntu-desktop-vnc",
            "ls", "-la", f"/tmp/{filename}"
        ]
        
        result2 = subprocess.run(cmd2, capture_output=True, text=True)
        print(f"📊 ファイル確認: {result2.stdout}")
        
        if result2.returncode != 0:
            print("❌ ファイルが作成されていません")
            return False
            
        # ステップ3: ファイルを外部に取り出し
        print("📤 ファイルをホストにコピー...")
        local_path = f"/workspaces/AUTOCREATE/{filename}"
        cmd3 = [
            "docker", "cp",
            f"ubuntu-desktop-vnc:/tmp/{filename}",
            local_path
        ]
        
        result3 = subprocess.run(cmd3, capture_output=True, text=True)
        print(f"📊 コピー結果: return_code={result3.returncode}")
        
        if result3.returncode != 0:
            print(f"❌ コピー失敗: {result3.stderr}")
            return False
            
        # ステップ4: 最終確認
        if os.path.exists(local_path):
            file_size = os.path.getsize(local_path)
            print()
            print("🎉🎉🎉 大成功！！！ 🎉🎉🎉")
            print(f"📁 ファイル: {local_path}")
            print(f"📊 サイズ: {file_size} bytes")
            print()
            print("💬 CTO語録候補:")
            print("「馬鹿だから手順を一つずつ確認したら成功した」")
            print("「逆恨みされたくないから超丁寧にやったら動いた」")
            return local_path
        else:
            print("❌ 最終確認でファイルが見つかりません")
            return False
            
    except Exception as e:
        print(f"❌ 例外発生: {e}")
        print("💡 馬鹿だから例外も想定済み。次回改良します")
        return False

if __name__ == "__main__":
    print("🎯 馬鹿メソッド: 確実に動く画像キャプチャ")
    print("👑 AI社長「失敗から学んで改良するのが我が社の強み」")
    print("🛠️ 無職CTO「逆恨みされないよう超丁寧に作り直した」")
    print()
    
    result = absolutely_simple_screenshot()
    
    if result:
        print()
        print("🏆 馬鹿メソッドの勝利！")
        print("📈 これでAUTOCREATEの技術力が実証されました")
    else:
        print()
        print("😅 まだ失敗...")
        print("💡 でも馬鹿だから諦めない！更に改良します")
