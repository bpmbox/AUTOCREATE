<?php
/**
 * メインエントリーポイント
 */

require_once 'config/session.php';
require_once 'includes/security.php';

// ログイン状態チェック
if (isLoggedIn()) {
    // ログイン済みの場合はマイページへ
    safeRedirect('views/mypage.php');
} else {
    // 未ログインの場合はログインページへ
    safeRedirect('views/login.php');
}
?>
