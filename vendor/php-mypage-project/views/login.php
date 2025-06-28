<?php
require_once '../config/session.php';
require_once '../includes/auth.php';
require_once '../includes/security.php';

$message = '';
$error = '';

// ログイン済みの場合はマイページへリダイレクト
if (isLoggedIn()) {
    safeRedirect('mypage.php');
}

// ログイン処理
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // CSRF チェック
    if (!validateCSRFToken($_POST['csrf_token'] ?? '')) {
        $error = 'セキュリティエラーが発生しました';
    } else {
        // レート制限チェック
        if (!checkRateLimit('login_' . getClientIP(), 5, 300)) {
            $error = 'ログイン試行回数が上限に達しました。5分後に再試行してください。';
        } else {
            $username = sanitizeInput($_POST['username'] ?? '');
            $password = $_POST['password'] ?? '';
            
            if (!empty($username) && !empty($password)) {
                $auth = new Auth();
                $result = $auth->login($username, $password);
                
                if ($result['success']) {
                    safeRedirect('mypage.php');
                } else {
                    $error = $result['message'];
                }
            } else {
                $error = 'ユーザー名とパスワードを入力してください';
            }
        }
    }
}
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ログイン - マイページシステム</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
        }
        .login-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            width: 100%;
            max-width: 400px;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-header h2 {
            color: #333;
            margin-bottom: 0.5rem;
        }
        .login-header p {
            color: #666;
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="login-container">
                    <div class="login-header">
                        <h2>ログイン</h2>
                        <p>マイページシステムへようこそ</p>
                    </div>
                    
                    <?php if ($error): ?>
                        <div class="alert alert-danger" role="alert">
                            <?= h($error) ?>
                        </div>
                    <?php endif; ?>
                    
                    <?php if ($message): ?>
                        <div class="alert alert-success" role="alert">
                            <?= h($message) ?>
                        </div>
                    <?php endif; ?>
                    
                    <form method="POST" action="login.php">
                        <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                        
                        <div class="mb-3">
                            <label for="username" class="form-label">ユーザー名またはメールアドレス</label>
                            <input type="text" class="form-control" id="username" name="username" 
                                   value="<?= h($_POST['username'] ?? '') ?>" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="password" class="form-label">パスワード</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">ログイン</button>
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <a href="register.php" class="text-decoration-none">アカウントをお持ちでない方はこちら</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
