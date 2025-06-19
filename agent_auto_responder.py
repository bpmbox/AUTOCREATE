#!/usr/bin/env python3
"""
Agent Auto Responder - Automatically responds "OK" when AI detects new questions
This script monitors the AI process output and confirms each question detection
"""

import subprocess
import sys
import time
import threading
import signal
from datetime import datetime

class AgentAutoResponder:
    def __init__(self):
        self.process = None
        self.running = False
        self.question_count = 0
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n[AGENT] Received signal {signum}. Shutting down gracefully...")
        self.running = False
        if self.process:
            self.process.terminate()
        sys.exit(0)
    
    def monitor_and_respond(self):
        """Monitor AI process output and auto-respond with OK"""
        try:
            # Start the AI monitoring process
            print("[AGENT] Starting AI monitoring process...")
            self.process = subprocess.Popen(
                ['python3', 'copilot_persistent_monitor.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.running = True
            print("[AGENT] AI monitoring process started. Waiting for questions...")
            print("[AGENT] I will automatically respond 'OK' for each new question detected.")
            print("-" * 80)
            
            # Monitor the output line by line
            for line in iter(self.process.stdout.readline, ''):
                if not self.running:
                    break
                    
                # Print the AI process output
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] {line.strip()}")
                
                # Check if AI detected a new question
                if "新しい質問を検出" in line or "New question detected" in line:
                    self.question_count += 1
                    print(f"[AGENT] ✅ OK - Question #{self.question_count} detected and confirmed!")
                    print("-" * 80)
                
                # Check if AI posted a response
                elif "応答を投稿しました" in line or "Response posted" in line:
                    print(f"[AGENT] ✅ OK - Response posted successfully!")
                    print("-" * 80)
                
                # Check for errors
                elif "エラー" in line or "Error" in line or "Exception" in line:
                    print(f"[AGENT] ⚠️  ERROR DETECTED: {line.strip()}")
                    print("-" * 80)
                    
        except KeyboardInterrupt:
            print("\n[AGENT] Monitoring stopped by user.")
        except Exception as e:
            print(f"[AGENT] Error in monitoring: {e}")
        finally:
            self.running = False
            if self.process:
                self.process.terminate()
                
    def start(self):
        """Start the agent auto responder"""
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("="*80)
        print("🤖 AGENT AUTO RESPONDER STARTED")
        print("="*80)
        print("[AGENT] Mission: Monitor AI process and confirm each question detection")
        print("[AGENT] Status: ACTIVE")
        print("[AGENT] Press Ctrl+C to stop")
        print("="*80)
        
        self.monitor_and_respond()

if __name__ == "__main__":
    agent = AgentAutoResponder()
    agent.start()
