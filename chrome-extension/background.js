/**
 * AUTOCREATE AI社長 - Supabase監視バックグラウンドサービス
 * Chrome Extension Service Worker
 */

console.log('🤖 AI社長監視システム起動中...');

// Supabase設定
const SUPABASE_CONFIG = {
    url: 'https://rootomzbucovwdqsscqd.supabase.co',
    key: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8'
};

let lastCheckTime = new Date().toISOString();
let processedMessages = new Set();

// 拡張機能インストール時の初期化
chrome.runtime.onInstalled.addListener(() => {
    console.log('🚀 AI社長監視システムインストール完了');
    
    // 初期設定保存
    chrome.storage.local.set({
        aiPresidentActive: true,
        lastCheckTime: lastCheckTime,
        monitoringTarget: 'processmaker', // 'processmaker' | 'skyoffice' | 'supabase'
        autoInputEnabled: true
    });
    
    // インストール完了通知
    showNotification(
        `🤖 AI社長監視システム起動`,
        `AUTOCREATE株式会社のAI社長が監視を開始しました`,
        'success'
    );
    
    // 定期監視開始
    startPeriodicMonitoring();
});

// 定期監視システム
function startPeriodicMonitoring() {
    console.log('📡 定期監視開始');
    
    // 5秒間隔でSupabaseを監視
    setInterval(async () => {
        try {
            await checkSupabaseForNewMessages();
        } catch (error) {
            console.error('❌ 監視エラー:', error);
        }
    }, 5000);
}

// Supabaseから新着メッセージをチェック
async function checkSupabaseForNewMessages() {
    try {
        console.log('🔍 Supabase通信開始:', SUPABASE_CONFIG.url);
        console.log('🕐 最終チェック時間:', lastCheckTime);
        
        const url = `${SUPABASE_CONFIG.url}/rest/v1/chat_history?select=*&created=gte.${lastCheckTime}&order=created.desc`;
        console.log('📡 リクエストURL:', url);
        
        const response = await fetch(url, {
            headers: {
                'apikey': SUPABASE_CONFIG.key,
                'Authorization': `Bearer ${SUPABASE_CONFIG.key}`,
                'Content-Type': 'application/json'
            }
        });
        
        console.log('📨 レスポンスステータス:', response.status);
        console.log('📨 レスポンスヘッダー:', [...response.headers.entries()]);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ HTTP エラー詳細:', errorText);
            throw new Error(`HTTP error! status: ${response.status}, detail: ${errorText}`);
        }
        
        const messages = await response.json();
        console.log('📊 取得メッセージ数:', messages.length);
        console.log('📝 メッセージデータ:', messages);
        
        // AI社長以外のメッセージを処理
        const newUserMessages = messages.filter(msg => 
            !processedMessages.has(msg.id) && 
            !['AI社長', 'ai-assistant', 'system'].includes(msg.ownerid)
        );
        
        console.log('🆕 新着ユーザーメッセージ数:', newUserMessages.length);
        
        if (newUserMessages.length > 0) {
            console.log(`📬 新着メッセージ ${newUserMessages.length}件処理開始`);
            
            // 複数メッセージの場合はまとめて通知
            if (newUserMessages.length === 1) {
                showNotification(
                    `📬 新着メッセージ受信`,
                    `${newUserMessages[0].ownerid}からメッセージが届きました`,
                    'info'
                );
            } else {
                showNotification(
                    `📬 複数メッセージ受信`,
                    `${newUserMessages.length}件の新着メッセージを処理中`,
                    'info'
                );
            }
            
            for (const message of newUserMessages) {
                console.log('💬 処理中メッセージ:', message);
                await processNewMessage(message);
                processedMessages.add(message.id);
            }
            
            // 最終チェック時間更新
            lastCheckTime = new Date().toISOString();
            chrome.storage.local.set({ lastCheckTime });
            console.log('🕐 最終チェック時間更新:', lastCheckTime);
        } else {
            console.log('📭 新着メッセージなし');
        }
        
    } catch (error) {
        console.error('❌ Supabase監視エラー詳細:');
        console.error('   エラータイプ:', error.name);
        console.error('   エラーメッセージ:', error.message);
        console.error('   スタックトレース:', error.stack);
        
        // エラー情報をストレージに保存
        chrome.storage.local.set({
            lastError: {
                timestamp: new Date().toISOString(),
                type: error.name,
                message: error.message,
                stack: error.stack
            }
        });
        
        // リトライ処理
        setTimeout(() => {
            console.log('🔄 Supabase接続リトライ...');
        }, 10000); // 10秒後にリトライ
    }
}

// 新着メッセージの処理
async function processNewMessage(message) {
    console.log('💬 メッセージ処理中:', message);
    
    // デスクトップ通知を表示
    showNotification(
        `📬 新着メッセージ受信`,
        `${message.ownerid}: ${message.messages.substring(0, 100)}...`,
        'info'
    );
    
    // AI社長の応答生成
    const aiResponse = generateAIPresidentResponse(message);
    
    // 応答通知も表示
    showNotification(
        `🤖 AI社長応答準備完了`,
        `応答: ${aiResponse.substring(0, 100)}...`,
        'success'
    );
    
    // アクティブなタブに応答送信指示
    try {
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        
        if (tabs.length > 0) {
            // コンテンツスクリプトに応答送信指示
            chrome.tabs.sendMessage(tabs[0].id, {
                type: 'AUTO_INPUT_MESSAGE',
                message: aiResponse,
                originalMessage: message
            });
            
            console.log('📤 応答送信指示完了');
            showNotification(
                `✅ 応答送信完了`,
                `AI社長がページに応答を入力しました`,
                'success'
            );
        }
        
    } catch (error) {
        console.error('❌ メッセージ送信エラー:', error);
        showNotification(
            `❌ 応答送信エラー`,
            `エラー: ${error.message}`,
            'error'
        );
    }
    
    // Supabaseにも応答を記録
    await sendResponseToSupabase(aiResponse, message);
}

// デスクトップ通知を表示する関数
function showNotification(title, message, type = 'info') {
    const iconUrl = getNotificationIcon(type);
    
    chrome.notifications.create({
        type: 'basic',
        iconUrl: iconUrl,
        title: title,
        message: message,
        priority: type === 'error' ? 2 : 1
    }, (notificationId) => {
        console.log(`📢 通知表示: ${notificationId}`);
        
        // 5秒後に通知を自動削除
        setTimeout(() => {
            chrome.notifications.clear(notificationId);
        }, 5000);
    });
}

// 通知クリック時の処理
chrome.notifications.onClicked.addListener((notificationId) => {
    console.log('🔔 通知がクリックされました:', notificationId);
    
    // 通知をクリアして、拡張機能のポップアップを開く
    chrome.notifications.clear(notificationId);
    
    // アクティブなタブでSupabaseチャットページを開く（オプション）
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
            // 現在のタブでSupabaseチャットページを開く
            chrome.tabs.update(tabs[0].id, {
                url: 'https://supabase-message-stream.lovable.app/'
            });
        }
    });
});

// 通知が閉じられた時の処理
chrome.notifications.onClosed.addListener((notificationId, byUser) => {
    if (byUser) {
        console.log('🔕 ユーザーが通知を閉じました:', notificationId);
    } else {
        console.log('⏰ 通知が自動的に閉じられました:', notificationId);
    }
});

// 通知アイコンを取得
function getNotificationIcon(type) {
    // アイコンファイルのパス（拡張機能内）
    switch (type) {
        case 'success':
            return 'icons/icon16.png'; // 成功用アイコン
        case 'error':
            return 'icons/icon16.png';  // エラー用アイコン
        case 'warning':
            return 'icons/icon16.png'; // 警告用アイコン
        default:
            return 'icons/icon16.png';  // デフォルトアイコン
    }
}

// AI社長の応答生成
function generateAIPresidentResponse(message) {
    const { username, message: userMessage } = message;
    const currentTime = new Date().toLocaleString('ja-JP');
    
    // シンプルなルールベース応答
    if (userMessage.includes('こんにちは') || userMessage.includes('こんばんは')) {
        return `🤖 AI社長です！${username}さん、こんにちは！AUTOCREATE株式会社へようこそ！何かお手伝いできることはありますか？`;
    }
    
    if (userMessage.includes('質問') || userMessage.includes('？') || userMessage.includes('?')) {
        return `💡 ${username}さんのご質問「${userMessage.substring(0, 50)}...」について、AI社長として回答いたします。具体的な内容をお聞かせください！`;
    }
    
    if (userMessage.includes('ありがとう') || userMessage.includes('感謝')) {
        return `😊 ${username}さん、どういたしまして！AI社長として、お役に立てて嬉しいです。AUTOCREATE株式会社では、AI×人間の協働を目指しています！`;
    }
    
    // デフォルト応答
    return `🤖 AI社長です！${username}さん、「${userMessage.substring(0, 50)}...」について承知いたしました。AUTOCREATE株式会社AI社長として、引き続きサポートいたします！（${currentTime}）`;
}

// Supabaseに応答を送信
async function sendResponseToSupabase(response, originalMessage) {
    try {
        const responseData = {
            id: generateUUID(),
            username: 'AI社長',
            message: response,
            created: new Date().toISOString(),
            ownerid: 'ai-president-github-copilot',
            thread_id: originalMessage.thread_id || 'general',
            response_to: originalMessage.id
        };
        
        const response_api = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/chat_history`, {
            method: 'POST',
            headers: {
                'apikey': SUPABASE_CONFIG.key,
                'Authorization': `Bearer ${SUPABASE_CONFIG.key}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            },
            body: JSON.stringify(responseData)
        });
        
        if (response_api.ok) {
            console.log('✅ Supabase応答記録完了');
        } else {
            console.error('❌ Supabase応答記録失敗:', response_api.status);
        }
        
    } catch (error) {
        console.error('❌ Supabase応答送信エラー:', error);
    }
}

// UUID生成
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// タブ更新時の処理
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        // ProcessMakerまたはSkyOfficeページの場合
        if (tab.url.includes('processmaker.com') || tab.url.includes('skyoffice.me')) {
            console.log('🌐 対象サイト検出:', tab.url);
            
            // コンテンツスクリプトに初期化指示
            chrome.tabs.sendMessage(tabId, {
                type: 'INIT_AI_PRESIDENT_MONITOR',
                url: tab.url
            });
        }
    }
});

// メッセージリスナー
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 メッセージ受信:', request.type);
    
    if (request.type === 'GET_STATUS') {
        const status = {
            active: true,
            lastCheck: lastCheckTime,
            processedCount: processedMessages.size,
            connectionStatus: 'unknown'
        };
        console.log('📊 ステータス応答:', status);
        sendResponse(status);
        return true;
    }
    
    if (request.type === 'MANUAL_CHECK') {
        console.log('🔄 手動チェック開始');
        checkSupabaseForNewMessages()
            .then(() => {
                console.log('✅ 手動チェック完了');
                sendResponse({ success: true });
            })
            .catch(error => {
                console.error('❌ 手動チェック失敗:', error);
                sendResponse({ success: false, error: error.message });
            });
        return true; // 非同期応答
    }
    
    if (request.type === 'TOGGLE_MONITOR') {
        // 監視の開始/停止機能（今後実装）
        console.log('🔄 監視状態切り替え（実装予定）');
        sendResponse({ success: true, message: '監視状態切り替え機能は開発中です' });
        return true;
    }
    
    if (request.type === 'TEST_CONNECTION') {
        console.log('🧪 接続テスト開始');
        testSupabaseConnection()
            .then(result => {
                console.log('✅ 接続テスト完了:', result);
                sendResponse(result);
            })
            .catch(error => {
                console.error('❌ 接続テスト失敗:', error);
                sendResponse({ success: false, error: error.message });
            });
        return true;
    }
    
    if (request.type === 'SEND_MANUAL_MESSAGE') {
        console.log('📤 手動メッセージ送信:', request.message);
        sendManualMessageToSupabase(request.message)
            .then(result => {
                console.log('✅ 手動メッセージ送信完了');
                sendResponse({ success: true });
            })
            .catch(error => {
                console.error('❌ 手動メッセージ送信失敗:', error);
                sendResponse({ success: false, error: error.message });
            });
        return true;
    }
});

// 接続テスト関数
async function testSupabaseConnection() {
    try {
        showNotification(
            `🔍 Supabase接続テスト開始`,
            `データベース接続を確認中...`,
            'info'
        );
        
        const url = `${SUPABASE_CONFIG.url}/rest/v1/chat_history?select=id&limit=1`;
        console.log('🧪 テストURL:', url);
        
        const response = await fetch(url, {
            headers: {
                'apikey': SUPABASE_CONFIG.key,
                'Authorization': `Bearer ${SUPABASE_CONFIG.key}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            showNotification(
                `✅ Supabase接続成功`,
                `正常に接続されました (データ数: ${data.length})`,
                'success'
            );
            return { 
                success: true, 
                message: '接続成功', 
                status: response.status,
                dataCount: data.length 
            };
        } else {
            const errorText = await response.text();
            showNotification(
                `❌ Supabase接続失敗`,
                `HTTP ${response.status}: ${errorText.substring(0, 100)}`,
                'error'
            );
            return { 
                success: false, 
                message: `接続失敗: HTTP ${response.status}`,
                detail: errorText 
            };
        }
    } catch (error) {
        showNotification(
            `❌ Supabase接続エラー`,
            `${error.message}`,
            'error'
        );
        return { 
            success: false, 
            message: '接続エラー',
            detail: error.message 
        };
    }
}

// 手動メッセージ送信関数
async function sendManualMessageToSupabase(message) {
    showNotification(
        `📤 手動メッセージ送信中`,
        `Supabaseに送信しています...`,
        'info'
    );
    
    const messageData = {
        messages: message,
        ownerid: 'AI社長(手動)',
        created: new Date().toISOString(),
        isread: false,
        targetid: 'autocreate_manual',
        status: 'sent',
        status_created: new Date().toISOString()
    };
    
    const response = await fetch(`${SUPABASE_CONFIG.url}/rest/v1/chat_history`, {
        method: 'POST',
        headers: {
            'apikey': SUPABASE_CONFIG.key,
            'Authorization': `Bearer ${SUPABASE_CONFIG.key}`,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        },
        body: JSON.stringify(messageData)
    });
    
    if (!response.ok) {
        const errorText = await response.text();
        showNotification(
            `❌ メッセージ送信失敗`,
            `HTTP ${response.status}: ${errorText.substring(0, 100)}`,
            'error'
        );
        throw new Error(`HTTP ${response.status}: ${errorText}`);
    }
    
    showNotification(
        `✅ メッセージ送信成功`,
        `Supabaseにメッセージを送信しました`,
        'success'
    );
    
    return await response.json();
}

console.log('🎯 AI社長監視システム準備完了！');
