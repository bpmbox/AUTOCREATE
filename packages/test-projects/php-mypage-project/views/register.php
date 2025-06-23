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

// 登録処理
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // CSRF チェック
    if (!validateCSRFToken($_POST['csrf_token'] ?? '')) {
        $error = 'セキュリティエラーが発生しました';
    } else {
        // レート制限チェック
        if (!checkRateLimit('register_' . getClientIP(), 3, 600)) {
            $error = '登録試行回数が上限に達しました。10分後に再試行してください。';
        } else {
            $username = sanitizeInput($_POST['username'] ?? '');
            $email = sanitizeInput($_POST['email'] ?? '');
            $password = $_POST['password'] ?? '';
            $password_confirm = $_POST['password_confirm'] ?? '';
            $full_name = sanitizeInput($_POST['full_name'] ?? '');
            
            // バリデーション
            if (empty($username) || empty($email) || empty($password)) {
                $error = 'すべての必須項目を入力してください';
            } elseif (!validateEmail($email)) {
                $error = '有効なメールアドレスを入力してください';
            } elseif (strlen($password) < 8) {
                $error = 'パスワードは8文字以上で入力してください';
            } elseif ($password !== $password_confirm) {
                $error = 'パスワードが一致しません';
            } else {
                $auth = new Auth();
                $result = $auth->register($username, $email, $password, $full_name);
                
                if ($result['success']) {
                    $message = $result['message'] . ' <a href="login.php">ログインページへ</a>';
                } else {
                    $error = $result['message'];
                }
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
    <title>ユーザー登録 - マイページシステム</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem 0;
        }
        .register-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            width: 100%;
            max-width: 500px;
        }
        .register-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .register-header h2 {
            color: #333;
            margin-bottom: 0.5rem;
        }
        .register-header p {
            color: #666;
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="register-container mx-auto">
                    <div class="register-header">
                        <h2>ユーザー登録</h2>
                        <p>新しいアカウントを作成</p>
                    </div>
                    
                    <?php if ($error): ?>
                        <div class="alert alert-danger" role="alert">
                            <?= h($error) ?>
                        </div>
                    <?php endif; ?>
                    
                    <?php if ($message): ?>
                        <div class="alert alert-success" role="alert">
                            <?= $message ?>
                        </div>
                    <?php endif; ?>
                    
                    <form method="POST" action="register.php">
                        <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="username" class="form-label">ユーザー名 <span class="text-danger">*</span></label>
                                    <input type="text" class="form-control" id="username" name="username" 
                                           value="<?= h($_POST['username'] ?? '') ?>" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="full_name" class="form-label">氏名</label>
                                    <input type="text" class="form-control" id="full_name" name="full_name" 
                                           value="<?= h($_POST['full_name'] ?? '') ?>">
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="email" class="form-label">メールアドレス <span class="text-danger">*</span></label>
                            <input type="email" class="form-control" id="email" name="email" 
                                   value="<?= h($_POST['email'] ?? '') ?>" required>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="password" class="form-label">パスワード <span class="text-danger">*</span></label>
                                    <input type="password" class="form-control" id="password" name="password" required>
                                    <div class="form-text">8文字以上で入力してください</div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="password_confirm" class="form-label">パスワード確認 <span class="text-danger">*</span></label>
                                    <input type="password" class="form-control" id="password_confirm" name="password_confirm" required>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">アカウント作成</button>
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <a href="login.php" class="text-decoration-none">既にアカウントをお持ちの方はこちら</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // パスワード確認のリアルタイムチェック
        document.getElementById('password_confirm').addEventListener('input', function() {
            const password = document.getElementById('password').value;
            const confirm = this.value;
            
            if (password !== confirm) {
                this.setCustomValidity('パスワードが一致しません');
            } else {
                this.setCustomValidity('');
            }
        });
    </script>
</body>
</html>
