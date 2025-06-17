#!/usr/bin/env python3
"""
Complete Port & Process Cleanup Script
======================================
複数ポート問題の完全解決用クリーンアップスクリプト
"""

import os
import subprocess
import signal
import time

def cleanup_all_gradio_processes():
    """全てのGradio関連プロセスを終了"""
    print("🧹 === COMPLETE GRADIO CLEANUP ===")
    
    # 1. Python関連プロセスを検索・終了
    processes_to_kill = [
        "python.*gradio",
        "python.*app\.py",
        "uvicorn",
        "fastapi",
        "gradio",
    ]
    
    for pattern in processes_to_kill:
        try:
            result = subprocess.run(
                f"pkill -f '{pattern}'", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                print(f"✅ Killed processes matching: {pattern}")
            else:
                print(f"ℹ️ No processes found for: {pattern}")
        except Exception as e:
            print(f"⚠️ Error killing {pattern}: {e}")
    
    # 2. ポート7860-7870を使用しているプロセスを終了
    ports_to_check = range(7860, 7871)
    
    for port in ports_to_check:
        try:
            # ポートを使用しているプロセスIDを取得
            result = subprocess.run(
                f"lsof -ti:{port} 2>/dev/null || fuser {port}/tcp 2>/dev/null | awk '{{print $1}}'",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid and pid.isdigit():
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            print(f"✅ Killed process {pid} using port {port}")
                        except ProcessLookupError:
                            print(f"ℹ️ Process {pid} already terminated")
                        except Exception as e:
                            print(f"⚠️ Error killing process {pid}: {e}")
        except Exception as e:
            print(f"⚠️ Error checking port {port}: {e}")
    
    # 3. 少し待機してから再確認
    print("⏱️ Waiting for processes to terminate...")
    time.sleep(2)
    
    # 4. 残っているプロセスを強制終了
    try:
        subprocess.run("pkill -9 -f 'python.*gradio'", shell=True)
        subprocess.run("pkill -9 -f 'uvicorn'", shell=True)
        print("✅ Force killed remaining processes")
    except:
        pass
    
    print("🧹 === CLEANUP COMPLETE ===")

if __name__ == "__main__":
    cleanup_all_gradio_processes()
    print("🚀 Ready for clean startup!")
