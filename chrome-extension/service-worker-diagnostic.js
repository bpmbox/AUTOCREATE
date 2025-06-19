// Service Worker通信診断ツール
console.log('🩺 Service Worker通信診断ツール読み込み開始');

// Service Worker状態監視
function monitorServiceWorkerState() {
    console.log('📊 Service Worker状態監視開始');
    
    // 基本情報の確認
    console.log('🔍 基本情報確認:');
    console.log('  - navigator.serviceWorker:', !!navigator.serviceWorker);
    console.log('  - chrome.runtime:', !!chrome.runtime);
    console.log('  - chrome.runtime.id:', chrome.runtime.id);
    
    // 現在のService Worker状態を確認
    if (navigator.serviceWorker) {
        navigator.serviceWorker.getRegistrations().then(registrations => {
            console.log('📋 Service Worker登録数:', registrations.length);
            registrations.forEach((registration, index) => {
                console.log(`📋 登録${index + 1}:`, {
                    scope: registration.scope,
                    active: !!registration.active,
                    installing: !!registration.installing,
                    waiting: !!registration.waiting
                });
            });
        });
    }
    
    // 定期的に生存確認
    setInterval(() => {
        const timestamp = new Date().toISOString();
        console.log(`💗 Service Worker生存確認: ${timestamp}`);
        
        // ストレージに生存記録
        if (chrome.storage && chrome.storage.local) {
            chrome.storage.local.set({
                lastHeartbeat: timestamp
            });
        }
    }, 30000); // 30秒ごと
}

// 通信診断テスト
function communicationDiagnostic() {
    console.log('🩺 通信診断テスト開始');
    
    // テスト1: 基本的なランタイム確認
    console.log('📋 テスト1: ランタイム確認');
    console.log('  - chrome.runtime:', !!chrome.runtime);
    console.log('  - chrome.runtime.sendMessage:', !!chrome.runtime.sendMessage);
    console.log('  - chrome.runtime.onMessage:', !!chrome.runtime.onMessage);
    
    // テスト2: メッセージリスナー確認
    console.log('📋 テスト2: メッセージリスナー確認');
    const hasListeners = chrome.runtime.onMessage.hasListeners();
    console.log('  - メッセージリスナー登録状況:', hasListeners);
    
    // テスト3: 自己通信テスト
    console.log('📋 テスト3: 自己通信テスト');
    try {
        chrome.runtime.sendMessage({
            type: 'DIAGNOSTIC_PING',
            timestamp: new Date().toISOString()
        }, (response) => {
            if (chrome.runtime.lastError) {
                console.error('❌ 自己通信エラー:', chrome.runtime.lastError.message);
            } else {
                console.log('✅ 自己通信成功:', response);
            }
        });
    } catch (error) {
        console.error('❌ 自己通信例外:', error);
    }
    
    return {
        runtime: !!chrome.runtime,
        sendMessage: !!chrome.runtime.sendMessage,
        onMessage: !!chrome.runtime.onMessage,
        hasListeners: hasListeners,
        timestamp: new Date().toISOString()
    };
}

// 診断リスナーを追加
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'DIAGNOSTIC_PING') {
        console.log('🏓 診断ping受信:', request);
        sendResponse({
            success: true,
            message: 'Service Worker is alive',
            timestamp: new Date().toISOString(),
            originalRequest: request
        });
        return true;
    }
    
    if (request.type === 'RUN_COMMUNICATION_DIAGNOSTIC') {
        console.log('🩺 通信診断実行要求');
        const result = communicationDiagnostic();
        sendResponse({
            success: true,
            diagnostic: result
        });
        return true;
    }
});

// 自動実行
setTimeout(() => {
    monitorServiceWorkerState();
    communicationDiagnostic();
}, 1000);

console.log('✅ Service Worker通信診断ツール読み込み完了');
