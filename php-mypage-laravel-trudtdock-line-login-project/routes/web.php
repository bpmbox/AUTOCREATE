<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Auth\LineLoginController;

/*
|--------------------------------------------------------------------------
| 🌐 Web Routes
|--------------------------------------------------------------------------
|
| Laravel + LINE Login 専用ルート設定
| 
*/

// 🏠 ホームページ
Route::get('/', function () {
    return view('auth.login');
})->name('home');

// 🔐 認証ルート
Route::prefix('auth')->group(function () {
    // LINE Login開始
    Route::get('/line', [LineLoginController::class, 'redirectToLine'])
        ->name('line.login');
    
    // LINE Loginコールバック
    Route::get('/line/callback', [LineLoginController::class, 'handleLineCallback'])
        ->name('line.callback');
    
    // ログアウト
    Route::post('/logout', [LineLoginController::class, 'logout'])
        ->name('line.logout');
});

// 🔒 ログイン必須ページ
Route::middleware(['auth:line'])->group(function () {
    // マイページ
    Route::get('/mypage', function () {
        return view('mypage.index', [
            'user' => auth('line')->user()
        ]);
    })->name('mypage');
    
    // プロフィール編集
    Route::get('/mypage/profile', function () {
        return view('mypage.profile', [
            'user' => auth('line')->user()
        ]);
    })->name('mypage.profile');
    
    // プロフィール更新
    Route::put('/mypage/profile', function () {
        // TODO: プロフィール更新ロジック実装
        return redirect()->route('mypage')->with('success', 'プロフィールを更新しました！');
    })->name('mypage.profile.update');
});

// 📱 API ルート
Route::prefix('api')->middleware(['auth:line'])->group(function () {
    // ユーザー情報取得
    Route::get('/user', function () {
        return response()->json([
            'success' => true,
            'user' => auth('line')->user()
        ]);
    });
    
    // ユーザー統計
    Route::get('/user/stats', function () {
        $user = auth('line')->user();
        return response()->json([
            'success' => true,
            'stats' => [
                'login_days' => $user->created_at->diffInDays(now()),
                'last_login' => $user->last_login_at,
                'is_active' => $user->is_active,
                'created_at' => $user->created_at,
            ]
        ]);
    });
});

// 🚫 ログインページ（認証済みユーザーはリダイレクト）
Route::get('/login', function () {
    if (auth('line')->check()) {
        return redirect()->route('mypage');
    }
    return view('auth.login');
})->name('login');
