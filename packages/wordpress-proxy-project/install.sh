#!/bin/bash

# WordPress Proxy Setup - Installation Script
# Version: 1.0

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# インストール先ディレクトリ
INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="/etc/wordpress-proxy"
SYSTEMD_DIR="/etc/systemd/system"

# root権限チェック
if [[ $EUID -ne 0 ]]; then
    log_error "このスクリプトはroot権限で実行してください"
    exit 1
fi

log_info "WordPress Proxy Setup インストール開始"

# ディレクトリ作成
mkdir -p "$CONFIG_DIR"
mkdir -p "/var/log/wordpress-proxy"

# スクリプトコピー
cp wordpress-proxy-setup.sh "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/wordpress-proxy-setup.sh"

# 設定ファイルコピー
cp sites-config.yml "$CONFIG_DIR/sites-config.yml.example"

# systemdサービスファイル作成
cat > "$SYSTEMD_DIR/wordpress-proxy-monitor.service" << 'EOF'
[Unit]
Description=WordPress Proxy Monitor
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/wordpress-proxy-monitor.sh
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

# モニタースクリプト作成
cat > "$INSTALL_DIR/wordpress-proxy-monitor.sh" << 'EOF'
#!/bin/bash

# WordPress Proxy Monitor Script
# 設定されたプロキシサイトの状態を監視

LOG_FILE="/var/log/wordpress-proxy/monitor.log"
CONFIG_FILE="/etc/wordpress-proxy/sites-config.yml"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

check_site() {
    local domain="$1"
    local backend="$2"
    
    # HTTP接続チェック
    if curl -s -o /dev/null -w "%{http_code}" "http://$domain" | grep -q "200\|301\|302"; then
        log_message "OK: $domain"
        return 0
    else
        log_message "ERROR: $domain is not responding"
        return 1
    fi
}

# メイン監視ループ
while true; do
    if [[ -f "$CONFIG_FILE" ]]; then
        # 設定ファイルから監視対象を読み込み
        while IFS= read -r line; do
            if [[ "$line" =~ domain:[[:space:]]*(.+) ]]; then
                domain="${BASH_REMATCH[1]}"
                check_site "$domain"
            fi
        done < "$CONFIG_FILE"
    fi
    
    sleep 300  # 5分間隔で監視
done
EOF

chmod +x "$INSTALL_DIR/wordpress-proxy-monitor.sh"

# bashコンプリート設定
cat > "/etc/bash_completion.d/wordpress-proxy-setup" << 'EOF'
_wordpress_proxy_setup() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--domain --backend --ssl --webserver --config --backup-dir --help"
    
    case ${prev} in
        --webserver|-w)
            COMPREPLY=( $(compgen -W "nginx apache" -- ${cur}) )
            return 0
            ;;
        --config|-c)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
        --backup-dir)
            COMPREPLY=( $(compgen -d -- ${cur}) )
            return 0
            ;;
        *)
            ;;
    esac
    
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}

complete -F _wordpress_proxy_setup wordpress-proxy-setup.sh
EOF

# サービス有効化
systemctl daemon-reload
systemctl enable wordpress-proxy-monitor.service

# シンボリックリンク作成
ln -sf "$INSTALL_DIR/wordpress-proxy-setup.sh" "/usr/local/bin/wp-proxy"

log_success "インストールが完了しました！"
echo
echo "使用方法:"
echo "  wp-proxy --domain example.com --backend 192.168.1.100:8080"
echo "  wp-proxy --config /etc/wordpress-proxy/sites-config.yml"
echo
echo "設定ファイル例: /etc/wordpress-proxy/sites-config.yml.example"
echo "ログファイル: /var/log/wordpress-proxy/monitor.log"
echo
echo "監視サービス開始: systemctl start wordpress-proxy-monitor"
echo "監視サービス状態: systemctl status wordpress-proxy-monitor"
