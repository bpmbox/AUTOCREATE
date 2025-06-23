# WordPress Proxy設定シェル - Notionナレッジベース

## 📋 プロジェクト概要

**プロジェクト名**: WordPress Proxy設定シェル  
**作成日**: 2024-01-15  
**ステータス**: ✅ 完了  
**カテゴリ**: WordPress, プロキシ設定, 自動化  

## 🎯 目的

WordPressサイトのプロキシ設定を自動化し、複数サイトの一括管理を可能にするシェルスクリプトの開発。

## ✨ 主要機能

- ✅ Nginx/Apache両対応のリバースプロキシ設定
- ✅ SSL証明書の自動取得・設定（Let's Encrypt）
- ✅ 複数WordPressサイトの一括管理
- ✅ ドメイン設定の自動化
- ✅ 設定ファイルの自動バックアップ・復元
- ✅ プロキシ状態の監視機能
- ✅ 自動テスト機能

## 📁 ファイル構成

```
packages/wordpress-proxy-project/
├── wordpress-proxy-setup.sh    # メインスクリプト
├── install.sh                  # インストールスクリプト
├── test.sh                     # テストスクリプト
├── sites-config.yml            # 設定ファイル例
├── n8n-workflow.json          # n8nワークフロー定義
└── README.md                   # ドキュメント
```

## 🚀 使用方法

### 基本的な使用方法

```bash
# 単一サイトの設定
./wordpress-proxy-setup.sh --domain example.com --backend 192.168.1.100:8080

# SSL証明書付きで設定
./wordpress-proxy-setup.sh --domain example.com --backend 192.168.1.100:8080 --ssl

# 複数サイトの一括設定
./wordpress-proxy-setup.sh --config sites-config.yml
```

### インストール

```bash
git clone https://github.com/bpmbox/AUTOCREATE.git
cd AUTOCREATE/packages/wordpress-proxy-project
chmod +x *.sh
sudo ./install.sh
```

### システムサービス化

```bash
# 監視サービス開始
sudo systemctl start wordpress-proxy-monitor

# 監視サービス状態確認
sudo systemctl status wordpress-proxy-monitor
```

## ⚙️ 設定オプション

| オプション | 説明 | 例 |
|-----------|------|-----|
| `--domain` | プロキシするドメイン名 | `example.com` |
| `--backend` | バックエンドサーバー | `192.168.1.100:8080` |
| `--ssl` | SSL証明書を有効にする | - |
| `--webserver` | Webサーバー指定 | `nginx` または `apache` |
| `--config` | 設定ファイルから一括設定 | `sites-config.yml` |
| `--backup-dir` | バックアップディレクトリ | `/etc/proxy-backups` |

## 🔧 対応環境

- **OS**: Ubuntu 20.04/22.04, CentOS 7/8
- **Webサーバー**: Nginx 1.18+, Apache 2.4+
- **SSL**: Let's Encrypt (certbot)

## 🧪 テスト

```bash
# テスト実行
./test.sh

# 個別テスト
./test.sh --test nginx-config
./test.sh --test ssl-setup
```

## 🔄 n8nワークフロー連携

プロジェクトには完全自動化のためのn8nワークフローが含まれています：

1. **Webhook受信** - プロキシ設定要求
2. **入力検証** - ドメイン・バックエンド検証
3. **プロキシ設定実行** - シェルスクリプト実行
4. **GitHub Issue作成** - 進捗管理
5. **JIRA チケット作成** - プロジェクト管理
6. **Notion ページ作成** - ナレッジベース更新
7. **miibo ナレッジ登録** - AI学習データ
8. **Supabase 結果更新** - 結果保存

## 📊 監視・ログ

- **ログファイル**: `/var/log/wordpress-proxy/monitor.log`
- **バックアップ**: `/etc/proxy-backups/`
- **設定ファイル**: `/etc/wordpress-proxy/`

## 🚨 トラブルシューティング

### よくある問題

1. **SSL証明書取得失敗**
   - DNS設定を確認
   - ファイアウォール設定を確認
   - certbotログを確認: `/var/log/letsencrypt/`

2. **プロキシ接続失敗**
   - バックエンドサーバーの状態確認
   - ネットワーク接続確認
   - Webサーバーログを確認

3. **設定ファイルエラー**
   - 構文チェック: `nginx -t` または `apache2ctl configtest`
   - バックアップから復元: `/etc/proxy-backups/`

## 🔗 関連リンク

- [GitHub Repository](https://github.com/bpmbox/AUTOCREATE)
- [GitHub Issue #36](https://github.com/bpmbox/AUTOCREATE/issues/36)
- [n8n Workflow Documentation](./n8n-workflow.json)

## 📝 更新履歴

| 日付 | バージョン | 変更内容 |
|------|------------|----------|
| 2024-01-15 | v1.0 | 初回リリース - 基本機能実装 |

## 👥 作成者

- **AI Auto-Dev System** - 自動開発システム
- **プロジェクト**: AUTOCREATE
- **リポジトリ**: bpmbox/AUTOCREATE

## 🏷️ タグ

`wordpress` `proxy` `nginx` `apache` `ssl` `automation` `shell-script` `devops` `infrastructure`
