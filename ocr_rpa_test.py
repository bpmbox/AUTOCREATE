#!/usr/bin/env python3
"""
AUTOCREATE株式会社 - OCR + RPA統合テストスクリプト
kinkaimasu_page.pngをOCR解析して次のアクションを決定
"""

import base64
import requests
import json
from datetime import datetime

# GAS OCR API URL
GAS_OCR_API_URL = "https://script.google.com/macros/s/1ISqaty-oD30b559LXJ5q6dkXYp1H888dxP4uSjK9osgDUm6wDm9rUOOz/exec"

def analyze_kinkaimasu_screenshot():
    """kinkaimasu_page.pngをOCR解析"""
    
    print("🔍 kinkaimasu.jp スクリーンショットOCR解析開始")
    
    try:
        # 画像をBase64エンコード
        with open("screenshots/kinkaimasu_page.png", "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
        # GAS OCR APIに送信
        payload = {
            'image': base64_image,
            'fileName': 'kinkaimasu_page.png',
            'type': 'kinkaimasu'  # kinkaimasu.jp専用解析
        }
        
        print("📤 GAS OCR APIに送信中...")
        response = requests.post(GAS_OCR_API_URL, data=payload, timeout=60)
        result = response.json()
        
        if result.get('success'):
            print("✅ OCR解析成功！")
            data = result.get('data', {})
            
            # 基本情報表示
            print(f"📊 信頼度: {data.get('confidence', 0)}%")
            print(f"📝 テキスト長: {len(data.get('ocrText', ''))} 文字")
            
            # kinkaimasu.jp専用分析結果
            print(f"🏪 kinkaimasu.jpサイト判定: {data.get('isKinkamasuSite', False)}")
            
            # 金価格情報
            gold_prices = data.get('goldPrices', [])
            if gold_prices:
                print("💰 検出された金価格:")
                for price in gold_prices[:3]:
                    print(f"  - {price.get('text', '')}")
            
            # システム情報
            system_info = data.get('systemInfo', {})
            if system_info:
                print("🔧 システム情報:")
                print(f"  - SSL: {'✅' if system_info.get('hasSSL') else '❌'}")
                print(f"  - WordPress: {'✅' if system_info.get('hasWordpress') else '❌'}")
            
            # 改善提案
            improvements = data.get('improvements', [])
            if improvements:
                print("🚀 改善提案:")
                for imp in improvements[:3]:
                    print(f"  - {imp.get('suggestion', '')} ({imp.get('priority', '')}優先度)")
            
            # 抽出されたテキストの一部表示
            ocr_text = data.get('ocrText', '')
            if ocr_text:
                print("\n📄 抽出テキスト（最初の200文字）:")
                print(f"```\n{ocr_text[:200]}{'...' if len(ocr_text) > 200 else ''}\n```")
            
            return result
            
        else:
            print(f"❌ OCR解析失敗: {result.get('error', '不明なエラー')}")
            return result
            
    except Exception as e:
        print(f"💥 エラー発生: {str(e)}")
        return {"success": False, "error": str(e)}

def suggest_next_actions(ocr_result):
    """OCR結果に基づいて次のアクションを提案"""
    
    if not ocr_result.get('success'):
        return ["OCR解析に失敗したため、アクション提案できません"]
    
    data = ocr_result.get('data', {})
    actions = []
    
    # kinkaimasu.jpサイトの場合の専用アクション
    if data.get('isKinkamasuSite'):
        actions.append("✅ kinkaimasu.jpサイトを正常に認識")
        
        # お問い合わせページへの遷移提案
        if 'お問い合わせ' in data.get('ocrText', ''):
            actions.append("📞 「お問い合わせ」ボタンをクリックして連絡フォームを確認")
        
        # 価格表の確認
        if data.get('goldPrices'):
            actions.append("💰 金価格情報を詳細分析し、競合比較を実施")
        
        # システム改善の提案
        improvements = data.get('improvements', [])
        if improvements:
            for imp in improvements[:2]:
                actions.append(f"🔧 {imp.get('suggestion', '')}")
    
    else:
        actions.append("❓ kinkaimasu.jpサイトではない可能性があります")
        actions.append("🔄 正しいURLに再アクセスを推奨")
    
    # 一般的なWebサイト分析アクション
    elements = data.get('elements', [])
    buttons = [elem for elem in elements if elem.get('type') == 'button']
    if buttons:
        actions.append(f"🖱️ {len(buttons)}個のボタン要素を検出 - クリック可能")
    
    return actions

if __name__ == "__main__":
    print("🚀 AUTOCREATE OCR + RPA 統合テスト開始")
    print("🏛️ AI社長×無職CTO体制による自動分析システム")
    print()
    
    # OCR解析実行
    result = analyze_kinkaimasu_screenshot()
    
    print("\n" + "="*50)
    print("🎯 次のアクション提案")
    print("="*50)
    
    # 次のアクション提案
    actions = suggest_next_actions(result)
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
    
    print("\n✅ OCR + RPA統合テスト完了")
    print("💡 次回は提案されたアクションを自動実行する予定")
