/**
 * AUTOCREATE AI社長 - コンテンツスクリプト
 * ページ内の入力欄を自動操作
 */

console.log('🤖 AI社長コンテンツスクリプト読み込み完了');

let aiPresidentMonitor = {
    active: false,
    inputSelector: null,
    submitSelector: null,
    currentSite: null
};

// XPath設定管理
let xpathConfig = {
    messageInput: '',
    sendButton: '',
    messageDisplay: ''
};

// ページの種類を判定して適切なセレクターを設定
function detectPageType() {
    const url = window.location.href;
    
    if (url.includes('processmaker.com')) {
        aiPresidentMonitor.currentSite = 'processmaker';
        // ProcessMaker用のセレクター（実際のサイト構造に合わせて調整が必要）
        aiPresidentMonitor.inputSelector = 'input[type="text"], textarea, [contenteditable="true"]';
        aiPresidentMonitor.submitSelector = 'button[type="submit"], .btn-primary, .submit-btn';
        
    } else if (url.includes('skyoffice.me')) {
        aiPresidentMonitor.currentSite = 'skyoffice';
        // SkyOffice用のセレクター
        aiPresidentMonitor.inputSelector = '.chat-input, .message-input, input[placeholder*="message"], textarea[placeholder*="message"]';
        aiPresidentMonitor.submitSelector = '.send-btn, .chat-send, button[type="submit"]';
        
    } else if (url.includes('supabase.co')) {
        aiPresidentMonitor.currentSite = 'supabase';
        // Supabase Dashboard用
        aiPresidentMonitor.inputSelector = 'input, textarea';
        aiPresidentMonitor.submitSelector = 'button';
        
    } else {
        // 汎用的なチャット・入力欄検出
        aiPresidentMonitor.currentSite = 'generic';
        aiPresidentMonitor.inputSelector = 'input[type="text"], textarea, [contenteditable="true"], .chat-input, .message-input';
        aiPresidentMonitor.submitSelector = 'button[type="submit"], .send-btn, .submit-btn';
    }
    
    console.log(`🎯 サイト検出: ${aiPresidentMonitor.currentSite}`);
    console.log(`📝 入力欄セレクター: ${aiPresidentMonitor.inputSelector}`);
    console.log(`🚀 送信ボタンセレクター: ${aiPresidentMonitor.submitSelector}`);
}

// 入力欄を検出
function findInputField() {
    const inputs = document.querySelectorAll(aiPresidentMonitor.inputSelector);
    
    // 表示されている入力欄を優先して選択
    for (const input of inputs) {
        if (input.offsetWidth > 0 && input.offsetHeight > 0 && !input.disabled) {
            return input;
        }
    }
    
    return inputs[0] || null;
}

// 送信ボタンを検出
function findSubmitButton() {
    const buttons = document.querySelectorAll(aiPresidentMonitor.submitSelector);
    
    for (const button of buttons) {
        if (button.offsetWidth > 0 && button.offsetHeight > 0 && !button.disabled) {
            return button;
        }
    }
    
    return buttons[0] || null;
}

// XPath設定を読み込み
async function loadXPathConfig() {
    try {
        const result = await chrome.storage.local.get(['xpathConfigs']);
        const configs = result.xpathConfigs || [];
        
        // 現在のURLに一致する設定を検索
        const currentUrl = window.location.href;
        const matchingConfig = configs.find(config => {
            if (config.targetSite === '*') return true;
            return currentUrl.includes(config.targetSite);
        });
        
        if (matchingConfig) {
            xpathConfig = matchingConfig.xpaths;
            console.log('✅ XPath設定読み込み完了:', matchingConfig.name);
            console.log('📋 設定内容:', xpathConfig);
        } else {
            console.log('⚠️ 一致するXPath設定が見つかりません');
        }
        
    } catch (error) {
        console.error('❌ XPath設定読み込みエラー:', error);
    }
}

// XPathで要素を検索
function findElementByXPath(xpath) {
    if (!xpath) return null;
    
    try {
        const result = document.evaluate(
            xpath,
            document,
            null,
            XPathResult.FIRST_ORDERED_NODE_TYPE,
            null
        );
        return result.singleNodeValue;
    } catch (error) {
        console.error(`❌ XPath評価エラー (${xpath}):`, error);
        return null;
    }
}

// XPathで複数要素を検索
function findElementsByXPath(xpath) {
    if (!xpath) return [];
    
    try {
        const result = document.evaluate(
            xpath,
            document,
            null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
            null
        );
        
        const elements = [];
        for (let i = 0; i < result.snapshotLength; i++) {
            elements.push(result.snapshotItem(i));
        }
        return elements;
    } catch (error) {
        console.error(`❌ XPath評価エラー (${xpath}):`, error);
        return [];
    }
}

// XPathテスト機能
function testXPaths(xpaths) {
    const results = {};
    
    Object.entries(xpaths).forEach(([key, xpath]) => {
        if (!xpath) {
            results[key] = { found: false, count: 0, error: 'XPathが空です' };
            return;
        }
        
        try {
            const elements = findElementsByXPath(xpath);
            results[key] = {
                found: elements.length > 0,
                count: elements.length,
                xpath: xpath,
                elements: elements.slice(0, 3).map(el => ({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    text: el.textContent?.substring(0, 50) + '...'
                }))
            };
        } catch (error) {
            results[key] = {
                found: false,
                count: 0,
                error: error.message,
                xpath: xpath
            };
        }
    });
    
    return results;
}

// 設定されたXPathを使用して入力欄を検出（既存のfindInputField関数を拡張）
function findInputFieldWithXPath() {
    // XPath設定がある場合はそれを優先
    if (xpathConfig.messageInput) {
        const element = findElementByXPath(xpathConfig.messageInput);
        if (element) {
            console.log('✅ XPath設定で入力欄を発見:', element);
            return element;
        }
    }
    
    // フォールバック: 既存のセレクター方式
    return findInputField();
}

// 設定されたXPathを使用して送信ボタンを検出
function findSubmitButtonWithXPath() {
    if (xpathConfig.sendButton) {
        const element = findElementByXPath(xpathConfig.sendButton);
        if (element) {
            console.log('✅ XPath設定で送信ボタンを発見:', element);
            return element;
        }
    }
    
    // フォールバック: 既存のセレクター方式
    return findSubmitButton();
}

// メッセージを入力欄に自動入力
function autoInputMessage(message) {
    const inputField = findInputFieldWithXPath();
    
    if (!inputField) {
        console.warn('⚠️ 入力欄が見つかりません');
        showNotification('入力欄が見つかりません', 'warning');
        return false;
    }
    
    try {
        // 入力欄にフォーカス
        inputField.focus();
        
        // 値を設定
        if (inputField.contentEditable === 'true') {
            // contenteditable要素の場合
            inputField.textContent = message;
            inputField.innerHTML = message;
        } else {
            // input/textarea要素の場合
            inputField.value = message;
        }
        
        // 入力イベントを発火
        const inputEvent = new Event('input', { bubbles: true });
        inputField.dispatchEvent(inputEvent);
        
        const changeEvent = new Event('change', { bubbles: true });
        inputField.dispatchEvent(changeEvent);
        
        console.log('✅ メッセージ入力完了:', message.substring(0, 50) + '...');
        
        // 送信ボタンを自動クリック（オプション）
        setTimeout(() => {
            autoSubmitMessage();
        }, 1000);
        
        return true;
        
    } catch (error) {
        console.error('❌ 自動入力エラー:', error);
        showNotification('自動入力エラー', 'error');
        return false;
    }
}

// メッセージを自動送信
function autoSubmitMessage() {
    const submitButton = findSubmitButtonWithXPath();
    
    if (!submitButton) {
        console.warn('⚠️ 送信ボタンが見つかりません');
        showNotification('送信ボタンが見つかりません', 'warning');
        return false;
    }
    
    try {
        // 送信ボタンをクリック
        submitButton.click();
        
        console.log('✅ メッセージ送信完了');
        showNotification('AI社長応答送信完了', 'success');
        
        return true;
        
    } catch (error) {
        console.error('❌ 自動送信エラー:', error);
        showNotification('自動送信エラー', 'error');
        return false;
    }
}

// 通知表示
function showNotification(message, type = 'info') {
    // 既存の通知があれば削除
    const existingNotification = document.querySelector('.ai-president-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // 通知要素作成
    const notification = document.createElement('div');
    notification.className = `ai-president-notification ai-president-${type}`;
    notification.textContent = `🤖 AI社長: ${message}`;
    
    // スタイル設定
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 16px',
        backgroundColor: type === 'success' ? '#4CAF50' : type === 'warning' ? '#FF9800' : type === 'error' ? '#F44336' : '#2196F3',
        color: 'white',
        borderRadius: '4px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
        zIndex: '10000',
        fontSize: '14px',
        maxWidth: '300px',
        transition: 'all 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // 3秒後に自動削除
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// メッセージリスナー
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 コンテンツスクリプト メッセージ受信:', request);
    
    if (request.type === 'INIT_AI_PRESIDENT_MONITOR') {
        detectPageType();
        aiPresidentMonitor.active = true;
        showNotification('AI社長監視システム起動', 'success');
        sendResponse({ success: true, site: aiPresidentMonitor.currentSite });
        return true;
    }
    
    if (request.type === 'AUTO_INPUT_MESSAGE') {
        const result = autoInputMessage(request.message);
        sendResponse({ success: result });
        return true;
    }
    
    if (request.type === 'GET_PAGE_INFO') {
        detectPageType();
        sendResponse({ 
            site: aiPresidentMonitor.currentSite,
            url: window.location.href,
            inputFound: !!findInputField(),
            submitFound: !!findSubmitButton(),
            inputSelector: aiPresidentMonitor.inputSelector,
            submitSelector: aiPresidentMonitor.submitSelector
        });
        return true;
    }
    
    if (request.type === 'TEST_INPUT') {
        console.log('🧪 入力テスト開始');
        const testMessage = '🤖 AI社長からのテストメッセージです！AUTOCREATE株式会社の入力システムが正常に動作しています。';
        
        const inputField = findInputField();
        const submitButton = findSubmitButton();
        
        if (!inputField) {
            console.error('❌ 入力欄が見つかりません');
            showNotification('入力欄が見つかりません', 'error');
            sendResponse({ 
                success: false, 
                error: '入力欄が見つかりません',
                debug: {
                    currentSite: aiPresidentMonitor.currentSite,
                    inputSelector: aiPresidentMonitor.inputSelector,
                    url: window.location.href
                }
            });
            return true;
        }
        
        if (!submitButton) {
            console.warn('⚠️ 送信ボタンが見つかりません（入力のみテスト）');
        }
        
        try {
            // テストメッセージを入力
            const result = autoInputMessage(testMessage);
            
            if (result) {
                console.log('✅ 入力テスト成功');
                showNotification('入力テスト成功！', 'success');
                sendResponse({ 
                    success: true, 
                    message: 'テストメッセージ入力完了',
                    debug: {
                        inputFound: true,
                        submitFound: !!submitButton,
                        site: aiPresidentMonitor.currentSite
                    }
                });
            } else {
                throw new Error('入力処理が失敗しました');
            }
        } catch (error) {
            console.error('❌ 入力テスト失敗:', error);
            showNotification('入力テスト失敗', 'error');
            sendResponse({ 
                success: false, 
                error: error.message,
                debug: {
                    inputFound: !!inputField,
                    submitFound: !!submitButton,
                    site: aiPresidentMonitor.currentSite,
                    error: error.message
                }
            });
        }
        return true;
    }
    
    if (request.type === 'TEST_XPATH') {
        console.log('🧪 XPathテスト開始:', request.xpaths);
        
        try {
            const results = testXPaths(request.xpaths);
            console.log('📊 XPathテスト結果:', results);
            
            sendResponse({ 
                success: true, 
                results: results,
                url: window.location.href,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            console.error('❌ XPathテストエラー:', error);
            sendResponse({ 
                success: false, 
                error: error.message,
                url: window.location.href
            });
        }
        return true;
    }
    
    if (request.type === 'LOAD_XPATH_CONFIG') {
        console.log('⚙️ XPath設定読み込み要求');
        loadXPathConfig().then(() => {
            sendResponse({ 
                success: true, 
                config: xpathConfig,
                url: window.location.href
            });
        }).catch(error => {
            sendResponse({ 
                success: false, 
                error: error.message
            });
        });
        return true;
    }
    
    if (request.type === 'USE_XPATH_INPUT') {
        console.log('🎯 XPath設定での入力実行:', request.message);
        
        try {
            const inputField = findInputFieldWithXPath();
            if (!inputField) {
                sendResponse({ 
                    success: false, 
                    error: 'XPath設定での入力欄が見つかりません'
                });
                return true;
            }
            
            const result = autoInputMessage(request.message);
            sendResponse({ 
                success: result,
                method: 'xpath',
                xpath: xpathConfig.messageInput
            });
        } catch (error) {
            sendResponse({ 
                success: false, 
                error: error.message
            });
        }
        return true;
    }
});

// 初期化処理
document.addEventListener('DOMContentLoaded', () => {
    console.log('📋 ページ読み込み完了 - XPath設定を読み込み中...');
    detectPageType();
    loadXPathConfig();
});

// ページが既に読み込まれている場合の初期化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        detectPageType();
        loadXPathConfig();
    });
} else {
    // 既に読み込まれている
    detectPageType();
    loadXPathConfig();
}

console.log('🎯 AI社長コンテンツスクリプト初期化完了 - XPath設定機能有効');

// DOM変更監視（動的コンテンツ対応）
const observer = new MutationObserver((mutations) => {
    let shouldRedetect = false;
    
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // 新しい要素が追加された場合、入力欄があるかチェック
            for (const node of mutation.addedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.matches && (node.matches('input') || node.matches('textarea') || node.matches('[contenteditable]'))) {
                        shouldRedetect = true;
                        break;
                    }
                }
            }
        }
    });
    
    if (shouldRedetect) {
        setTimeout(detectPageType, 500);
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

console.log('🎯 AI社長コンテンツスクリプト初期化完了');
