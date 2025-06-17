@extends('layouts.app')

@section('content')
<div class="row">
    <div class="col-12">
        <h1 class="mb-4">
            <i class="fas fa-search"></i> WIKI RAG検索
        </h1>
        <p class="lead text-muted">
            AI-powered knowledge base search with semantic understanding
        </p>
    </div>
</div>

<!-- Search Form -->
<div class="search-form">
    <form id="searchForm" method="POST" action="{{ route('wiki-rag.search') }}">
        @csrf
        <div class="row">
            <div class="col-md-8">
                <div class="mb-3">
                    <label for="query" class="form-label">検索クエリ</label>
                    <input type="text" 
                           class="form-control form-control-lg" 
                           id="query" 
                           name="query" 
                           placeholder="例: Pythonの基本的な使い方について教えて"
                           value="{{ old('query') }}"
                           required>
                    <div class="form-text">2-500文字で検索したい内容を入力してください</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="mb-3">
                    <label for="max_results" class="form-label">最大結果数</label>
                    <select class="form-select" id="max_results" name="max_results">
                        <option value="3">3件</option>
                        <option value="5" selected>5件</option>
                        <option value="10">10件</option>
                        <option value="20">20件</option>
                    </select>
                </div>
            </div>
        </div>
        
        <!-- Advanced Options -->
        <div class="row">
            <div class="col-md-6">
                <div class="mb-3">
                    <label for="threshold" class="form-label">
                        類似度閾値 <span class="text-muted">(0.0-1.0)</span>
                    </label>
                    <input type="range" 
                           class="form-range" 
                           id="threshold" 
                           name="threshold" 
                           min="0" 
                           max="1" 
                           step="0.1" 
                           value="0.3">
                    <div class="d-flex justify-content-between">
                        <small class="text-muted">低い (多くの結果)</small>
                        <small class="text-muted" id="thresholdValue">0.3</small>
                        <small class="text-muted">高い (厳密な結果)</small>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="mb-3">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="realtime" checked>
                        <label class="form-check-label" for="realtime">
                            リアルタイム検索
                        </label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="highlight" checked>
                        <label class="form-check-label" for="highlight">
                            キーワードハイライト
                        </label>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button type="button" class="btn btn-outline-secondary" id="clearBtn">
                <i class="fas fa-eraser"></i> クリア
            </button>
            <button type="submit" class="btn btn-primary btn-lg" id="searchBtn">
                <i class="fas fa-search"></i> 検索実行
            </button>
        </div>
    </form>
</div>

<!-- Search Results -->
<div id="searchResults" class="mt-4"></div>

<!-- Loading Animation -->
<div id="loadingAnimation" class="loading d-none">
    <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">検索中...</span>
    </div>
    <p class="mt-3">AI-powered search in progress...</p>
</div>

<!-- Sample Queries -->
<div class="mt-5">
    <h4>サンプルクエリ</h4>
    <div class="row">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">プログラミング</h6>
                    <div class="d-grid gap-2">
                        <button class="btn btn-outline-primary btn-sm sample-query" 
                                data-query="Pythonの基本的な文法について">
                            Python文法
                        </button>
                        <button class="btn btn-outline-primary btn-sm sample-query" 
                                data-query="機械学習アルゴリズムの種類">
                            機械学習
                        </button>
                        <button class="btn btn-outline-primary btn-sm sample-query" 
                                data-query="データベース設計のベストプラクティス">
                            DB設計
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">技術トピック</h6>
                    <div class="d-grid gap-2">
                        <button class="btn btn-outline-success btn-sm sample-query" 
                                data-query="クラウドコンピューティングの利点">
                            クラウド
                        </button>
                        <button class="btn btn-outline-success btn-sm sample-query" 
                                data-query="セキュリティのベストプラクティス">
                            セキュリティ
                        </button>
                        <button class="btn btn-outline-success btn-sm sample-query" 
                                data-query="APIの設計原則">
                            API設計
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">開発手法</h6>
                    <div class="d-grid gap-2">
                        <button class="btn btn-outline-info btn-sm sample-query" 
                                data-query="アジャイル開発の手法">
                            アジャイル
                        </button>
                        <button class="btn btn-outline-info btn-sm sample-query" 
                                data-query="テスト駆動開発のメリット">
                            TDD
                        </button>
                        <button class="btn btn-outline-info btn-sm sample-query" 
                                data-query="CI/CDパイプラインの構築">
                            CI/CD
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

@push('scripts')
<script>
$(document).ready(function() {
    // Threshold value display
    $('#threshold').on('input', function() {
        $('#thresholdValue').text($(this).val());
    });
    
    // Sample query buttons
    $('.sample-query').click(function() {
        const query = $(this).data('query');
        $('#query').val(query);
        if ($('#realtime').is(':checked')) {
            performSearch();
        }
    });
    
    // Clear button
    $('#clearBtn').click(function() {
        $('#query').val('');
        $('#searchResults').empty();
    });
    
    // Real-time search
    let searchTimeout;
    $('#query').on('input', function() {
        if ($('#realtime').is(':checked') && $(this).val().length > 2) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(performSearch, 1000);
        }
    });
    
    // Form submission
    $('#searchForm').submit(function(e) {
        e.preventDefault();
        performSearch();
    });
    
    // Search function
    function performSearch() {
        const query = $('#query').val().trim();
        if (query.length < 2) {
            alert('検索クエリは2文字以上で入力してください。');
            return;
        }
        
        const formData = {
            query: query,
            max_results: $('#max_results').val(),
            threshold: $('#threshold').val()
        };
        
        // Show loading
        $('#loadingAnimation').removeClass('d-none');
        $('#searchResults').empty();
        $('#searchBtn').prop('disabled', true);
        
        $.ajax({
            url: '{{ route("wiki-rag.search") }}',
            method: 'POST',
            data: formData,
            success: function(response) {
                displayResults(response.data);
            },
            error: function(xhr) {
                console.error('Search failed:', xhr);
            },
            complete: function() {
                $('#loadingAnimation').addClass('d-none');
                $('#searchBtn').prop('disabled', false);
            }
        });
    }
    
    // Display results function
    function displayResults(data) {
        const resultsContainer = $('#searchResults');
        resultsContainer.empty();
        
        if (!data.results || data.results.length === 0) {
            resultsContainer.html(`
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> 
                    検索結果が見つかりませんでした。別のキーワードで検索してみてください。
                </div>
            `);
            return;
        }
        
        // Results header
        resultsContainer.append(`
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4>検索結果 (${data.total_results}件)</h4>
                <small class="text-muted">
                    応答時間: ${data.response_time_ms}ms | 
                    閾値: ${data.threshold}
                </small>
            </div>
        `);
        
        // Results items
        data.results.forEach(function(result, index) {
            const highlight = $('#highlight').is(':checked');
            const content = highlight ? result.highlight : result.content;
            
            resultsContainer.append(`
                <div class="result-item">
                    <div class="d-flex justify-content-between align-items-start">
                        <h6 class="mb-2">結果 ${index + 1}</h6>
                        <span class="result-score">${(result.score * 100).toFixed(1)}%</span>
                    </div>
                    <div class="result-content">
                        ${content.substring(0, 500)}${content.length > 500 ? '...' : ''}
                    </div>
                    ${result.metadata && Object.keys(result.metadata).length > 0 ? `
                        <div class="result-metadata">
                            <strong>メタデータ:</strong> 
                            ${JSON.stringify(result.metadata)}
                        </div>
                    ` : ''}
                </div>
            `);
        });
        
        // Scroll to results
        resultsContainer[0].scrollIntoView({ behavior: 'smooth' });
    }
});
</script>
@endpush
