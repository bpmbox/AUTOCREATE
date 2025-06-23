#!/bin/bash

# WordPress Proxy Setup Script
# Version: 1.0
# Author: AI Auto-Dev System

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 設定変数
DOMAIN=""
BACKEND=""
SSL_ENABLED=false
WEBSERVER=""
CONFIG_FILE=""
BACKUP_DIR="/etc/proxy-backups"
NGINX_SITES_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"
APACHE_SITES_DIR="/etc/apache2/sites-available"

# ヘルプ表示
show_help() {
    cat << EOF
WordPress Proxy Setup Script

使用方法:
    $0 [OPTIONS]

オプション:
    -d, --domain DOMAIN         プロキシするドメイン名
    -b, --backend BACKEND       バックエンドサーバー（IP:PORT）
    -s, --ssl                   SSL証明書を有効にする
    -w, --webserver SERVER      Webサーバー (nginx|apache)
    -c, --config FILE           設定ファイルから複数サイトを設定
    --backup-dir DIR            バックアップディレクトリ
    -h, --help                  このヘルプを表示

例:
    $0 --domain example.com --backend 192.168.1.100:8080
    $0 --domain example.com --backend 192.168.1.100:8080 --ssl
    $0 --config sites-config.yml

EOF
}

# 引数解析
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--domain)
                DOMAIN="$2"
                shift 2
                ;;
            -b|--backend)
                BACKEND="$2"
                shift 2
                ;;
            -s|--ssl)
                SSL_ENABLED=true
                shift
                ;;
            -w|--webserver)
                WEBSERVER="$2"
                shift 2
                ;;
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --backup-dir)
                BACKUP_DIR="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "不明なオプション: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 必要なパッケージの確認・インストール
install_dependencies() {
    log_info "依存関係をチェック中..."
    
    # OS検出
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$ID
    else
        log_error "OSを検出できません"
        exit 1
    fi
    
    case $OS in
        ubuntu|debian)
            apt-get update
            if [[ "$WEBSERVER" == "nginx" || -z "$WEBSERVER" ]]; then
                apt-get install -y nginx
            fi
            if [[ "$WEBSERVER" == "apache" ]]; then
                apt-get install -y apache2
            fi
            if [[ "$SSL_ENABLED" == true ]]; then
                apt-get install -y certbot
                if [[ "$WEBSERVER" == "nginx" || -z "$WEBSERVER" ]]; then
                    apt-get install -y python3-certbot-nginx
                fi
                if [[ "$WEBSERVER" == "apache" ]]; then
                    apt-get install -y python3-certbot-apache
                fi
            fi
            ;;
        centos|rhel|fedora)
            if command -v dnf &> /dev/null; then
                PKG_MGR="dnf"
            else
                PKG_MGR="yum"
            fi
            
            $PKG_MGR update -y
            if [[ "$WEBSERVER" == "nginx" || -z "$WEBSERVER" ]]; then
                $PKG_MGR install -y nginx
            fi
            if [[ "$WEBSERVER" == "apache" ]]; then
                $PKG_MGR install -y httpd
            fi
            if [[ "$SSL_ENABLED" == true ]]; then
                $PKG_MGR install -y certbot
                if [[ "$WEBSERVER" == "nginx" || -z "$WEBSERVER" ]]; then
                    $PKG_MGR install -y python3-certbot-nginx
                fi
                if [[ "$WEBSERVER" == "apache" ]]; then
                    $PKG_MGR install -y python3-certbot-apache
                fi
            fi
            ;;
        *)
            log_error "サポートされていないOS: $OS"
            exit 1
            ;;
    esac
    
    log_success "依存関係のインストールが完了しました"
}

# Webサーバー自動検出
detect_webserver() {
    if [[ -n "$WEBSERVER" ]]; then
        return
    fi
    
    if command -v nginx &> /dev/null && systemctl is-active --quiet nginx; then
        WEBSERVER="nginx"
        log_info "Nginxが検出されました"
    elif command -v apache2 &> /dev/null && systemctl is-active --quiet apache2; then
        WEBSERVER="apache"
        log_info "Apacheが検出されました"
    elif command -v httpd &> /dev/null && systemctl is-active --quiet httpd; then
        WEBSERVER="apache"
        log_info "Apache (httpd)が検出されました"
    else
        log_warning "Webサーバーが検出されませんでした。Nginxをインストールします"
        WEBSERVER="nginx"
    fi
}

# バックアップディレクトリ作成
create_backup_dir() {
    if [[ ! -d "$BACKUP_DIR" ]]; then
        mkdir -p "$BACKUP_DIR"
        log_info "バックアップディレクトリを作成しました: $BACKUP_DIR"
    fi
}

# 設定ファイルバックアップ
backup_config() {
    local config_file="$1"
    local backup_name="$(basename "$config_file").$(date +%Y%m%d_%H%M%S).bak"
    
    if [[ -f "$config_file" ]]; then
        cp "$config_file" "$BACKUP_DIR/$backup_name"
        log_info "設定ファイルをバックアップしました: $backup_name"
    fi
}

# Nginx設定生成
generate_nginx_config() {
    local domain="$1"
    local backend="$2"
    local config_file="$NGINX_SITES_DIR/$domain"
    
    backup_config "$config_file"
    
    cat > "$config_file" << EOF
server {
    listen 80;
    server_name $domain;
    
    # セキュリティヘッダー
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # リアルIPの取得
    real_ip_header X-Forwarded-For;
    real_ip_recursive on;
    
    # ログ設定
    access_log /var/log/nginx/${domain}_access.log;
    error_log /var/log/nginx/${domain}_error.log;
    
    location / {
        proxy_pass http://$backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # タイムアウト設定
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # バッファリング設定
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        
        # WordPress用設定
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Server \$host;
        proxy_redirect off;
    }
    
    # WordPress管理画面用設定
    location /wp-admin/ {
        proxy_pass http://$backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # 管理画面用タイムアウト延長
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
    
    # 静的ファイル用設定
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://$backend;
        proxy_set_header Host \$host;
        proxy_cache_valid 200 1d;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

    if [[ "$SSL_ENABLED" == true ]]; then
        cat >> "$config_file" << EOF

# SSL設定（certbotで自動生成される予定）
EOF
    fi
    
    # サイト有効化
    if [[ ! -L "$NGINX_ENABLED_DIR/$domain" ]]; then
        ln -s "$config_file" "$NGINX_ENABLED_DIR/$domain"
    fi
    
    log_success "Nginx設定を生成しました: $config_file"
}

# Apache設定生成
generate_apache_config() {
    local domain="$1"
    local backend="$2"
    local config_file="$APACHE_SITES_DIR/$domain.conf"
    
    backup_config "$config_file"
    
    cat > "$config_file" << EOF
<VirtualHost *:80>
    ServerName $domain
    
    # ログ設定
    ErrorLog \${APACHE_LOG_DIR}/${domain}_error.log
    CustomLog \${APACHE_LOG_DIR}/${domain}_access.log combined
    
    # プロキシ設定
    ProxyPreserveHost On
    ProxyRequests Off
    
    # セキュリティヘッダー
    Header always set X-Frame-Options SAMEORIGIN
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    
    # メインプロキシ設定
    ProxyPass / http://$backend/
    ProxyPassReverse / http://$backend/
    
    # WordPress用ヘッダー設定
    ProxyPassReverse / http://$backend/
    ProxyPassReverseRewrite Location ^http://$backend/ http://$domain/
    
    # 静的ファイル用キャッシュ設定
    <LocationMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$">
        ExpiresActive On
        ExpiresDefault "access plus 1 day"
        Header set Cache-Control "public, immutable"
    </LocationMatch>
</VirtualHost>
EOF

    if [[ "$SSL_ENABLED" == true ]]; then
        cat >> "$config_file" << EOF

# SSL設定（certbotで自動生成される予定）
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName $domain
    
    # SSL設定はcertbotで自動生成されます
    
    # ログ設定
    ErrorLog \${APACHE_LOG_DIR}/${domain}_ssl_error.log
    CustomLog \${APACHE_LOG_DIR}/${domain}_ssl_access.log combined
    
    # プロキシ設定
    ProxyPreserveHost On
    ProxyRequests Off
    
    # セキュリティヘッダー
    Header always set X-Frame-Options SAMEORIGIN
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    
    # メインプロキシ設定
    ProxyPass / http://$backend/
    ProxyPassReverse / http://$backend/
    
    # WordPress用ヘッダー設定
    ProxyPassReverse / http://$backend/
    ProxyPassReverseRewrite Location ^http://$backend/ https://$domain/
    
    # 静的ファイル用キャッシュ設定
    <LocationMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$">
        ExpiresActive On
        ExpiresDefault "access plus 1 day"
        Header set Cache-Control "public, immutable"
    </LocationMatch>
</VirtualHost>
</IfModule>
EOF
    fi
    
    # サイト有効化
    a2ensite "$domain"
    
    # 必要なモジュール有効化
    a2enmod proxy
    a2enmod proxy_http
    a2enmod headers
    a2enmod expires
    if [[ "$SSL_ENABLED" == true ]]; then
        a2enmod ssl
    fi
    
    log_success "Apache設定を生成しました: $config_file"
}

# SSL証明書取得
setup_ssl() {
    local domain="$1"
    
    if [[ "$SSL_ENABLED" != true ]]; then
        return
    fi
    
    log_info "SSL証明書を取得中: $domain"
    
    case $WEBSERVER in
        nginx)
            certbot --nginx -d "$domain" --non-interactive --agree-tos --email admin@"$domain" --redirect
            ;;
        apache)
            certbot --apache -d "$domain" --non-interactive --agree-tos --email admin@"$domain" --redirect
            ;;
    esac
    
    if [[ $? -eq 0 ]]; then
        log_success "SSL証明書の取得が完了しました: $domain"
        
        # 自動更新の設定
        if ! crontab -l 2>/dev/null | grep -q "certbot renew"; then
            (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
            log_info "SSL証明書の自動更新を設定しました"
        fi
    else
        log_error "SSL証明書の取得に失敗しました: $domain"
    fi
}

# Webサーバー再起動
restart_webserver() {
    log_info "Webサーバーを再起動中..."
    
    case $WEBSERVER in
        nginx)
            # 設定テスト
            if nginx -t; then
                systemctl reload nginx
                log_success "Nginxを再起動しました"
            else
                log_error "Nginx設定にエラーがあります"
                exit 1
            fi
            ;;
        apache)
            # 設定テスト
            if apache2ctl configtest; then
                systemctl reload apache2 || systemctl reload httpd
                log_success "Apacheを再起動しました"
            else
                log_error "Apache設定にエラーがあります"
                exit 1
            fi
            ;;
    esac
}

# 設定検証
verify_setup() {
    local domain="$1"
    local backend="$2"
    
    log_info "設定を検証中: $domain"
    
    # DNS解決確認
    if ! nslookup "$domain" &>/dev/null; then
        log_warning "DNS解決ができません: $domain"
    fi
    
    # バックエンド接続確認
    local backend_ip=$(echo "$backend" | cut -d: -f1)
    local backend_port=$(echo "$backend" | cut -d: -f2)
    
    if ! nc -z "$backend_ip" "$backend_port" 2>/dev/null; then
        log_warning "バックエンドサーバーに接続できません: $backend"
    fi
    
    # HTTP接続テスト
    if curl -s -o /dev/null -w "%{http_code}" "http://$domain" | grep -q "200\|301\|302"; then
        log_success "HTTP接続テスト成功: $domain"
    else
        log_warning "HTTP接続テストに失敗: $domain"
    fi
    
    # HTTPS接続テスト（SSL有効時）
    if [[ "$SSL_ENABLED" == true ]]; then
        if curl -s -o /dev/null -w "%{http_code}" "https://$domain" | grep -q "200\|301\|302"; then
            log_success "HTTPS接続テスト成功: $domain"
        else
            log_warning "HTTPS接続テストに失敗: $domain"
        fi
    fi
}

# 設定ファイルから複数サイト設定
setup_from_config() {
    local config_file="$1"
    
    if [[ ! -f "$config_file" ]]; then
        log_error "設定ファイルが見つかりません: $config_file"
        exit 1
    fi
    
    log_info "設定ファイルから複数サイトを設定中: $config_file"
    
    # YAML解析（簡単な実装）
    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*domain:[[:space:]]*(.+)$ ]]; then
            current_domain="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]*backend:[[:space:]]*(.+)$ ]]; then
            current_backend="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ ^[[:space:]]*ssl:[[:space:]]*(.+)$ ]]; then
            current_ssl="${BASH_REMATCH[1]}"
            
            # 1つのサイト設定完了
            if [[ -n "$current_domain" && -n "$current_backend" ]]; then
                log_info "サイト設定中: $current_domain -> $current_backend"
                
                if [[ "$current_ssl" == "true" ]]; then
                    SSL_ENABLED=true
                else
                    SSL_ENABLED=false
                fi
                
                setup_single_site "$current_domain" "$current_backend"
                
                # 変数リセット
                current_domain=""
                current_backend=""
                current_ssl=""
            fi
        fi
    done < "$config_file"
}

# 単一サイト設定
setup_single_site() {
    local domain="$1"
    local backend="$2"
    
    log_info "プロキシ設定を開始: $domain -> $backend"
    
    # Webサーバー設定生成
    case $WEBSERVER in
        nginx)
            generate_nginx_config "$domain" "$backend"
            ;;
        apache)
            generate_apache_config "$domain" "$backend"
            ;;
        *)
            log_error "サポートされていないWebサーバー: $WEBSERVER"
            exit 1
            ;;
    esac
    
    # SSL設定
    setup_ssl "$domain"
    
    # 設定検証
    verify_setup "$domain" "$backend"
    
    log_success "プロキシ設定が完了しました: $domain"
}

# メイン処理
main() {
    log_info "WordPress Proxy Setup Script 開始"
    
    # 引数解析
    parse_arguments "$@"
    
    # root権限チェック
    if [[ $EUID -ne 0 ]]; then
        log_error "このスクリプトはroot権限で実行してください"
        exit 1
    fi
    
    # バックアップディレクトリ作成
    create_backup_dir
    
    # Webサーバー検出
    detect_webserver
    
    # 依存関係インストール
    install_dependencies
    
    if [[ -n "$CONFIG_FILE" ]]; then
        # 設定ファイルから複数サイト設定
        setup_from_config "$CONFIG_FILE"
    elif [[ -n "$DOMAIN" && -n "$BACKEND" ]]; then
        # 単一サイト設定
        setup_single_site "$DOMAIN" "$BACKEND"
    else
        log_error "ドメインとバックエンドサーバーを指定してください"
        show_help
        exit 1
    fi
    
    # Webサーバー再起動
    restart_webserver
    
    log_success "すべての設定が完了しました！"
    echo
    echo "設定済みサイト:"
    if [[ -n "$DOMAIN" ]]; then
        echo "  - http://$DOMAIN"
        if [[ "$SSL_ENABLED" == true ]]; then
            echo "  - https://$DOMAIN"
        fi
    fi
    echo
    echo "設定ファイル: $BACKUP_DIR にバックアップされています"
    echo
}

# スクリプト実行
main "$@"
