<?php
/**
 * パフォーマンステスト - SQLite版
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
        $this->processor = new BulkBatchProcessor($dsn, $username, $password, 1000);
        
        // テスト用テーブル作成
        $this->createTestTable();
    }
    
    private function createTestTable()
    {
        $sql = "CREATE TABLE IF NOT EXISTS performance_test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )";
        
        $this->pdo->exec($sql);
        $this->pdo->exec("DELETE FROM performance_test"); // クリア
    }
    
    public function runComparison($testData, $tableName, $columns)
    {
        echo "🔥 パフォーマンステスト開始\n";
        echo "📊 テストデータ数: " . count($testData) . "件\n";
        echo "=" . str_repeat("=", 50) . "\n";
        
        // 1. 通常のインサート（1件ずつ）
        echo "\n⚡ 通常処理テスト (1件ずつ)\n";
        $this->pdo->exec("DELETE FROM $tableName");
        
        $normalStart = microtime(true);
        
        $stmt = $this->pdo->prepare("INSERT INTO $tableName (name, email, age, created_at) VALUES (?, ?, ?, ?)");
        
        foreach ($testData as $data) {
            $stmt->execute([
                $data['name'],
                $data['email'], 
                $data['age'],
                $data['created_at']
            ]);
        }
        
        $normalTime = microtime(true) - $normalStart;
        $normalCount = $this->pdo->query("SELECT COUNT(*) FROM $tableName")->fetchColumn();
        
        echo "✅ 通常処理完了: {$normalCount}件\n";
        echo "⏱️ 処理時間: " . number_format($normalTime, 3) . "秒\n";
        
        // 2. バルク処理
        echo "\n🚀 バルク処理テスト (1000件ずつ)\n";
        $this->pdo->exec("DELETE FROM $tableName");
        
        $bulkStart = microtime(true);
        
        $bulkCount = $this->processor->bulkInsert($tableName, $testData, $columns);
        
        $bulkTime = microtime(true) - $bulkStart;
        $actualCount = $this->pdo->query("SELECT COUNT(*) FROM $tableName")->fetchColumn();
        
        echo "✅ バルク処理完了: {$actualCount}件\n";
        echo "⏱️ 処理時間: " . number_format($bulkTime, 3) . "秒\n";
        
        // 結果比較
        echo "\n📈 パフォーマンス比較結果\n";
        echo "-" . str_repeat("-", 30) . "\n";
        
        $speedup = $normalTime / $bulkTime;
        $efficiency = (($normalTime - $bulkTime) / $normalTime) * 100;
        
        echo "📊 通常処理: " . number_format($normalTime, 3) . "秒\n";
        echo "🚀 バルク処理: " . number_format($bulkTime, 3) . "秒\n";
        echo "⚡ 速度向上: " . number_format($speedup, 2) . "倍\n";
        echo "💡 効率化: " . number_format($efficiency, 1) . "%改善\n";
        
        if ($speedup > 10) {
            echo "🎉 素晴らしい！バルク処理が大幅に高速化されました！\n";
        } elseif ($speedup > 5) {
            echo "✅ バルク処理による大幅な速度向上を確認！\n";
        } else {
            echo "📝 バルク処理による速度向上を確認\n";
        }
        
        return [
            'normal_time' => $normalTime,
            'bulk_time' => $bulkTime,
            'speedup' => $speedup,
            'efficiency' => $efficiency,
            'data_count' => count($testData)
        ];
    }
}

// SQLite設定（テスト用）
$dsn = "sqlite:" . __DIR__ . "/storage/database.sqlite";

try {
    $tester = new PerformanceTest($dsn);
    
    // テストデータ生成（5000件）
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
        'performance_test', 
        ['name', 'email', 'age', 'created_at']
    );
    
    echo "\n🎯 テスト完了！\n";
    echo "📋 結果サマリー:\n";
    echo "  - データ数: {$results['data_count']}件\n";
    echo "  - 速度向上: {$results['speedup']}倍\n";
    echo "  - 効率化: {$results['efficiency']}%\n";
    
} catch (Exception $e) {
    echo "❌ エラー: " . $e->getMessage() . "\n";
}
?>
