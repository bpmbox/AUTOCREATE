/**
 * AUTOCREATE AI社長 - ポップアップ制御スクリプト
 */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🤖 AI社長ポップアップ初期化');
    
    // 要素取得
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    const lastCheck = document.getElementById('last-check');
    const processedCount = document.getElementById('processed-count');
    const currentSite = document.getElementById('current-site');
    
    const manualCheckBtn = document.getElementById('manual-check');
    const toggleMonitorBtn = document.getElementById('toggle-monitor');
    const testInputBtn = document.getElementById('test-input');
    const sendManualBtn = document.getElementById('send-manual');
    const manualMessage = document.getElementById('manual-message');
    
    const logContainer = document.getElementById('log-container');
    
    // エラー表示要素
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    const errorDetail = document.getElementById('error-detail');
    const clearErrorBtn = document.getElementById('clear-error');
    
    // デバッグ情報要素
    const supabaseUrl = document.getElementById('supabase-url');
    const apiKeyStatus = document.getElementById('api-key-status');
    const permissionsStatus = document.getElementById('permissions-status');
    const lastRequestInfo = document.getElementById('last-request-info');
    
    // デバッグ情報初期化
    initDebugInfo();
    
    // エラー表示関数
    function showError(message, detail) {
        errorMessage.textContent = message;
        errorDetail.textContent = detail || '';
        errorSection.classList.add('show');
        addLog(`❌ エラー: ${message}`, 'error');
    }
    
    // エラークリア関数
    function clearError() {
        errorSection.classList.remove('show');
        addLog('✅ エラークリア', 'success');
    }
    
    // デバッグ情報初期化
    async function initDebugInfo() {
        // Supabase URL表示
        supabaseUrl.textContent = 'Supabase URL: https://rootomzbucovwdqsscqd.supabase.co';
        
        // APIキー状態
        const storage = await chrome.storage.local.get(['supabaseKey']);
        apiKeyStatus.textContent = `APIキー: ${storage.supabaseKey ? '設定済み' : '未設定'}`;
        
        // 権限チェック
        const permissions = await chrome.permissions.getAll();
        permissionsStatus.textContent = `権限: ${permissions.origins ? permissions.origins.length : 0}件`;
        
        // 最終リクエスト情報
        const lastError = await chrome.storage.local.get(['lastError']);
        if (lastError.lastError) {
            lastRequestInfo.textContent = `最終エラー: ${lastError.lastError.message}`;
            showError(lastError.lastError.message, lastError.lastError.stack);
        } else {
            lastRequestInfo.textContent = '最終リクエスト: 正常';
        }
    }
    
    // 状態更新
    async function updateStatus() {
        try {
            // バックグラウンドスクリプトから状態取得
            const response = await chrome.runtime.sendMessage({ type: 'GET_STATUS' });
            
            if (response && response.active) {
                statusIndicator.className = 'indicator active';
                statusText.textContent = '監視中';
                toggleMonitorBtn.textContent = '監視停止';
                toggleMonitorBtn.className = 'btn-secondary';
            } else {
                statusIndicator.className = 'indicator inactive';
                statusText.textContent = '停止中';
                toggleMonitorBtn.textContent = '監視開始';
                toggleMonitorBtn.className = 'btn-success';
            }
            
            if (response.lastCheck) {
                const date = new Date(response.lastCheck);
                lastCheck.textContent = date.toLocaleTimeString('ja-JP');
            }
            
            if (response.processedCount !== undefined) {
                processedCount.textContent = `${response.processedCount}件`;
            }
            
        } catch (error) {
            console.error('状態更新エラー:', error);
            statusIndicator.className = 'indicator inactive';
            statusText.textContent = 'エラー';
        }
        
        // 現在のページ情報取得
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            if (tabs.length > 0) {
                const response = await chrome.tabs.sendMessage(tabs[0].id, { type: 'GET_PAGE_INFO' });
                if (response && response.site) {
                    currentSite.textContent = response.site;
                } else {
                    currentSite.textContent = '未対応サイト';
                }
            }
        } catch (error) {
            currentSite.textContent = '情報取得不可';
        }
    }
    
    // ログ追加
    function addLog(message, type = 'info') {
        const logItem = document.createElement('div');
        logItem.className = 'log-item';
        
        const time = new Date().toLocaleTimeString('ja-JP');
        logItem.textContent = `[${time}] ${message}`;
        
        logContainer.insertBefore(logItem, logContainer.firstChild);
        
        // ログが多すぎる場合は古いものを削除
        while (logContainer.children.length > 10) {
            logContainer.removeChild(logContainer.lastChild);
        }
    }
    
    // 手動チェックボタン
    manualCheckBtn.addEventListener('click', async () => {
        addLog('手動チェック実行中...');
        manualCheckBtn.disabled = true;
        manualCheckBtn.textContent = 'チェック中...';
        
        try {
            await chrome.runtime.sendMessage({ type: 'MANUAL_CHECK' });
            addLog('手動チェック完了');
        } catch (error) {
            addLog('手動チェック失敗');
            console.error('手動チェックエラー:', error);
        }
        
        manualCheckBtn.disabled = false;
        manualCheckBtn.textContent = '手動チェック';
        
        setTimeout(updateStatus, 1000);
    });
    
    // 監視切り替えボタン
    toggleMonitorBtn.addEventListener('click', async () => {
        // 実装は後で追加（バックグラウンドスクリプトの監視開始/停止）
        addLog('監視状態切り替え（未実装）');
    });
    
    // 入力テストボタン
    testInputBtn.addEventListener('click', async () => {
        const testMessage = '🤖 AI社長テストメッセージです！システムが正常に動作しています。';
        
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            if (tabs.length > 0) {
                await chrome.tabs.sendMessage(tabs[0].id, {
                    type: 'MANUAL_INPUT',
                    message: testMessage
                });
                addLog('入力テスト実行');
            } else {
                addLog('アクティブなタブが見つかりません');
            }
        } catch (error) {
            addLog('入力テスト失敗');
            console.error('入力テストエラー:', error);
        }
    });
    
    // 手動送信ボタン
    sendManualBtn.addEventListener('click', async () => {
        const message = manualMessage.value.trim();
        
        if (!message) {
            addLog('メッセージが空です');
            return;
        }
        
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            if (tabs.length > 0) {
                await chrome.tabs.sendMessage(tabs[0].id, {
                    type: 'MANUAL_INPUT',
                    message: `🤖 AI社長: ${message}`
                });
                addLog(`手動送信: ${message.substring(0, 20)}...`);
                manualMessage.value = '';
            } else {
                addLog('アクティブなタブが見つかりません');
            }
        } catch (error) {
            addLog('手動送信失敗');
            console.error('手動送信エラー:', error);
        }
    });
    
    // エラークリアボタン
    clearErrorBtn.addEventListener('click', () => {
        clearError();
        chrome.storage.local.remove(['lastError']);
        initDebugInfo(); // デバッグ情報再更新
    });
    
    // 初期状態更新
    await updateStatus();
    
    // 定期的に状態更新
    setInterval(updateStatus, 5000);
    
    addLog('AI社長ポップアップ初期化完了');
});
