<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 LINE ログイン - MyPage</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #00C300 0%, #00B300 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .login-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            max-width: 400px;
            width: 100%;
        }
        .login-header {
            background: linear-gradient(135deg, #00C300 0%, #00B300 100%);
            color: white;
            text-align: center;
            padding: 2rem;
        }
        .login-header h1 {
            margin: 0;
            font-size: 1.8rem;
            font-weight: 600;
        }
        .login-body {
            padding: 2rem;
        }
        .line-login-btn {
            background: #00C300;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }
        .line-login-btn:hover {
            background: #00B300;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 195, 0, 0.3);
            color: white;
        }
        .feature-list {
            list-style: none;
            padding: 0;
            margin: 1.5rem 0;
        }
        .feature-list li {
            padding: 0.5rem 0;
            color: #666;
        }
        .feature-list i {
            color: #00C300;
            margin-right: 0.5rem;
        }
        .alert {
            border-radius: 10px;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <!-- 🎨 ヘッダー -->
        <div class="login-header">
            <h1>
                <i class="fab fa-line"></i>
                LINE ログイン
            </h1>
            <p class="mb-0">🚀 MyPageへようこそ</p>
        </div>

        <!-- 📝 ボディ -->
        <div class="login-body">
            <!-- ⚠️ エラー・成功メッセージ -->
            @if(session('error'))
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i>
                    {{ session('error') }}
                </div>
            @endif

            @if(session('success'))
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i>
                    {{ session('success') }}
                </div>
            @endif

            <!-- 📋 機能一覧 -->
            <ul class="feature-list">
                <li><i class="fas fa-user"></i> プロフィール管理</li>
                <li><i class="fas fa-shield-alt"></i> セキュア認証</li>
                <li><i class="fas fa-mobile-alt"></i> モバイル対応</li>
                <li><i class="fas fa-bolt"></i> 高速ログイン</li>
            </ul>

            <!-- 🔐 LINE ログインボタン -->
            <a href="{{ route('line.login') }}" class="line-login-btn">
                <i class="fab fa-line"></i>
                LINEでログイン
            </a>

            <!-- 📞 サポート -->
            <div class="text-center mt-3">
                <small class="text-muted">
                    <i class="fas fa-question-circle"></i>
                    お困りの場合は
                    <a href="mailto:support@example.com" class="text-decoration-none">
                        サポート
                    </a>
                    まで
                </small>
            </div>
        </div>
    </div>

    <!-- 📱 Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
