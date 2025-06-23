<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\WikiRagController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

/*
|--------------------------------------------------------------------------
| WIKI RAG API Routes
|--------------------------------------------------------------------------
|
| RESTful API endpoints for WIKI RAG functionality
|
*/

Route::prefix('wiki-rag')->name('api.wiki-rag.')->group(function () {
    // 検索クエリ実行
    Route::post('/query', [WikiRagController::class, 'apiQuery'])->name('query');
    
    // ヘルスチェック
    Route::get('/health', [WikiRagController::class, 'health'])->name('health');
    
    // 統計情報取得
    Route::get('/stats', [WikiRagController::class, 'stats'])->name('stats');
    
    // キャッシュクリア (管理者用)
    Route::delete('/cache', [WikiRagController::class, 'clearCache'])->name('cache.clear');
});

/*
|--------------------------------------------------------------------------
| API Rate Limiting
|--------------------------------------------------------------------------
|
| Apply rate limiting to WIKI RAG API endpoints to prevent abuse
|
*/

Route::middleware(['throttle:wiki-rag'])->group(function () {
    // Rate-limited routes can be defined here
});

/*
|--------------------------------------------------------------------------
| API Documentation
|--------------------------------------------------------------------------
|
| API documentation endpoints
|
*/

Route::get('/wiki-rag/docs', function () {
    return response()->json([
        'name' => 'WIKI RAG API',
        'version' => '1.0.0',
        'description' => 'RESTful API for WIKI RAG search functionality',
        'endpoints' => [
            'POST /api/wiki-rag/query' => 'Execute search query',
            'GET /api/wiki-rag/health' => 'Health check',
            'GET /api/wiki-rag/stats' => 'Get statistics',
            'DELETE /api/wiki-rag/cache' => 'Clear cache (admin only)'
        ],
        'documentation' => url('/wiki-rag/docs')
    ]);
})->name('api.wiki-rag.docs');
