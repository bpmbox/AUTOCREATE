<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👤 マイページ - {{ $user->display_name ?? 'ユーザー' }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar {
            background: linear-gradient(135deg, #00C300 0%, #00B300 100%);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .profile-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            margin-top: 2rem;
        }
        .profile-header {
            background: linear-gradient(135deg, #00C300 0%, #00B300 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }
        .profile-image {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 5px solid white;
            margin-bottom: 1rem;
            object-fit: cover;
        }
        .profile-body {
            padding: 2rem;
        }
        .info-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 5px solid #00C300;
        }
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #00C300;
        }
        .btn-line {
            background: #00C300;
            color: white;
            border: none;
            border-radius: 50px;
            padding: 10px 25px;
            transition: all 0.3s ease;
        }
        .btn-line:hover {
            background: #00B300;
            color: white;
            transform: translateY(-2px);
        }
        .activity-item {
            border-left: 3px solid #00C300;
            padding-left: 1rem;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <!-- 🎯 ナビゲーション -->
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand text-white fw-bold" href="#">
                <i class="fab fa-line"></i>
                MyPage
            </a>
            <div class="navbar-nav ms-auto">
                <form action="{{ route('line.logout') }}" method="POST" class="d-inline">
                    @csrf
                    <button type="submit" class="btn btn-outline-light btn-sm">
                        <i class="fas fa-sign-out-alt"></i>
                        ログアウト
                    </button>
                </form>
            </div>
        </div>
    </nav>

    <div class="container">
        <!-- ⚠️ メッセージ表示 -->
        @if(session('success'))
            <div class="alert alert-success alert-dismissible fade show mt-3" role="alert">
                <i class="fas fa-check-circle"></i>
                {{ session('success') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        @endif

        @if(session('error'))
            <div class="alert alert-danger alert-dismissible fade show mt-3" role="alert">
                <i class="fas fa-exclamation-triangle"></i>
                {{ session('error') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        @endif

        <div class="row">
            <!-- 👤 プロフィールカード -->
            <div class="col-lg-4">
                <div class="profile-card">
                    <div class="profile-header">
                        @if($user->picture_url)
                            <img src="{{ $user->picture_url }}" alt="プロフィール画像" class="profile-image">
                        @else
                            <div class="profile-image bg-white d-flex align-items-center justify-content-center">
                                <i class="fas fa-user fa-3x text-muted"></i>
                            </div>
                        @endif
                        <h3 class="mb-1">{{ $user->display_name ?? 'ユーザー' }}</h3>
                        @if($user->status_message)
                            <p class="mb-0 opacity-75">{{ $user->status_message }}</p>
                        @endif
                    </div>
                    <div class="profile-body">
                        <div class="info-card">
                            <h6><i class="fas fa-calendar-plus text-primary"></i> 登録日</h6>
                            <p class="mb-0">{{ $user->created_at->format('Y年m月d日') }}</p>
                        </div>
                        <div class="info-card">
                            <h6><i class="fas fa-clock text-success"></i> 最終ログイン</h6>
                            <p class="mb-0">{{ $user->last_login_at ? $user->last_login_at->format('Y年m月d日 H:i') : '不明' }}</p>
                        </div>
                        <div class="info-card">
                            <h6><i class="fas fa-globe text-info"></i> 言語設定</h6>
                            <p class="mb-0">{{ $user->language === 'ja' ? '日本語' : $user->language }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 📊 統計・機能 -->
            <div class="col-lg-8">
                <!-- 📈 統計カード -->
                <div class="row mt-4 mt-lg-0">
                    <div class="col-md-4 mb-3">
                        <div class="stat-card">
                            <div class="stat-number">{{ $user->created_at->diffInDays(now()) }}</div>
                            <div class="text-muted">利用日数</div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="stat-card">
                            <div class="stat-number">{{ $user->is_active ? '有効' : '無効' }}</div>
                            <div class="text-muted">アカウント状態</div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="stat-card">
                            <div class="stat-number">
                                <i class="fab fa-line text-success"></i>
                            </div>
                            <div class="text-muted">LINE連携</div>
                        </div>
                    </div>
                </div>

                <!-- 🛠️ 機能パネル -->
                <div class="profile-card mt-4">
                    <div class="profile-body">
                        <h5 class="mb-3">
                            <i class="fas fa-cogs text-primary"></i>
                            機能メニュー
                        </h5>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <button class="btn btn-line w-100">
                                    <i class="fas fa-edit"></i>
                                    プロフィール編集
                                </button>
                            </div>
                            <div class="col-md-6 mb-3">
                                <button class="btn btn-outline-secondary w-100">
                                    <i class="fas fa-shield-alt"></i>
                                    セキュリティ設定
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 📋 最近のアクティビティ -->
                <div class="profile-card mt-4">
                    <div class="profile-body">
                        <h5 class="mb-3">
                            <i class="fas fa-history text-warning"></i>
                            最近のアクティビティ
                        </h5>
                        <div class="activity-item">
                            <h6 class="mb-1">🔐 ログイン</h6>
                            <small class="text-muted">{{ $user->last_login_at ? $user->last_login_at->format('Y年m月d日 H:i') : '不明' }}</small>
                        </div>
                        <div class="activity-item">
                            <h6 class="mb-1">📝 アカウント作成</h6>
                            <small class="text-muted">{{ $user->created_at->format('Y年m月d日 H:i') }}</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 📱 Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
