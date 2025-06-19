/**
 * AUTOCREATE AI社長 - Supabase監視バックグラウンドサービス
 * Chrome Extension Service Worker
 */

console.log('🤖 AI社長監視システム起動中...');

// Service Worker の生存確認
console.log('🔍 Service Worker状態確認');
console.log('📋 self:', typeof self);
console.log('📋 chrome:', typeof chrome);
console.log('📋 chrome.runtime:', typeof chrome.runtime);
console.log('📋 chrome.notifications:', typeof chrome.notifications);

// Service Worker のアクティブ状態を維持
self.addEventListener('install', (event) => {
    console.log('🔧 Service Worker インストール');
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('🔧 Service Worker アクティベート');
    event.waitUntil(self.clients.claim());
});

// Supabase設定
const SUPABASE_CONFIG = {
    url: 'https://rootomzbucovwdqsscqd.supabase.co',
    key: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvb3RvbXpidWNvdndkcXNzY3FkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU4OTE4ODMsImV4cCI6MjA1MTQ2Nzg4M30.fYKOe-HPh4WUdvBhEJxakLWCMQBp4E90EDwARk7ucf8'
};

let lastCheckTime = new Date().toISOString();
let processedMessages = new Set();

// 拡張機能インストール時の初期化（通信エラー対策版）
chrome.runtime.onInstalled.addListener((details) => {
    console.log('🚀 AI社長監視システムインストール完了');
    console.log('📋 インストール詳細:', details);
    
    // Service Worker の生存を明示的に示す
    console.log('💗 Service Worker生存確認 - onInstalled');
    
    // 初期設定保存
    chrome.storage.local.set({
        aiPresidentActive: true,
        lastCheckTime: lastCheckTime,
        monitoringTarget: 'processmaker',
        autoInputEnabled: true,
        serviceWorkerActive: true
    }, () => {
        console.log('💾 初期設定保存完了');
    });
    
    // インストール完了通知（一時的に無効化してデバッグ）
    console.log('🔧 インストール完了 - 通知テスト無効化中');
    /*
    showNotification(
        `🤖 AI社長監視システム起動`,
        `AUTOCREATE株式会社のAI社長が監視を開始しました`,
        'success'
    );
    */
    
    // 定期監視開始
    startPeriodicMonitoring();
});

// Service Worker起動時の処理
chrome.runtime.onStartup.addListener(() => {
    console.log('🔄 Service Worker起動');
    console.log('💗 Service Worker生存確認 - onStartup');
    
    // 生存状態を記録
    chrome.storage.local.set({
        serviceWorkerActive: true,
        lastStartup: new Date().toISOString()
    });
    
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
        
        // AI社長以外のメッセージを処理 - 安全なowneridチェック
        const newUserMessages = messages.filter(msg => {
            // メッセージIDとowneridの安全な確認
            if (!msg || !msg.id) {
                console.warn('⚠️ 無効なメッセージオブジェクト:', msg);
                return false;
            }
            
            // 既に処理済みかチェック
            if (processedMessages.has(msg.id)) {
                return false;
            }
            
            // owneridの安全なチェック
            const ownerId = msg.ownerid || msg.owner || msg.username || msg.user || '';
            const systemUsers = ['AI社長', 'ai-assistant', 'system'];
            
            return !systemUsers.includes(ownerId);
        });
        
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
    
    // メッセージの安全な取得
    const safeMessage = message || {};
    const ownerId = safeMessage.ownerid || safeMessage.owner || safeMessage.username || safeMessage.user || '不明なユーザー';
    const messageContent = safeMessage.messages || safeMessage.message || safeMessage.content || '空のメッセージ';
    
    console.log('📋 安全なメッセージデータ:', { ownerId, messageContent: messageContent.substring(0, 100) });
    
    // デスクトップ通知を表示
    showNotification(
        `📬 新着メッセージ受信`,
        `${ownerId}: ${messageContent.toString().substring(0, 100)}...`,
        'info'
    );
    
    // AI社長の応答生成
    const aiResponse = generateAIPresidentResponse(safeMessage);
    
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

// デスクトップ通知を表示する関数（デバッグ強化版）
function showNotification(title, message, type = 'info') {
    console.log('🔍 showNotification called with:', { title, message, type });
    
    // 引数の厳密な検証とデバッグ
    if (!title || typeof title !== 'string') {
        console.warn('⚠️ Invalid title provided:', title, typeof title);
        title = 'AI President Monitor';
    }
    if (!message || typeof message !== 'string') {
        console.warn('⚠️ Invalid message provided:', message, typeof message);
        message = 'Notification from AI President Monitor';
    }
    
    // 最終的な値を確認
    console.log('✅ Final notification values:', { title, message, type });
    
    // メッセージの長さ制限（通知の制限を考慮）
    if (title.length > 100) {
        title = title.substring(0, 97) + '...';
    }
    if (message.length > 300) {
        message = message.substring(0, 297) + '...';
    }
    
    try {
        // Chrome通知APIで適切なアイコンファイルを使用
        const notificationOptions = {
            type: 'basic',
            iconUrl: 'icon16.png',
            title: title,
            message: message
        };

        console.log('📋 Notification options created:', JSON.stringify(notificationOptions, null, 2));
        
        // オプションの各プロパティを個別に検証
        const requiredProps = ['type', 'iconUrl', 'title', 'message'];
        const missingProps = requiredProps.filter(prop => !notificationOptions[prop]);
        
        if (missingProps.length > 0) {
            console.error('❌ Missing required properties:', missingProps);
            console.error('❌ Current options:', notificationOptions);
            return;
        }

        chrome.notifications.create(notificationOptions, (notificationId) => {
            if (chrome.runtime.lastError) {
                console.error('❌ 通知作成エラー:', chrome.runtime.lastError.message);
                // エラー時のフォールバック - より詳細な情報を表示
                console.log(`📢 フォールバック通知: ${title} - ${message}`);
                console.log('🔍 デバッグ情報:', {
                    titleType: typeof title,
                    messageType: typeof message,
                    titleLength: title?.length,
                    messageLength: message?.length
                });
            } else {
                console.log(`✅ 通知表示成功: ${notificationId}`);
                console.log(`📋 通知内容: タイトル="${title}", メッセージ="${message}"`);
                
                // 5秒後に通知を安全に削除
                setTimeout(() => {
                    safeClearNotification(notificationId);
                }, 5000);
            }
        });
    } catch (error) {
        console.error('通知処理エラー:', error);
        // フォールバック: console.logで代替
        console.log(`📢 通知(フォールバック): ${title} - ${message}`);
    }
}

// 安全な通知削除関数（修正版）
function safeClearNotification(notificationId) {
    if (!notificationId || typeof notificationId !== 'string') {
        console.warn('無効な通知ID:', notificationId);
        return;
    }
    
    try {
        // コールバック関数なしで呼び出す
        chrome.notifications.clear(notificationId);
        console.log('通知削除実行:', notificationId);
    } catch (error) {
        console.error('通知削除処理エラー:', error);
    }
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

// 通知アイコンを取得（無効化）
function getNotificationIcon(type) {
    // アイコンを使用せずnullを返す
    return null;
}

// AI社長の応答生成（エラー対策版）
function generateAIPresidentResponse(message) {
    console.log('🤖 AI社長応答生成開始:', message);
    
    // メッセージオブジェクトの安全な取得
    let username = 'ユーザー';
    let userMessage = '';
    
    try {
        // メッセージ構造の確認とログ出力
        console.log('📋 メッセージオブジェクト構造:', JSON.stringify(message, null, 2));
        
        // 様々なメッセージ構造に対応
        if (message) {
            if (typeof message === 'string') {
                userMessage = message;
            } else if (message.message) {
                userMessage = message.message;
            } else if (message.messages) {
                userMessage = message.messages;
            } else if (message.content) {
                userMessage = message.content;
            } else {
                console.warn('⚠️ 不明なメッセージ構造:', message);
                userMessage = JSON.stringify(message);
            }
            
            // ユーザー名の取得
            if (message.username) {
                username = message.username;
            } else if (message.ownerid) {
                username = message.ownerid;
            } else if (message.user) {
                username = message.user;
            } else if (message.from) {
                username = message.from;
            }
        }
        
        // 空の場合のデフォルト値 - より厳密なチェック
        if (!userMessage || typeof userMessage !== 'string' || userMessage.trim() === '') {
            userMessage = '不明なメッセージ';
        }
        if (!username || typeof username !== 'string' || username.trim() === '') {
            username = 'ユーザー';
        }
        
        console.log('📋 解析結果:', { username, userMessage });
        
    } catch (error) {
        console.error('❌ メッセージ解析エラー:', error);
        userMessage = '解析エラー';
        username = 'ユーザー';
    }
    
    const currentTime = new Date().toLocaleString('ja-JP');
    
    try {
        // 安全な文字列チェック - より厳密な確認
        let safeMessage = '';
        if (userMessage !== null && userMessage !== undefined) {
            try {
                safeMessage = String(userMessage).toLowerCase();
            } catch (stringError) {
                console.warn('⚠️ 文字列変換エラー:', stringError);
                safeMessage = '';
            }
        }
        
        console.log('🔍 安全な文字列チェック完了:', { userMessage, safeMessage });
        
        // 安全なメッセージ内容確認（safeMessageが有効な文字列の場合のみ）
        if (safeMessage && typeof safeMessage === 'string') {
            // シンプルなルールベース応答
            if (safeMessage.includes('こんにちは') || safeMessage.includes('こんばんは')) {
                return `🤖 AI社長です！${username}さん、こんにちは！AUTOCREATE株式会社へようこそ！何かお手伝いできることはありますか？`;
            }
            
            if (safeMessage.includes('質問') || safeMessage.includes('？') || safeMessage.includes('?')) {
                const truncatedMessage = String(userMessage).substring(0, 50);
                return `💡 ${username}さんのご質問「${truncatedMessage}...」について、AI社長として回答いたします。具体的な内容をお聞かせください！`;
            }
            
            if (safeMessage.includes('ありがとう') || safeMessage.includes('感謝')) {
                return `😊 ${username}さん、どういたしまして！AI社長として、お役に立てて嬉しいです。AUTOCREATE株式会社では、AI×人間の協働を目指しています！`;
            }
        }
        
        // デフォルト応答（安全な文字列処理）
        const truncatedMessage = userMessage ? String(userMessage).substring(0, 50) : 'メッセージ';
        return `🤖 AI社長です！${username}さん、「${truncatedMessage}...」について承知いたしました。AUTOCREATE株式会社AI社長として、引き続きサポートいたします！（${currentTime}）`;
        
    } catch (responseError) {
        console.error('❌ 応答生成エラー:', responseError);
        return `🤖 AI社長です！${username}さん、メッセージを受信いたしました。現在システム調整中のため、後ほど詳細な応答をいたします。（${currentTime}）`;
    }
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

// メッセージリスナー（接続エラー修正版）
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 メッセージ受信:', request.type, 'from:', sender);
    
    try {
        if (request.type === 'GET_STATUS') {
            const status = {
                active: true,
                lastCheck: lastCheckTime,
                processedCount: processedMessages.size,
                connectionStatus: 'connected'
            };
            console.log('📊 ステータス応答:', status);
            sendResponse(status);
            return true; // 非同期レスポンス維持
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
            return true; // 非同期応答を維持
        }
        
        if (request.type === 'TOGGLE_MONITOR') {
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
        
        if (request.type === 'GET_RECENT_MESSAGES') {
            console.log('💬 最近のメッセージ取得');
            getRecentMessages()
                .then(result => {
                    console.log('✅ 最近のメッセージ取得完了:', result);
                    sendResponse(result);
                })
                .catch(error => {
                    console.error('❌ 最近のメッセージ取得失敗:', error);
                    sendResponse({ success: false, error: error.message });
                });
            return true;
        }
        
        if (request.type === 'BASIC_NOTIFICATION_TEST') {
            console.log('📨 基本通知テストメッセージ受信');
            // basic-notification-test.jsの関数を呼び出す前に存在確認
            if (typeof basicNotificationTest === 'function') {
                basicNotificationTest();
            } else {
                console.warn('⚠️ basicNotificationTest関数が見つかりません');
            }
            sendResponse({success: true, message: '基本テスト実行'});
            return true;
        }
        
        if (request.type === 'test_ai_response') {
            console.log('🧪 AI応答機能テスト受信:', request.data);
            try {
                const response = generateAIPresidentResponse(request.data);
                console.log('✅ AI応答生成成功:', response);
                sendResponse({ success: true, response: response });
            } catch (error) {
                console.error('❌ AI応答生成エラー:', error);
                sendResponse({ success: false, error: error.message, stack: error.stack });
            }
            return true;
        }
        
        if (request.type === 'GET_SUPABASE_CONFIG') {
            console.log('⚙️ Supabase設定情報取得要求');
            try {
                const config = {
                    url: SUPABASE_CONFIG.url,
                    keySet: SUPABASE_CONFIG.key ? true : false,
                    keyPreview: SUPABASE_CONFIG.key ? SUPABASE_CONFIG.key.substring(0, 20) + '...' : 'なし'
                };
                console.log('✅ Supabase設定情報応答:', config);
                sendResponse({ success: true, config: config });
            } catch (error) {
                console.error('❌ Supabase設定情報取得エラー:', error);
                sendResponse({ success: false, error: error.message });
            }
            return true;
        }
        
        if (request.type === 'GET_XPATH_CONFIGS') {
            console.log('⚙️ XPath設定一覧取得要求');
            chrome.storage.local.get(['xpathConfigs'])
                .then(result => {
                    const configs = result.xpathConfigs || [];
                    console.log('✅ XPath設定一覧取得完了:', configs.length);
                    sendResponse({ success: true, configs: configs });
                })
                .catch(error => {
                    console.error('❌ XPath設定一覧取得エラー:', error);
                    sendResponse({ success: false, error: error.message });
                });
            return true;
        }
        
        if (request.type === 'SAVE_XPATH_CONFIG') {
            console.log('💾 XPath設定保存要求:', request.config);
            chrome.storage.local.get(['xpathConfigs'])
                .then(result => {
                    const configs = result.xpathConfigs || [];
                    
                    // 同じ名前の設定があれば更新、なければ追加
                    const existingIndex = configs.findIndex(c => c.name === request.config.name);
                    if (existingIndex >= 0) {
                        configs[existingIndex] = request.config;
                    } else {
                        configs.push(request.config);
                    }
                    
                    return chrome.storage.local.set({ xpathConfigs: configs });
                })
                .then(() => {
                    console.log('✅ XPath設定保存完了');
                    sendResponse({ success: true });
                })
                .catch(error => {
                    console.error('❌ XPath設定保存エラー:', error);
                    sendResponse({ success: false, error: error.message });
                });
            return true;
        }
        
        if (request.type === 'DELETE_XPATH_CONFIG') {
            console.log('🗑️ XPath設定削除要求:', request.configName);
            chrome.storage.local.get(['xpathConfigs'])
                .then(result => {
                    const configs = result.xpathConfigs || [];
                    const filteredConfigs = configs.filter(c => c.name !== request.configName);
                    return chrome.storage.local.set({ xpathConfigs: filteredConfigs });
                })
                .then(() => {
                    console.log('✅ XPath設定削除完了');
                    sendResponse({ success: true });
                })
                .catch(error => {
                    console.error('❌ XPath設定削除エラー:', error);
                    sendResponse({ success: false, error: error.message });
                });
            return true;
        }
        
        if (request.type === 'APPLY_XPATH_CONFIG') {
            console.log('🎯 XPath設定適用要求:', request.configName);
            chrome.tabs.query({ active: true, currentWindow: true })
                .then(tabs => {
                    if (tabs.length > 0) {
                        return chrome.tabs.sendMessage(tabs[0].id, {
                            type: 'LOAD_XPATH_CONFIG'
                        });
                    } else {
                        throw new Error('アクティブなタブが見つかりません');
                    }
                })
                .then(response => {
                    console.log('✅ XPath設定適用完了');
                    sendResponse({ success: true, response: response });
                })
                .catch(error => {
                    console.error('❌ XPath設定適用エラー:', error);
                    sendResponse({ success: false, error: error.message });
                });
            return true;
        }

        // 未知のメッセージタイプ
        console.warn('⚠️ 未知のメッセージタイプ:', request.type);
        sendResponse({ success: false, error: 'Unknown message type' });
        return true;
        
    } catch (error) {
        console.error('❌ メッセージハンドラーエラー:', error);
        sendResponse({ success: false, error: error.message });
        return true;
    }
});

// 最近のメッセージを取得
async function getRecentMessages(limit = 10) {
    try {
        const url = `${SUPABASE_CONFIG.url}/rest/v1/chat_history?select=*&order=created.desc&limit=${limit}`;
        
        const response = await fetch(url, {
            headers: {
                'apikey': SUPABASE_CONFIG.key,
                'Authorization': `Bearer ${SUPABASE_CONFIG.key}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const messages = await response.json();
            return {
                success: true,
                messages: messages.reverse() // 古い順に並び替え
            };
        } else {
            const errorText = await response.text();
            return {
                success: false,
                error: `HTTP ${response.status}: ${errorText}`
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

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
