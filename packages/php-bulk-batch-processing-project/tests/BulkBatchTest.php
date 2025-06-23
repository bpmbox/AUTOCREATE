<?php
/**
 * BulkBatchProcessor ユニットテスト
 */

require_once __DIR__ . '/../BulkBatchProcessor.php';

class BulkBatchTest
{
    private $processor;
    private $testDb = ':memory:'; // SQLite インメモリDB
    
    public function setUp()
    {
        // テスト用SQLiteデータベース
        $dsn = "sqlite:{$this->testDb}";
        $this->processor = new BulkBatchProcessor($dsn, '', '', 100);
        
        // テストテーブル作成
        $this->createTestTables();
    }
    
    private function createTestTables()
    {
        $sql = "
        CREATE TABLE test_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TEXT
        );
        
        CREATE TABLE test_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            category TEXT
        );
        ";
        
        $this->processor->getPdo()->exec($sql);
    }
    
    public function testBulkInsert()
    {
        echo "🧪 バルクインサートテスト\n";
        
        $testData = [];
        for ($i = 1; $i <= 250; $i++) {
            $testData[] = [
                'name' => "ユーザー{$i}",
                'email' => "user{$i}@test.com",
                'age' => 20 + ($i % 50),
                'created_at' => date('Y-m-d H:i:s')
            ];
        }
        
        $insertedCount = $this->processor->bulkInsert(
            'test_users', 
            $testData, 
            ['name', 'email', 'age', 'created_at']
        );
        
        $this->assertEqual($insertedCount, 250, "バルクインサート件数");
        
        // 実際にDBに挿入されているか確認
        $stmt = $this->processor->getPdo()->query("SELECT COUNT(*) as count FROM test_users");
        $result = $stmt->fetch();
        $this->assertEqual($result['count'], 250, "DB内レコード数");
        
        echo "✅ バルクインサートテスト成功\n";
    }
    
    public function testBatchUpdate()
    {
        echo "🧪 バッチ更新テスト\n";
        
        // 先にデータを挿入
        $this->testBulkInsert();
        
        $updateData = [];
        for ($i = 1; $i <= 50; $i++) {
            $updateData[] = [
                'id' => $i,
                'age' => 30 + $i
            ];
        }
        
        $updatedCount = $this->processor->batchUpdate('test_users', $updateData, 'id');
        $this->assertEqual($updatedCount, 50, "バッチ更新件数");
        
        // 更新内容確認
        $stmt = $this->processor->getPdo()->query("SELECT age FROM test_users WHERE id = 1");
        $result = $stmt->fetch();
        $this->assertEqual($result['age'], 31, "更新内容確認");
        
        echo "✅ バッチ更新テスト成功\n";
    }
    
    public function testBatchDelete()
    {
        echo "🧪 バッチ削除テスト\n";
        
        // 先にデータを挿入
        $this->testBulkInsert();
        
        $deleteIds = range(1, 30);
        $deletedCount = $this->processor->batchDelete('test_users', $deleteIds, 'id');
        
        $this->assertEqual($deletedCount, 30, "バッチ削除件数");
        
        // 削除確認
        $stmt = $this->processor->getPdo()->query("SELECT COUNT(*) as count FROM test_users");
        $result = $stmt->fetch();
        $this->assertEqual($result['count'], 220, "削除後のレコード数");
        
        echo "✅ バッチ削除テスト成功\n";
    }
    
    public function testCSVLoad()
    {
        echo "🧪 CSV読み込みテスト\n";
        
        // テスト用CSV作成
        $csvFile = 'test_data.csv';
        $handle = fopen($csvFile, 'w');
        fputcsv($handle, ['name', 'price', 'category']);
        
        for ($i = 1; $i <= 100; $i++) {
            fputcsv($handle, [
                "商品{$i}",
                rand(100, 10000),
                ['電子機器', '書籍', '衣類'][rand(0, 2)]
            ]);
        }
        fclose($handle);
        
        $data = $this->processor->loadFromCSV($csvFile, [
            0 => 'name',
            1 => 'price', 
            2 => 'category'
        ]);
        
        $this->assertEqual(count($data), 100, "CSV読み込み件数");
        $this->assertTrue(isset($data[0]['name']), "CSV列マッピング");
        
        // クリーンアップ
        unlink($csvFile);
        
        echo "✅ CSV読み込みテスト成功\n";
    }
    
    public function testMemoryUsage()
    {
        echo "🧪 メモリ使用量テスト\n";
        
        $memoryInfo = $this->processor->getMemoryUsage();
        
        $this->assertTrue(is_array($memoryInfo), "メモリ情報配列");
        $this->assertTrue(isset($memoryInfo['current']), "現在メモリ");
        $this->assertTrue(isset($memoryInfo['peak']), "ピークメモリ");
        $this->assertTrue($memoryInfo['current'] > 0, "メモリ使用量正数");
        
        echo "✅ メモリ使用量テスト成功\n";
    }
    
    public function testErrorHandling()
    {
        echo "🧪 エラーハンドリングテスト\n";
        
        // 存在しないテーブルでエラー発生
        try {
            $this->processor->bulkInsert('nonexistent_table', [['test' => 'data']], ['test']);
            $this->assertTrue(false, "例外が発生すべき");
        } catch (Exception $e) {
            $this->assertTrue(true, "例外ハンドリング");
        }
        
        // 重複キーエラー
        $testData = [
            ['name' => 'テスト', 'email' => 'test@test.com', 'age' => 25],
            ['name' => 'テスト2', 'email' => 'test@test.com', 'age' => 30] // 同じメール
        ];
        
        try {
            $this->processor->bulkInsert('test_users', $testData, ['name', 'email', 'age']);
            $this->assertTrue(false, "重複キーエラーが発生すべき");
        } catch (Exception $e) {
            $this->assertTrue(true, "重複キーエラーハンドリング");
        }
        
        echo "✅ エラーハンドリングテスト成功\n";
    }
    
    // アサーション関数
    private function assertEqual($actual, $expected, $message)
    {
        if ($actual === $expected) {
            echo "  ✓ {$message}: {$actual}\n";
        } else {
            echo "  ❌ {$message}: 期待値 {$expected}, 実際値 {$actual}\n";
            throw new Exception("テスト失敗: {$message}");
        }
    }
    
    private function assertTrue($condition, $message)
    {
        if ($condition) {
            echo "  ✓ {$message}\n";
        } else {
            echo "  ❌ {$message}\n";
            throw new Exception("テスト失敗: {$message}");
        }
    }
    
    public function runAllTests()
    {
        echo "🚀 BulkBatchProcessor ユニットテスト開始\n";
        echo "=" . str_repeat("=", 50) . "\n";
        
        $this->setUp();
        
        try {
            $this->testBulkInsert();
            $this->setUp(); // リセット
            
            $this->testBatchUpdate();
            $this->setUp(); // リセット
            
            $this->testBatchDelete();
            $this->setUp(); // リセット
            
            $this->testCSVLoad();
            $this->testMemoryUsage();
            $this->testErrorHandling();
            
            echo "\n🎉 全テスト成功！\n";
            
        } catch (Exception $e) {
            echo "\n❌ テスト失敗: " . $e->getMessage() . "\n";
        }
    }
}

// テスト実行
if (php_sapi_name() === 'cli') {
    $test = new BulkBatchTest();
    $test->runAllTests();
}
