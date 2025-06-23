<?php
/**
 * PHP バルクバッチ処理サンプル
 * 大量データの効率的な処理を行うクラス
 * 
 * 機能:
 * - データベース接続（PDO）
 * - バルクインサート
 * - バッチ更新
 * - メモリ効率化
 * - エラーハンドリング
 * - ログ機能
 */

class BulkBatchProcessor
{
    private $pdo;
    private $batchSize;
    private $logFile;
      public function __construct($dsn, $username = null, $password = null, $batchSize = 1000)
    {
        try {
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            ];
            
            // MySQLの場合のみ追加オプション
            if (strpos($dsn, 'mysql:') === 0) {
                $options[PDO::MYSQL_ATTR_USE_BUFFERED_QUERY] = false;
            }
            
            $this->pdo = new PDO($dsn, $username, $password, $options);
            $this->batchSize = $batchSize;
            $this->logFile = 'batch_processing_' . date('Y-m-d') . '.log';
            $this->log("バッチ処理システム初期化完了");
        } catch (PDOException $e) {
            throw new Exception("データベース接続エラー: " . $e->getMessage());
        }
    }
    
    /**
     * バルクインサート実行
     * 
     * @param string $table テーブル名
     * @param array $data 挿入データ配列
     * @param array $columns カラム名配列
     * @return int 処理件数
     */
    public function bulkInsert($table, $data, $columns)
    {
        $totalProcessed = 0;
        $chunks = array_chunk($data, $this->batchSize);
        
        foreach ($chunks as $chunk) {
            try {
                $this->pdo->beginTransaction();
                
                // プレースホルダー生成
                $placeholders = '(' . str_repeat('?,', count($columns) - 1) . '?)';
                $sql = "INSERT INTO {$table} (" . implode(',', $columns) . ") VALUES ";
                $sql .= str_repeat($placeholders . ',', count($chunk) - 1) . $placeholders;
                
                // データ平坦化
                $flatData = [];
                foreach ($chunk as $row) {
                    foreach ($columns as $column) {
                        $flatData[] = $row[$column] ?? null;
                    }
                }
                
                $stmt = $this->pdo->prepare($sql);
                $stmt->execute($flatData);
                
                $this->pdo->commit();
                $processed = count($chunk);
                $totalProcessed += $processed;
                
                $this->log("バルクインサート完了: {$processed}件 (累計: {$totalProcessed}件)");
                
            } catch (Exception $e) {
                $this->pdo->rollBack();
                $this->log("エラー: " . $e->getMessage(), 'ERROR');
                throw $e;
            }
        }
        
        return $totalProcessed;
    }
    
    /**
     * バッチ更新実行
     * 
     * @param string $table テーブル名
     * @param array $updates 更新データ配列（IDと更新値のペア）
     * @param string $idColumn ID列名
     * @return int 更新件数
     */
    public function batchUpdate($table, $updates, $idColumn = 'id')
    {
        $totalUpdated = 0;
        $chunks = array_chunk($updates, $this->batchSize);
        
        foreach ($chunks as $chunk) {
            try {
                $this->pdo->beginTransaction();
                
                foreach ($chunk as $update) {
                    $id = $update[$idColumn];
                    unset($update[$idColumn]);
                    
                    $setParts = [];
                    $values = [];
                    
                    foreach ($update as $column => $value) {
                        $setParts[] = "{$column} = ?";
                        $values[] = $value;
                    }
                    $values[] = $id;
                    
                    $sql = "UPDATE {$table} SET " . implode(', ', $setParts) . " WHERE {$idColumn} = ?";
                    $stmt = $this->pdo->prepare($sql);
                    $stmt->execute($values);
                }
                
                $this->pdo->commit();
                $updated = count($chunk);
                $totalUpdated += $updated;
                
                $this->log("バッチ更新完了: {$updated}件 (累計: {$totalUpdated}件)");
                
            } catch (Exception $e) {
                $this->pdo->rollBack();
                $this->log("エラー: " . $e->getMessage(), 'ERROR');
                throw $e;
            }
        }
        
        return $totalUpdated;
    }
    
    /**
     * バッチ削除実行
     * 
     * @param string $table テーブル名
     * @param array $ids 削除するID配列
     * @param string $idColumn ID列名
     * @return int 削除件数
     */
    public function batchDelete($table, $ids, $idColumn = 'id')
    {
        $totalDeleted = 0;
        $chunks = array_chunk($ids, $this->batchSize);
        
        foreach ($chunks as $chunk) {
            try {
                $this->pdo->beginTransaction();
                
                $placeholders = str_repeat('?,', count($chunk) - 1) . '?';
                $sql = "DELETE FROM {$table} WHERE {$idColumn} IN ({$placeholders})";
                
                $stmt = $this->pdo->prepare($sql);
                $stmt->execute($chunk);
                
                $this->pdo->commit();
                $deleted = $stmt->rowCount();
                $totalDeleted += $deleted;
                
                $this->log("バッチ削除完了: {$deleted}件 (累計: {$totalDeleted}件)");
                
            } catch (Exception $e) {
                $this->pdo->rollBack();
                $this->log("エラー: " . $e->getMessage(), 'ERROR');
                throw $e;
            }
        }
        
        return $totalDeleted;
    }
    
    /**
     * CSVファイルから一括読み込み
     * 
     * @param string $filePath CSVファイルパス
     * @param array $columns カラムマッピング
     * @return array データ配列
     */
    public function loadFromCSV($filePath, $columns)
    {
        if (!file_exists($filePath)) {
            throw new Exception("CSVファイルが見つかりません: {$filePath}");
        }
        
        $data = [];
        $handle = fopen($filePath, 'r');
        
        if ($handle === false) {
            throw new Exception("CSVファイルを開けません: {$filePath}");
        }
        
        // ヘッダー行をスキップ
        fgetcsv($handle);
        
        while (($row = fgetcsv($handle)) !== false) {
            $rowData = [];
            foreach ($columns as $index => $columnName) {
                $rowData[$columnName] = $row[$index] ?? null;
            }
            $data[] = $rowData;
        }
        
        fclose($handle);
        $this->log("CSV読み込み完了: " . count($data) . "件");
        
        return $data;
    }
    
    /**
     * メモリ使用量監視
     * 
     * @return array メモリ情報
     */
    public function getMemoryUsage()
    {
        return [
            'current' => memory_get_usage(true),
            'peak' => memory_get_peak_usage(true),
            'current_formatted' => $this->formatBytes(memory_get_usage(true)),
            'peak_formatted' => $this->formatBytes(memory_get_peak_usage(true))
        ];
    }
    
    /**
     * バイト数を読みやすい形式に変換
     */
    private function formatBytes($bytes)
    {
        $units = ['B', 'KB', 'MB', 'GB'];
        for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
            $bytes /= 1024;
        }
        return round($bytes, 2) . ' ' . $units[$i];
    }
    
    /**
     * ログ出力
     */
    private function log($message, $level = 'INFO')
    {
        $timestamp = date('Y-m-d H:i:s');
        $memory = $this->formatBytes(memory_get_usage(true));
        $logMessage = "[{$timestamp}] [{$level}] [Memory: {$memory}] {$message}" . PHP_EOL;
        
        file_put_contents($this->logFile, $logMessage, FILE_APPEND | LOCK_EX);
        echo $logMessage;
    }
    
    /**
     * 統計情報取得
     */
    public function getTableStats($table)
    {
        $stmt = $this->pdo->query("SELECT COUNT(*) as total_rows FROM {$table}");
        $stats = $stmt->fetch();
        
        $stmt = $this->pdo->query("SHOW TABLE STATUS LIKE '{$table}'");
        $tableInfo = $stmt->fetch();
        
        return [
            'total_rows' => $stats['total_rows'],
            'data_length' => $tableInfo['Data_length'] ?? 0,
            'index_length' => $tableInfo['Index_length'] ?? 0,
            'data_free' => $tableInfo['Data_free'] ?? 0
        ];
    }
}
