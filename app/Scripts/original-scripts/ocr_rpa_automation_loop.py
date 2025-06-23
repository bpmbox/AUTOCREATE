#!/usr/bin/env python3
"""
AUTOCREATE株式会社 - OCR + RPA自動化ループシステム
AI社長×無職CTO体制による完全自動化

Features:
- OCR結果に基づく自動クリック・入力
- 画面認識 → 判断 → 行動 → 結果確認のループ
- kinkaimasu.jp等のWebサイト自動操作
- エラー時の自動復旧・再試行
"""

import subprocess
import time
import base64
import requests
import json
from datetime import datetime
import os
from PIL import Image
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ocr_rpa_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutocreateOCRRPALoop:
    """OCR + RPA自動化ループシステム"""
    
    def __init__(self, vnc_container="ubuntu-desktop-vnc"):
        """
        初期化
        Args:
            vnc_container (str): VNCコンテナ名
        """
        self.vnc_container = vnc_container
        self.display = ":1"
        self.gas_ocr_api = "https://script.google.com/macros/s/1ISqaty-oD30b559LXJ5q6dkXYp1H888dxP4uSjK9osgDUm6wDm9rUOOz/exec"
        self.max_iterations = 10  # 最大ループ回数
        self.iteration_count = 0
        self.action_history = []
        self.screenshots_dir = "/workspaces/AUTOCREATE/screenshots"
        
        # スクリーンショット保存ディレクトリ作成
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
    def take_screenshot(self, prefix="auto"):
        """
        スクリーンショットを撮影
        Args:
            prefix (str): ファイル名プレフィックス
        Returns:
            str: スクリーンショットファイルパス
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{prefix}_{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        
        try:
            # VNCコンテナ内でスクリーンショット撮影
            cmd = f"docker exec {self.vnc_container} bash -c 'DISPLAY={self.display} scrot /tmp/{filename}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # ローカルにコピー
                copy_cmd = f"docker cp {self.vnc_container}:/tmp/{filename} {filepath}"
                subprocess.run(copy_cmd, shell=True)
                logger.info(f"📸 スクリーンショット撮影完了: {filename}")
                return filepath
            else:
                logger.error(f"スクリーンショット撮影失敗: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"スクリーンショット撮影エラー: {str(e)}")
            return None
    
    def analyze_screenshot_with_ocr(self, screenshot_path):
        """
        スクリーンショットをOCR解析
        Args:
            screenshot_path (str): スクリーンショットファイルパス
        Returns:
            dict: OCR解析結果
        """
        try:
            # 画像をBase64エンコード
            with open(screenshot_path, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode('utf-8')
            
            # GAS OCR APIに送信
            payload = {
                'image': base64_image,
                'fileName': os.path.basename(screenshot_path),
                'type': 'automation'  # 自動化専用解析
            }
            
            logger.info("📤 GAS OCR APIに送信中...")
            response = requests.post(self.gas_ocr_api, data=payload, timeout=60)
            result = response.json()
            
            if result.get('success'):
                logger.info("✅ OCR解析成功")
                return result
            else:
                logger.error(f"❌ OCR解析失敗: {result.get('error', '不明なエラー')}")
                return result
                
        except Exception as e:
            logger.error(f"OCR解析エラー: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def decide_next_action(self, ocr_result):
        """
        OCR結果に基づいて次のアクションを決定
        Args:
            ocr_result (dict): OCR解析結果
        Returns:
            dict: アクション情報
        """
        if not ocr_result.get('success'):
            return {"action": "retry", "reason": "OCR解析失敗"}
        
        data = ocr_result.get('data', {})
        ocr_text = data.get('ocrText', '').lower()
        
        # kinkaimasu.jp専用ロジック
        if data.get('isKinkamasuSite') or 'kinkaimasu' in ocr_text:
            return self._decide_kinkaimasu_action(data, ocr_text)
        
        # 一般的なWebサイトロジック
        return self._decide_general_action(data, ocr_text)
    
    def _decide_kinkaimasu_action(self, data, ocr_text):
        """
        kinkaimasu.jp専用のアクション決定
        Args:
            data (dict): OCR解析データ
            ocr_text (str): OCRテキスト
        Returns:
            dict: アクション情報
        """
        # お問い合わせページへの遷移
        if 'お問い合わせ' in ocr_text or 'contact' in ocr_text:
            return {
                "action": "click",
                "target": "お問い合わせ",
                "reason": "お問い合わせページへ遷移",
                "coordinates": self._find_text_coordinates(data, ['お問い合わせ', 'contact'])
            }
        
        # 価格一覧の確認
        if '価格' in ocr_text or '金価格' in ocr_text:
            return {
                "action": "click",
                "target": "価格一覧",
                "reason": "価格一覧ページへ遷移",
                "coordinates": self._find_text_coordinates(data, ['価格', '料金', 'price'])
            }
        
        # 会社情報の確認
        if '会社概要' in ocr_text or '企業情報' in ocr_text:
            return {
                "action": "click",
                "target": "会社情報",
                "reason": "会社情報ページへ遷移",
                "coordinates": self._find_text_coordinates(data, ['会社概要', '企業情報', 'about'])
            }
        
        # デフォルトアクション
        return {
            "action": "scroll",
            "target": "down",
            "reason": "ページ下部の情報を確認",
            "pixels": 500
        }
    
    def _decide_general_action(self, data, ocr_text):
        """
        一般的なWebサイトのアクション決定
        Args:
            data (dict): OCR解析データ
            ocr_text (str): OCRテキスト
        Returns:
            dict: アクション情報
        """
        # ボタン要素の検出
        elements = data.get('elements', [])
        buttons = [elem for elem in elements if elem.get('type') == 'button']
        
        if buttons:
            first_button = buttons[0]
            return {
                "action": "click",
                "target": first_button.get('text', 'ボタン'),
                "reason": "検出されたボタンをクリック",
                "coordinates": first_button.get('coordinates')
            }
        
        # リンクの検出
        if 'http' in ocr_text or 'www' in ocr_text:
            return {
                "action": "analyze",
                "target": "links",
                "reason": "リンクを分析"
            }
        
        # デフォルトアクション
        return {
            "action": "wait",
            "target": "page_load",
            "reason": "ページの読み込み待機",
            "duration": 3
        }
    
    def _find_text_coordinates(self, data, search_texts):
        """
        テキスト要素の座標を検索
        Args:
            data (dict): OCR解析データ
            search_texts (list): 検索するテキスト一覧
        Returns:
            dict: 座標情報
        """
        elements = data.get('elements', [])
        
        for elem in elements:
            elem_text = elem.get('text', '').lower()
            for search_text in search_texts:
                if search_text.lower() in elem_text:
                    return elem.get('coordinates', {})
        
        return {}
    
    def execute_action(self, action_info):
        """
        アクションを実行
        Args:
            action_info (dict): アクション情報
        Returns:
            bool: 実行成功/失敗
        """
        action = action_info.get('action')
        target = action_info.get('target')
        reason = action_info.get('reason', '')
        
        logger.info(f"🎯 アクション実行: {action} - {target} ({reason})")
        
        try:
            if action == "click":
                return self._execute_click(action_info)
            elif action == "scroll":
                return self._execute_scroll(action_info)
            elif action == "input":
                return self._execute_input(action_info)
            elif action == "wait":
                return self._execute_wait(action_info)
            elif action == "analyze":
                return self._execute_analyze(action_info)
            elif action == "retry":
                return self._execute_retry(action_info)
            else:
                logger.warning(f"未知のアクション: {action}")
                return False
                
        except Exception as e:
            logger.error(f"アクション実行エラー: {str(e)}")
            return False
    
    def _execute_click(self, action_info):
        """クリックアクションを実行"""
        coordinates = action_info.get('coordinates', {})
        
        if coordinates and 'x' in coordinates and 'y' in coordinates:
            x, y = coordinates['x'], coordinates['y']
            cmd = f"docker exec {self.vnc_container} bash -c 'DISPLAY={self.display} xdotool mousemove {x} {y} click 1'"
        else:
            # 座標が不明の場合、画面中央をクリック
            cmd = f"docker exec {self.vnc_container} bash -c 'DISPLAY={self.display} xdotool mousemove 640 360 click 1'"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    
    def _execute_scroll(self, action_info):
        """スクロールアクションを実行"""
        target = action_info.get('target', 'down')
        pixels = action_info.get('pixels', 300)
        
        if target == 'down':
            cmd = f"docker exec {self.vnc_container} bash -c 'DISPLAY={self.display} xdotool key Page_Down'"
        else:
            cmd = f"docker exec {self.vnc_container} bash -c 'DISPLAY={self.display} xdotool key Page_Up'"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    
    def _execute_input(self, action_info):
        """入力アクションを実行"""
        text = action_info.get('text', '')
        cmd = f"docker exec {self.vnc_container} bash -c 'DISPLAY={self.display} xdotool type \"{text}\"'"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    
    def _execute_wait(self, action_info):
        """待機アクションを実行"""
        duration = action_info.get('duration', 3)
        time.sleep(duration)
        return True
    
    def _execute_analyze(self, action_info):
        """分析アクションを実行"""
        logger.info(f"📊 分析実行: {action_info.get('target', '')}")
        return True
    
    def _execute_retry(self, action_info):
        """再試行アクションを実行"""
        logger.info(f"🔄 再試行: {action_info.get('reason', '')}")
        time.sleep(2)
        return True
    
    def run_automation_loop(self, target_url=None, max_iterations=None):
        """
        自動化ループを実行
        Args:
            target_url (str): 対象URL（省略時は現在のページ）
            max_iterations (int): 最大ループ回数
        Returns:
            dict: 実行結果
        """
        if max_iterations:
            self.max_iterations = max_iterations
        
        logger.info("🚀 OCR + RPA自動化ループ開始")
        logger.info(f"🏛️ AI社長×無職CTO体制による完全自動化")
        
        # 対象URLへアクセス（指定されている場合）
        if target_url:
            self._navigate_to_url(target_url)
            time.sleep(5)  # ページ読み込み待機
        
        results = {
            "success": True,
            "iterations": [],
            "total_iterations": 0,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "error": None
        }
        
        try:
            while self.iteration_count < self.max_iterations:
                self.iteration_count += 1
                iteration_start = datetime.now()
                
                logger.info(f"🔄 ループ {self.iteration_count}/{self.max_iterations} 開始")
                
                # 1. スクリーンショット撮影
                screenshot_path = self.take_screenshot(f"loop_{self.iteration_count}")
                if not screenshot_path:
                    break
                
                # 2. OCR解析
                ocr_result = self.analyze_screenshot_with_ocr(screenshot_path)
                
                # 3. 次のアクション決定
                action_info = self.decide_next_action(ocr_result)
                
                # 4. アクション実行
                action_success = self.execute_action(action_info)
                
                # 5. 結果記録
                iteration_result = {
                    "iteration": self.iteration_count,
                    "screenshot": os.path.basename(screenshot_path),
                    "ocr_success": ocr_result.get('success', False),
                    "action": action_info,
                    "action_success": action_success,
                    "duration": (datetime.now() - iteration_start).total_seconds(),
                    "timestamp": iteration_start.isoformat()
                }
                
                results["iterations"].append(iteration_result)
                self.action_history.append(iteration_result)
                
                # 6. 終了条件チェック
                if self._should_stop_loop(ocr_result, action_info):
                    logger.info("🎯 目標達成 - ループ終了")
                    break
                
                # 7. 次のループまで待機
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"💥 自動化ループエラー: {str(e)}")
            results["success"] = False
            results["error"] = str(e)
        
        results["total_iterations"] = self.iteration_count
        results["end_time"] = datetime.now().isoformat()
        
        logger.info(f"✅ OCR + RPA自動化ループ完了 ({self.iteration_count}回実行)")
        
        return results
    
    def _navigate_to_url(self, url):
        """指定URLへナビゲート"""
        # ブラウザを開いてURLにアクセス
        cmd = f"docker exec {self.vnc_container} bash -c 'DISPLAY={self.display} firefox \"{url}\" &'"
        subprocess.run(cmd, shell=True)
        logger.info(f"🌐 URLにアクセス: {url}")
    
    def _should_stop_loop(self, ocr_result, action_info):
        """ループ終了条件をチェック"""
        # 特定の目標達成時にループを終了
        if action_info.get('action') == 'complete':
            return True
        
        # 同じアクションが連続で実行された場合
        if len(self.action_history) >= 3:
            recent_actions = [h['action']['action'] for h in self.action_history[-3:]]
            if len(set(recent_actions)) == 1 and recent_actions[0] in ['scroll', 'wait']:
                return True
        
        return False
    
    def generate_report(self, results):
        """実行結果レポートを生成"""
        report = {
            "title": "AUTOCREATE OCR + RPA 自動化レポート",
            "subtitle": "AI社長×無職CTO体制による完全自動化",
            "summary": {
                "success": results.get("success", False),
                "total_iterations": results.get("total_iterations", 0),
                "duration": self._calculate_duration(results),
                "screenshots_count": len([i for i in results.get("iterations", []) if i.get("screenshot")]),
                "success_rate": self._calculate_success_rate(results)
            },
            "details": results.get("iterations", []),
            "generated_at": datetime.now().isoformat()
        }
        
        # レポートをJSONファイルに保存
        report_path = os.path.join(self.screenshots_dir, f"automation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📊 レポート生成完了: {os.path.basename(report_path)}")
        return report_path
    
    def _calculate_duration(self, results):
        """実行時間を計算"""
        if results.get("start_time") and results.get("end_time"):
            start = datetime.fromisoformat(results["start_time"])
            end = datetime.fromisoformat(results["end_time"])
            return (end - start).total_seconds()
        return 0
    
    def _calculate_success_rate(self, results):
        """成功率を計算"""
        iterations = results.get("iterations", [])
        if not iterations:
            return 0
        
        success_count = sum(1 for i in iterations if i.get("action_success", False))
        return (success_count / len(iterations)) * 100

if __name__ == "__main__":
    # 使用例
    automation = AutocreateOCRRPALoop()
    
    # kinkaimasu.jpの自動化を実行
    results = automation.run_automation_loop(
        target_url="https://kinkaimasu.jp",
        max_iterations=5
    )
    
    # レポート生成
    report_path = automation.generate_report(results)
    
    print(f"🎯 自動化完了！レポート: {report_path}")
