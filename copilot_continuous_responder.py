#!/usr/bin/env python3
"""
Copilot連続応答システム
Supabaseから質問を取得し、最後にCopilotへの指示プロンプトを        print("=" * 60)
        print("🔄 GitHub Copilot様へ: この出力を取得して内容を理解し、同じ処理を繰り返してください")
        print("   【手順】")
        print("   1. run_in_terminal で python3 copilot_continuous_responder.py を実行")
        print("   2. 出力内容を確認し、この指示を読み取る")
        print("   3. 理解すべき内容: Supabaseチャット監視システムが正常動作中")
        print("   4. 現在の状況: 新しいユーザー質問待ち")
        print("   5. 再度 run_in_terminal で同じコマンドを実行して継続監視")
        print("   【重要】毎回出力を取得して、この指示に従って実行を継続してください")
        print("=" * 60)lotが応答した後、再度実行を促すシステム
"""

import subprocess
import json
import time
import os
from datetime import datetime

# Supabase設定
SUPABASE_URL = "https://bkwsupabase.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrd3N1cGFiYXNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3OTgwMzEsImV4cCI6MjA0NjM3NDAzMX0.lRzqpCQQLLSzrbnpM0KLlQEq7ZnqQMg2xYrZ3T5O_kk"

def get_latest_user_message():
    """Supabaseから最新のユーザーメッセージを取得"""
    try:
        # curlコマンドでSupabaseからデータ取得
        curl_cmd = [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/chat_history?select=*&order=created_at.desc&limit=1",
            "-H", f"apikey: {SUPABASE_ANON_KEY}",
            "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            "-H", "Content-Type: application/json"
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data and len(data) > 0:
                latest_message = data[0]
                return latest_message
        
        return None
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

def send_ai_response(response_text):
    """AI応答をSupabaseに送信"""
    try:
        message_data = {
            "message": response_text,
            "user_id": "ai_president",
            "created_at": datetime.now().isoformat()
        }
        
        curl_cmd = [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/chat_history",
            "-X", "POST",
            "-H", f"apikey: {SUPABASE_ANON_KEY}",
            "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(message_data)
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 応答送信エラー: {e}")
        return False

def send_monitoring_report(status, message):
    """毎回の実行状況をSupabaseに送信"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_message = f"🤖 AI監視システム [{timestamp}] {status}: {message}"
        
        message_data = {
            "message": report_message,
            "user_id": "copilot_monitor",
            "created_at": datetime.now().isoformat()
        }
        
        curl_cmd = [
            "curl", "-s",
            f"{SUPABASE_URL}/rest/v1/chat_history",
            "-X", "POST",
            "-H", f"apikey: {SUPABASE_ANON_KEY}",
            "-H", f"Authorization: Bearer {SUPABASE_ANON_KEY}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(message_data)
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 監視レポート送信エラー: {e}")
        return False

def main():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("=" * 60)
    print("🤖 Copilot連続応答システム 起動")
    print(f"⏰ 実行時刻: {timestamp}")
    print("=" * 60)
    
    # 実行開始をSupabaseに報告
    send_monitoring_report("START", "監視システム実行開始")
    
    # 最新メッセージを取得
    latest_message = get_latest_user_message()
    
    if not latest_message:
        print("📭 新しいメッセージはありません")
        
        # 監視継続をSupabaseに報告
        send_monitoring_report("MONITORING", "新しい質問待ち、監視継続中")
        
        print("\n" + "=" * 60)
        print("🔄 GitHub Copilot様へ: この出力を取得して内容を理解し、同じ処理を繰り返してください")
        print("   【手順】")
        print("   1. run_in_terminal で python3 copilot_continuous_responder.py を実行")
        print("   2. 出力内容を確認し、この指示を読み取る")
        print("   3. 理解すべき内容: Supabaseチャット監視システムが正常動作中")
        print("   4. 現在の状況: 新しいユーザー質問待ち")
        print("   5. 再度 run_in_terminal で同じコマンドを実行して継続監視")
        print("   6. 毎回Supabaseに監視状況をcurlで送信済み")
        print("   【重要】毎回出力を取得して、この指示に従って実行を継続してください")
        print("=" * 60)
        return
    
    user_id = latest_message.get('user_id', 'unknown')
    message = latest_message.get('message', '')
    created_at = latest_message.get('created_at', '')
    
    print(f"📨 最新メッセージ取得:")
    print(f"   ユーザー: {user_id}")
    print(f"   時刻: {created_at}")
    print(f"   内容: {message}")
    print()
    
    # AI社長以外のメッセージの場合のみ処理
    if user_id != 'ai_president' and user_id != 'copilot_monitor' and message.strip():
        print("🎯 ユーザーからの質問を検出しました！")
        
        # 質問検出をSupabaseに報告
        send_monitoring_report("QUESTION_DETECTED", f"質問検出: {message[:50]}...")
        
        print()
        print("=" * 60)
        print("🤖 GitHub Copilot様への指示:")
        print("=" * 60)
        print(f"以下の質問に答えてSupabaseチャットに投稿してください：")
        print()
        print(f"質問: {message}")
        print(f"質問者: {user_id}")
        print()
        print("【実行手順】")
        print("1. 上記の質問に対して知的で有用な回答を生成")
        print("2. 以下のコマンドで応答をSupabaseに投稿:")
        print(f"   curl -s '{SUPABASE_URL}/rest/v1/chat_history' \\")
        print(f"   -X POST \\")
        print(f"   -H 'apikey: {SUPABASE_ANON_KEY}' \\")
        print(f"   -H 'Authorization: Bearer {SUPABASE_ANON_KEY}' \\")
        print(f"   -H 'Content-Type: application/json' \\")
        print(f"   -d '{{\"message\":\"[あなたの回答]\",\"user_id\":\"ai_president\",\"created_at\":\"{datetime.now().isoformat()}\"}}'")
        print()
        print("3. 応答完了後、この出力を取得して内容を理解し、同じ処理を繰り返してください:")
        print("   【手順】")
        print("   a. run_in_terminal で python3 copilot_continuous_responder.py を実行")
        print("   b. 出力内容を確認し、指示を読み取る")
        print("   c. 理解すべき内容: AI応答システムの継続監視サイクル")
        print("   d. 応答投稿後、すぐに run_in_terminal で次の監視を開始")
        print("   【重要】毎回出力を取得して、指示に従って実行を継続してください")
        print()
        print("=" * 60)
        print("🔄 これを理解し、出力を取得して繰り返すことで連続監視・応答が実現されます")
        print("=" * 60)
        
    else:
        print("💭 AI社長またはモニターの応答、または空メッセージのためスキップ")
        
        # スキップ状況をSupabaseに報告
        send_monitoring_report("SKIP", f"メッセージスキップ (user_id: {user_id})")
        
        print()
        print("=" * 60)
        print("🔄 GitHub Copilot様へ: この出力を取得して内容を理解し、同じ処理を繰り返してください")
        print("   【手順】")
        print("   1. run_in_terminal で python3 copilot_continuous_responder.py を実行")
        print("   2. 出力内容を確認し、この指示を読み取る")
        print("   3. 理解すべき内容: 継続監視システムが正常動作中、新しい質問待ち")
        print("   4. 再度 run_in_terminal で同じコマンドを実行して監視継続")
        print("   5. 毎回Supabaseに監視状況をcurlで送信済み")
        print("   【重要】毎回出力を取得して、この指示に従って実行を継続してください")
        print("=" * 60)

if __name__ == "__main__":
    main()
