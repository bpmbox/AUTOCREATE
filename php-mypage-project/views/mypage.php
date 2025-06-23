<?php
require_once '../config/session.php';
require_once '../includes/auth.php';
require_once '../includes/security.php';

// ログイン必須
requireLogin();

$auth = new Auth();
$user = $auth->getUserInfo($_SESSION['user_id']);

if (!$user) {
    logout();
    safeRedirect('login.php');
}

// ログアウト処理
if (isset($_GET['logout'])) {
    logout();
    safeRedirect('login.php');
}
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>マイページ - <?= h($user['username']) ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .profile-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        .profile-avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid white;
            object-fit: cover;
        }
        .card {
            border: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        .card-header {
            background-color: #fff;
            border-bottom: 2px solid #e9ecef;
            font-weight: 600;
        }
        .info-item {
            padding: 0.75rem 0;
            border-bottom: 1px solid #e9ecef;
        }
        .info-item:last-child {
            border-bottom: none;
        }
        .info-label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 0.25rem;
        }
        .info-value {
            color: #6c757d;
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
                <a class="nav-link" href="edit_profile.php">
                    <i class="fas fa-edit me-1"></i>プロフィール編集
                </a>
                <a class="nav-link" href="mypage.php?logout=1" 
                   onclick="return confirm('ログアウトしますか？')">
                    <i class="fas fa-sign-out-alt me-1"></i>ログアウト
                </a>
            </div>
        </div>
    </nav>

    <!-- プロフィールヘッダー -->
    <div class="profile-header">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-3 text-center text-md-start">
                    <img src="<?= h($user['avatar_url'] ?: '../public/images/default-avatar.png') ?>" 
                         alt="プロフィール画像" class="profile-avatar" 
                         onerror="this.src='https://via.placeholder.com/120x120/6c757d/ffffff?text=Avatar'">
                </div>
                <div class="col-md-9 text-center text-md-start mt-3 mt-md-0">
                    <h1 class="mb-2"><?= h($user['full_name'] ?: $user['username']) ?></h1>
                    <p class="mb-1">@<?= h($user['username']) ?></p>
                    <p class="mb-0 opacity-75">
                        <i class="fas fa-calendar-alt me-2"></i>
                        <?= date('Y年n月j日 登録', strtotime($user['created_at'])) ?>
                    </p>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="row">
            <!-- プロフィール情報 -->
            <div class="col-lg-8">
                <div class="card mb-4">
                    <div class="card-header">
                        <i class="fas fa-user me-2"></i>プロフィール情報
                    </div>
                    <div class="card-body">
                        <div class="info-item">
                            <div class="info-label">氏名</div>
                            <div class="info-value">
                                <?= h($user['full_name'] ?: '未設定') ?>
                            </div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">ユーザー名</div>
                            <div class="info-value">
                                <?= h($user['username']) ?>
                            </div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">メールアドレス</div>
                            <div class="info-value">
                                <?= h($user['email']) ?>
                            </div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">自己紹介</div>
                            <div class="info-value">
                                <?= nl2br(h($user['bio'] ?: 'まだ自己紹介が設定されていません。')) ?>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- アクティビティ -->
                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-chart-line me-2"></i>アクティビティ
                    </div>
                    <div class="card-body">
                        <div class="row text-center">
                            <div class="col-md-4 mb-3">
                                <div class="card bg-primary text-white">
                                    <div class="card-body">
                                        <i class="fas fa-calendar-day fa-2x mb-2"></i>
                                        <h5>最終ログイン</h5>
                                        <p class="mb-0">今日</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card bg-success text-white">
                                    <div class="card-body">
                                        <i class="fas fa-user-check fa-2x mb-2"></i>
                                        <h5>アカウント状態</h5>
                                        <p class="mb-0">アクティブ</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card bg-info text-white">
                                    <div class="card-body">
                                        <i class="fas fa-shield-alt fa-2x mb-2"></i>
                                        <h5>セキュリティ</h5>
                                        <p class="mb-0">安全</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- サイドバー -->
            <div class="col-lg-4">
                <div class="card mb-4">
                    <div class="card-header">
                        <i class="fas fa-cogs me-2"></i>アカウント設定
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <a href="edit_profile.php" class="btn btn-outline-primary">
                                <i class="fas fa-edit me-2"></i>プロフィール編集
                            </a>
                            <a href="change_password.php" class="btn btn-outline-secondary">
                                <i class="fas fa-key me-2"></i>パスワード変更
                            </a>
                            <a href="mypage.php?logout=1" class="btn btn-outline-danger" 
                               onclick="return confirm('ログアウトしますか？')">
                                <i class="fas fa-sign-out-alt me-2"></i>ログアウト
                            </a>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <i class="fas fa-info-circle me-2"></i>システム情報
                    </div>
                    <div class="card-body">
                        <small class="text-muted">
                            <div class="mb-2">
                                <strong>ユーザーID:</strong> <?= h($user['id']) ?>
                            </div>
                            <div class="mb-2">
                                <strong>登録日:</strong> <?= date('Y/m/d', strtotime($user['created_at'])) ?>
                            </div>
                            <div>
                                <strong>最終更新:</strong> <?= date('Y/m/d H:i', strtotime($user['created_at'])) ?>
                            </div>
                        </small>
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
</body>
</html>
