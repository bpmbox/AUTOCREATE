#!/usr/bin/env python3
"""
軽量版 Lavelo AI 自動化テスト
重いインポートを避けて核心機能のみテスト
"""
import os
import sys
import requests
import json
from datetime import datetime

def test_supabase_direct():
    """Direct HTTP で Supabase をテスト"""
    print("🔍 Supabase HTTP 接続テスト...")
    
    SUPABASE_URL = 'https://rootomzbucovwdqsscqd.supabase.co'
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8'
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        # データ取得テスト
        url = f'{SUPABASE_URL}/rest/v1/chat_history?select=id,messages,group_name&limit=3'
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ データ取得成功: {len(data)}件")
            
            # None安全性テスト
            for row in data:
                messages = row.get('messages')
                if messages is None:
                    print(f"  ⚠️ ID {row['id']}: messages = None (修正済み対応)")
                else:
                    print(f"  ✅ ID {row['id']}: messages OK ({len(messages)}文字)")
                    
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 接続エラー: {e}")
        return False

def test_memory_operations():
    """記憶操作の HTTP テスト"""
    print("\n🧠 記憶操作テスト...")
    
    SUPABASE_URL = 'https://rootomzbucovwdqsscqd.supabase.co'
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8'
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    try:
        # テスト用記憶保存
        test_data = {
            'ownerid': 'lavelo_automation_test',
            'messages': f'🧪 自動化テスト記憶 - {datetime.now().isoformat()}',
            'targetid': 'automation_test',
            'created': datetime.now().isoformat(),
            'status': 'importance_90',
            'group_name': 'lavelo_test'
        }
        
        url = f'{SUPABASE_URL}/rest/v1/chat_history'
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        
        if response.status_code in [200, 201]:
            result = response.json()
            test_id = result[0]['id'] if result else 'unknown'
            print(f"✅ 記憶保存成功: ID {test_id}")
            
            # 保存した記憶を検索
            search_url = f'{SUPABASE_URL}/rest/v1/chat_history?messages=ilike.*自動化テスト記憶*&limit=1'
            search_response = requests.get(search_url, headers=headers, timeout=10)
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                print(f"✅ 記憶検索成功: {len(search_data)}件見つかりました")
                return True
            else:
                print(f"❌ 検索エラー: {search_response.status_code}")
                return False
        else:
            print(f"❌ 保存エラー: {response.status_code}")
            print(f"エラー内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 記憶操作エラー: {e}")
        return False

def main():
    print("🚀 軽量版 Lavelo AI 自動化テスト")
    print(f"⏰ 開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Supabase接続
    if test_supabase_direct():
        tests_passed += 1
    
    # Test 2: 記憶操作
    if test_memory_operations():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 テスト結果: {tests_passed}/{total_tests} 成功")
    
    if tests_passed == total_tests:
        print("🎉 すべてのテストが成功しました！")
        print("✅ Lavelo AI システムは正常に動作しています")
        return True
    else:
        print("⚠️ 一部のテストが失敗しました")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
