import gradio as gr
import subprocess
import os
import yaml
import json
from pathlib import Path

class WordPressProxyManager:
    def __init__(self):
        self.script_path = "./wordpress-proxy-setup.sh"
        self.config_dir = "./configs"
        os.makedirs(self.config_dir, exist_ok=True)
    
    def setup_single_site(self, domain, backend, ssl_enabled=False, webserver="nginx"):
        """単一サイトのプロキシ設定"""
        try:
            cmd = [
                self.script_path,
                "--domain", domain,
                "--backend", backend,
                "--webserver", webserver
            ]
            
            if ssl_enabled:
                cmd.append("--ssl")
            
            # デモ環境では実際の設定は実行せず、コマンドのみ生成
            command_str = " ".join(cmd)
            
            result = f"""
✅ WordPress Proxy設定コマンド生成完了

🔧 実行コマンド:
```bash
{command_str}
```

📋 設定内容:
- ドメイン: {domain}
- バックエンド: {backend}
- SSL: {'有効' if ssl_enabled else '無効'}
- Webサーバー: {webserver}

📝 注意事項:
実際の本番環境では、このコマンドをroot権限で実行してください。
設定前に必ずバックアップを取得することをお勧めします。
"""
            return result, self.generate_nginx_config(domain, backend, ssl_enabled)
            
        except Exception as e:
            return f"❌ エラーが発生しました: {str(e)}", ""
    
    def setup_multiple_sites(self, config_yaml):
        """複数サイトの一括設定"""
        try:
            config_path = os.path.join(self.config_dir, "sites-config.yml")
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_yaml)
            
            # 設定ファイルの検証
            config = yaml.safe_load(config_yaml)
            
            cmd = [self.script_path, "--config", config_path]
            command_str = " ".join(cmd)
            
            sites_info = []
            if 'sites' in config:
                for site in config['sites']:
                    domain = site.get('domain', '')
                    backend = site.get('backend', '')
                    ssl = site.get('ssl', False)
                    sites_info.append(f"- {domain} → {backend} (SSL: {'有効' if ssl else '無効'})")
            
            result = f"""
✅ 複数サイト設定コマンド生成完了

🔧 実行コマンド:
```bash
{command_str}
```

📋 設定対象サイト:
{chr(10).join(sites_info)}

📁 設定ファイル: {config_path}

📝 注意事項:
実際の本番環境では、このコマンドをroot権限で実行してください。
すべてのドメインのDNS設定が完了していることを確認してください。
"""
            return result, config_yaml
            
        except yaml.YAMLError as e:
            return f"❌ YAML形式エラー: {str(e)}", ""
        except Exception as e:
            return f"❌ エラーが発生しました: {str(e)}", ""
    
    def generate_nginx_config(self, domain, backend, ssl_enabled):
        """Nginx設定ファイル生成"""
        config = f"""server {{
    listen 80;
    server_name {domain};
    
    # セキュリティヘッダー
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # リアルIPの取得
    real_ip_header X-Forwarded-For;
    real_ip_recursive on;
    
    # ログ設定
    access_log /var/log/nginx/{domain}_access.log;
    error_log /var/log/nginx/{domain}_error.log;
    
    location / {{
        proxy_pass http://{backend};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # タイムアウト設定
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # WordPress用設定
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Server $host;
        proxy_redirect off;
    }}
    
    # WordPress管理画面用設定
    location /wp-admin/ {{
        proxy_pass http://{backend};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 管理画面用タイムアウト延長
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }}
    
    # 静的ファイル用設定
    location ~* \\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {{
        proxy_pass http://{backend};
        proxy_set_header Host $host;
        proxy_cache_valid 200 1d;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }}
}}"""
        
        if ssl_enabled:
            config += f"""

# SSL設定（certbotで自動生成される予定）
server {{
    listen 443 ssl http2;
    server_name {domain};
    
    # SSL証明書（certbotで設定される）
    # ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    
    # SSL設定
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # セキュリティヘッダー
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # プロキシ設定（HTTP設定と同様）
    location / {{
        proxy_pass http://{backend};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }}
}}"""
        
        return config
    
    def validate_config(self, config_yaml):
        """設定ファイルの検証"""
        try:
            config = yaml.safe_load(config_yaml)
            
            if not isinstance(config, dict):
                return "❌ ルートは辞書形式である必要があります"
            
            if 'sites' not in config:
                return "❌ 'sites' キーが見つかりません"
            
            if not isinstance(config['sites'], list):
                return "❌ 'sites' は配列である必要があります"
            
            for i, site in enumerate(config['sites']):
                if not isinstance(site, dict):
                    return f"❌ サイト設定 {i+1} は辞書形式である必要があります"
                
                if 'domain' not in site:
                    return f"❌ サイト設定 {i+1} に 'domain' が見つかりません"
                
                if 'backend' not in site:
                    return f"❌ サイト設定 {i+1} に 'backend' が見つかりません"
                
                domain = site['domain']
                backend = site['backend']
                
                if not domain or not isinstance(domain, str):
                    return f"❌ サイト設定 {i+1} の 'domain' が無効です"
                
                if not backend or not isinstance(backend, str):
                    return f"❌ サイト設定 {i+1} の 'backend' が無効です"
                
                if ':' not in backend:
                    return f"❌ サイト設定 {i+1} の 'backend' にポート番号が含まれていません"
            
            return "✅ 設定ファイルは有効です"
            
        except yaml.YAMLError as e:
            return f"❌ YAML形式エラー: {str(e)}"
        except Exception as e:
            return f"❌ 検証エラー: {str(e)}"

# WordPress Proxy Managerインスタンス作成
proxy_manager = WordPressProxyManager()

# サンプル設定
sample_config = """sites:
  - domain: example1.com
    backend: 192.168.1.100:8080
    ssl: true
    
  - domain: example2.com
    backend: 192.168.1.101:8080
    ssl: true
    
  - domain: test.example.com
    backend: 192.168.1.102:8080
    ssl: false

global:
  webserver: nginx
  backup_dir: /etc/proxy-backups
  ssl_email: admin@example.com
"""

# Gradio UI作成
def create_ui():
    with gr.Blocks(title="WordPress Proxy設定ツール", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🔧 WordPress Proxy設定ツール
        
        WordPressサイトのリバースプロキシ設定を簡単に生成・管理できるツールです。
        Nginx/Apache両対応で、SSL証明書の自動設定も可能です。
        
        ## 📋 主要機能
        - 単一サイトのプロキシ設定
        - 複数サイトの一括設定
        - SSL証明書の自動取得設定
        - Nginx/Apache設定ファイル生成
        - 設定ファイルの検証
        """)
        
        with gr.Tab("単一サイト設定"):
            gr.Markdown("### 🎯 単一WordPressサイトのプロキシ設定")
            
            with gr.Row():
                with gr.Column():
                    domain_input = gr.Textbox(
                        label="ドメイン名",
                        placeholder="example.com",
                        info="プロキシ設定するドメイン名を入力"
                    )
                    backend_input = gr.Textbox(
                        label="バックエンドサーバー",
                        placeholder="192.168.1.100:8080",
                        info="WordPressサーバーのIP:PORT"
                    )
                    
                with gr.Column():
                    ssl_checkbox = gr.Checkbox(
                        label="SSL証明書を有効にする",
                        info="Let's Encryptで自動取得"
                    )
                    webserver_radio = gr.Radio(
                        choices=["nginx", "apache"],
                        value="nginx",
                        label="Webサーバー"
                    )
            
            setup_button = gr.Button("🚀 プロキシ設定生成", variant="primary")
            
            with gr.Row():
                with gr.Column():
                    single_result = gr.Textbox(
                        label="実行結果",
                        lines=15,
                        max_lines=20
                    )
                with gr.Column():
                    nginx_config = gr.Code(
                        label="生成されたNginx設定",
                        language="nginx",
                        lines=15
                    )
        
        with gr.Tab("複数サイト一括設定"):
            gr.Markdown("### 📦 複数WordPressサイトの一括プロキシ設定")
            
            with gr.Row():
                with gr.Column():
                    config_editor = gr.Code(
                        label="サイト設定（YAML形式）",
                        language="yaml",
                        value=sample_config,
                        lines=20
                    )
                    
                    with gr.Row():
                        validate_button = gr.Button("✅ 設定検証", variant="secondary")
                        batch_setup_button = gr.Button("🚀 一括設定生成", variant="primary")
                
                with gr.Column():
                    validation_result = gr.Textbox(
                        label="検証結果",
                        lines=5
                    )
                    batch_result = gr.Textbox(
                        label="実行結果",
                        lines=15,
                        max_lines=20
                    )
        
        with gr.Tab("ヘルプ・ドキュメント"):
            gr.Markdown("""
            ### 📚 使用方法ガイド
            
            #### 単一サイト設定
            1. **ドメイン名**: プロキシ設定したいWordPressサイトのドメイン
            2. **バックエンドサーバー**: WordPressが稼働しているサーバーのIP:PORT
            3. **SSL設定**: Let's Encryptで自動的にSSL証明書を取得する場合はチェック
            4. **Webサーバー**: nginx または apache を選択
            
            #### 複数サイト一括設定
            YAML形式で複数のサイト設定を記述：
            
            ```yaml
            sites:
              - domain: example1.com
                backend: 192.168.1.100:8080
                ssl: true
              - domain: example2.com
                backend: 192.168.1.101:8080
                ssl: false
            ```
            
            #### 📋 必要な前提条件
            - Ubuntu 20.04/22.04 または CentOS 7/8
            - Nginx 1.18+ または Apache 2.4+
            - DNS設定が完了していること
            - 80番・443番ポートが開放されていること
            
            #### 🔧 実際の実行方法
            本ツールで生成されたコマンドを、実際のサーバーでroot権限で実行してください：
            
            ```bash
            sudo ./wordpress-proxy-setup.sh --domain example.com --backend 192.168.1.100:8080 --ssl
            ```
            
            #### 🚨 重要な注意事項
            - 実行前に必ず設定ファイルのバックアップを取得してください
            - DNS設定が完了していることを確認してください
            - ファイアウォールの設定を確認してください
            - バックエンドサーバーが正常に動作していることを確認してください
            
            #### 🔗 関連リンク
            - [GitHub Repository](https://github.com/bpmbox/AUTOCREATE)
            - [完全なドキュメント](https://github.com/bpmbox/AUTOCREATE/tree/main/packages/wordpress-proxy-project)
            """)
        
        # イベントハンドラー設定
        setup_button.click(
            fn=proxy_manager.setup_single_site,
            inputs=[domain_input, backend_input, ssl_checkbox, webserver_radio],
            outputs=[single_result, nginx_config]
        )
        
        validate_button.click(
            fn=proxy_manager.validate_config,
            inputs=[config_editor],
            outputs=[validation_result]
        )
        
        batch_setup_button.click(
            fn=proxy_manager.setup_multiple_sites,
            inputs=[config_editor],
            outputs=[batch_result, config_editor]
        )
    
    return demo

# アプリケーション起動
if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )
