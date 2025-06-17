@extends('layouts.app')

@section('content')
<div class="row">
    <div class="col-12">
        <h1 class="mb-4">
            <i class="fas fa-comments"></i> WIKI RAGチャット
        </h1>
        <p class="lead text-muted">
            Interactive conversational search with AI-powered knowledge base
        </p>
    </div>
</div>

<div class="row">
    <div class="col-md-8">
        <!-- Chat Container -->
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">
                    <i class="fas fa-robot"></i> AI Assistant
                    <span class="badge bg-light text-primary ms-2" id="messageCount">0 messages</span>
                </h5>
            </div>
            <div class="card-body p-0">
                <div id="chatContainer" class="chat-container">
                    <div class="chat-message chat-assistant">
                        <strong>AI Assistant:</strong> こんにちは！WIKI RAGシステムへようこそ。何について知りたいですか？
                    </div>
                </div>
            </div>
            <div class="card-footer">
                <form id="chatForm">
                    <div class="input-group">
                        <input type="text" 
                               class="form-control" 
                               id="chatInput" 
                               placeholder="質問を入力してください..." 
                               autocomplete="off">
                        <button class="btn btn-primary" type="submit" id="sendBtn">
                            <i class="fas fa-paper-plane"></i> 送信
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <!-- Chat Settings -->
        <div class="card mb-3">
            <div class="card-header">
                <h6 class="mb-0">チャット設定</h6>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label for="chatMaxResults" class="form-label">結果数</label>
                    <select class="form-select form-select-sm" id="chatMaxResults">
                        <option value="3" selected>3件</option>
                        <option value="5">5件</option>
                        <option value="10">10件</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="chatThreshold" class="form-label">
                        類似度閾値: <span id="chatThresholdValue">0.3</span>
                    </label>
                    <input type="range" 
                           class="form-range" 
                           id="chatThreshold" 
                           min="0" 
                           max="1" 
                           step="0.1" 
                           value="0.3">
                </div>
                <div class="mb-3">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="showScores" checked>
                        <label class="form-check-label" for="showScores">
                            スコア表示
                        </label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="autoScroll" checked>
                        <label class="form-check-label" for="autoScroll">
                            自動スクロール
                        </label>
                    </div>
                </div>
                <div class="d-grid">
                    <button type="button" class="btn btn-outline-secondary btn-sm" id="clearChat">
                        <i class="fas fa-trash"></i> チャットクリア
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="card mb-3">
            <div class="card-header">
                <h6 class="mb-0">クイックアクション</h6>
            </div>
            <div class="card-body">
                <div class="d-grid gap-2">
                    <button class="btn btn-outline-primary btn-sm quick-question" 
                            data-question="Python学習の始め方を教えて">
                        <i class="fas fa-code"></i> Python学習
                    </button>
                    <button class="btn btn-outline-success btn-sm quick-question" 
                            data-question="機械学習の基本概念について">
                        <i class="fas fa-brain"></i> 機械学習
                    </button>
                    <button class="btn btn-outline-info btn-sm quick-question" 
                            data-question="Webアプリケーションの作り方">
                        <i class="fas fa-globe"></i> Web開発
                    </button>
                    <button class="btn btn-outline-warning btn-sm quick-question" 
                            data-question="データベース設計の手順">
                        <i class="fas fa-database"></i> DB設計
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Chat Statistics -->
        <div class="card">
            <div class="card-header">
                <h6 class="mb-0">統計情報</h6>
            </div>
            <div class="card-body">
                <div class="row text-center">
                    <div class="col-6">
                        <div class="border-end">
                            <div class="h4 mb-0" id="totalQueries">0</div>
                            <small class="text-muted">質問数</small>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="h4 mb-0" id="avgResponseTime">0ms</div>
                        <small class="text-muted">平均応答時間</small>
                    </div>
                </div>
                <hr>
                <div class="text-center">
                    <div class="h6 mb-0" id="sessionTime">00:00</div>
                    <small class="text-muted">セッション時間</small>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

@push('scripts')
<script>
$(document).ready(function() {
    let messageCount = 0;
    let totalQueries = 0;
    let totalResponseTime = 0;
    let sessionStart = Date.now();
    
    // Update session time every second
    setInterval(updateSessionTime, 1000);
    
    // Threshold value display
    $('#chatThreshold').on('input', function() {
        $('#chatThresholdValue').text($(this).val());
    });
    
    // Quick question buttons
    $('.quick-question').click(function() {
        const question = $(this).data('question');
        $('#chatInput').val(question);
        sendMessage();
    });
    
    // Clear chat button
    $('#clearChat').click(function() {
        if (confirm('チャット履歴をクリアしますか？')) {
            $('#chatContainer').html(`
                <div class="chat-message chat-assistant">
                    <strong>AI Assistant:</strong> チャットがクリアされました。新しい質問をどうぞ！
                </div>
            `);
            messageCount = 0;
            updateMessageCount();
        }
    });
    
    // Form submission
    $('#chatForm').submit(function(e) {
        e.preventDefault();
        sendMessage();
    });
    
    // Enter key submission
    $('#chatInput').keypress(function(e) {
        if (e.which === 13 && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    function sendMessage() {
        const input = $('#chatInput');
        const message = input.val().trim();
        
        if (message.length === 0) {
            return;
        }
        
        // Add user message to chat
        addChatMessage('user', message);
        input.val('');
        
        // Disable send button
        const sendBtn = $('#sendBtn');
        sendBtn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> 検索中...');
        
        // Prepare search data
        const searchData = {
            query: message,
            max_results: $('#chatMaxResults').val(),
            threshold: $('#chatThreshold').val()
        };
        
        const startTime = Date.now();
        
        // Send request
        $.ajax({
            url: '{{ route("wiki-rag.search") }}',
            method: 'POST',
            data: searchData,
            success: function(response) {
                const endTime = Date.now();
                const responseTime = endTime - startTime;
                
                // Update statistics
                totalQueries++;
                totalResponseTime += responseTime;
                updateStatistics();
                
                // Format and add assistant response
                const assistantMessage = formatAssistantResponse(response.data);
                addChatMessage('assistant', assistantMessage);
            },
            error: function(xhr) {
                const errorMessage = xhr.responseJSON?.error || 'エラーが発生しました。もう一度お試しください。';
                addChatMessage('assistant', `<div class="alert alert-danger mb-0">${errorMessage}</div>`);
            },
            complete: function() {
                sendBtn.prop('disabled', false).html('<i class="fas fa-paper-plane"></i> 送信');
            }
        });
    }
    
    function addChatMessage(type, content) {
        const chatContainer = $('#chatContainer');
        const messageClass = type === 'user' ? 'chat-user' : 'chat-assistant';
        const sender = type === 'user' ? 'あなた' : 'AI Assistant';
        
        const messageHtml = `
            <div class="chat-message ${messageClass}">
                <strong>${sender}:</strong> ${content}
            </div>
        `;
        
        chatContainer.append(messageHtml);
        messageCount++;
        updateMessageCount();
        
        // Auto scroll if enabled
        if ($('#autoScroll').is(':checked')) {
            chatContainer.scrollTop(chatContainer[0].scrollHeight);
        }
    }
    
    function formatAssistantResponse(data) {
        if (!data.results || data.results.length === 0) {
            return '申し訳ありませんが、該当する情報が見つかりませんでした。別の質問をお試しください。';
        }
        
        let response = `${data.total_results}件の関連情報を見つけました：<br><br>`;
        
        data.results.forEach(function(result, index) {
            const score = $('#showScores').is(':checked') ? 
                ` <span class="badge bg-primary">${(result.score * 100).toFixed(1)}%</span>` : '';
            
            response += `
                <div class="border-start border-primary ps-3 mb-3">
                    <strong>結果 ${index + 1}${score}</strong><br>
                    ${result.content.substring(0, 300)}${result.content.length > 300 ? '...' : ''}
                </div>
            `;
        });
        
        response += `<small class="text-muted">応答時間: ${data.response_time_ms}ms</small>`;
        
        return response;
    }
    
    function updateMessageCount() {
        $('#messageCount').text(`${messageCount} messages`);
    }
    
    function updateStatistics() {
        $('#totalQueries').text(totalQueries);
        const avgTime = totalQueries > 0 ? Math.round(totalResponseTime / totalQueries) : 0;
        $('#avgResponseTime').text(`${avgTime}ms`);
    }
    
    function updateSessionTime() {
        const elapsed = Math.floor((Date.now() - sessionStart) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        $('#sessionTime').text(`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
    }
});
</script>
@endpush
