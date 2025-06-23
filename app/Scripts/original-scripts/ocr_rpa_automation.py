#!/usr/bin/env python3
"""
AUTOCREATE株式会社 - OCR連携RPA自動化システム
AI社長×無職CTO体制による知的自動化

Features:
- スクリーンショット → OCR解析 → アクション決定 → 実行のループ
- GAS OCR APIによる画像解析
- 状況に応じた動的アクション生成
- kinkaimasu.jp専用の知識ベース
"""

import json
import time
import re
from datetime import datetime
from scripts.vnc_desktop_automation import AutocreateVNCAutomation, AUTOMATION_SEQUENCES

class OCRRPAAutomation(AutocreateVNCAutomation):
    def __init__(self, vnc_container="ubuntu-desktop-vnc", gas_ocr_url=None):
        """
        OCR連携RPA自動化システム初期化
        Args:
            vnc_container (str): VNCコンテナ名
            gas_ocr_url (str): GAS OCR API URL
        """
        super().__init__(vnc_container)
        if gas_ocr_url:
            self.gas_ocr_api = gas_ocr_url
        
        # kinkaimasu.jp専用の知識ベース
        self.kinkaimasu_knowledge = {
            "navigation": {
                "top_menu": ["ホーム", "買取", "出品", "査定", "ログイン"],
                "categories": ["ブランド品", "時計", "貴金属", "宝石", "家電"],
                "actions": ["買取依頼", "査定申込", "会員登録", "問い合わせ"]
            },
            "patterns": {
                "price": r'(\d{1,3}(?:,\d{3})*)\s*円',
                "phone": r'0\d{1,4}-\d{1,4}-\d{4}',
                "email": r'[\w\.-]+@[\w\.-]+\.\w+',
                "button_keywords": ["クリック", "申込", "登録", "送信", "確認", "次へ", "戻る"]
            },
            "expected_elements": {
                "homepage": ["買取価格表", "無料査定", "店舗情報", "お客様の声"],
                "assessment": ["査定フォーム", "商品写真", "送付方法", "査定額"]
            }
        }
        
        self.action_rules = {
            "page_load_wait": 3,
            "screenshot_interval": 2,
            "max_retry_attempts": 3,
            "ocr_confidence_threshold": 0.7
        }
        
    def intelligent_screen_analysis(self, screenshot_path):
        """
        知的画面解析（OCR + パターンマッチング）
        Args:
            screenshot_path (str): スクリーンショットファイルパス
        Returns:
            dict: 解析結果と推奨アクション
        """
        print(f"🔍 画面解析開始: {screenshot_path}")
        
        # OCR解析実行
        ocr_result = self.analyze_screen_with_ocr(screenshot_path)
        
        if not ocr_result.get('success'):
            return {
                "analysis": "OCR解析失敗",
                "confidence": 0.0,
                "recommended_actions": []
            }
        
        # OCRテキストを取得
        ocr_text = ocr_result.get('text', '')
        print(f"📄 OCR抽出テキスト: {ocr_text[:200]}...")
        
        # パターン解析
        analysis_result = {
            "detected_page_type": self._identify_page_type(ocr_text),
            "found_prices": re.findall(self.kinkaimasu_knowledge["patterns"]["price"], ocr_text),
            "found_buttons": self._find_action_buttons(ocr_text),
            "found_forms": self._find_form_elements(ocr_text),
            "navigation_elements": self._find_navigation_elements(ocr_text),
            "confidence": 0.8,  # 実際は複数の指標から算出
            "raw_ocr": ocr_result
        }
        
        # 推奨アクション生成
        recommended_actions = self._generate_recommended_actions(analysis_result)
        
        analysis_result["recommended_actions"] = recommended_actions
        
        return analysis_result
    
    def _identify_page_type(self, text):
        """
        ページタイプを識別
        Args:
            text (str): OCRテキスト
        Returns:
            str: ページタイプ
        """
        text_lower = text.lower()
        
        if "買取価格" in text or "査定" in text:
            return "assessment_page"
        elif "ログイン" in text and "パスワード" in text:
            return "login_page"
        elif "商品詳細" in text or "買取依頼" in text:
            return "product_detail"
        elif "金・貴金属" in text or "ブランド" in text:
            return "category_page"
        elif "kinkaimasu" in text_lower or "金買います" in text:
            return "homepage"
        else:
            return "unknown_page"
    
    def _find_action_buttons(self, text):
        """
        アクションボタンを検出
        Args:
            text (str): OCRテキスト
        Returns:
            list: 検出されたボタンのリスト
        """
        buttons = []
        for keyword in self.kinkaimasu_knowledge["patterns"]["button_keywords"]:
            if keyword in text:
                buttons.append({
                    "text": keyword,
                    "type": "button",
                    "action_priority": self._get_button_priority(keyword)
                })
        return sorted(buttons, key=lambda x: x["action_priority"], reverse=True)
    
    def _find_form_elements(self, text):
        """
        フォーム要素を検出
        Args:
            text (str): OCRテキスト
        Returns:
            list: 検出されたフォーム要素
        """
        forms = []
        form_keywords = ["お名前", "電話番号", "メールアドレス", "住所", "商品名", "備考"]
        
        for keyword in form_keywords:
            if keyword in text:
                forms.append({
                    "label": keyword,
                    "type": "form_field",
                    "required": keyword in ["お名前", "電話番号"]
                })
        return forms
    
    def _find_navigation_elements(self, text):
        """
        ナビゲーション要素を検出
        Args:
            text (str): OCRテキスト
        Returns:
            list: ナビゲーション要素
        """
        nav_elements = []
        for nav_item in self.kinkaimasu_knowledge["navigation"]["top_menu"]:
            if nav_item in text:
                nav_elements.append({
                    "text": nav_item,
                    "type": "navigation",
                    "target_page": nav_item.lower()
                })
        return nav_elements
    
    def _get_button_priority(self, button_text):
        """
        ボタンの優先度を取得
        Args:
            button_text (str): ボタンテキスト
        Returns:
            int: 優先度（高いほど重要）
        """
        priority_map = {
            "申込": 10,
            "送信": 9,
            "確認": 8,
            "次へ": 7,
            "登録": 6,
            "クリック": 5,
            "戻る": 3
        }
        return priority_map.get(button_text, 1)
    
    def _generate_recommended_actions(self, analysis):
        """
        解析結果から推奨アクションを生成
        Args:
            analysis (dict): 画面解析結果
        Returns:
            list: 推奨アクションリスト
        """
        actions = []
        page_type = analysis.get("detected_page_type", "unknown")
        
        if page_type == "homepage":
            actions.extend([
                {
                    "type": "scroll",
                    "direction": "down",
                    "description": "ページ内容をスクロールして探索",
                    "priority": 8
                },
                {
                    "type": "click_text",
                    "target_text": "無料査定",
                    "description": "無料査定ボタンをクリック",
                    "priority": 9
                }
            ])
        
        elif page_type == "assessment_page":
            actions.extend([
                {
                    "type": "fill_form",
                    "form_data": {
                        "お名前": "テスト太郎",
                        "電話番号": "03-1234-5678",
                        "メールアドレス": "test@example.com"
                    },
                    "description": "査定フォームに入力",
                    "priority": 10
                }
            ])
        
        # 検出されたボタンに基づくアクション
        for button in analysis.get("found_buttons", []):
            actions.append({
                "type": "click_text",
                "target_text": button["text"],
                "description": f"「{button['text']}」ボタンをクリック",
                "priority": button["action_priority"]
            })
        
        # ナビゲーション要素に基づくアクション
        for nav in analysis.get("navigation_elements", []):
            actions.append({
                "type": "click_text",
                "target_text": nav["text"],
                "description": f"「{nav['text']}」メニューをクリック",
                "priority": 6
            })
        
        return sorted(actions, key=lambda x: x.get("priority", 0), reverse=True)
    
    def execute_intelligent_action(self, action):
        """
        知的アクションを実行
        Args:
            action (dict): 実行するアクション
        Returns:
            bool: 実行成功/失敗
        """
        action_type = action.get("type")
        success = False
        
        print(f"🎯 アクション実行: {action.get('description', 'Unknown')}")
        
        if action_type == "click_text":
            # テキストベースクリック（簡易版）
            # 実際の実装では画面上のテキスト位置を特定する必要がある
            success = self.click_at_position(400, 300)  # 画面中央をクリック
            
        elif action_type == "scroll":
            direction = action.get("direction", "down")
            if direction == "down":
                success = self.press_key("Page_Down")
            else:
                success = self.press_key("Page_Up")
                
        elif action_type == "fill_form":
            form_data = action.get("form_data", {})
            for field, value in form_data.items():
                # フィールドをクリック（簡易版）
                self.click_at_position(400, 250)
                time.sleep(0.5)
                # 既存テキストをクリア
                self.press_key("ctrl+a")
                time.sleep(0.2)
                # 新しいテキストを入力
                self.type_text(value)
                time.sleep(0.5)
                # 次のフィールドへ
                self.press_key("Tab")
                time.sleep(0.5)
            success = True
            
        elif action_type == "wait":
            time.sleep(action.get("seconds", 2))
            success = True
        
        return success
    
    def run_intelligent_automation_loop(self, max_iterations=10, target_goal="data_collection"):
        """
        知的自動化ループを実行
        Args:
            max_iterations (int): 最大反復回数
            target_goal (str): 目標（data_collection, form_submission, navigation_test）
        Returns:
            dict: 実行結果サマリー
        """
        print("🚀 AUTOCREATE知的自動化ループ開始")
        print(f"🎯 目標: {target_goal}")
        print(f"🔄 最大反復: {max_iterations}回")
        
        loop_results = {
            "iterations": [],
            "total_screenshots": 0,
            "successful_actions": 0,
            "failed_actions": 0,
            "collected_data": [],
            "goal_achieved": False
        }
        
        for iteration in range(max_iterations):
            print(f"\n🔄 反復 {iteration + 1}/{max_iterations}")
            
            iteration_result = {
                "iteration": iteration + 1,
                "timestamp": datetime.now().isoformat(),
                "actions_taken": [],
                "analysis": None,
                "success": False
            }
            
            try:
                # 1. スクリーンショット撮影
                screenshot_filename = f"auto_analysis_{iteration+1:02d}.png"
                screenshot_path = self.take_screenshot(screenshot_filename)
                loop_results["total_screenshots"] += 1
                
                print(f"📸 スクリーンショット: {screenshot_path}")
                
                # 2. 知的画面解析
                analysis = self.intelligent_screen_analysis(screenshot_path)
                iteration_result["analysis"] = analysis
                
                print(f"🧠 ページタイプ: {analysis.get('detected_page_type')}")
                print(f"🎯 推奨アクション数: {len(analysis.get('recommended_actions', []))}")
                
                # 3. データ収集
                if analysis.get("found_prices"):
                    loop_results["collected_data"].extend([
                        {"type": "price", "value": price, "iteration": iteration+1}
                        for price in analysis["found_prices"]
                    ])
                
                # 4. 推奨アクション実行
                recommended_actions = analysis.get("recommended_actions", [])[:3]  # 上位3つ
                
                if not recommended_actions:
                    print("⚠️  推奨アクションが見つかりません。探索を続行...")
                    # デフォルトアクション: スクロールまたはクリック
                    default_action = {
                        "type": "scroll",
                        "direction": "down",
                        "description": "探索のためのスクロール",
                        "priority": 1
                    }
                    recommended_actions = [default_action]
                
                for action in recommended_actions:
                    print(f"⚡ 実行: {action.get('description')}")
                    
                    success = self.execute_intelligent_action(action)
                    iteration_result["actions_taken"].append({
                        "action": action,
                        "success": success
                    })
                    
                    if success:
                        loop_results["successful_actions"] += 1
                    else:
                        loop_results["failed_actions"] += 1
                    
                    # アクション間の待機
                    time.sleep(self.action_rules["screenshot_interval"])
                
                iteration_result["success"] = True
                
                # 5. 目標達成チェック
                if target_goal == "data_collection" and len(loop_results["collected_data"]) >= 5:
                    print("🎉 データ収集目標達成！")
                    loop_results["goal_achieved"] = True
                    break
                
                # 6. 次の反復への準備
                time.sleep(self.action_rules["page_load_wait"])
                
            except Exception as e:
                print(f"❌ 反復 {iteration+1} でエラー: {str(e)}")
                iteration_result["error"] = str(e)
            
            loop_results["iterations"].append(iteration_result)
        
        # 結果サマリー
        print("\n📊 自動化ループ完了")
        print(f"✅ 成功アクション: {loop_results['successful_actions']}")
        print(f"❌ 失敗アクション: {loop_results['failed_actions']}")
        print(f"📄 スクリーンショット: {loop_results['total_screenshots']}枚")
        print(f"💎 収集データ: {len(loop_results['collected_data'])}件")
        print(f"🎯 目標達成: {'はい' if loop_results['goal_achieved'] else 'いいえ'}")
        
        return loop_results
    
    def save_results_report(self, results, output_file="automation_report.json"):
        """
        結果レポートを保存
        Args:
            results (dict): 自動化結果
            output_file (str): 出力ファイル名
        """
        report_path = f"./reports/{output_file}"
        
        # レポートディレクトリ作成
        import os
        os.makedirs("./reports", exist_ok=True)
        
        # 結果をJSONで保存
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"📋 レポート保存: {report_path}")
        return report_path

def demo_ocr_rpa_automation():
    """OCR連携RPA自動化のデモンストレーション"""
    print("🏛️ AUTOCREATE株式会社 - AI社長×無職CTO体制")
    print("🤖 OCR連携RPA知的自動化システム デモ")
    
    # GAS OCR API URLを設定（実際のURLに変更）
    gas_ocr_url = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"
    
    automation = OCRRPAAutomation(
        vnc_container="ubuntu-desktop-vnc",
        gas_ocr_url=gas_ocr_url
    )
    
    print("\n🌐 Step 1: kinkaimasu.jpにアクセス")
    # まずブラウザでkinkaimasu.jpを開く
    browser_sequence = AUTOMATION_SEQUENCES["browser_open_kinkaimasu"]
    automation.execute_automation_sequence(browser_sequence)
    
    print("\n🧠 Step 2: 知的自動化ループ開始")
    # OCR連携の知的自動化ループを実行
    results = automation.run_intelligent_automation_loop(
        max_iterations=5,
        target_goal="data_collection"
    )
    
    print("\n📋 Step 3: 結果レポート生成")
    report_path = automation.save_results_report(
        results, 
        f"kinkaimasu_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    print("\n🎉 デモ完了！")
    print("これがAUTOCREATE式「自然言語で思ったことを作れる」AIシステムの実力です。")
    
    return results, report_path

if __name__ == "__main__":
    # デモ実行
    demo_ocr_rpa_automation()
