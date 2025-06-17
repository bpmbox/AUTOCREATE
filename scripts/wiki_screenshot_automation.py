#!/usr/bin/env python3
"""
WIKI Screenshot Automation Script
現在の画面状況をキャプチャーしてWIKIに自動更新するスクリプト

Usage:
    python scripts/wiki_screenshot_automation.py --action capture
    python scripts/wiki_screenshot_automation.py --action update-wiki
    python scripts/wiki_screenshot_automation.py --action full-workflow
"""

import argparse
import datetime
import os
import subprocess
import sys
import time
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class WikiScreenshotAutomation:
    def __init__(self):
        self.project_root = Path("/workspaces/AUTOCREATE")
        self.wiki_dir = self.project_root / "AUTOCREATE.wiki"
        self.screenshots_dir = self.wiki_dir / "screenshots"
        self.vnc_url = "http://localhost:6081"
        
        # スクリーンショットディレクトリを作成
        self.screenshots_dir.mkdir(exist_ok=True)
        
    def check_vnc_status(self):
        """VNC環境の状態をチェック"""
        try:
            result = subprocess.run([
                "docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
            ], capture_output=True, text=True)
            
            if "ubuntu-desktop-vnc" in result.stdout:
                print("✅ VNC Desktop Environment: RUNNING")
                print("🌐 Access URL: http://localhost:6081")
                return True
            else:
                print("❌ VNC Desktop Environment: NOT RUNNING")
                return False
        except Exception as e:
            print(f"❌ VNC Status Check Error: {e}")
            return False
    
    def capture_vnc_screenshot(self):
        """VNC環境のスクリーンショットをキャプチャー"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"vnc_desktop_{timestamp}.png"
        screenshot_path = self.screenshots_dir / screenshot_filename
        
        try:
            # Docker exec でVNCコンテナ内のスクリーンショット
            result = subprocess.run([
                "docker", "exec", "ubuntu-desktop-vnc",
                "import", "-window", "root", f"/tmp/{screenshot_filename}"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # コンテナからホストにファイルをコピー
                copy_result = subprocess.run([
                    "docker", "cp", f"ubuntu-desktop-vnc:/tmp/{screenshot_filename}",
                    str(screenshot_path)
                ], capture_output=True, text=True)
                
                if copy_result.returncode == 0:
                    print(f"📸 Screenshot captured: {screenshot_path}")
                    return screenshot_path, screenshot_filename
                else:
                    print(f"❌ Failed to copy screenshot: {copy_result.stderr}")
            else:
                print(f"❌ Failed to take screenshot: {result.stderr}")
        except Exception as e:
            print(f"❌ Screenshot capture error: {e}")
        
        return None, None
    
    def capture_browser_screenshot(self, url="http://localhost:8000"):
        """ブラウザでURLを開いてスクリーンショット"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"browser_{url.replace('://', '_').replace('/', '_')}_{timestamp}.png"
        screenshot_path = self.screenshots_dir / screenshot_filename
        
        try:
            # Docker exec でブラウザを開いてスクリーンショット
            commands = [
                # ブラウザを開く
                f"DISPLAY=:1 firefox {url} &",
                "sleep 5",  # ページロード待機
                f"import -window root /tmp/{screenshot_filename}"
            ]
            
            for cmd in commands:
                result = subprocess.run([
                    "docker", "exec", "ubuntu-desktop-vnc", "bash", "-c", cmd
                ], capture_output=True, text=True)
            
            # ファイルをコピー
            copy_result = subprocess.run([
                "docker", "cp", f"ubuntu-desktop-vnc:/tmp/{screenshot_filename}",
                str(screenshot_path)
            ], capture_output=True, text=True)
            
            if copy_result.returncode == 0:
                print(f"🌐 Browser screenshot captured: {screenshot_path}")
                return screenshot_path, screenshot_filename
            else:
                print(f"❌ Failed to copy browser screenshot: {copy_result.stderr}")
        except Exception as e:
            print(f"❌ Browser screenshot error: {e}")
        
        return None, None
    
    def update_wiki_page(self, page_name="System-Status", screenshots=[]):
        """WIKI ページを更新"""
        wiki_page_path = self.wiki_dir / f"{page_name}.md"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # WIKIページのコンテンツを生成
        content = f"""# {page_name.replace('-', ' ')}

Last Updated: {timestamp}

## Current System Status

### VNC Desktop Environment
- Status: {'✅ RUNNING' if self.check_vnc_status() else '❌ NOT RUNNING'}
- Access URL: http://localhost:6081
- Password: mypassword

### Screenshots

"""
        
        # スクリーンショットセクションを追加
        for screenshot_path, screenshot_filename in screenshots:
            if screenshot_path and screenshot_path.exists():
                content += f"""#### {screenshot_filename}
![{screenshot_filename}](screenshots/{screenshot_filename})

"""
        
        content += f"""
## System Information

### Docker Containers Status
```bash
# Check running containers
docker ps --format "table {{{{.Names}}}}\\t{{{{.Status}}}}\\t{{{{.Ports}}}}"
```

### Project Structure
- Project Root: `/workspaces/AUTOCREATE`
- Wiki Directory: `AUTOCREATE.wiki/`
- Screenshots: `AUTOCREATE.wiki/screenshots/`

### Access Points
- VNC Desktop: http://localhost:6081 (password: mypassword)
- Main Application: http://localhost:8000 (if running)
- Gradio Interface: http://localhost:7860 (if running)

## Automated Workflow

This page is automatically updated by `scripts/wiki_screenshot_automation.py`.

### Usage
```bash
# Capture current desktop screenshot
python scripts/wiki_screenshot_automation.py --action capture

# Update this wiki page with latest screenshots
python scripts/wiki_screenshot_automation.py --action update-wiki

# Full workflow: capture + update
python scripts/wiki_screenshot_automation.py --action full-workflow
```

---
*Generated by AUTOCREATE Wiki Automation System*
"""
        
        try:
            wiki_page_path.write_text(content, encoding='utf-8')
            print(f"📝 Wiki page updated: {wiki_page_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to update wiki page: {e}")
            return False
    
    def run_capture_workflow(self):
        """画面キャプチャーワークフローを実行"""
        print("🚀 Starting screenshot capture workflow...")
        
        # VNC環境チェック
        if not self.check_vnc_status():
            print("⚠️ Starting VNC environment...")
            subprocess.run([
                "docker-compose", "-f", "docker-compose-vnc.yml", "up", "-d"
            ], cwd=self.project_root)
            time.sleep(10)  # 起動待機
        
        screenshots = []
        
        # デスクトップスクリーンショット
        desktop_path, desktop_filename = self.capture_vnc_screenshot()
        if desktop_path:
            screenshots.append((desktop_path, desktop_filename))
        
        # ブラウザスクリーンショット（複数URL）
        urls = [
            "http://localhost:8000",  # Main app
            "http://localhost:7860",  # Gradio
            "https://github.com/your-repo/AUTOCREATE"  # GitHub
        ]
        
        for url in urls:
            try:
                browser_path, browser_filename = self.capture_browser_screenshot(url)
                if browser_path:
                    screenshots.append((browser_path, browser_filename))
            except:
                continue
        
        return screenshots
    
    def run_wiki_update_workflow(self, screenshots=None):
        """WIKI更新ワークフローを実行"""
        print("📝 Starting wiki update workflow...")
        
        if screenshots is None:
            # 既存のスクリーンショットを検索
            screenshots = []
            for img_file in self.screenshots_dir.glob("*.png"):
                screenshots.append((img_file, img_file.name))
        
        # WIKI ページを更新
        success = self.update_wiki_page("System-Status", screenshots)
        
        if success:
            print("✅ Wiki update workflow completed successfully!")
        else:
            print("❌ Wiki update workflow failed!")
        
        return success
    
    def run_full_workflow(self):
        """フルワークフロー：キャプチャー + WIKI更新"""
        print("🎯 Starting full automation workflow...")
        
        # 1. スクリーンショットキャプチャー
        screenshots = self.run_capture_workflow()
        
        # 2. WIKI更新
        success = self.run_wiki_update_workflow(screenshots)
        
        if success:
            print("🎉 Full automation workflow completed successfully!")
            print(f"📸 {len(screenshots)} screenshots captured and documented")
        else:
            print("❌ Full automation workflow failed!")
        
        return success

def main():
    parser = argparse.ArgumentParser(description="AUTOCREATE Wiki Screenshot Automation")
    parser.add_argument(
        "--action",
        choices=["capture", "update-wiki", "full-workflow", "status"],
        default="status",
        help="Action to perform"
    )
    
    args = parser.parse_args()
    automation = WikiScreenshotAutomation()
    
    if args.action == "status":
        automation.check_vnc_status()
    elif args.action == "capture":
        screenshots = automation.run_capture_workflow()
        print(f"📸 Captured {len(screenshots)} screenshots")
    elif args.action == "update-wiki":
        automation.run_wiki_update_workflow()
    elif args.action == "full-workflow":
        automation.run_full_workflow()

if __name__ == "__main__":
    main()
