<?php
/**
 * データベース設定ファイル
 * 環境変数を使用したセキュアな設定
 */

return [
    'database' => [
        'default' => 'sqlite',
        
        'connections' => [
            'mysql' => [
                'driver' => 'mysql',
                'host' => $_ENV['DB_HOST'] ?? 'localhost',
                'port' => $_ENV['DB_PORT'] ?? '3306',
                'database' => $_ENV['DB_NAME'] ?? 'bulk_batch_db',
                'username' => $_ENV['DB_USER'] ?? 'root',
                'password' => $_ENV['DB_PASS'] ?? '',
                'charset' => 'utf8mb4',
                'collation' => 'utf8mb4_unicode_ci',
                'options' => [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                    PDO::MYSQL_ATTR_USE_BUFFERED_QUERY => false,
                    PDO::ATTR_EMULATE_PREPARES => false,
                ]
            ],
            
            'sqlite' => [
                'driver' => 'sqlite',
                'database' => $_ENV['SQLITE_DB_PATH'] ?? __DIR__ . '/../storage/database.sqlite',
                'options' => [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                ]
            ]
        ]
    ],
    
    'batch' => [
        'default_size' => $_ENV['BATCH_SIZE'] ?? 1000,
        'max_size' => $_ENV['MAX_BATCH_SIZE'] ?? 5000,
        'memory_limit' => $_ENV['MEMORY_LIMIT'] ?? '256M',
        'log_enabled' => $_ENV['LOG_ENABLED'] ?? true,
        'log_level' => $_ENV['LOG_LEVEL'] ?? 'INFO',
        'log_file' => $_ENV['LOG_FILE'] ?? null,
    ]
];
