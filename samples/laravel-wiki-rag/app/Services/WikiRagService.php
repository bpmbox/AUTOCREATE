<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;
use Exception;

/**
 * WIKI RAG統合サービス
 * 
 * LaravelアプリケーションからWIKI RAGシステムAPIを呼び出すためのサービスクラス
 */
class WikiRagService
{
    private string $apiUrl;
    private string $apiKey;
    private bool $cacheEnabled;
    private int $cacheTtl;
    private int $timeout;

    public function __construct()
    {
        $this->apiUrl = config('wiki-rag.api_url', 'http://localhost:8000');
        $this->apiKey = config('wiki-rag.api_key', '');
        $this->cacheEnabled = config('wiki-rag.cache_enabled', true);
        $this->cacheTtl = config('wiki-rag.cache_ttl', 3600);
        $this->timeout = config('wiki-rag.timeout', 30);
    }

    /**
     * WIKI RAG検索を実行
     *
     * @param string $query 検索クエリ
     * @param int $maxResults 最大結果数
     * @param float $threshold 閾値
     * @return array 検索結果
     * @throws Exception
     */
    public function query(string $query, int $maxResults = 5, float $threshold = 0.3): array
    {
        // 入力値検証
        if (empty(trim($query))) {
            throw new Exception('Query cannot be empty');
        }

        if ($maxResults < 1 || $maxResults > 100) {
            throw new Exception('Max results must be between 1 and 100');
        }

        if ($threshold < 0 || $threshold > 1) {
            throw new Exception('Threshold must be between 0 and 1');
        }

        // キャッシュキー生成
        $cacheKey = $this->generateCacheKey($query, $maxResults, $threshold);

        // キャッシュから結果取得を試行
        if ($this->cacheEnabled) {
            $cachedResult = Cache::get($cacheKey);
            if ($cachedResult !== null) {
                Log::info('WIKI RAG cache hit', ['query' => $query]);
                return $cachedResult;
            }
        }

        try {
            // API呼び出し
            $startTime = microtime(true);
            
            $response = Http::timeout($this->timeout)
                ->withHeaders($this->getHeaders())
                ->post("{$this->apiUrl}/api/v1/query", [
                    'query' => $query,
                    'max_results' => $maxResults,
                    'threshold' => $threshold
                ]);

            $endTime = microtime(true);
            $responseTime = round(($endTime - $startTime) * 1000, 2);

            // レスポンス検証
            if (!$response->successful()) {
                throw new Exception("API request failed with status {$response->status()}: {$response->body()}");
            }

            $result = $response->json();

            // 結果の構造検証
            if (!isset($result['results']) || !is_array($result['results'])) {
                throw new Exception('Invalid API response structure');
            }

            // 結果を正規化
            $normalizedResult = $this->normalizeResult($result, $responseTime);

            // キャッシュに保存
            if ($this->cacheEnabled) {
                Cache::put($cacheKey, $normalizedResult, $this->cacheTtl);
            }

            // ログ記録
            Log::info('WIKI RAG query executed', [
                'query' => $query,
                'max_results' => $maxResults,
                'threshold' => $threshold,
                'response_time_ms' => $responseTime,
                'result_count' => count($normalizedResult['results'])
            ]);

            return $normalizedResult;

        } catch (Exception $e) {
            Log::error('WIKI RAG query failed', [
                'query' => $query,
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
            
            throw new Exception("WIKI RAG query failed: {$e->getMessage()}");
        }
    }

    /**
     * ヘルスチェック実行
     *
     * @return array ヘルスチェック結果
     */
    public function healthCheck(): array
    {
        try {
            $startTime = microtime(true);
            
            $response = Http::timeout(10)
                ->withHeaders($this->getHeaders())
                ->get("{$this->apiUrl}/health");
            
            $endTime = microtime(true);
            $responseTime = round(($endTime - $startTime) * 1000, 2);

            return [
                'status' => $response->successful() ? 'healthy' : 'unhealthy',
                'response_time_ms' => $responseTime,
                'api_url' => $this->apiUrl,
                'timestamp' => now()->toISOString()
            ];

        } catch (Exception $e) {
            return [
                'status' => 'unhealthy',
                'error' => $e->getMessage(),
                'api_url' => $this->apiUrl,
                'timestamp' => now()->toISOString()
            ];
        }
    }

    /**
     * 統計情報取得
     *
     * @return array 統計情報
     */
    public function getStats(): array
    {
        try {
            $response = Http::timeout(10)
                ->withHeaders($this->getHeaders())
                ->get("{$this->apiUrl}/api/v1/stats");

            if ($response->successful()) {
                return $response->json();
            }

            return ['error' => 'Failed to fetch stats'];

        } catch (Exception $e) {
            return ['error' => $e->getMessage()];
        }
    }

    /**
     * キャッシュクリア
     *
     * @param string|null $pattern キャッシュキーパターン
     * @return bool 成功可否
     */
    public function clearCache(?string $pattern = null): bool
    {
        try {
            if ($pattern) {
                // パターンマッチでキャッシュクリア
                $keys = Cache::getRedis()->keys("wiki_rag:*{$pattern}*");
                if (!empty($keys)) {
                    Cache::getRedis()->del($keys);
                }
            } else {
                // 全WIKI RAGキャッシュクリア
                $keys = Cache::getRedis()->keys('wiki_rag:*');
                if (!empty($keys)) {
                    Cache::getRedis()->del($keys);
                }
            }

            Log::info('WIKI RAG cache cleared', ['pattern' => $pattern]);
            return true;

        } catch (Exception $e) {
            Log::error('Failed to clear WIKI RAG cache', ['error' => $e->getMessage()]);
            return false;
        }
    }

    /**
     * HTTPヘッダーを取得
     *
     * @return array HTTPヘッダー
     */
    private function getHeaders(): array
    {
        $headers = [
            'Content-Type' => 'application/json',
            'Accept' => 'application/json',
            'User-Agent' => 'Laravel-WikiRAG/1.0'
        ];

        if (!empty($this->apiKey)) {
            $headers['Authorization'] = "Bearer {$this->apiKey}";
        }

        return $headers;
    }

    /**
     * キャッシュキーを生成
     *
     * @param string $query
     * @param int $maxResults
     * @param float $threshold
     * @return string
     */
    private function generateCacheKey(string $query, int $maxResults, float $threshold): string
    {
        $hash = md5($query . $maxResults . $threshold);
        return "wiki_rag:query:{$hash}";
    }

    /**
     * API結果を正規化
     *
     * @param array $result
     * @param float $responseTime
     * @return array
     */
    private function normalizeResult(array $result, float $responseTime): array
    {
        return [
            'query' => $result['query'] ?? '',
            'results' => array_map(function ($item) {
                return [
                    'content' => $item['content'] ?? '',
                    'score' => $item['score'] ?? 0.0,
                    'metadata' => $item['metadata'] ?? [],
                    'highlight' => $this->generateHighlight($item['content'] ?? '', $result['query'] ?? '')
                ];
            }, $result['results'] ?? []),
            'total_results' => count($result['results'] ?? []),
            'response_time_ms' => $responseTime,
            'threshold' => $result['threshold'] ?? 0.3,
            'timestamp' => now()->toISOString()
        ];
    }

    /**
     * ハイライト生成
     *
     * @param string $content
     * @param string $query
     * @return string
     */
    private function generateHighlight(string $content, string $query): string
    {
        if (empty($query) || empty($content)) {
            return $content;
        }

        // 簡単なハイライト処理 (実際はより高度な処理が必要)
        $words = explode(' ', $query);
        foreach ($words as $word) {
            if (strlen($word) > 2) {
                $content = preg_replace(
                    '/(' . preg_quote($word, '/') . ')/ui',
                    '<mark>$1</mark>',
                    $content
                );
            }
        }

        return $content;
    }
}
