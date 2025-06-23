# WordPress Proxy設定シェル

## 概要
WordPressサイトのプロキシ設定を自動化するシェルスクリプトです。Nginx/Apache両対応でSSL証明書の自動設定も行います。

## 機能
- リバースプロキシ設定の自動生成
- SSL証明書の自動取得・設定（Let's Encrypt対応）
- 複数WordPressサイトの一括管理
- ドメイン設定の自動化
- 設定ファイルの自動バックアップ・復元

## 使用方法
```bash
# 基本的な設定
./wordpress-proxy-setup.sh --domain example.com --backend 192.168.1.100:8080

# SSL証明書付きで設定
./wordpress-proxy-setup.sh --domain example.com --backend 192.168.1.100:8080 --ssl

# 複数サイトの一括設定
./wordpress-proxy-setup.sh --config sites-config.yml
```

## 対応環境
- Ubuntu 20.04/22.04
- CentOS 7/8
- Nginx 1.18+
- Apache 2.4+

## インストール
```bash
git clone https://github.com/bpmbox/AUTOCREATE.git
cd AUTOCREATE/packages/wordpress-proxy-project
chmod +x wordpress-proxy-setup.sh
sudo ./install.sh
```
