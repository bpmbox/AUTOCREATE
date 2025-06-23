<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\View\View;
use App\Services\WikiRagService;
use App\Http\Requests\WikiRagRequest;
use Exception;

/**
 * WIKI RAG Webコントローラー
 * 
 * Web UI とAPIエンドポイントを提供
 */
class WikiRagController extends Controller
{
    private WikiRagService $wikiRagService;

    public function __construct(WikiRagService $wikiRagService)
    {
        $this->wikiRagService = $wikiRagService;
    }

    /**
     * 検索画面表示
     *
     * @return View
     */
    public function index(): View
    {
        return view('wiki-rag.index', [
            'title' => 'WIKI RAG検索',
            'health' => $this->wikiRagService->healthCheck()
        ]);
    }

    /**
     * チャット画面表示
     *
     * @return View
     */
    public function chat(): View
    {
        return view('wiki-rag.chat', [
            'title' => 'WIKI RAGチャット',
            'health' => $this->wikiRagService->healthCheck()
        ]);
    }

    /**
     * 検索実行 (Web Form)
     *
     * @param WikiRagRequest $request
     * @return View|JsonResponse
     */
    public function search(WikiRagRequest $request)
    {
        try {
            $query = $request->input('query');
            $maxResults = $request->input('max_results', 5);
            $threshold = $request->input('threshold', 0.3);

            $result = $this->wikiRagService->query($query, $maxResults, $threshold);

            // Ajax リクエストの場合はJSON返却
            if ($request->ajax()) {
                return response()->json([
                    'success' => true,
                    'data' => $result
                ]);
            }

            // 通常リクエストの場合はView返却
            return view('wiki-rag.results', [
                'title' => '検索結果',
                'query' => $query,
                'result' => $result,
                'maxResults' => $maxResults,
                'threshold' => $threshold
            ]);

        } catch (Exception $e) {
            if ($request->ajax()) {
                return response()->json([
                    'success' => false,
                    'error' => $e->getMessage()
                ], 400);
            }

            return back()->withErrors(['query' => $e->getMessage()])->withInput();
        }
    }

    /**
     * API検索エンドポイント
     *
     * @param WikiRagRequest $request
     * @return JsonResponse
     */
    public function apiQuery(WikiRagRequest $request): JsonResponse
    {
        try {
            $query = $request->input('query');
            $maxResults = $request->input('max_results', 5);
            $threshold = $request->input('threshold', 0.3);

            $result = $this->wikiRagService->query($query, $maxResults, $threshold);

            return response()->json([
                'success' => true,
                'data' => $result
            ]);

        } catch (Exception $e) {
            return response()->json([
                'success' => false,
                'error' => $e->getMessage()
            ], 400);
        }
    }

    /**
     * ヘルスチェックエンドポイント
     *
     * @return JsonResponse
     */
    public function health(): JsonResponse
    {
        $health = $this->wikiRagService->healthCheck();
        
        return response()->json($health, 
            $health['status'] === 'healthy' ? 200 : 503
        );
    }

    /**
     * 統計情報エンドポイント
     *
     * @return JsonResponse
     */
    public function stats(): JsonResponse
    {
        $stats = $this->wikiRagService->getStats();
        
        return response()->json([
            'success' => true,
            'data' => $stats
        ]);
    }

    /**
     * キャッシュクリアエンドポイント
     *
     * @param Request $request
     * @return JsonResponse
     */
    public function clearCache(Request $request): JsonResponse
    {
        $pattern = $request->input('pattern');
        $success = $this->wikiRagService->clearCache($pattern);
        
        return response()->json([
            'success' => $success,
            'message' => $success ? 'Cache cleared successfully' : 'Failed to clear cache'
        ]);
    }

    /**
     * 管理画面表示
     *
     * @return View
     */
    public function admin(): View
    {
        $health = $this->wikiRagService->healthCheck();
        $stats = $this->wikiRagService->getStats();

        return view('wiki-rag.admin', [
            'title' => 'WIKI RAG管理画面',
            'health' => $health,
            'stats' => $stats
        ]);
    }
}
