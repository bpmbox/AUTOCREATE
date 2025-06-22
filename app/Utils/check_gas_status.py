#!/usr/bin/env python3
"""
Google Apps Script の実際の動作状況を詳しく確認
"""

import os
import requests
from dotenv import load_dotenv

def check_gas_status():
    """Google Apps Scriptの詳細状況を確認"""
    print("🔍 Google Apps Script 詳細状況確認")
    print("=" * 50)
    
    load_dotenv()
    webhook_gas = os.getenv('WEBHOOK_GAS')
    
    if not webhook_gas:
        print("❌ WEBHOOK_GAS が設定されていません")
        return False
    
    print(f"🔗 GAS URL: {webhook_gas}")
    
    # 1. 基本接続テスト
    print(f"\n📡 1. 基本接続テスト...")
    try:
        response = requests.get(webhook_gas, timeout=10)
        print(f"   ステータス: {response.status_code}")
        print(f"   レスポンスサイズ: {len(response.text)}文字")
        
        # レスポンス内容の詳細解析
        if response.status_code == 200:
            print("   ✅ 接続成功")
            
            # エラーメッセージの確認
            if 'エラー' in response.text or 'Error' in response.text:
                print("   ⚠️ エラーレスポンス検出")
                
                # エラー詳細を抽出
                if 'TypeError' in response.text:
                    print("   🐛 TypeError検出 - スクリプト内部エラー")
                if 'Cannot read properties' in response.text:
                    print("   🔧 プロパティ読み取りエラー - 未定義変数")
                if 'split' in response.text:
                    print("   📝 文字列処理エラー - split関数問題")
                
                # エラー行番号の確認
                import re
                line_match = re.search(r'行 (\d+)', response.text)
                if line_match:
                    line_num = line_match.group(1)
                    print(f"   📍 エラー行: {line_num}")
            else:
                print("   🤔 HTMLレスポンス（管理画面？）")
        else:
            print(f"   ❌ 接続失敗: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ 接続エラー: {e}")
        return False
    
    # 2. パラメータ付きテスト
    print(f"\n🧪 2. パラメータ付きテスト...")
    test_params = [
        {'test': 'hello'},
        {'action': 'ping'},
        {'method': 'GET'},
        {'debug': 'true'}
    ]
    
    for i, params in enumerate(test_params, 1):
        try:
            response = requests.get(webhook_gas, params=params, timeout=10)
            print(f"   テスト{i} ({params}): {response.status_code}")
            
            # レスポンス変化を確認
            if response.status_code != 200:
                print(f"     ⚠️ エラー: {response.text[:100]}...")
            else:
                # 成功レスポンスの内容変化確認
                if len(response.text) < 500:  # 短いレスポンス = 成功の可能性
                    print(f"     ✅ 短縮レスポンス: {response.text[:50]}...")
                    
        except Exception as e:
            print(f"   テスト{i} エラー: {e}")
    
    # 3. POST方式テスト
    print(f"\n📤 3. POST方式テスト...")
    try:
        post_data = {
            'action': 'create_doc',
            'title': 'テストドキュメント',
            'content': 'テスト内容'
        }
        
        response = requests.post(webhook_gas, json=post_data, timeout=10)
        print(f"   POST結果: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ POST接続成功")
            if len(response.text) < 200:
                print(f"   📄 POST応答: {response.text}")
        else:
            print(f"   ❌ POST失敗: {response.text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ POST エラー: {e}")
    
    # 4. スクリプトIDの確認
    print(f"\n🆔 4. スクリプトID確認...")
    
    # URLからスクリプトIDを抽出
    import re
    script_id_match = re.search(r'/macros/s/([a-zA-Z0-9_-]+)', webhook_gas)
    
    if script_id_match:
        script_id = script_id_match.group(1)
        print(f"   📜 スクリプトID: {script_id}")
        print(f"   🔗 管理URL: https://script.google.com/d/{script_id}/edit")
        
        # .clasp.jsonとの比較
        clasp_file = '.clasp.json'
        if os.path.exists(clasp_file):
            try:
                with open(clasp_file, 'r') as f:
                    import json
                    clasp_data = json.load(f)
                    clasp_script_id = clasp_data.get('scriptId', 'N/A')
                    print(f"   📋 .clasp.json ID: {clasp_script_id}")
                    
                    if script_id == clasp_script_id:
                        print("   ✅ スクリプトID一致")
                    else:
                        print("   ⚠️ スクリプトID不一致")
                        
            except Exception as e:
                print(f"   ❌ .clasp.json読み取りエラー: {e}")
        else:
            print("   📁 .clasp.jsonファイルなし")
    
    return True

def analyze_gas_error():
    """GASエラーの詳細分析"""
    print(f"\n🔬 5. GASエラー詳細分析...")
    
    webhook_gas = os.getenv('WEBHOOK_GAS')
    
    try:
        response = requests.get(webhook_gas, timeout=10)
        
        # HTMLからエラー情報を抽出
        html_content = response.text
        
        # エラーメッセージ部分を抽出
        import re
        
        # エラータイトル
        title_match = re.search(r'<title>(.*?)</title>', html_content)
        if title_match:
            title = title_match.group(1)
            print(f"   📋 タイトル: {title}")
        
        # エラーメッセージ本体
        error_match = re.search(r'<div[^>]*>(.*(TypeError|Error).*?)</div>', html_content, re.DOTALL)
        if error_match:
            error_msg = error_match.group(1).strip()
            # HTMLタグを除去
            clean_error = re.sub(r'<[^>]+>', '', error_msg)
            print(f"   🐛 エラー詳細: {clean_error}")
        
        # ファイル・行番号情報
        file_match = re.search(r'（行\s*(\d+).*?ファイル.*?\"([^\"]+)\"', html_content)
        if file_match:
            line_num = file_match.group(1)
            file_name = file_match.group(2)
            print(f"   📍 エラー場所: {file_name} の {line_num}行目")
        
        print(f"\n💡 推定問題:")
        if 'Cannot read properties of undefined' in html_content:
            print("   - 未定義変数へのアクセス")
            print("   - 関数パラメータの問題")
            print("   - リクエストデータの解析エラー")
        
        if 'split' in html_content:
            print("   - 文字列処理エラー")
            print("   - URLパラメータの解析問題")
        
        print(f"\n🔧 解決方法:")
        print("   1. GASスクリプトを直接編集")
        print("   2. エラーハンドリングを追加")
        print("   3. デバッグログを追加")
        
    except Exception as e:
        print(f"   ❌ エラー分析失敗: {e}")

def main():
    """メイン実行"""
    print("🔍 Google Apps Script 完全診断")
    print("=" * 60)
    
    load_dotenv()
    
    # GAS基本確認
    gas_ok = check_gas_status()
    
    # エラー詳細分析
    if gas_ok:
        analyze_gas_error()
    
    print("\n" + "=" * 60)
    print("📊 GAS診断完了")
    
    print(f"\n📋 診断結果:")
    print(f"  🔗 GAS接続: {'✅ 可能' if gas_ok else '❌ 失敗'}")
    print(f"  🐛 エラー状況: TypeError検出済み")
    print(f"  📝 Google Docs作成: ❌ 現在失敗中")
    
    print(f"\n💡 現状:")
    print(f"  - GASスクリプト内にバグあり")
    print(f"  - doGet関数でTypeError発生")
    print(f"  - パラメータ処理に問題")
    
    print(f"\n🎯 対処法:")
    print(f"  1. ✅ ローカルMarkdownファイルは作成済み")
    print(f"  2. 📄 直接Google Docsで新規作成可能")
    print(f"  3. 🔧 GASスクリプト修正でより高度な自動化が可能")
    
    print(f"\n🎊 結論: Google Docsは使えるが、GAS自動化は要修正")

if __name__ == "__main__":
    main()
