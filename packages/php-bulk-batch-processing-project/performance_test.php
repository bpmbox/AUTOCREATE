<?php
/**
 * パフォーマンステスト
 * 通常処理 vs バルク処理の比較
 */

require_once 'BulkBatchProcessor.php';

class PerformanceTest
{
    private $pdo;
    private $processor;
      public function __construct($dsn, $username = null, $password = null)
    {
        $options = [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ];
        
        $this->pdo = new PDO($dsn, $username, $password, $options);
        
        $this->processor = new BulkBatchProcessor($dsn, $username, $password);
    }
    
    /**
     * 通常の一件ずつインサート
     */
    public function normalInsert($data, $table, $columns)
    {
        $this->pdo->beginTransaction();
        
        $placeholders = '(' . str_repeat('?,', count($columns) - 1) . '?)';
        $sql = "INSERT INTO {$table} (" . implode(',', $columns) . ") VALUES {$placeholders}";
        $stmt = $this->pdo->prepare($sql);
        
        $count = 0;
        foreach ($data as $row) {
            $values = [];
            foreach ($columns as $column) {
                $values[] = $row[$column];
            }
            $stmt->execute($values);
            $count++;
        }
        
        $this->pdo->commit();
        return $count;
    }
    
    /**
     * パフォーマンス比較実行
     */
    public function runComparison($testData, $table, $columns)
    {
        echo "🏃‍♂️ パフォーマンステスト開始\n";
        echo "=" . str_repeat("=", 50) . "\n";
        echo "データ件数: " . count($testData) . "件\n\n";
        
        // テーブルクリア
        $this->pdo->exec("TRUNCATE TABLE {$table}");
        
        // 1. 通常インサートテスト
        echo "1️⃣ 通常インサート（一件ずつ）\n";
        echo "-" . str_repeat("-", 30) . "\n";
        
        $startTime = microtime(true);
        $normalCount = $this->normalInsert($testData, $table, $columns);
        $normalTime = microtime(true) - $startTime;
        
        echo "✅ 処理完了: {$normalCount}件\n";
        echo "⏱️ 処理時間: " . round($normalTime, 3) . "秒\n";
        echo "⚡ 処理速度: " . round($normalCount / $normalTime) . "件/秒\n\n";
        
        // テーブルクリア
        $this->pdo->exec("TRUNCATE TABLE {$table}");
        
        // 2. バルクインサートテスト
        echo "2️⃣ バルクインサート\n";
        echo "-" . str_repeat("-", 30) . "\n";
        
        $startTime = microtime(true);
        $bulkCount = $this->processor->bulkInsert($table, $testData, $columns);
        $bulkTime = microtime(true) - $startTime;
        
        echo "✅ 処理完了: {$bulkCount}件\n";
        echo "⏱️ 処理時間: " . round($bulkTime, 3) . "秒\n";
        echo "⚡ 処理速度: " . round($bulkCount / $bulkTime) . "件/秒\n\n";
        
        // 3. 比較結果
        echo "📊 比較結果\n";
        echo "-" . str_repeat("-", 30) . "\n";
        
        $speedup = $normalTime / $bulkTime;
        $percentImprovement = (($normalTime - $bulkTime) / $normalTime) * 100;
        
        echo "🚀 バルク処理は通常処理より " . round($speedup, 2) . "倍高速\n";
        echo "📈 パフォーマンス向上: " . round($percentImprovement, 1) . "%\n";
        echo "⏰ 時間短縮: " . round($normalTime - $bulkTime, 3) . "秒\n";
        
        return [
            'normal_time' => $normalTime,
            'bulk_time' => $bulkTime,
            'speedup' => $speedup,
            'improvement_percent' => $percentImprovement
        ];
    }
}

// 設定
$dbConfig = [
    'host' => $_ENV['DB_HOST'] ?? 'localhost',
    'dbname' => $_ENV['DB_NAME'] ?? 'test_db',
    'username' => $_ENV['DB_USER'] ?? 'root',
    'password' => $_ENV['DB_PASS'] ?? ''
];

$dsn = "mysql:host={$dbConfig['host']};dbname={$dbConfig['dbname']};charset=utf8mb4";

try {
    $tester = new PerformanceTest($dsn, $dbConfig['username'], $dbConfig['password']);
    
    // テストデータ生成
    $testData = [];
    for ($i = 1; $i <= 5000; $i++) {
        $testData[] = [
            'name' => "テストユーザー{$i}",
            'email' => "test{$i}@example.com",
            'age' => rand(18, 80),
            'created_at' => date('Y-m-d H:i:s')
        ];
    }
    
    // パフォーマンステスト実行
    $results = $tester->runComparison(
        $testData, 
        'users', 
        ['name', 'email', 'age', 'created_at']
    );
    
} catch (Exception $e) {
    echo "❌ エラー: " . $e->getMessage() . "\n";
}
