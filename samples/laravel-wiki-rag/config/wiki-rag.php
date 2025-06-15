<?php

return [
    /*
    |--------------------------------------------------------------------------
    | WIKI RAG API Configuration
    |--------------------------------------------------------------------------
    |
    | This file contains the configuration options for the WIKI RAG system
    | integration with Laravel. You can configure the API endpoint, cache
    | settings, and other related options here.
    |
    */

    /*
    |--------------------------------------------------------------------------
    | API Settings
    |--------------------------------------------------------------------------
    |
    | Configure the WIKI RAG API endpoint and authentication settings.
    |
    */
    'api_url' => env('WIKI_RAG_API_URL', 'http://localhost:8000'),
    'api_key' => env('WIKI_RAG_API_KEY', ''),
    'timeout' => env('WIKI_RAG_TIMEOUT', 30),

    /*
    |--------------------------------------------------------------------------
    | Cache Settings
    |--------------------------------------------------------------------------
    |
    | Configure caching behavior for WIKI RAG query results.
    |
    */
    'cache_enabled' => env('WIKI_RAG_CACHE_ENABLED', true),
    'cache_ttl' => env('WIKI_RAG_CACHE_TTL', 3600), // seconds
    'cache_prefix' => 'wiki_rag',

    /*
    |--------------------------------------------------------------------------
    | Default Query Settings
    |--------------------------------------------------------------------------
    |
    | Default values for query parameters.
    |
    */
    'defaults' => [
        'max_results' => 5,
        'threshold' => 0.3,
        'timeout' => 30,
    ],

    /*
    |--------------------------------------------------------------------------
    | UI Settings
    |--------------------------------------------------------------------------
    |
    | Configuration for the web interface.
    |
    */
    'ui' => [
        'results_per_page' => 10,
        'show_scores' => true,
        'show_metadata' => true,
        'enable_highlight' => true,
        'theme' => 'bootstrap', // bootstrap, tailwind, custom
    ],

    /*
    |--------------------------------------------------------------------------
    | Security Settings
    |--------------------------------------------------------------------------
    |
    | Security-related configuration options.
    |
    */
    'security' => [
        'rate_limit' => 60, // requests per minute
        'max_query_length' => 500,
        'allowed_characters' => '/^[a-zA-Z0-9\s\p{Hiragana}\p{Katakana}\p{Han}ー〜！？、。（）「」【】・]+$/u',
    ],

    /*
    |--------------------------------------------------------------------------
    | Logging Settings
    |--------------------------------------------------------------------------
    |
    | Configure logging behavior for WIKI RAG operations.
    |
    */
    'logging' => [
        'enabled' => env('WIKI_RAG_LOGGING_ENABLED', true),
        'channel' => env('WIKI_RAG_LOG_CHANNEL', 'default'),
        'level' => env('WIKI_RAG_LOG_LEVEL', 'info'),
        'log_queries' => true,
        'log_performance' => true,
    ],

    /*
    |--------------------------------------------------------------------------
    | Feature Flags
    |--------------------------------------------------------------------------
    |
    | Enable or disable specific features.
    |
    */
    'features' => [
        'chat_interface' => true,
        'admin_panel' => true,
        'api_endpoints' => true,
        'statistics' => true,
        'health_check' => true,
    ],

    /*
    |--------------------------------------------------------------------------
    | Performance Settings
    |--------------------------------------------------------------------------
    |
    | Performance-related configuration options.
    |
    */
    'performance' => [
        'enable_compression' => true,
        'enable_etag' => true,
        'cache_control_max_age' => 3600,
    ],
];
