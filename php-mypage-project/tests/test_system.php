<?php
/**
 * PHPマイページシステム テストスイート
 */

require_once 'config/database.php';
require_once 'includes/auth.php';
require_once 'includes/security.php';

class MypageSystemTest {
    private $db;
    private $auth;
    
    public function __construct() {
        $this->db = getDB();
        $this->auth = new Auth();
    }
    
    public function runAllTests() {
        echo "=== PHPマイページシステム テスト開始 ===\n\n";
        
        $tests = [
            'testDatabaseConnection',
            'testUserRegistration',
            'testUserLogin',
            'testProfileUpdate',
            'testSecurityFunctions',
            'testSessionManagement'
        ];
        
        $passed = 0;
        $failed = 0;
        
        foreach ($tests as $test) {
            echo "テスト実行: $test\n";
            try {
                if ($this->$test()) {
                    echo "✅ PASS\n";
                    $passed++;
                } else {
                    echo "❌ FAIL\n";
                    $failed++;
                }
            } catch (Exception $e) {
                echo "❌ ERROR: " . $e->getMessage() . "\n";
                $failed++;
            }
            echo "\n";
        }
        
        echo "=== テスト結果 ===\n";
        echo "成功: $passed\n";
        echo "失敗: $failed\n";
        echo "合計: " . ($passed + $failed) . "\n";
        
        return $failed === 0;
    }
    
    public function testDatabaseConnection() {
        return $this->db !== null;
    }
    
    public function testUserRegistration() {
        $test_username = 'test_' . time();
        $test_email = 'test_' . time() . '@example.com';
        $test_password = 'TestPassword123';
        
        $result = $this->auth->register($test_username, $test_email, $test_password, 'Test User');
        
        // クリーンアップ
        if ($result['success']) {
            $stmt = $this->db->prepare("DELETE FROM users WHERE username = ?");
            $stmt->execute([$test_username]);
        }
        
        return $result['success'];
    }
    
    public function testUserLogin() {
        // テストユーザーを作成
        $test_username = 'login_test_' . time();
        $test_email = 'login_test_' . time() . '@example.com';
        $test_password = 'TestPassword123';
        
        $register_result = $this->auth->register($test_username, $test_email, $test_password);
        if (!$register_result['success']) {
            return false;
        }
        
        // ログインテスト
        $login_result = $this->auth->login($test_username, $test_password);
        
        // クリーンアップ
        $stmt = $this->db->prepare("DELETE FROM users WHERE username = ?");
        $stmt->execute([$test_username]);
        
        return $login_result['success'];
    }
    
    public function testProfileUpdate() {
        // テストユーザーを作成
        $test_username = 'profile_test_' . time();
        $test_email = 'profile_test_' . time() . '@example.com';
        $test_password = 'TestPassword123';
        
        $register_result = $this->auth->register($test_username, $test_email, $test_password);
        if (!$register_result['success']) {
            return false;
        }
        
        // ユーザーIDを取得
        $stmt = $this->db->prepare("SELECT id FROM users WHERE username = ?");
        $stmt->execute([$test_username]);
        $user = $stmt->fetch();
        
        if (!$user) {
            return false;
        }
        
        // プロフィール更新テスト
        $update_result = $this->auth->updateProfile(
            $user['id'],
            'Updated Name',
            'Updated bio',
            'updated_' . time() . '@example.com'
        );
        
        // クリーンアップ
        $stmt = $this->db->prepare("DELETE FROM users WHERE id = ?");
        $stmt->execute([$user['id']]);
        
        return $update_result['success'];
    }
    
    public function testSecurityFunctions() {
        // XSS対策テスト
        $malicious_input = '<script>alert("XSS")</script>';
        $escaped = h($malicious_input);
        $xss_test = !strpos($escaped, '<script>');
        
        // メール検証テスト
        $email_test = validateEmail('test@example.com') && !validateEmail('invalid-email');
        
        // パスワード強度テスト
        $password_test = !validatePassword('weak') && validatePassword('StrongPass123');
        
        return $xss_test && $email_test && $password_test;
    }
    
    public function testSessionManagement() {
        // セッション開始テスト
        if (session_status() !== PHP_SESSION_ACTIVE) {
            session_start();
        }
        
        // CSRFトークン生成テスト
        $token1 = generateCSRFToken();
        $token2 = generateCSRFToken();
        
        // 同じセッション内では同じトークンが返される
        $token_test = $token1 === $token2;
        
        // トークン検証テスト
        $validation_test = validateCSRFToken($token1);
        
        return $token_test && $validation_test;
    }
}

// テスト実行（コマンドライン）
if (php_sapi_name() === 'cli') {
    $tester = new MypageSystemTest();
    $success = $tester->runAllTests();
    
    exit($success ? 0 : 1);
}

// Web経由でのテスト実行
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>システムテスト - PHPマイページシステム</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>PHPマイページシステム テスト</h1>
        
        <?php if (isset($_GET['run'])): ?>
            <div class="card">
                <div class="card-body">
                    <pre><?php
                        $tester = new MypageSystemTest();
                        $tester->runAllTests();
                    ?></pre>
                </div>
            </div>
        <?php else: ?>
            <div class="alert alert-info">
                <h4>テストを実行</h4>
                <p>システムの動作確認を行います。</p>
                <a href="?run=1" class="btn btn-primary">テスト実行</a>
            </div>
        <?php endif; ?>
    </div>
</body>
</html>
