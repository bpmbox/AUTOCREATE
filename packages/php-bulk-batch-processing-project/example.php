<?php
/**
 * PHP バルクバッチ処理 使用例
 * BulkBatchProcessorクラスの実用例
 */

require_once 'BulkBatchProcessor.php';

// SQLite設定（テスト用）
$dsn = "sqlite:" . __DIR__ . "/storage/database.sqlite";
$username = null;
$password = null;

try {    // バッチ処理器初期化
    $processor = new BulkBatchProcessor(
        $dsn, 
        $username, 
        $password, 
        1000 // バッチサイズ
    );
    
    echo "🚀 PHP バルクバッチ処理サンプル実行開始\n";
    echo "=" . str_repeat("=", 50) . "\n";
    
    // 例1: バルクインサート
    echo "\n📥 バルクインサート例\n";
    echo "-" . str_repeat("-", 30) . "\n";
    
    // サンプルデータ生成
    $sampleData = [];
    for ($i = 1; $i <= 10000; $i++) {
        $sampleData[] = [
            'name' => "ユーザー{$i}",
            'email' => "user{$i}@example.com",
            'age' => rand(18, 80),
            'created_at' => date('Y-m-d H:i:s')
        ];
    }
    
    $startTime = microtime(true);
    $insertedCount = $processor->bulkInsert(
        'users', 
        $sampleData, 
        ['name', 'email', 'age', 'created_at']
    );
    $endTime = microtime(true);
    
    echo "✅ バルクインサート完了: {$insertedCount}件\n";
    echo "⏱️ 処理時間: " . round($endTime - $startTime, 3) . "秒\n";
    
    // 例2: バッチ更新
    echo "\n📝 バッチ更新例\n";
    echo "-" . str_repeat("-", 30) . "\n";
    
    // 更新データ準備
    $updateData = [];
    for ($i = 1; $i <= 1000; $i++) {
        $updateData[] = [
            'id' => $i,
            'age' => rand(20, 90),
            'updated_at' => date('Y-m-d H:i:s')
        ];
    }
    
    $startTime = microtime(true);
    $updatedCount = $processor->batchUpdate('users', $updateData, 'id');
    $endTime = microtime(true);
    
    echo "✅ バッチ更新完了: {$updatedCount}件\n";
    echo "⏱️ 処理時間: " . round($endTime - $startTime, 3) . "秒\n";
    
    // 例3: CSV一括読み込み
    echo "\n📄 CSV一括読み込み例\n";
    echo "-" . str_repeat("-", 30) . "\n";
    
    // サンプルCSV作成
    $csvFile = 'sample_data.csv';
    $csvHandle = fopen($csvFile, 'w');
    fputcsv($csvHandle, ['name', 'email', 'department']);
    
    for ($i = 1; $i <= 5000; $i++) {
        fputcsv($csvHandle, [
            "従業員{$i}",
            "employee{$i}@company.com",
            ['開発部', '営業部', '管理部'][rand(0, 2)]
        ]);
    }
    fclose($csvHandle);
    
    $csvData = $processor->loadFromCSV($csvFile, [0 => 'name', 1 => 'email', 2 => 'department']);
    echo "✅ CSV読み込み完了: " . count($csvData) . "件\n";
    
    // CSV データをバルクインサート
    $insertedCount = $processor->bulkInsert(
        'employees', 
        $csvData, 
        ['name', 'email', 'department']
    );
    echo "✅ CSV→DB一括登録完了: {$insertedCount}件\n";
    
    // 例4: メモリ使用量監視
    echo "\n💾 メモリ使用量\n";
    echo "-" . str_repeat("-", 30) . "\n";
    
    $memoryInfo = $processor->getMemoryUsage();
    echo "現在のメモリ使用量: {$memoryInfo['current_formatted']}\n";
    echo "ピークメモリ使用量: {$memoryInfo['peak_formatted']}\n";
    
    // 例5: テーブル統計情報
    echo "\n📊 テーブル統計\n";
    echo "-" . str_repeat("-", 30) . "\n";
    
    $userStats = $processor->getTableStats('users');
    echo "users テーブル:\n";
    echo "  - 総行数: {$userStats['total_rows']}\n";
    echo "  - データサイズ: " . round($userStats['data_length'] / 1024 / 1024, 2) . " MB\n";
    
    // 例6: バッチ削除
    echo "\n🗑️ バッチ削除例\n";
    echo "-" . str_repeat("-", 30) . "\n";
    
    // 削除対象ID（最後の100件）
    $deleteIds = range($insertedCount - 99, $insertedCount);
    
    $startTime = microtime(true);
    $deletedCount = $processor->batchDelete('users', $deleteIds, 'id');
    $endTime = microtime(true);
    
    echo "✅ バッチ削除完了: {$deletedCount}件\n";
    echo "⏱️ 処理時間: " . round($endTime - $startTime, 3) . "秒\n";
    
    // クリーンアップ
    unlink($csvFile);
    
    echo "\n🎉 全処理完了！\n";
    echo "📝 詳細ログ: batch_processing_" . date('Y-m-d') . ".log\n";
    
} catch (Exception $e) {
    echo "❌ エラー発生: " . $e->getMessage() . "\n";
    echo "📍 ファイル: " . $e->getFile() . " 行: " . $e->getLine() . "\n";
}

/**
 * テーブル作成用SQLサンプル
 */
function createSampleTables($pdo) {
    $sql = "
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        age INT,
        created_at DATETIME,
        updated_at DATETIME DEFAULT NULL,
        INDEX idx_email (email),
        INDEX idx_age (age)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
    CREATE TABLE IF NOT EXISTS employees (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        department VARCHAR(50),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_department (department)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ";
    
    $pdo->exec($sql);
}
