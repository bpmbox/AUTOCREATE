#!/usr/bin/env python3
"""
🔥 ホットリロード実行システム

ファイル変更を監視して自動的にcopilot_direct_answer_fixed.pyを再起動
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

def watch_and_reload():
    """ファイル監視とホットリロード"""
    target_file = Path("tests/Feature/copilot_direct_answer_fixed.py")
    
    if not target_file.exists():
        print(f"❌ ファイルが見つかりません: {target_file}")
        return
    
    print("🔥 ホットリロード システム起動!")
    print(f"📁 監視対象: {target_file}")
    print("🔄 ファイル変更時に自動再起動します")
    print("="*50)
    
    last_modified = target_file.stat().st_mtime
    process = None
    
    # 初回実行
    print("🚀 初回実行中...")
    process = subprocess.Popen([sys.executable, str(target_file), "--auto"])
    
    try:
        while True:
            time.sleep(2)  # 2秒間隔でチェック
            
            try:
                current_modified = target_file.stat().st_mtime
                if current_modified > last_modified:
                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"\n🔥 {current_time} ファイル変更検出!")
                    
                    # 古いプロセスを終了
                    if process and process.poll() is None:
                        print("⏹️ 既存プロセス終了中...")
                        process.terminate()
                        process.wait()
                    
                    # 新しいプロセスを起動
                    print("🚀 新しいプロセス起動中...")
                    process = subprocess.Popen([sys.executable, str(target_file), "--auto"])
                    
                    last_modified = current_modified
                    print("✅ ホットリロード完了!")
                    print("="*30)
                    
            except Exception as e:
                print(f"⚠️ 監視エラー: {e}")
                
    except KeyboardInterrupt:
        print("\n\n⚠️ ホットリロード システム停止")
        if process and process.poll() is None:
            print("⏹️ プロセス終了中...")
            process.terminate()
            process.wait()
        print("✨ 完了!")

if __name__ == "__main__":
    watch_and_reload()
