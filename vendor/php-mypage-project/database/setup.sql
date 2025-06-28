-- PHPマイページシステム データベースセットアップ

-- データベース作成
CREATE DATABASE IF NOT EXISTS mypage_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mypage_system;

-- ユーザーテーブル
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) DEFAULT NULL,
    bio TEXT DEFAULT NULL,
    avatar_url VARCHAR(255) DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- セッションテーブル
CREATE TABLE sessions (
    id VARCHAR(128) PRIMARY KEY,
    user_id INT DEFAULT NULL,
    data LONGTEXT,
    ip_address VARCHAR(45) DEFAULT NULL,
    user_agent TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at)
);

-- ログインログテーブル（セキュリティ監視用）
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    username VARCHAR(50) DEFAULT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    status ENUM('success', 'failed', 'blocked') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_ip_address (ip_address),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- サンプルユーザー作成（テスト用）
-- パスワード: password123
INSERT INTO users (username, email, password_hash, full_name, bio) VALUES 
('admin', 'admin@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '管理者', 'システム管理者です。'),
('testuser', 'test@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'テストユーザー', 'テスト用のユーザーアカウントです。');

-- 古いセッションクリーンアップ用のイベント（オプション）
-- SET GLOBAL event_scheduler = ON;
-- 
-- DELIMITER $$
-- CREATE EVENT IF NOT EXISTS cleanup_expired_sessions
-- ON SCHEDULE EVERY 1 HOUR
-- DO
-- BEGIN
--     DELETE FROM sessions WHERE expires_at < NOW();
-- END$$
-- DELIMITER ;

-- 権限設定（本番環境用）
-- CREATE USER IF NOT EXISTS 'mypage_user'@'localhost' IDENTIFIED BY 'secure_password_here';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON mypage_system.* TO 'mypage_user'@'localhost';
-- FLUSH PRIVILEGES;

COMMIT;
