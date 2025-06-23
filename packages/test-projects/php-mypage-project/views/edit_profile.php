<?php
require_once '../config/session.php';
require_once '../includes/auth.php';
require_once '../includes/security.php';

// ログイン必須
requireLogin();

$auth = new Auth();
$user = $auth->getUserInfo($_SESSION['user_id']);
$message = '';
$error = '';

if (!$user) {
    logout();
    safeRedirect('login.php');
}

// プロフィール更新処理
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // CSRF チェック
    if (!validateCSRFToken($_POST['csrf_token'] ?? '')) {
        $error = 'セキュリティエラーが発生しました';
    } else {
        $full_name = sanitizeInput($_POST['full_name'] ?? '');
        $email = sanitizeInput($_POST['email'] ?? '');
        $bio = sanitizeInput($_POST['bio'] ?? '');
        
        // バリデーション
        if (!validateEmail($email)) {
            $error = '有効なメールアドレスを入力してください';
        } else {
            $result = $auth->updateProfile($_SESSION['user_id'], $full_name, $bio, $email);
            
            if ($result['success']) {
                $message = $result['message'];
                // セッション情報も更新
                $_SESSION['full_name'] = $full_name;
                $_SESSION['email'] = $email;
                // 更新されたユーザー情報を再取得
                $user = $auth->getUserInfo($_SESSION['user_id']);
            } else {
                $error = $result['message'];
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
    <title>プロフィール編集 - マイページシステム</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .card {
            border: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px 10px 0 0 !important;
        }
    </style>
</head>
<body>
    <!-- ナビゲーション -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="mypage.php">
                <i class="fas fa-user-circle me-2"></i>マイページシステム
            </a>
            
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="mypage.php">
                    <i class="fas fa-home me-1"></i>マイページ
                </a>
                <a class="nav-link" href="mypage.php?logout=1" 
                   onclick="return confirm('ログアウトしますか？')">
                    <i class="fas fa-sign-out-alt me-1"></i>ログアウト
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header">
                        <h4 class="mb-0">
                            <i class="fas fa-edit me-2"></i>プロフィール編集
                        </h4>
                    </div>
                    <div class="card-body">
                        <?php if ($error): ?>
                            <div class="alert alert-danger" role="alert">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                <?= h($error) ?>
                            </div>
                        <?php endif; ?>
                        
                        <?php if ($message): ?>
                            <div class="alert alert-success" role="alert">
                                <i class="fas fa-check-circle me-2"></i>
                                <?= h($message) ?>
                            </div>
                        <?php endif; ?>
                        
                        <form method="POST" action="edit_profile.php">
                            <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="username" class="form-label">
                                            <i class="fas fa-user me-1"></i>ユーザー名
                                        </label>
                                        <input type="text" class="form-control" id="username" 
                                               value="<?= h($user['username']) ?>" disabled>
                                        <div class="form-text">ユーザー名は変更できません</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="full_name" class="form-label">
                                            <i class="fas fa-id-card me-1"></i>氏名
                                        </label>
                                        <input type="text" class="form-control" id="full_name" name="full_name" 
                                               value="<?= h($user['full_name']) ?>" placeholder="山田 太郎">
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="email" class="form-label">
                                    <i class="fas fa-envelope me-1"></i>メールアドレス
                                </label>
                                <input type="email" class="form-control" id="email" name="email" 
                                       value="<?= h($user['email']) ?>" required>
                            </div>
                            
                            <div class="mb-3">
                                <label for="bio" class="form-label">
                                    <i class="fas fa-file-text me-1"></i>自己紹介
                                </label>
                                <textarea class="form-control" id="bio" name="bio" rows="4" 
                                          placeholder="自己紹介文を入力してください..."><?= h($user['bio']) ?></textarea>
                                <div class="form-text">
                                    <span id="bio-count">0</span>/500文字
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col">
                                    <div class="alert alert-info">
                                        <i class="fas fa-info-circle me-2"></i>
                                        <strong>アカウント情報:</strong><br>
                                        ユーザーID: <?= h($user['id']) ?><br>
                                        登録日: <?= date('Y年n月j日', strtotime($user['created_at'])) ?>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="d-flex justify-content-between">
                                <a href="mypage.php" class="btn btn-secondary">
                                    <i class="fas fa-arrow-left me-1"></i>キャンセル
                                </a>
                                <button type="submit" class="btn btn-primary">
                                    <i class="fas fa-save me-1"></i>更新する
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
                
                <!-- パスワード変更セクション -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-key me-2"></i>セキュリティ設定
                        </h5>
                    </div>
                    <div class="card-body">
                        <p class="text-muted">
                            アカウントのセキュリティを保つため、定期的にパスワードを変更することをお勧めします。
                        </p>
                        <a href="change_password.php" class="btn btn-outline-warning">
                            <i class="fas fa-key me-1"></i>パスワードを変更
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-light text-center py-3 mt-5">
        <div class="container">
            <p class="text-muted mb-0">
                &copy; 2024 マイページシステム. All rights reserved.
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 文字数カウント
        const bioTextarea = document.getElementById('bio');
        const bioCount = document.getElementById('bio-count');
        
        function updateBioCount() {
            const count = bioTextarea.value.length;
            bioCount.textContent = count;
            
            if (count > 500) {
                bioCount.style.color = 'red';
                bioTextarea.setCustomValidity('自己紹介は500文字以内で入力してください');
            } else {
                bioCount.style.color = '';
                bioTextarea.setCustomValidity('');
            }
        }
        
        bioTextarea.addEventListener('input', updateBioCount);
        updateBioCount(); // 初期表示
    </script>
</body>
</html>
