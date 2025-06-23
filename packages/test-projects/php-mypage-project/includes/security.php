<?php
/**
 * セキュリティ関数
 */

/**
 * XSS対策 - HTMLエスケープ
 */
function h($string) {
    return htmlspecialchars($string, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

/**
 * 入力値サニタイズ
 */
function sanitizeInput($input) {
    return trim(stripslashes($input));
}

/**
 * メールアドレス検証
 */
function validateEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * パスワード強度チェック
 */
function validatePassword($password) {
    return strlen($password) >= 8 && 
           preg_match('/[A-Z]/', $password) && 
           preg_match('/[a-z]/', $password) && 
           preg_match('/[0-9]/', $password);
}

/**
 * ファイルアップロード検証
 */
function validateImageUpload($file) {
    $allowed_types = ['image/jpeg', 'image/png', 'image/gif'];
    $max_size = 2 * 1024 * 1024; // 2MB
    
    if (!in_array($file['type'], $allowed_types)) {
        return ['success' => false, 'message' => '対応していないファイル形式です'];
    }
    
    if ($file['size'] > $max_size) {
        return ['success' => false, 'message' => 'ファイルサイズが大きすぎます（最大2MB）'];
    }
    
    return ['success' => true];
}

/**
 * リダイレクト（ヘッダーインジェクション対策）
 */
function safeRedirect($url) {
    // 相対URLのみ許可
    if (strpos($url, 'http') === 0) {
        $url = '/';
    }
    
    header('Location: ' . $url);
    exit;
}

/**
 * ログイン必須チェック
 */
function requireLogin() {
    if (!isLoggedIn()) {
        safeRedirect('login.php');
    }
}

/**
 * レート制限（簡易版）
 */
function checkRateLimit($key, $limit = 5, $period = 300) {
    if (!isset($_SESSION['rate_limit'])) {
        $_SESSION['rate_limit'] = [];
    }
    
    $now = time();
    $rate_data = $_SESSION['rate_limit'][$key] ?? ['count' => 0, 'first_attempt' => $now];
    
    // 期間リセット
    if ($now - $rate_data['first_attempt'] > $period) {
        $rate_data = ['count' => 0, 'first_attempt' => $now];
    }
    
    $rate_data['count']++;
    $_SESSION['rate_limit'][$key] = $rate_data;
    
    return $rate_data['count'] <= $limit;
}

/**
 * IPアドレス取得
 */
function getClientIP() {
    $ip_keys = ['HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'];
    foreach ($ip_keys as $key) {
        if (array_key_exists($key, $_SERVER) === true) {
            foreach (explode(',', $_SERVER[$key]) as $ip) {
                $ip = trim($ip);
                if (filter_var($ip, FILTER_VALIDATE_IP, 
                    FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) !== false) {
                    return $ip;
                }
            }
        }
    }
    return $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
}
?>
