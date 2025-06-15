<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\WikiRagController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

/*
|--------------------------------------------------------------------------
| WIKI RAG Web Routes
|--------------------------------------------------------------------------
|
| Web interface routes for WIKI RAG functionality
|
*/

Route::prefix('wiki-rag')->name('wiki-rag.')->group(function () {
    // 検索画面
    Route::get('/', [WikiRagController::class, 'index'])->name('index');
    
    // 検索実行
    Route::post('/search', [WikiRagController::class, 'search'])->name('search');
    
    // チャット画面
    Route::get('/chat', [WikiRagController::class, 'chat'])->name('chat');
    
    // 管理画面 (認証が必要な場合はここでミドルウェア追加)
    Route::get('/admin', [WikiRagController::class, 'admin'])->name('admin');
    
    // ヘルスチェック
    Route::get('/health', [WikiRagController::class, 'health'])->name('health');
    
    // キャッシュクリア
    Route::post('/cache/clear', [WikiRagController::class, 'clearCache'])->name('cache.clear');
});

/*
|--------------------------------------------------------------------------
| Additional Routes
|--------------------------------------------------------------------------
|
| Add any additional routes here as needed
|
*/
