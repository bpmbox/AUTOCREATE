# PHP バルクバッチ処理サンプル

大量データを効率的に処理するためのPHPクラスライブラリです。

## 🎯 概要

このプロジェクトは、PHPでデータベースへの大量データ操作（バルクインサート、バッチ更新、バッチ削除）を効率的に行うためのサンプル実装です。

## ✨ 主な機能

- **バルクインサート**: 大量データの一括挿入
- **バッチ更新**: 複数レコードの一括更新
- **バッチ削除**: 複数レコードの一括削除
- **CSV一括読み込み**: CSVファイルからのデータ取り込み
- **メモリ効率化**: 大量データ処理時のメモリ使用量最適化
- **エラーハンドリング**: トランザクション管理とエラー処理
- **ログ機能**: 処理状況の詳細ログ
- **パフォーマンス監視**: 処理時間とメモリ使用量の監視

## 📁 ファイル構成

```
php-bulk-batch-processing-project/
├── BulkBatchProcessor.php    # メインクラス
├── example.php              # 使用例
├── performance_test.php     # パフォーマンステスト
├── config/
│   └── database.php        # データベース設定
├── tests/
│   └── BulkBatchTest.php   # ユニットテスト
└── README.md               # このファイル
```

## 🚀 使用方法

### 1. 基本的な使用例

```php
<?php
require_once 'BulkBatchProcessor.php';

// データベース接続
$dsn = "mysql:host=localhost;dbname=your_db;charset=utf8mb4";
$processor = new BulkBatchProcessor($dsn, $username, $password, 1000);

// バルクインサート
$data = [
    ['name' => 'ユーザー1', 'email' => 'user1@example.com'],
    ['name' => 'ユーザー2', 'email' => 'user2@example.com'],
    // ... 大量データ
];

$count = $processor->bulkInsert('users', $data, ['name', 'email']);
echo "挿入完了: {$count}件";
```

### 2. バッチ更新

```php
// 更新データ準備
$updates = [
    ['id' => 1, 'status' => 'active', 'updated_at' => date('Y-m-d H:i:s')],
    ['id' => 2, 'status' => 'inactive', 'updated_at' => date('Y-m-d H:i:s')],
    // ... 
];

$count = $processor->batchUpdate('users', $updates, 'id');
echo "更新完了: {$count}件";
```

### 3. CSV一括読み込み

```php
// CSVからデータ読み込み
$data = $processor->loadFromCSV('data.csv', [
    0 => 'name',
    1 => 'email', 
    2 => 'age'
]);

// データベースに一括挿入
$count = $processor->bulkInsert('users', $data, ['name', 'email', 'age']);
```

## ⚙️ 設定

### 環境変数

```bash
# データベース設定
DB_HOST=localhost
DB_NAME=your_database
DB_USER=your_username
DB_PASS=your_password
```

### データベーステーブル例

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT NULL,
    INDEX idx_email (email),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 📊 パフォーマンス

### ベンチマーク結果例

| データ件数 | 通常処理 | バルク処理 | 高速化倍率 |
|-----------|---------|-----------|-----------|
| 1,000件   | 2.3秒   | 0.1秒     | 23倍      |
| 10,000件  | 23.1秒  | 0.8秒     | 29倍      |
| 100,000件 | 235秒   | 7.2秒     | 33倍      |

### メモリ使用量

- **通常処理**: データ件数に比例してメモリ使用量増加
- **バルク処理**: バッチサイズで制御、一定メモリ使用量

## 🔧 カスタマイズ

### バッチサイズの調整

```php
// バッチサイズを2000件に設定
$processor = new BulkBatchProcessor($dsn, $user, $pass, 2000);
```

### ログレベルの設定

```php
// ログファイルをカスタマイズ
$processor->setLogFile('custom_batch.log');
```

## 🧪 テスト実行

```bash
# ユニットテスト
php tests/BulkBatchTest.php

# パフォーマンステスト
php performance_test.php

# 使用例実行
php example.php
```

## 📝 ログ例

```
[2024-12-19 21:45:30] [INFO] [Memory: 2.5 MB] バッチ処理システム初期化完了
[2024-12-19 21:45:31] [INFO] [Memory: 15.3 MB] バルクインサート完了: 1000件 (累計: 1000件)
[2024-12-19 21:45:32] [INFO] [Memory: 15.8 MB] バルクインサート完了: 1000件 (累計: 2000件)
[2024-12-19 21:45:33] [INFO] [Memory: 16.1 MB] CSV読み込み完了: 5000件
```

## ⚠️ 注意事項

1. **メモリ制限**: 大量データ処理時はPHPのメモリ制限に注意
2. **トランザクション**: 大きなバッチサイズでは長時間のロックに注意
3. **インデックス**: 更新対象カラムに適切なインデックスを設定
4. **バックアップ**: 本番環境での実行前は必ずバックアップを取得

## 📈 最適化のポイント

1. **バッチサイズ**: データ量とメモリに応じて調整
2. **インデックス**: WHERE句で使用するカラムにインデックス
3. **トランザクション**: 適切なサイズでコミット
4. **メモリ**: 不要な変数の解放とガベージコレクション

## 🤝 貢献

バグレポートや機能改善の提案は、GitHubのIssueまたはPull Requestでお願いします。

## 📄 ライセンス

MIT License

## 🔗 関連リンク

- [PHP PDO公式ドキュメント](https://www.php.net/manual/ja/book.pdo.php)
- [MySQL バルクインサート最適化](https://dev.mysql.com/doc/refman/8.0/ja/insert-optimization.html)
- [PHPパフォーマンス最適化](https://www.php.net/manual/ja/features.gc.php)

---

📅 **生成日時**: 2024-12-19  
🤖 **生成システム**: AI自動開発パイプライン  
📂 **プロジェクトパス**: packages/php-bulk-batch-processing-project/
