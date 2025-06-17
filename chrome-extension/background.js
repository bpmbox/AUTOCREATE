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
    
    // AI社長の応答生成
    const aiResponse = generateAIPresidentResponse(message);
    
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
        }
        
    } catch (error) {
        console.error('❌ メッセージ送信エラー:', error);
    }
    
    // Supabaseにも応答を記録
    await sendResponseToSupabase(aiResponse, message);
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
    if (request.type === 'GET_STATUS') {
        sendResponse({
            active: true,
            lastCheck: lastCheckTime,
            processedCount: processedMessages.size
        });
    }
    
    if (request.type === 'MANUAL_CHECK') {
        checkSupabaseForNewMessages();
        sendResponse({ success: true });
    }
});

console.log('🎯 AI社長監視システム準備完了！');
